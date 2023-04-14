# Tai Sakuma <tai.sakuma@gmail.com>
import atexit
import multiprocessing
import contextlib

from .machine import StateMachine

##__________________________________________________________________||
_machine = StateMachine()

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
    return _machine.find_reporter()

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
    _machine.register_reporter(reporter)

##__________________________________________________________________||
def flush(blocking=True, timeout=-1):
    """flushes progress bars

    This function flushes all active progress bars. It returns when
    the progress bars finish updating.

    Parameters
    ----------
    blocking : bool
        Should the call to acquire the reporter lock be blocking
    timeout : float
        Timeout for the reporter lock acquiring


    Returns
    -------
    Success to acquire reporter the lock

    """
    return _machine.flush(blocking, timeout)

##__________________________________________________________________||
def disable():
    """disables progress bars

    This function needs to be called in the main process before
    `atpbar()` or `find_reporter()` is used.

    Returns
    -------
    None

    """
    _machine.disable()

##__________________________________________________________________||

##__________________________________________________________________||
def shutdown():
    """shutdowns the progress bars

    Returns
    -------
    None

    """
    _machine.shutdown()


import multiprocessing.queues # This import prevents the issue
                              # https://github.com/alphatwirl/atpbar/issues/4

atexit.register(shutdown)

##__________________________________________________________________||
@contextlib.contextmanager
def fetch_reporter():
    yield from _machine.fetch_reporter()

##__________________________________________________________________||
