# Tai Sakuma <tai.sakuma@gmail.com>
import threading
import multiprocessing

from .reporter import ProgressReporter
from .pickup import ProgressReportPickup
from .presentation.create import create_presentation
from .misc import in_main_thread
from . import detach

##__________________________________________________________________||
class StateMachine:
    def __init__(self):
        self.lock = threading.Lock()
        self.state = Initial(self)

    def change_state(self, state):
        self.state = state

##__________________________________________________________________||
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

    def fetch_reporter(self):
        yield None

    def flush(self):
        pass

    def end_pickup(self):
        pass

##__________________________________________________________________||
class Initial(State):
    """Initial state

    The pickup is not running.
    """

    def __init__(self, machine, reporter=None, queue=None):
        super().__init__(machine)
        self.reporter = reporter
        self.queue = queue

    def prepare_reporter(self):
        next_state = Started(self.machine, reporter=self.reporter, queue=self.queue)
        self.machine.change_state(next_state)

    def fetch_reporter(self):
        yield self.reporter

    def flush(self):
        next_state = Started(self.machine, reporter=self.reporter, queue=self.queue)
        self.machine.change_state(next_state)

class Started(State):
    """Started state

    The pickup started and is running, typically, in the main process
    """
    def __init__(self, machine, reporter=None, queue=None):
        super().__init__(machine)

        self.reporter = reporter
        self.queue = queue
        self.pickup = None
        self.pickup_owned = False

        if self.reporter is None:
            if self.queue is None:
                self.queue = multiprocessing.Queue()
            self.reporter = ProgressReporter(queue=self.queue)

        self._start_pickup()

    def _start_pickup(self):
        presentation = create_presentation()
        self.pickup = ProgressReportPickup(self.queue, presentation)
        self.pickup.start()

    def _end_pickup(self):
        self.queue.put(None)
        self.pickup.join()
        self.pickup = None
        detach.to_detach_pickup = False

    def _restart_pickup(self):
        self._end_pickup()
        self._start_pickup()

    def fetch_reporter(self):

        if not in_main_thread():
            yield self.reporter
            return

        if self.pickup_owned:
            yield self.reporter
            return

        self.pickup_owned = True

        try:
            yield self.reporter
        finally:
            with self.machine.lock:
                self.pickup_owned = False
                if detach.to_detach_pickup:
                    return
                self._restart_pickup()

    def flush(self):
        self._restart_pickup()

    def end_pickup(self):
        self._end_pickup()
        next_state = Initial(self.machine, reporter=self.reporter, queue=self.queue)
        self.machine.change_state(next_state)

##__________________________________________________________________||
class Registered(State):
    """Registered state

    Typically, in a sub-process. The reporter, which has been created
    in the main process, is registered in the sub-process
    """

    def __init__(self, machine, reporter):
        super().__init__(machine)
        self.reporter = reporter

    def fetch_reporter(self):
        yield self.reporter

class Disabled(State):
    """Disabled state
    """
    def __init__(self, machine):
        super().__init__(machine)
        self.reporter = None

##__________________________________________________________________||
