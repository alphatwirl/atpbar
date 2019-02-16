# Tai Sakuma <tai.sakuma@gmail.com>
import time

##__________________________________________________________________||
class ProgressReporter(object):
    """A progress reporter

    This class sends a `ProgressReport` to a progress monitor, e.g.,
    `ProgressMonitor` or `BProgressMonitor`, which, for example, uses
    the reports to update `ProgressBar` on the screen.

    An instance of this class is initialized with a message queue::

        reporter = ProgressReporter(queue)

    A reporter, an instance of this class, is typically created and
    initialized by a progress monitor (`ProgressMonitor` or
    `BProgressMonitor`), which keeps the other end of the message
    queue. A reporter and a monitor might be running in different
    processes.

    A report, an instance of `ProgressReport`, can be sent as::

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
        self.interval = 0.1 # [second]
        self.last_time = { } # key: taskid

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

        if not self._need_to_report(report):
            return

        self.queue.put(report)

        self.last_time[report.taskid] = self._time()

    def _need_to_report(self, report):

        if report.first():
            return True

        if report.last():
            return True

        if report.taskid not in self.last_time:
            return True

        if self._time() - self.last_time[report.taskid] > self.interval:
            return True

        return False

    def _time(self):
        return time.time()

##__________________________________________________________________||
