from __future__ import annotations

import abc
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from threading import Lock
from typing import Protocol

from .progress_report import ProgressReporter

'''Finite state machine

State Diagram:

     .-------------.        shutdown() 
     |   Initial   |<------------------*
     '-------------'
            | prepare_reporter()
            | flush()
            v 
     .-------------.     on_resumed() .-------------.
     |   Active    |<---------------->|   Yielded   |
     '-------------' on_yielded()     '-------------'


        register_reporter()    .-------------.
      *----------------------->| Registered  |
                               '-------------'


         disable()             .-------------.
      *----------------------->|  Disabled   |
                               '-------------'

NOTE: In a forked sub-process, the state starts from the same state as the parent process.
'''


class Callback(Protocol):
    reporter: ProgressReporter | None
    _machine: 'StateMachine'
    _lock: Lock

    def __init__(self) -> None: ...

    def on_active(self) -> None: ...

    def fetch_reporter_in_active(
        self,
    ) -> AbstractContextManager[ProgressReporter | None]: ...

    def fetch_reporter_in_yielded(
        self,
    ) -> AbstractContextManager[ProgressReporter | None]: ...

    def flush_in_active(self) -> None: ...

    def shutdown_in_active(self) -> None: ...

    def on_registered(self, reporter: ProgressReporter | None) -> None: ...

    def fetch_reporter_in_registered(
        self,
    ) -> AbstractContextManager[ProgressReporter | None]: ...

    def on_disabled(self) -> None: ...

    def fetch_reporter_in_disabled(
        self,
    ) -> AbstractContextManager[ProgressReporter | None]: ...


class StateMachine:
    def __init__(self, callback: Callback) -> None:
        callback._machine = self
        self.lock = callback._lock = Lock()
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
        return self.state.fetch_reporter()

    def on_yielded(self) -> None:
        self.state = self.state.on_yielded()

    def on_resumed(self) -> None:
        self.state = self.state.on_resumed()


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
    def fetch_reporter(self) -> AbstractContextManager[ProgressReporter | None]: ...

    def on_yielded(self) -> 'State':
        return self

    def on_resumed(self) -> 'State':
        return self

    def flush(self) -> 'State':
        return self

    def shutdown(self) -> 'State':
        return Initial(callback=self._callback)


class Initial(State):
    '''Initial state

    The pickup is not running.
    '''

    def __init__(self, callback: Callback) -> None:
        super().__init__(callback)

    def prepare_reporter(self) -> State:
        return Active(callback=self._callback)

    @contextmanager
    def fetch_reporter(self) -> Iterator[ProgressReporter | None]:
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

    def fetch_reporter(self) -> AbstractContextManager[ProgressReporter | None]:
        return self._callback.fetch_reporter_in_active()

    def on_yielded(self) -> State:
        return Yielded(callback=self._callback, active=self)

    def flush(self) -> State:
        self._callback.flush_in_active()
        return self

    def shutdown(self) -> State:
        self._callback.shutdown_in_active()
        return Initial(callback=self._callback)


class Yielded(State):
    '''Yielded state

    The state during yielded from Active.fetch_reporter(). Inner loops of nested loops.
    '''

    def __init__(self, callback: Callback, active: Active) -> None:
        super().__init__(callback)
        self._active = active

    def fetch_reporter(self) -> AbstractContextManager[ProgressReporter | None]:
        return self._callback.fetch_reporter_in_yielded()

    def on_resumed(self) -> State:
        return self._active


class Registered(State):
    '''Registered state

    Typically, in a sub-process. The reporter, which has been created
    in the main process, is registered in the sub-process
    '''

    def __init__(self, callback: Callback, reporter: ProgressReporter | None) -> None:
        super().__init__(callback)
        self._callback.on_registered(reporter)

    def fetch_reporter(self) -> AbstractContextManager[ProgressReporter | None]:
        return self._callback.fetch_reporter_in_registered()


class Disabled(State):
    '''Disabled state'''

    def __init__(self, callback: Callback) -> None:
        super().__init__(callback)
        self._callback.on_disabled()

    def fetch_reporter(self) -> AbstractContextManager[ProgressReporter | None]:
        return self._callback.fetch_reporter_in_disabled()
