# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import atexit
import threading
import multiprocessing
import contextlib

from .reporter import ProgressReporter
from .pickup import ProgressReportPickup
from .presentation.create import create_presentation
from . import detach

##__________________________________________________________________||
def find_reporter():
    """returns the progress reporter

    This function is to be called in the main process of a
    multiprocessing program. The reporter should be registered in
    sub-processes with the function `register_reporter()`

    Returns
    -------
    object
        The progress reporter

    """
    return _machine.state.find_reporter()

##__________________________________________________________________||
def register_reporter(reporter):
    """registers a reporter

    This function is to be called in sub-processes of a
    multiprocessing program.

    Parameters
    ----------
    reporter : object
        The reporter obtained in the main process by the function
        `find_reporter()`


    Returns
    -------
    None

    """
    _machine.state.register_reporter(reporter)

##__________________________________________________________________||
def flush():
    """flushes progress bars

    This function flushes all active progress bars. It returns when
    the progress bars finish updating.

    Returns
    -------
    None

    """
    _machine.state.flush()

##__________________________________________________________________||
def disable():
    """disables progress bars

    This function needs to be called in the main process before
    `atpbar()` or `find_reporter()` is used.

    Returns
    -------
    None

    """
    _machine.state.disable()

##__________________________________________________________________||
def end_pickup():
    """ends the pickup

    Returns
    -------
    None

    """
    _machine.state.end_pickup()


import multiprocessing.queues # This import prevents the issue
                              # https://github.com/alphatwirl/atpbar/issues/4

atexit.register(end_pickup)

##__________________________________________________________________||
@contextlib.contextmanager
def fetch_reporter():
    yield from _machine.state.fetch_reporter()

def in_main_thread():
    return threading.current_thread() == threading.main_thread()

##__________________________________________________________________||
class StateMachine:
    def __init__(self):
        self.state = Initial(self)

        self._lock = threading.Lock()
        self._queue = None
        self._reporter = None
        self._pickup = None
        self._pickup_owned = False

    def change_state(self, State):
        self.state = State(self)

class State:
    """The base class of the states
    """
    def __init__(self, machine):
        self.machine = machine
    def find_reporter(self):
        with self.machine._lock:
            self._start_pickup_if_necessary()

        return self.machine._reporter

    def register_reporter(self, reporter):
        self.machine._reporter = reporter
        self.machine.change_state(Registered)

    def disable(self):
        self.machine.change_state(Disabled)

    def end_pickup(self):
        with self.machine._lock:
            self._end_pickup()

    def _end_pickup(self):
        if self.machine._pickup:
            self.machine._queue.put(None)
            self.machine._pickup.join()
            self.machine._pickup = None
            detach.to_detach_pickup = False

class Initial(State):
    """Initial state
    """
    def fetch_reporter(self):
        with self.machine._lock:
            self._start_pickup_if_necessary()

        own_pickup = False
        if in_main_thread():
            if not self.machine._pickup_owned:
                own_pickup = True
                self.machine._pickup_owned = True


        try:
            yield self.machine._reporter
        finally:
            with self.machine._lock:
                if detach.to_detach_pickup:
                    if own_pickup:
                        own_pickup = False
                        self.machine._pickup_owned = False
                if own_pickup:
                    self._end_pickup()
                    self._start_pickup_if_necessary()

    def _start_pickup_if_necessary(self):
        if self.machine._reporter is None:
            if self.machine._queue is None:
                self.machine._queue = multiprocessing.Queue()
            self.machine._reporter = ProgressReporter(queue=self.machine._queue)

        if self.machine._pickup is not None:
            return

        presentation = create_presentation()
        self.machine._pickup = ProgressReportPickup(self.machine._queue, presentation)
        self.machine._pickup.start()
        self.machine._pickup_owned = False

        return

    def flush(self):
        with self.machine._lock:
            self._end_pickup()
            self._start_pickup_if_necessary()

class Registered(State):
    """Registered state
    """
    def fetch_reporter(self):
        try:
            yield self.machine._reporter
        finally:
            pass

    def flush(self):
        with self.machine._lock:
            self._end_pickup()

class Disabled(State):
    """Disabled state
    """
    def fetch_reporter(self):
        try:
            yield self.machine._reporter
        finally:
            pass

    def flush(self):
        pass

_machine = StateMachine()

##__________________________________________________________________||
