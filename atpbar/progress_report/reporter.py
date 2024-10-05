import time
from multiprocessing import Queue
from uuid import UUID

from atpbar.presentation import create_presentation
from atpbar.stream import StreamQueue, StreamRedirection, register_stream_queue

from .pickup import ProgressReportPickup
from .report import Report

DEFAULT_INTERVAL = 0.1  # [second]


class ProgressReporter:
    '''A progress reporter.

    NOTE: This docstring is outdated.

    This class sends progress reports. The reports will be picked up
    by the pickup (`ProgressReportPickup`), which uses the reports,
    for example, to update `ProgressBar` on the screen.

    An instance of this class is initialized with a message queue::

        reporter = ProgressReporter(queue)

    The pickup, which is running in a sub-thread of the main process,
    needs to have the same queue.

    A report can be sent as::

        reporter.report(report)

    This method can be frequently called multiple times. However,
    after sending one report, the reporter wait for a certain
    ``interval`` (0.1 seconds by default) before sending another
    report of the same task. Reports from the same task received
    within this interval will be discarded. The exception for this is
    the last report. The last report, which indicates the completion
    of the task, will be always sent to the progress monitor
    regardless of whether it is given within the interval.

    Parameters
    ----------
    queue : multiprocessing.Queue
        The queue through which this class sends progress reports.
    '''

    def __init__(self) -> None:
        self.queue: Queue[Report] = Queue()
        self.notices_from_sub_processes: Queue[bool] = Queue()
        self.stream_queue: StreamQueue = Queue()
        self.interval = DEFAULT_INTERVAL  # [second]
        self.last_time = dict[UUID, float]()
        self.stream_redirection_enabled = True

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(queue={self.queue!r}, interval={self.interval!r})'

    def start_pickup(self) -> None:
        presentation = create_presentation()
        self.pickup = ProgressReportPickup(self.queue, presentation)

        self.stream_redirection = StreamRedirection(
            queue=self.stream_queue, presentation=presentation
        )
        self.stream_redirection.start()
        self.stream_redirection_enabled = not self.stream_redirection.disabled

    def end_pickup(self) -> None:
        self.pickup.end()
        self.stream_redirection.end()

    def restart_pickup(self) -> None:
        self.end_pickup()
        self.start_pickup()

    def notice(self) -> None:
        self.notices_from_sub_processes.put(True)

    def empty_notices(self) -> bool:
        ret = False
        while not self.notices_from_sub_processes.empty():
            _ = self.notices_from_sub_processes.get()
            ret = True
        return ret

    def register(self) -> None:
        if self.stream_redirection_enabled:
            register_stream_queue(self.stream_queue)

    def report(self, report: Report) -> None:
        '''send ``report`` to a progress monitor

        Parameters
        ----------
        report : ProgressReport
            a progress report

        '''

        if not self._need_to_report(report):
            return

        self.queue.put(report)

        self.last_time[report['task_id']] = time.time()

    def _need_to_report(self, report: Report) -> bool:
        if report['first']:
            return True

        if report['last']:
            return True

        if report['task_id'] not in self.last_time:
            return True

        if time.time() - self.last_time[report['task_id']] > self.interval:
            return True

        return False
