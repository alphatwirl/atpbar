import abc
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from multiprocessing import Queue
from threading import Lock, current_thread, main_thread

from .presentation import create_presentation
from .progress_report import ProgressReporter, ProgressReportPickup, Report
from .stream import StreamQueue, StreamRedirection, register_stream_queue

'''Finite state machine

State Diagram:

     .----------------------------------------------.
     |                                              |
     |               .-------------.                |
     |    .--------->|   Initial   |                |
     |    |          '-------------'                |
     |    |                 | prepare_reporter()    |
     |  shutdown()          | flush()               |
     |    |                 v                       |
     |    |          .-------------.                |
     |    '----------|   Active    |                |
     |               '-------------'                |
     '----------------------------------------------'
              |                               |
              |--------------------------.    |-------------.
         register_reporter()             |    | disable()   |
              |                          |    |             |
              v                          |    v             |
        .-------------.              .-------------.        |
        | Registered  |              |  Disabled   |        |
        '-------------'              '-------------'        |
              |                                             |
              '---------------------------------------------'


'''


class Callback:

    def __init__(self) -> None:
        self.reporter: ProgressReporter | None = None

    def on_active(self) -> None:

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
            self.reporter.stream_redirection_enabled = False

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

    @contextmanager
    def fetch_reporter_in_active(self, lock: Lock) -> Iterator[ProgressReporter | None]:

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

    def flush_in_active(self) -> None:
        self._restart_pickup()

    def shutdown_in_active(self) -> None:
        self._end_pickup()

    def on_registered(self, reporter: ProgressReporter | None) -> None:
        self.reporter = reporter
        if reporter is None:
            return
        if reporter.stream_redirection_enabled:
            register_stream_queue(reporter.stream_queue)

    @contextmanager
    def fetch_reporter_in_registered(
        self, lock: Lock
    ) -> Iterator[ProgressReporter | None]:
        if self.reporter is None:
            yield self.reporter
            return

        self.reporter.notices_from_sub_processes.put(True)
        yield self.reporter

    def on_disabled(self) -> None:
        self.reporter = None

    @contextmanager
    def fetch_reporter_in_disabled(self, lock: Lock) -> Iterator[None]:
        yield None


class StateMachine:
    def __init__(self) -> None:
        self.lock = Lock()
        callback = Callback()
        self.state: State = Initial(callback=callback)

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

    def fetch_reporter(self) -> AbstractContextManager[ProgressReporter | None]:
        with self.lock:
            self.state = self.state.prepare_reporter()
        return self.state.fetch_reporter(lock=self.lock)


class State(abc.ABC):
    '''The base class of the states'''

    def __init__(self, callback: Callback) -> None:
        self._callback = callback

    @property
    def reporter(self) -> ProgressReporter | None:
        return self._callback.reporter

    def prepare_reporter(self) -> 'State':
        return self

    def register_reporter(self, reporter: ProgressReporter) -> 'State':
        return Registered(callback=self._callback, reporter=reporter)

    def disable(self) -> 'State':
        return Disabled(callback=self._callback)

    @abc.abstractmethod
    def fetch_reporter(
        self, lock: Lock
    ) -> AbstractContextManager[ProgressReporter | None]: ...

    def flush(self) -> 'State':
        return self

    def shutdown(self) -> 'State':
        return self


class Initial(State):
    '''Initial state

    The pickup is not running.
    '''

    def __init__(self, callback: Callback) -> None:
        super().__init__(callback)

    def prepare_reporter(self) -> State:
        return Active(callback=self._callback)

    @contextmanager
    def fetch_reporter(self, lock: Lock) -> Iterator[ProgressReporter | None]:
        yield self.reporter

    def flush(self) -> State:
        return Active(callback=self._callback)


class Active(State):
    '''Active state

    The pickup started and is running, typically, in the main process
    '''

    def __init__(self, callback: Callback) -> None:
        super().__init__(callback)
        self._callback.on_active()

    def fetch_reporter(
        self, lock: Lock
    ) -> AbstractContextManager[ProgressReporter | None]:
        return self._callback.fetch_reporter_in_active(lock=lock)

    def flush(self) -> State:
        self._callback.flush_in_active()
        return self

    def shutdown(self) -> State:
        self._callback.shutdown_in_active()
        return Initial(callback=self._callback)


class Registered(State):
    '''Registered state

    Typically, in a sub-process. The reporter, which has been created
    in the main process, is registered in the sub-process
    '''

    def __init__(self, callback: Callback, reporter: ProgressReporter | None) -> None:
        super().__init__(callback)
        self._callback.on_registered(reporter)

    def fetch_reporter(
        self, lock: Lock
    ) -> AbstractContextManager[ProgressReporter | None]:
        return self._callback.fetch_reporter_in_registered(lock=lock)


class Disabled(State):
    '''Disabled state'''

    def __init__(self, callback: Callback) -> None:
        super().__init__(callback)
        self._callback.on_disabled()

    def fetch_reporter(
        self, lock: Lock
    ) -> AbstractContextManager[ProgressReporter | None]:
        return self._callback.fetch_reporter_in_disabled(lock=lock)


def in_main_thread() -> bool:
    '''test if in the main thread'''
    return current_thread() == main_thread()
