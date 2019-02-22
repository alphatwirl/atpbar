# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ProgressReportComplementer(object):
    """Complement progress reports

    Complement a progress report with the previous report for the same
    task.

    Parameters
    ----------
    report : dict
        A progress report, a dict with the following entries. The
        `taskid` must be always given. The first report for a task
        must include `done`, `total`, 'name', 'pid', and
        'in_main_thread`. The `first` and `last` will be automatically
        determined if not given.

        taskid : immutable
            The unique task ID.
        done : int, optional
            The number of the iterations done so far
        total : int
            The total iterations to be done
        name : str
            A name of the task. It will be use as the label on the
            progress bars.
        pid : optional
            The process ID, e.g., the value returned by `os.getpid()`
        in_main_thread : bool
            `True` if the task is running in the main thread of the
            process. `False` otherwise
        first : bool
            `True` if the first report for the task. If not given,
            automatically determined from `done`; `True` if `done` is
            0, `False` otherwise
        last : bool
            `True` if the last report for the task. If not given,
            automatically determined from `done` and `total`; `True`
            if `done` equals `total`, `False` otherwise

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
