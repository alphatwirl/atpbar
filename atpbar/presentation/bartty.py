# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys

from .base import Presentation

##__________________________________________________________________||
MINIMUM_TERMINAL_WIDTH = 90

##__________________________________________________________________||
class ProgressBar(Presentation):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.lines = [ ]
        self.interval = 0.1 # [second]
        self.width = self._get_width()

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def _get_width(self):
        try:
            import shutil
            columns = shutil.get_terminal_size().columns
            return max(MINIMUM_TERMINAL_WIDTH, columns - 1)
        except AttributeError:
            # Python 2
            pass

        try:
            rows, columns = os.popen('stty size', 'r').read().split()
            columns = int(columns)
            return max(MINIMUM_TERMINAL_WIDTH, columns - 1)
        except Exception:
            return MINIMUM_TERMINAL_WIDTH

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
        percent = float(report['done'])/report['total'] if report['total'] > 0 else 1
        bar = (':' * int(percent * 40)).ljust(40, " ")
        percent = round(percent * 100, 2)
        format = ' {percent:6.2f}% {bar:s} | {done:8d} / {total:8d} |:  {name} '
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
