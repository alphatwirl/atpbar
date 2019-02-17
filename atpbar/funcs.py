# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import atexit
import threading

from .monitor import ProgressMonitor
from .presentation.create import create_presentation

##__________________________________________________________________||
do_not_start_monitor = False
_reporter = None
_monitor = None

##__________________________________________________________________||
def find_reporter():
    global _reporter
    _start_monitor_if_necessary()
    return _reporter

def register_reporter(reporter):
    global _reporter
    _reporter = reporter

##__________________________________________________________________||
_lock = threading.Lock()

def _start_monitor_if_necessary():
    global _lock
    _lock.acquire()
    _start_monitor_if_necessary_()
    _lock.release()

def _start_monitor_if_necessary_():
    global _reporter
    global _monitor

    if do_not_start_monitor:
        return

    if _reporter:
        return

    if _monitor:
        # This shouldn't happen.
        # But if it does, end the old monitor.
        _end_monitor()

    presentation = create_presentation()
    monitor = ProgressMonitor(presentation=presentation)
    monitor.begin()
    _reporter = monitor.create_reporter()
    _monitor = monitor

    atexit.register(_end_monitor)

def _end_monitor():
    global _reporter
    global _monitor
    if _monitor:
        _monitor.end()
        _monitor = None
    _reporter = None

##__________________________________________________________________||
