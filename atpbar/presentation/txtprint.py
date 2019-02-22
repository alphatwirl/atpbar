# Tai Sakuma <tai.sakuma@gmail.com>
import sys, time

from .base import Presentation

##__________________________________________________________________||
class ProgressPrint(Presentation):
    def __init__(self):
        super(ProgressPrint, self).__init__()
        self.interval = 60.0 # [second]
        self.last_time = { } # key: taskid

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def present(self, report):

        if not self._register_report(report):
            return

        if not self._need_to_present(report):
            return

        self._present(report)

        self.last_time[report['taskid']] = self._time()

    def _present(self, report):
        time_ = time.strftime('%m/%d %H:%M', time.localtime(time.time()))
        percent = float(report['done'])/report['total'] if report['total'] > 0 else 1
        percent = round(percent * 100, 2)
        line = "{time} : {done:8d} / {total:8d} ({percent:6.2f}%): {name} ".format(
            time=time_,
            done=report['done'], total=report['total'],
            percent=percent, name=report['name']
        )
        line = '{}\n'.format(line)
        sys.stdout.write(line)
        sys.stdout.flush()

    def _need_to_present(self, report):

        if report['first']:
            return True

        if report['last']:
            return True

        if report['taskid'] not in self.last_time:
            return True

        if self._time() - self.last_time[report['taskid']] > self.interval:
            return True

        return False

    def _time(self):
        return time.time()

##__________________________________________________________________||
