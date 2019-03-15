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
_lock = threading.Lock()
_queue = None
_reporter = None
_pickup = None
_pickup_owned = False
_do_not_start_pickup = False

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

    global _lock
    global _reporter

    _lock.acquire()
    _start_pickup_if_necessary()
    _lock.release()

    return _reporter

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

    global _reporter
    global _do_not_start_pickup
    _reporter = reporter
    _do_not_start_pickup = True

##__________________________________________________________________||
def flush():
    """flushes progress bars

    This function flushes all active progress bars. It returns when
    the progress bars finish updating.

    Returns
    -------
    None

    """
    global _lock
    _lock.acquire()
    _end_pickup()
    _start_pickup_if_necessary()
    _lock.release()

##__________________________________________________________________||
def disable():
    """disables progress bars

    This function needs to be called in the main process before
    `atpbar()` or `find_reporter()` is used.

    Returns
    -------
    None

    """
    global _do_not_start_pickup
    _do_not_start_pickup = True

##__________________________________________________________________||
def end_pickup():
    """ends the pickup

    Returns
    -------
    None

    """
    global _lock
    _lock.acquire()
    _end_pickup()
    _lock.release()


import multiprocessing.queues # This import prevents the issue
                              # https://github.com/alphatwirl/atpbar/issues/4

atexit.register(end_pickup)

##__________________________________________________________________||
@contextlib.contextmanager
def fetch_reporter():
    global _lock
    global _reporter
    global _do_not_start_pickup
    global _pickup_owned

    _lock.acquire()
    _start_pickup_if_necessary()
    _lock.release()

    own_pickup = False
    if not _do_not_start_pickup:
        if in_main_thread():
            if not _pickup_owned:
                own_pickup = True
                _pickup_owned = True


    try:
        yield _reporter
    finally:
        _lock.acquire()
        if detach.to_detach_pickup:
            if own_pickup:
                own_pickup = False
                _pickup_owned = False
        if own_pickup:
            _end_pickup()
            _start_pickup_if_necessary()
        _lock.release()

def in_main_thread():
    try:
        return threading.current_thread() == threading.main_thread()
    except:
        # python 2
        return isinstance(threading.current_thread(), threading._MainThread)

##__________________________________________________________________||
def _start_pickup_if_necessary():
    global _reporter
    global _queue
    global _pickup
    global _pickup_owned
    global _do_not_start_pickup

    if _do_not_start_pickup:
        return

    if _reporter is None:
        if _queue is None:
            _queue = multiprocessing.Queue()
        _reporter = ProgressReporter(queue=_queue)

    if _pickup is not None:
        return

    presentation = create_presentation()
    _pickup = ProgressReportPickup(_queue, presentation)
    _pickup.daemon = True # this makes the functions
                          # registered at atexit called even
                          # if the pickup is still running

    _pickup.start()
    _pickup_owned = False

    return

##__________________________________________________________________||
def _end_pickup():
    global _queue
    global _pickup
    if _pickup:
        _queue.put(None)
        _pickup.join()
        _pickup = None
        detach.to_detach_pickup = False

##__________________________________________________________________||
