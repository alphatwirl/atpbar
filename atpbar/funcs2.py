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
_queue = multiprocessing.Queue()
_presentation = create_presentation()
_reporter = None
_pickup = None

##__________________________________________________________________||
def find_reporter():
    global _queue
    global _presentation
    global _reporter
    global _pickup

    if _reporter is not None:
        return _reporter

    _reporter = ProgressReporter(queue=_queue)

    _pickup = ProgressReportPickup(_queue, _presentation)
    _pickup.daemon = True # this makes the functions
                          # registered at atexit called even
                          # if the pickup is still running
    _pickup.start()
    atexit.register(_end_pickup)

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
    global _queue
    global _presentation
    global _reporter
    global _pickup

    if _reporter is not None:
        yield _reporter
        return

    _reporter = ProgressReporter(queue=_queue)

    _pickup = ProgressReportPickup(_queue, _presentation)
    _pickup.daemon = True # this makes the functions
                          # registered at atexit called even
                          # if the pickup is still running
    _pickup.start()
    atexit.register(_end_pickup)

    yield _reporter
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
