
import shutil

from .base import Presentation

##__________________________________________________________________||
MINIMUM_TERMINAL_WIDTH = 90

##__________________________________________________________________||
class ProgressBar(Presentation):
    stdout_stderr_redrection = True

    def __init__(self):
        super().__init__()
        self.interval = 0.1 # [second]
        self.width = self._get_width()

        self.active_bars = [ ]
        self.just_finised_bars = [ ]

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
        self._erase_active_bars()
        self._compose_just_finised_bars()
        self._compose_active_bars()
        self._draw_just_finised_bars()
        self._draw_active_bars()

    def _write(self, s, out):
        if not s:
            return
        self._erase_active_bars()
        out.write(s.rstrip())
        out.write('\n')
        out.flush()
        self._draw_active_bars()

    def _erase_active_bars(self):
        nlines = len(self._active_taskids) + len(self._finishing_taskids)
        # must be the same as len(self.active_bars)

        if nlines == 0:
            return

        code = '\033[1G' + '\033[A'*(nlines-1) + '\033[0J'
        # '\033[1G' move the cursor to the beginning of the line
        # '\033[A' move the cursor up
        # '\033[0J' clear from cursor to end of screen

        self.out.write(code)
        self.out.flush()

    def _compose_just_finised_bars(self):
        self.just_finised_bars = [
            self._compose_bar_from_taskid(i) for i in
            self._finishing_taskids]

    def _compose_active_bars(self):
        self.active_bars = [
            self._compose_bar_from_taskid(i) for i in
            self._active_taskids + self._new_taskids]

    def _compose_bar_from_taskid(self, taskid):
        report = self._report_dict[taskid]
        return self._compose_bar_from_report(report)

    def _compose_bar_from_report(self, report):

        percent = float(report['done'])/report['total'] if report['total'] > 0 else 1
        # e.g., 0.7143369818769065

        bar = (':' * int(percent * 40)).ljust(40, " ")
        # e.g., "::::::::::::::::::::::::::::            "

        percent = round(percent * 100, 2)
        # e.g., 71.43

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
        # e.g., "  71.43% ::::::::::::::::::::::::::::             |     3981 /     5573 |:  task name "

        ret = ret[:self.width].ljust(self.width, ' ')
        # e.g., "  71.43% ::::::::::::::::::::::::::::             |     3981 /     5573 |:  task na"

        return ret

    def _draw_just_finised_bars(self):
        if self.just_finised_bars:
            self.out.write("\n".join(self.just_finised_bars) + "\n")
            self.out.flush()

    def _draw_active_bars(self):
        if self.active_bars:
            self.out.write("\n".join(self.active_bars))
            self.out.flush()

##__________________________________________________________________||
