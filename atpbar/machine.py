# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import threading
import multiprocessing

from .progressreport.reporter import ProgressReporter
from .progressreport.pickup import ProgressReportPickup
from .stream import StreamRedirection, register_stream_queue
from .presentation.create import create_presentation

##__________________________________________________________________||
class StateMachine:
    def __init__(self):
        self.lock = threading.Lock()
        self.state = Initial()

    def find_reporter(self):
        with self.lock:
            self.state = self.state.prepare_reporter()
        return self.state.reporter

    def register_reporter(self, reporter):
        self.state = self.state.register_reporter(reporter)

    def flush(self):
        with self.lock:
            self.state = self.state.flush()

    def disable(self):
        self.state = self.state.disable()

    def shutdown(self):
        with self.lock:
            self.state = self.state.shutdown()

    def fetch_reporter(self):
        with self.lock:
            self.state = self.state.prepare_reporter()
        yield from self.state.fetch_reporter(lock=self.lock)

##__________________________________________________________________||
class State:
    """The base class of the states
    """
    def prepare_reporter(self):
        return self

    def register_reporter(self, reporter):
        return Registered(reporter=reporter)

    def disable(self):
        return Disabled()

    def fetch_reporter(self, lock):
        yield None

    def flush(self):
        return self

    def shutdown(self):
        return self

##__________________________________________________________________||
class Initial(State):
    """Initial state

    The pickup is not running.
    """

    def __init__(self):
        self.reporter = None

    def prepare_reporter(self):
        return Active()

    def fetch_reporter(self, lock):
        yield self.reporter

    def flush(self):
        return Active()

class Active(State):
    """Active state

    The pickup started and is running, typically, in the main process
    """
    def __init__(self,):

        self.queue = multiprocessing.Queue()
        self.reporter = ProgressReporter(queue=self.queue)
        self.reporter.queue_detach = self.queue_detach = multiprocessing.Queue()

        self.reporter.stream_queue = self.stream_queue = multiprocessing.Queue()

        self.reporter_yielded = False

        self._start_pickup()

        self.reporter.stream_redirection_enablaed = True
        if self.stream_redirection.disabled:
            self.reporter.stream_redirection_enablaed = False

    def _start_pickup(self):
        presentation = create_presentation()
        self.pickup = ProgressReportPickup(self.queue, presentation)

        self.stream_redirection = StreamRedirection(queue=self.stream_queue, presentation=presentation)
        self.stream_redirection.start()

    def _end_pickup(self):
        self.pickup.end()

        self.stream_redirection.end()

    def _restart_pickup(self):
        self._end_pickup()
        self._start_pickup()

    def fetch_reporter(self, lock):

        if not in_main_thread():
            self.to_restart_pickup = False
            yield self.reporter
            return

        if self.reporter_yielded:
            # called from an inner loop
            yield self.reporter
            return

        self.reporter_yielded = True
        self.to_restart_pickup = True
        while not self.queue_detach.empty():
            _ = self.queue_detach.get()

        try:
            yield self.reporter
        finally:
            self.reporter_yielded = False
            while not self.queue_detach.empty():
                _ = self.queue_detach.get()
                self.to_restart_pickup = False
            if not self.to_restart_pickup:
                return
            with lock:
                self._restart_pickup()

    def flush(self):
        self._restart_pickup()
        return self

    def shutdown(self):
        self._end_pickup()
        return Initial()

##__________________________________________________________________||
class Registered(State):
    """Registered state

    Typically, in a sub-process. The reporter, which has been created
    in the main process, is registered in the sub-process
    """

    def __init__(self, reporter):
        self.reporter = reporter
        if self.reporter is None:
            return
        if reporter.stream_redirection_enablaed:
            register_stream_queue(reporter.stream_queue)

    def fetch_reporter(self, lock):
        if self.reporter is None:
            yield self.reporter
            return

        self.reporter.queue_detach.put(True)
        yield self.reporter

class Disabled(State):
    """Disabled state
    """
    def __init__(self):
        self.reporter = None

##__________________________________________________________________||
def in_main_thread():
    """test if in the main thread
    """
    return threading.current_thread() == threading.main_thread()

##__________________________________________________________________||
