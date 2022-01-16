# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import threading
import time


##__________________________________________________________________||
class Presentation:
    """A base class of the progress presentation.

    A subclass of this class should implement ``_present()``.
    """

    stdout_stderr_redrection = False

    def __init__(self):

        self.out = sys.stdout
        self.err = sys.stderr

        self.lock = threading.Lock()

        self._new_taskids = []
        self._active_taskids = []  # in order of arrival
        self._finishing_taskids = []
        self._complete_taskids = []  # in order of completion
        self._report_dict = {}

        self.interval = 1.0  # [second]
        self.last_time = time.time()

    def active(self):
        if self._active_taskids:
            return True
        return False

    def present(self, report):
        with self.lock:
            if not self._register_report(report):
                return
            if not self._need_to_present():
                return
            self._present()
            self._update_registry()
            self.last_time = time.time()

    def _register_report(self, report):

        taskid = report["taskid"]

        if taskid in self._complete_taskids:
            return False

        self._report_dict[taskid] = report

        if taskid in self._finishing_taskids:
            return True

        if report["last"]:
            try:
                self._active_taskids.remove(taskid)
            except ValueError:
                pass

            try:
                self._new_taskids.remove(taskid)
            except ValueError:
                pass

            self._finishing_taskids.append(taskid)

            return True

        if taskid in self._active_taskids:
            return True

        if taskid in self._new_taskids:
            return True

        self._new_taskids.append(taskid)
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

        if time.time() - self.last_time > self.interval:
            return True

        return False

    def _get_time_track(self, start_time, percent):
        """Format seconds as hours, minutes and seconds."""
        time_elapsed = time.time() - start_time
        time_remaining = (time_elapsed * (100 / percent)) - time_elapsed if percent > 0 else 0

        return self._time_to_str(time_elapsed), self._time_to_str(time_remaining)

    def _time_to_str(self, t):
        mins = t // 60
        s = int(t % 60)

        h = int(mins // 60)
        m = int(mins % 60)

        if h:
            return "{0:d}:{1:02d}:{2:02d}".format(h, m, s)
        else:
            return "{0:02d}:{1:02d}".format(m, s)

    def stdout_write(self, s):
        with self.lock:
            self._stdout_write(s)

    def stderr_write(self, s):
        with self.lock:
            self._stderr_write(s)

    def _stdout_write(self, s):
        self._write(s, out=self.out)

    def _stderr_write(self, s):
        self._write(s, out=self.err)

    def _write(self, s, out):
        out.write(s.rstrip())
        out.write("\n")
        out.flush()


##__________________________________________________________________||
