import time
from uuid import UUID

from .base import Presentation, Report


class ProgressPrint(Presentation):
    def __init__(self) -> None:
        super().__init__()
        self.interval = 60.0  # [second]
        self.last_time_map = dict[UUID, float]()

    def __repr__(self) -> str:
        return "{}()".format(self.__class__.__name__)

    def present(self, report: Report) -> None:

        if not self._register_report(report):
            return

        if not self._need_to_present_(report):
            return

        self._present_(report)

        self.last_time_map[report["taskid"]] = self._time()
    
    def _present(self) -> None:
        pass

    def _present_(self, report: Report) -> None:
        time_ = time.strftime("%m/%d %H:%M", time.localtime(time.time()))
        percent = float(report["done"]) / report["total"] if report["total"] > 0 else 1
        percent = round(percent * 100, 2)
        line = "{time} : {done:8d} / {total:8d} ({percent:6.2f}%): {name} ".format(
            time=time_,
            done=report["done"],
            total=report["total"],
            percent=percent,
            name=report["name"],
        )
        line = "{}\n".format(line)
        self.out.write(line)
        self.out.flush()

    def _need_to_present_(self, report: Report) -> bool:

        if report["first"]:
            return True

        if report["last"]:
            return True

        if report["taskid"] not in self.last_time_map:
            return True

        if self._time() - self.last_time_map[report["taskid"]] > self.interval:
            return True

        return False

    def _time(self) -> float:
        return time.time()
