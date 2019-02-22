# Tai Sakuma <tai.sakuma@gmail.com>
import time
from .report import ProgressReportComplementer

##__________________________________________________________________||
DEFAULT_INTERVAL = 0.1 # [second]

##__________________________________________________________________||
class ProgressReporter(object):
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

    """
    def __init__(self, queue):
        self.queue = queue
        self.interval = DEFAULT_INTERVAL # [second]
        self.last_time = { } # key: taskid
        self.complete_report = ProgressReportComplementer()

    def __repr__(self):
        return '{}(queue={!r}, interval={!r})'.format(
            self.__class__.__name__,
            self.queue,
            self.interval
        )

    def report(self, report):
        """send ``report`` to a progress monitor

        Args:
            report (ProgressReport): a progress report

        """

        self.complete_report(report)

        if not self._need_to_report(report):
            return

        self.queue.put(report)

        self.last_time[report['taskid']] = self._time()

    def _need_to_report(self, report):

        if report['first']:
            return True

        if report['last']:
            return True

        if report['taskid'] not in self.last_time:
            return True

        if self._time() - self.last_time[report['taskid']] > self.interval:
            return True

        return False

    def _time(self):
        return time.time()

##__________________________________________________________________||
