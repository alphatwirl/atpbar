# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import atexit
import threading
import multiprocessing
import contextlib

from .monitor import ProgressMonitor
from .reporter import ProgressReporter
from .pickup import ProgressReportPickup
from .presentation.create import create_presentation

##__________________________________________________________________||
_presentation = None
_reporter = None
_pickup = None
_queue = None
_lock = threading.Lock()

##__________________________________________________________________||
def find_reporter():
    global _lock
    global _reporter

    _lock.acquire()
    _start_pickup_if_necessary()
    _lock.release()

    return _reporter

##__________________________________________________________________||
def register_reporter(reporter):
    global _reporter
    _reporter = reporter

##__________________________________________________________________||
def flush():
    _end_pickup()

##__________________________________________________________________||
@contextlib.contextmanager
def fetch_reporter():
    global _lock
    global _reporter

    _lock.acquire()
    started = _start_pickup_if_necessary()
    _lock.release()

    need_end_pickup = started and in_main_thread()

    try:
        yield _reporter
    finally:
        if need_end_pickup:
            _end_pickup()

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
    atexit.register(_end_pickup)

    return True

##__________________________________________________________________||
def _end_pickup():
    global _lock
    global _queue
    global _presentation
    global _pickup
    global _reporter
    _lock.acquire()
    if _pickup:
        _queue.put(None)
        _pickup.join()
        _pickup = None
        _presentation = None
    _reporter = None
    _lock.release()

##__________________________________________________________________||
