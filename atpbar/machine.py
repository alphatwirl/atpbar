import abc
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from threading import Lock

from .callback import Callback
from .progress_report import ProgressReporter

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


class StateMachine:
    def __init__(self, callback: Callback) -> None:
        self.lock = Lock()
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
