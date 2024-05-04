import sys
import threading
import time
from abc import ABC, abstractmethod
from typing import TextIO
from uuid import UUID

from atpbar.progressreport import Report


class Presentation(ABC):
    """A base class of the progress presentation.

    A subclass of this class should implement ``_present()``.
    """

    stdout_stderr_redrection = False

    def __init__(self) -> None:

        self.out = sys.stdout
        self.err = sys.stderr

        self.lock = threading.Lock()

        self._new_taskids = list[UUID]()
        self._active_taskids = list[UUID]()  # in order of arrival
        self._finishing_taskids = list[UUID]()
        self._complete_taskids = list[UUID]()  # in order of completion
        self._report_dict = dict[UUID, Report]()

        self.interval = 1.0  # [second]
        self.last_time = time.time()

    def active(self) -> bool:
        if self._active_taskids:
            return True
        return False

    def present(self, report: Report) -> None:
        with self.lock:
            if not self._register_report(report):
                return
            if not self._need_to_present():
                return
            self._present()
            self._update_registry()
            self.last_time = time.time()

    @abstractmethod
    def _present(self) -> None:
        pass

    def _register_report(self, report: Report) -> bool:

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

    def _update_registry(self) -> None:
        self._active_taskids.extend(self._new_taskids)
        del self._new_taskids[:]

        self._complete_taskids.extend(self._finishing_taskids)
        del self._finishing_taskids[:]

    def _need_to_present(self) -> bool:

        if self._new_taskids:
            return True

        if self._finishing_taskids:
            return True

        if time.time() - self.last_time > self.interval:
            return True

        return False

    def stdout_write(self, s: str) -> None:
        with self.lock:
            self._stdout_write(s)

    def stderr_write(self, s: str) -> None:
        with self.lock:
            self._stderr_write(s)

    def _stdout_write(self, s: str) -> None:
        self._write(s, out=self.out)

    def _stderr_write(self, s: str) -> None:
        self._write(s, out=self.err)

    def _write(self, s: str, out: TextIO) -> None:
        out.write(s.rstrip())
        out.write("\n")
        out.flush()
