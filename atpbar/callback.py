from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from threading import Lock, current_thread, main_thread

from .machine import StateMachine
from .progress_report import ProgressReporter


class CallbackImp:
    def __init__(self) -> None:
        self.reporter: ProgressReporter | None = None
        self._machine: StateMachine  # to be set by the StateMachine
        self._lock: Lock  # to be set by the StateMachine

    def on_active(self) -> None:
        self.reporter = ProgressReporter()
        self.reporter.start_pickup()

    @contextmanager
    def fetch_reporter_in_active(self) -> Iterator[ProgressReporter | None]:
        assert self.reporter

        if not in_main_thread():
            self.to_restart_pickup = False
            yield self.reporter
            return

        self.to_restart_pickup = True
        self.reporter.empty_notices()
        self._machine.on_yielded()

        try:
            yield self.reporter
        finally:
            self._machine.on_resumed()

            if self.reporter.empty_notices():
                self.to_restart_pickup = False

            if not self.to_restart_pickup:
                return

            with self._lock:  # NOTE: This lock is probably unnecessary
                self.reporter.restart_pickup()

    def flush_in_active(self) -> None:
        assert self.reporter
        self.reporter.restart_pickup()

    def shutdown_in_active(self) -> None:
        assert self.reporter
        self.reporter.end_pickup()

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
        reporter.register()

    @contextmanager
    def fetch_reporter_in_registered(self) -> Iterator[ProgressReporter | None]:
        if self.reporter is None:
            yield self.reporter
            return

        self.reporter.notice()
        yield self.reporter

    def on_disabled(self) -> None:
        self.reporter = None

    @contextmanager
    def fetch_reporter_in_disabled(self) -> Iterator[None]:
        yield None


def in_main_thread() -> bool:
    '''test if in the main thread'''
    return current_thread() == main_thread()
