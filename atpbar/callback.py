from collections.abc import Iterator
from contextlib import contextmanager
from threading import Lock, current_thread, main_thread

from .machine import StateMachine
from .presentation import create_presentation
from .progress_report import ProgressReporter, ProgressReportPickup
from .stream import StreamRedirection, register_stream_queue


class CallbackImp:

    def __init__(self) -> None:
        self.reporter: ProgressReporter | None = None
        self._machine: StateMachine  # to be set by the StateMachine
        self._lock: Lock  # to be set by the StateMachine

    def on_active(self) -> None:

        self.reporter = ProgressReporter()
        self.queue = self.reporter.queue
        self.notices_from_sub_processes = self.reporter.notices_from_sub_processes
        self.stream_queue = self.reporter.stream_queue

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
    def fetch_reporter_in_active(self) -> Iterator[ProgressReporter | None]:

        if not in_main_thread():
            self.to_restart_pickup = False
            yield self.reporter
            return

        self.to_restart_pickup = True

        while not self.notices_from_sub_processes.empty():
            _ = self.notices_from_sub_processes.get()

        self._machine.on_yielded()

        try:
            yield self.reporter
        finally:
            self._machine.on_resumed()

            while not self.notices_from_sub_processes.empty():
                _ = self.notices_from_sub_processes.get()
                self.to_restart_pickup = False

            if not self.to_restart_pickup:
                return

            with self._lock:
                self._restart_pickup()

    def flush_in_active(self) -> None:
        self._restart_pickup()

    def shutdown_in_active(self) -> None:
        self._end_pickup()

    @contextmanager
    def fetch_reporter_in_yielded(self) -> Iterator[ProgressReporter | None]:

        if not in_main_thread():
            self.to_restart_pickup = False
            yield self.reporter
            return

        yield self.reporter

    def on_registered(self, reporter: ProgressReporter | None) -> None:
        self.reporter = reporter
        if reporter is None:
            return
        if reporter.stream_redirection_enabled:
            register_stream_queue(reporter.stream_queue)

    @contextmanager
    def fetch_reporter_in_registered(self) -> Iterator[ProgressReporter | None]:
        if self.reporter is None:
            yield self.reporter
            return

        self.reporter.notices_from_sub_processes.put(True)
        yield self.reporter

    def on_disabled(self) -> None:
        self.reporter = None

    @contextmanager
    def fetch_reporter_in_disabled(self) -> Iterator[None]:
        yield None


def in_main_thread() -> bool:
    '''test if in the main thread'''
    return current_thread() == main_thread()
