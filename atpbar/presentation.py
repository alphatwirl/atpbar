# Tai Sakuma <tai.sakuma@gmail.com>
import time

##__________________________________________________________________||
class Presentation(object):
    """A base class of the progress presentation.

    A subclass of this class should implement ``_present()``.
    """

    def __init__(self):

        self._new_taskids = [ ]
        self._active_taskids = [ ] # in order of arrival
        self._finishing_taskids = [ ]
        self._complete_taskids = [ ] # in order of completion
        self._report_dict = { }

        self.interval = 1.0 # [second]
        self._read_time()

    def active(self):
        if self._active_taskids:
            return True
        return False

    def present(self, report):

        if not self._register_report(report):
            return

        if not self._need_to_present():
            return

        self._present()

        self._update_registry()

        self._read_time()

    def _register_report(self, report):

        if report.taskid in self._complete_taskids:
            return False

        self._report_dict[report.taskid] = report

        if report.taskid in self._finishing_taskids:
            return True

        if report.last():
            try:
                self._active_taskids.remove(report.taskid)
            except ValueError:
                pass

            try:
                self._new_taskids.remove(report.taskid)
            except ValueError:
                pass

            self._finishing_taskids.append(report.taskid)

            return True

        if report.taskid in self._active_taskids:
            return True

        if report.taskid in self._new_taskids:
            return True

        self._new_taskids.append(report.taskid)
        return True

    def _update_registry(self):
        self._active_taskids.extend(self._new_taskids)
        del self._new_taskids[:]

        self._complete_taskids.extend(self._finishing_taskids)
        del self._finishing_taskids[:]

    def _need_to_present(self):

        if self._new_taskids:
            return True

        if self._finishing_taskids:
            return True

        if self._time() - self.last_time > self.interval:
            return True

        return False

    def _time(self):
        return time.time()

    def _read_time(self):
        self.last_time = self._time()

##__________________________________________________________________||
