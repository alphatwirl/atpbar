# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import atexit
import threading
import multiprocessing
import contextlib

from .reporter import ProgressReporter
from .pickup import ProgressReportPickup
from .presentation.create import create_presentation

##__________________________________________________________________||
_presentation = None
_reporter = None
_pickup = None
_queue = None
_detach_pickup = False
_lock = threading.Lock()

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
    _reporter = reporter

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
    _lock.release()

atexit.register(flush)

##__________________________________________________________________||
def detach_pickup():
    global _lock
    global _detach_pickup
    # _lock.acquire() # This lock causes a deadlock. `flush()` locks while
                      # ending the pickup. Before receiving the end order, the
                      # pickup might still receives a report with a new task ID
                      # from a sub-thread or sub-process, it will call this
                      # function and will cause a deadlock.
    _detach_pickup = True
    # _lock.release()

##__________________________________________________________________||
@contextlib.contextmanager
def fetch_reporter():
    global _lock
    global _reporter
    global _detach_pickup

    _lock.acquire()
    started = _start_pickup_if_necessary()
    if not in_main_thread():
        _detach_pickup = True
    _lock.release()

    own_pickup = started and in_main_thread()

    try:
        yield _reporter
    finally:
        _lock.acquire()
        if _detach_pickup:
            own_pickup = False
        if own_pickup:
            _end_pickup()
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
    global _presentation
    global _pickup

    if _reporter is not None:
        return False

    if _queue is None:
        _queue = multiprocessing.Queue()

    _reporter = ProgressReporter(queue=_queue)
    _presentation = create_presentation()
    _pickup = ProgressReportPickup(_queue, _presentation)
    _pickup.daemon = True # this makes the functions
                          # registered at atexit called even
                          # if the pickup is still running

    _pickup.start()

    return True

##__________________________________________________________________||
def _end_pickup():
    global _queue
    global _presentation
    global _pickup
    global _reporter
    global _detach_pickup
    if _pickup:
        _queue.put(None)
        _pickup.join()
        _pickup = None
        _presentation = None
        _detach_pickup = False
    _reporter = None

##__________________________________________________________________||
