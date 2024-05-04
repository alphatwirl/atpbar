import time
from multiprocessing import Queue
from typing import TYPE_CHECKING
from uuid import UUID

from .complement import ProgressReportComplementer
from .report import Report

if TYPE_CHECKING:
    from atpbar.stream import StreamQueue

DEFAULT_INTERVAL = 0.1  # [second]


class ProgressReporter:
    """A progress reporter

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
    """

    def __init__(
        self,
        queue: 'Queue[Report]',
        notices_from_sub_processes: 'Queue[bool]',
        stream_queue: 'StreamQueue',
    ) -> None:
        self.queue = queue
        self.interval = DEFAULT_INTERVAL  # [second]
        self.last_time = dict[UUID, float]()
        self.complete_report = ProgressReportComplementer()
        self.notices_from_sub_processes = notices_from_sub_processes
        self.stream_queue = stream_queue
        self.stream_redirection_enablaed = True

    def __repr__(self) -> str:
        return "{}(queue={!r}, interval={!r})".format(
            self.__class__.__name__, self.queue, self.interval
        )

    def report(self, report: Report) -> None:
        """send ``report`` to a progress monitor

        Parameters
        ----------
        report : ProgressReport
            a progress report

        """

        self.complete_report(report)

        if not self._need_to_report(report):
            return

        self.queue.put(report)

        self.last_time[report["taskid"]] = time.time()

    def _need_to_report(self, report: Report) -> bool:

        if report["first"]:
            return True

        if report["last"]:
            return True

        if report["taskid"] not in self.last_time:
            return True

        if time.time() - self.last_time[report["taskid"]] > self.interval:
            return True

        return False
