# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import shutil

from .base import Presentation

##__________________________________________________________________||
MINIMUM_TERMINAL_WIDTH = 90

##__________________________________________________________________||
class ProgressBar(Presentation):
    def __init__(self):
        super().__init__()
        self.lines = [ ]
        self.interval = 0.1 # [second]
        self.width = self._get_width()

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def _get_width(self):
        try:
            columns = shutil.get_terminal_size().columns
            return max(MINIMUM_TERMINAL_WIDTH, columns - 1)
        except AttributeError:
            return MINIMUM_TERMINAL_WIDTH

    def _present(self):
        self._delete_previous_lines()
        self._create_lines()
        self._print_lines()

    def _delete_previous_lines(self):
        if len(self.lines) >= 1:
            sys.stdout.write('\033[2K\033[1G')
            # '\033[2K' erase the line
            # '\033[1G' move the cursor to the beginning of the line
        if len(self.lines) >= 2:
            sys.stdout.write('\033[A\033[K'*(len(self.lines) - 1))
            # '\033[A' move the cursor up
            # '\033[K' clear from cursor to the end of the line
        self.lines = [ ]
        self.last = [ ]

    def _create_lines(self):
        for taskid in self._active_taskids + self._new_taskids:
            report = self._report_dict[taskid]
            line = self._create_line(report)
            self.lines.append(line)
        for taskid in self._finishing_taskids:
            report = self._report_dict[taskid]
            line = self._create_line(report)
            self.last.append(line)

    def _create_line(self, report):
        percent = float(report['done'])/report['total'] if report['total'] > 0 else 1
        bar = (':' * int(percent * 40)).ljust(40, " ")
        percent = round(percent * 100, 2)
        format = ' {percent:6.2f}% {bar:s} | {done:8d} / {total:8d} |:  {name} '

        if "start_time" in report.keys():
            elapsed_str, remaining_str = self._get_time_track(
                report["start_time"], percent
            )
            format += " | [{:s} / {:s}]".format(elapsed_str, remaining_str)

        ret = format.format(
            percent=percent, bar=bar,
            done=report['done'], total=report['total'],
            name=report['name'])
        ret = ret[:self.width].ljust(self.width, ' ')
        return ret

    def _print_lines(self):
        if len(self.last) > 0: sys.stdout.write("\n".join(self.last) + "\n")
        sys.stdout.write("\n".join(self.lines))
        sys.stdout.flush()

##__________________________________________________________________||
