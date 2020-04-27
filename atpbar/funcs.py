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
    with _machine.lock:
        _machine.state.prepare_reporter()
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
    with _machine.lock:
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
    with _machine.lock:
        _machine.state.end_pickup()


import multiprocessing.queues # This import prevents the issue
                              # https://github.com/alphatwirl/atpbar/issues/4

atexit.register(end_pickup)

##__________________________________________________________________||
@contextlib.contextmanager
def fetch_reporter():
    with _machine.lock:
        _machine.state.prepare_reporter()
    yield from _machine.state.fetch_reporter()

def in_main_thread():
    return threading.current_thread() == threading.main_thread()

##__________________________________________________________________||
class StateMachine:
    def __init__(self):
        self.lock = threading.Lock()
        self.state = Initial(self)

    def change_state(self, state):
        self.state = state

class State:
    """The base class of the states
    """
    def __init__(self, machine):
        self.machine = machine

    def prepare_reporter(self):
        pass

    def register_reporter(self, reporter):
        next_state = Registered(self.machine, reporter=reporter)
        self.machine.change_state(next_state)

    def disable(self):
        self.machine.change_state(Disabled(self.machine))

class MainProcess(State):
    """The base class of the states in the main process
    """
    def __init__(self, machine, reporter, queue):
        super().__init__(machine)

        self.reporter = reporter
        self.queue = queue

class Initial(MainProcess):
    """Initial state

    The pickup is not running
    """

    def __init__(self, machine, reporter=None, queue=None):
        super().__init__(machine, reporter=reporter, queue=queue)

        self.pickup = None
        self.pickup_owned = False

    def prepare_reporter(self):
        self._start_pickup_if_necessary()

    def find_reporter(self):
        return self.reporter

    def fetch_reporter(self):
        own_pickup = False
        if in_main_thread():
            if not self.pickup_owned:
                own_pickup = True
                self.pickup_owned = True

        try:
            yield self.reporter
        finally:
            with self.machine.lock:
                if detach.to_detach_pickup:
                    if own_pickup:
                        own_pickup = False
                        self.pickup_owned = False
                if own_pickup:
                    self._end_pickup()
                    self._start_pickup_if_necessary()

    def _start_pickup_if_necessary(self):
        if self.reporter is None:
            if self.queue is None:
                self.queue = multiprocessing.Queue()
            self.reporter = ProgressReporter(queue=self.queue)

        if self.pickup is not None:
            return

        presentation = create_presentation()
        self.pickup = ProgressReportPickup(self.queue, presentation)
        self.pickup.start()
        self.pickup_owned = False

        return

    def flush(self):
        self._end_pickup()
        self._start_pickup_if_necessary()

    def end_pickup(self):
        self._end_pickup()

    def _end_pickup(self):
        if self.pickup:
            self.queue.put(None)
            self.pickup.join()
            self.pickup = None
            detach.to_detach_pickup = False

class Started(MainProcess):
    """Started state

    The pickup started and is running.
    """
    pass

class Registered(State):
    """Registered state

    Typically, in a sub-process. The reporter, which has been created
    in the main process, is registered in the sub-process
    """

    def __init__(self, machine, reporter):
        super().__init__(machine)
        self.reporter = reporter

    def find_reporter(self):
        return self.reporter

    def fetch_reporter(self):
        yield self.reporter

    def flush(self):
        pass

    def end_pickup(self):
        pass

class Disabled(State):
    """Disabled state
    """

    def find_reporter(self):
        return None

    def fetch_reporter(self):
        yield None

    def flush(self):
        pass

    def end_pickup(self):
        pass

_machine = StateMachine()

##__________________________________________________________________||
