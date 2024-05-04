import shutil
from typing import TextIO
from uuid import UUID

from .base import Presentation, Report

MINIMUM_TERMINAL_WIDTH = 90


class ProgressBar(Presentation):
    stdout_stderr_redrection = True

    def __init__(self) -> None:
        super().__init__()
        self.interval = 0.1  # [second]
        self.width = self._get_width()

        self.active_bars = list[str]()
        self.just_finised_bars = list[str]()

    def __repr__(self) -> str:
        return "{}()".format(self.__class__.__name__)

    def _get_width(self) -> int:
        try:
            columns = shutil.get_terminal_size().columns
            return max(MINIMUM_TERMINAL_WIDTH, columns - 1)
        except AttributeError:
            return MINIMUM_TERMINAL_WIDTH

    def _present(self) -> None:
        self._erase_active_bars()
        self._compose_just_finised_bars()
        self._compose_active_bars()
        self._draw_just_finised_bars()
        self._draw_active_bars()

    def _write(self, s: str, out: TextIO) -> None:
        if not s:
            return
        self._erase_active_bars()
        out.write(s.rstrip())
        out.write("\n")
        out.flush()
        self._draw_active_bars()

    def _erase_active_bars(self) -> None:
        nlines = len(self._active_taskids) + len(self._finishing_taskids)
        # must be the same as len(self.active_bars)

        if nlines == 0:
            return

        code = "\033[1G" + "\033[A" * (nlines - 1) + "\033[0J"
        # '\033[1G' move the cursor to the beginning of the line
        # '\033[A' move the cursor up
        # '\033[0J' clear from cursor to end of screen

        self.out.write(code)
        self.out.flush()

    def _compose_just_finised_bars(self) -> None:
        self.just_finised_bars = [
            self._compose_bar_from_taskid(i) for i in self._finishing_taskids
        ]

    def _compose_active_bars(self) -> None:
        self.active_bars = [
            self._compose_bar_from_taskid(i)
            for i in self._active_taskids + self._new_taskids
        ]

    def _compose_bar_from_taskid(self, taskid: UUID) -> str:
        report = self._report_dict[taskid]
        return self._compose_bar_from_report(report)

    def _compose_bar_from_report(self, report: Report) -> str:

        percent = float(report["done"]) / report["total"] if report["total"] > 0 else 1
        # e.g., 0.7143369818769065

        bar = (":" * int(percent * 40)).ljust(40, " ")
        # e.g., "::::::::::::::::::::::::::::            "

        percent = round(percent * 100, 2)
        # e.g., 71.43

        format = " {percent:6.2f}% {bar:s} | {done:8d} / {total:8d} |:  {name} "

        ret = format.format(
            percent=percent,
            bar=bar,
            done=report["done"],
            total=report["total"],
            name=report["name"],
        )
        # e.g., "  71.43% ::::::::::::::::::::::::::::             |     3981 /     5573 |:  task name "

        ret = ret[: self.width].ljust(self.width, " ")
        # e.g., "  71.43% ::::::::::::::::::::::::::::             |     3981 /     5573 |:  task na"

        return ret

    def _draw_just_finised_bars(self) -> None:
        if self.just_finised_bars:
            self.out.write("\n".join(self.just_finised_bars) + "\n")
            self.out.flush()

    def _draw_active_bars(self) -> None:
        if self.active_bars:
            self.out.write("\n".join(self.active_bars))
            self.out.flush()
