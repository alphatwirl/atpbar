from .BProgressMonitor import BProgressMonitor
from .NullProgressMonitor import NullProgressMonitor
from .ProgressBar import ProgressBar
from .ProgressMonitor import ProgressMonitor, Queue
from .ProgressPrint import ProgressPrint
from .ProgressReportPickup import ProgressReportPickup
from .ProgressReport import ProgressReport
from .ProgressReporter import ProgressReporter
from .main import atpbar

##__________________________________________________________________||
try:
    from .ProgressBarJupyter import ProgressBarJupyter
except ImportError:
    pass

##__________________________________________________________________||
def report_progress(report):
    if _reporter is None:
        return
    _reporter.report(report)

##__________________________________________________________________||
do_not_start_monitor = False
_reporter = None
_monitor = None

import sys
import atexit

import threading
_lock = threading.Lock()

def reporter():
    global _reporter
    _start_monitor_if_necessary()
    return _reporter

def register_reporter(reporter):
    global _reporter
    _reporter = reporter

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

    presentation = _create_presentation()
    monitor = BProgressMonitor(presentation=presentation)
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

def _create_presentation():
    if sys.stdout.isatty():
        return ProgressBar()
    if is_jupyter_notebook():
        return ProgressBarJupyter()
    return ProgressPrint()

def is_jupyter_notebook():
    try:
        from IPython import get_ipython
        if 'IPKernelApp' in get_ipython().config:
            return True
    except:
        pass
    return False

##__________________________________________________________________||
