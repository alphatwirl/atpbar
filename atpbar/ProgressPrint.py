# Tai Sakuma <tai.sakuma@gmail.com>
import sys, time

from .presentation import Presentation

##__________________________________________________________________||
class ProgressPrint(Presentation):
    def __init__(self):
        super(ProgressPrint, self).__init__()
        self.lines = [ ]
        self.last = [ ]
        self.interval = 60.0 # [second]

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def _present(self):
        self._create_lines()
        self._print_lines()

    def _create_lines(self):
        self.lines = [ ]
        for taskid in self._active_taskids + self._new_taskids:
            report = self._report_dict[taskid]
            line = self._create_line(report)
            self.lines.append(line)
        for taskid in self._finishing_taskids:
            report = self._report_dict[taskid]
            line = self._create_line(report)
            self.last.append(line)

    def _print_lines(self):
        sys.stdout.write("\n")
        sys.stdout.write(time.asctime(time.localtime(time.time())))
        sys.stdout.write("\n")
        if len(self.last) > 0: sys.stdout.write("\n".join(self.last) + "\n")
        sys.stdout.write("\n".join(self.lines) + "\n")
        sys.stdout.flush()

    def _create_line(self, report):
        percent = float(report.done)/report.total if report.total > 0 else 1
        percent = round(percent * 100, 2)
        return " {1:8d} / {2:8d} ({0:6.2f}%) {3} ".format(percent, report.done, report.total, report.name)

##__________________________________________________________________||
