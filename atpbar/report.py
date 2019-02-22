# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ProgressReport(object):
    """A progress report

    The `taskid` is mandatory. The other fields will be complemented
    with the previous report for the same `taskid`.

    Parameters
    ----------
    taskid : immutable
        The unique task ID.
    name : str, optional
        A name of the task. It will be use as the label on the
        progress bars.
    done : int, optional
        The number of the iterations done so far
    total : int, optional
        The total iterations to be done
    pid : optional
        The process ID, e.g., the value returned by `os.getpid()`
    in_main_thread : bool, optional
        True if the task is running in the main thread of the process.
        False otherwise

    """

    def __init__(self, taskid, done=None, total=None, name=None, pid=None,
                 in_main_thread=None):
        self.taskid = taskid
        self.name = name
        self.done = done
        self.total = total
        self.pid = pid
        self.in_main_thread = in_main_thread

    def __repr__(self):
        name_value_pairs = (
            ('taskid', self.taskid),
            ('name', self.name),
            ('done', self.done),
            ('total', self.total),
            ('pid', self.pid),
            ('in_main_thread', self.in_main_thread),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def last(self):
         return self.done == self.total

    def first(self):
         return self.done == 0

##__________________________________________________________________||
class ProgressReportComplementer(object):
    """Complement progress reports

    Complement a progress report with the previous report for the same
    task.

    """
    def __init__(self):
        self.previous_reports = { }
        self.volatile_fileds = ('first', 'last')

    def __call__(self, report):
        taskid = report['taskid']
        if taskid in self.previous_reports:
            self._complement(taskid, report)
        self._first(report)
        self._last(report)
        self._store(taskid, report.copy())

    def _complement(self, taskid, report):
        report_copy = report.copy()
        report.clear()
        report.update(self.previous_reports[taskid])
        report.update(report_copy)

    def _first(self, report):
        if 'first' in report:
            return
        report['first'] = (report['done'] == 0)

    def _last(self, report):
        if 'last' in report:
            return
        report['last'] = (report['done'] >= report['total'])

    def _store(self, taskid, report):
        for k in self.volatile_fileds:
            report.pop(k, None)
        self.previous_reports[taskid] = report

##__________________________________________________________________||
