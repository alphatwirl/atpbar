# Tai Sakuma <tai.sakuma@gmail.com>
import sys

from .presentation import Presentation

##__________________________________________________________________||
class ProgressBar(Presentation):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.lines = [ ]
        self.interval = 0.1 # [second]

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def _present(self):
        self._delete_previous_lines()
        self._create_lines()
        self._print_lines()

    def _delete_previous_lines(self):
        if len(self.lines) >= 1:
            sys.stdout.write('\b'*len(self.lines[-1]))
        if len(self.lines) >= 2:
            sys.stdout.write('\033M'*(len(self.lines) - 1))
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
        nameFieldLength = 32
        percent = float(report.done)/report.total if report.total > 0 else 1
        bar = (':' * int(percent * 40)).ljust(40, " ")
        percent = round(percent * 100, 2)
        name = report.name[0:nameFieldLength]
        return " {3:6.2f}% {2:s} | {4:8d} / {5:8d} |:  {0:<{1}s} ".format(name, nameFieldLength, bar, percent, report.done, report.total)

    def _print_lines(self):
        if len(self.last) > 0: sys.stdout.write("\n".join(self.last) + "\n")
        sys.stdout.write("\n".join(self.lines))
        sys.stdout.flush()

##__________________________________________________________________||
