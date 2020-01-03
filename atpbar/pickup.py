# Tai Sakuma <tai.sakuma@gmail.com>
import os, time
import threading

from .detach import detach_pickup

##__________________________________________________________________||
class ProgressReportPickup(threading.Thread):
    """A pickup of progress reports.

    This class picks up progress reports and presents them.

    """
    def __init__(self, queue, presentation):
        threading.Thread.__init__(self)
        self.queue = queue
        self.presentation = presentation
        self.last_wait_time = 1.0 # [second]
        self.taskids = set()

    def run(self):
        try:
            self._run_until_the_end_order_arrives()
            self._run_until_reports_stop_coming()
        except EOFError:
            pass

    def _run_until_the_end_order_arrives(self):
        end_order_arrived = False
        while not end_order_arrived:
            while not self.queue.empty():
                report = self.queue.get()
                if report is None: # the end order
                    end_order_arrived = True
                    continue
                self._process_report(report)
            time.sleep(0.001)

    def _run_until_reports_stop_coming(self):
        self._read_time()
        while self.presentation.active():
            if self._time() - self.last_time > self.last_wait_time:
                break
            while not self.queue.empty():
                report = self.queue.get()
                if report is None:
                    continue
                self._read_time()
                self._process_report(report)

    def _process_report(self, report):
        self._detach_self_if_necessary(report)
        self.presentation.present(report)

    def _detach_self_if_necessary(self, report):
        if report['taskid'] in self.taskids:
            return
        self.taskids.add(report['taskid'])
        if os.getpid() == report['pid'] and report['in_main_thread']:
            return
        detach_pickup()

    def _time(self):
        return time.time()

    def _read_time(self):
        self.last_time = self._time()

##__________________________________________________________________||
