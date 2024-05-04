from collections.abc import Iterator
from multiprocessing import Queue
from threading import Lock, current_thread, main_thread

from .presentation import create_presentation
from .progressreport import ProgressReporter, ProgressReportPickup, Report
from .stream import StreamQueue, StreamRedirection, register_stream_queue


class StateMachine:
    def __init__(self) -> None:
        self.lock = Lock()
        self.state: State = Initial()

    def find_reporter(self) -> ProgressReporter | None:
        with self.lock:
            self.state = self.state.prepare_reporter()
        return self.state.reporter

    def register_reporter(self, reporter: ProgressReporter) -> None:
        self.state = self.state.register_reporter(reporter)

    def flush(self) -> None:
        with self.lock:
            self.state = self.state.flush()

    def disable(self) -> None:
        self.state = self.state.disable()

    def shutdown(self) -> None:
        with self.lock:
            self.state = self.state.shutdown()

    def fetch_reporter(self) -> Iterator[ProgressReporter | None]:
        with self.lock:
            self.state = self.state.prepare_reporter()
        yield from self.state.fetch_reporter(lock=self.lock)


class State:
    """The base class of the states"""

    def __init__(self) -> None:
        self.reporter: ProgressReporter | None = None

    def prepare_reporter(self) -> 'State':
        return self

    def register_reporter(self, reporter: ProgressReporter) -> 'State':
        return Registered(reporter=reporter)

    def disable(self) -> 'State':
        return Disabled()

    def fetch_reporter(self, lock: Lock) -> Iterator[ProgressReporter | None]:
        yield None

    def flush(self) -> 'State':
        return self

    def shutdown(self) -> 'State':
        return self


class Initial(State):
    """Initial state

    The pickup is not running.
    """

    def __init__(self) -> None:
        self.reporter = None

    def prepare_reporter(self) -> State:
        return Active()

    def fetch_reporter(self, lock: Lock) -> Iterator[ProgressReporter | None]:
        yield self.reporter

    def flush(self) -> State:
        return Active()


class Active(State):
    """Active state

    The pickup started and is running, typically, in the main process
    """

    def __init__(self) -> None:

        self.queue: Queue[Report] = Queue()
        self.notices_from_sub_processes: Queue[bool] = Queue()
        self.stream_queue: StreamQueue = Queue()
        self.reporter = ProgressReporter(
            queue=self.queue,
            notices_from_sub_processes=self.notices_from_sub_processes,
            stream_queue=self.stream_queue,
        )

        self.reporter_yielded = False

        self._start_pickup()

        if self.stream_redirection.disabled:
            self.reporter.stream_redirection_enablaed = False

    def _start_pickup(self) -> None:
        presentation = create_presentation()
        self.pickup = ProgressReportPickup(self.queue, presentation)

        self.stream_redirection = StreamRedirection(
            queue=self.stream_queue, presentation=presentation
        )
        self.stream_redirection.start()

    def _end_pickup(self) -> None:
        self.pickup.end()

        self.stream_redirection.end()

    def _restart_pickup(self) -> None:
        self._end_pickup()
        self._start_pickup()

    def fetch_reporter(self, lock: Lock) -> Iterator[ProgressReporter | None]:

        if not in_main_thread():
            self.to_restart_pickup = False
            yield self.reporter
            return

        if self.reporter_yielded:
            # called from an inner loop
            yield self.reporter
            return

        self.reporter_yielded = True
        self.to_restart_pickup = True

        while not self.notices_from_sub_processes.empty():
            _ = self.notices_from_sub_processes.get()

        try:
            yield self.reporter
        finally:
            self.reporter_yielded = False

            while not self.notices_from_sub_processes.empty():
                _ = self.notices_from_sub_processes.get()
                self.to_restart_pickup = False

            if not self.to_restart_pickup:
                return

            with lock:
                self._restart_pickup()

    def flush(self) -> State:
        self._restart_pickup()
        return self

    def shutdown(self) -> State:
        self._end_pickup()
        return Initial()


class Registered(State):
    """Registered state

    Typically, in a sub-process. The reporter, which has been created
    in the main process, is registered in the sub-process
    """

    def __init__(self, reporter: ProgressReporter | None) -> None:
        self.reporter = reporter
        if reporter is None:
            return
        if reporter.stream_redirection_enablaed:
            register_stream_queue(reporter.stream_queue)

    def fetch_reporter(self, lock: Lock) -> Iterator[ProgressReporter | None]:
        if self.reporter is None:
            yield self.reporter
            return

        self.reporter.notices_from_sub_processes.put(True)
        yield self.reporter


class Disabled(State):
    """Disabled state"""

    def __init__(self) -> None:
        self.reporter = None


def in_main_thread() -> bool:
    """test if in the main thread"""
    return current_thread() == main_thread()
