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
_presentation = create_presentation()
_reporter = None
_pickup = None
_queue = None
_lock = threading.Lock()

##__________________________________________________________________||
def find_reporter():
    global _lock
    global _reporter
    global _queue
    global _presentation
    global _pickup

    _lock.acquire()
    if _reporter is None:
        if _queue is None:
            # mananger = multiprocessing.Manager()
            # _queue = mananger.Queue()
            _queue = multiprocessing.Queue()
            # _queue.cancel_join_thread()
        _reporter = ProgressReporter(queue=_queue)
        _pickup = ProgressReportPickup(_queue, _presentation)
        _pickup.daemon = True # this makes the functions
                              # registered at atexit called even
                              # if the pickup is still running
        _pickup.start()
        atexit.register(_end_pickup)
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
    global _queue
    global _presentation
    global _pickup

    _lock.acquire()
    if _reporter is None:
        _need_end_pickup = True
        if _queue is None:
            # mananger = multiprocessing.Manager()
            # _queue = mananger.Queue()
            _queue = multiprocessing.Queue()
            # _queue.cancel_join_thread()
        _reporter = ProgressReporter(queue=_queue)
        _pickup = ProgressReportPickup(_queue, _presentation)
        _pickup.daemon = True # this makes the functions
                              # registered at atexit called even
                              # if the pickup is still running
        _pickup.start()
        atexit.register(_end_pickup)
    else:
        _need_end_pickup = False
    _lock.release()

    yield _reporter

    if _need_end_pickup:
        _end_pickup()
        _reporter = None

##__________________________________________________________________||
def _end_pickup():
    global _queue
    global _pickup
    if _pickup:
        _queue.put(None)
        _pickup.join()
        _pickup = None

##__________________________________________________________________||
