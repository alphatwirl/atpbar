from .report import Report


class ProgressReportComplementer:
    '''Complement progress reports

    Complement a progress report with the previous report for the same
    task.

    Parameters
    ----------
    report : Report
        A report must always include `task_id`. The first report for a task must
        include `done`, `total`, and 'name'. The `first` and `last` will be
        automatically determined if not given.

    '''

    def __init__(self) -> None:
        self._prev: Report | None = None

    def __call__(self, report: Report) -> None:
        self._complement(report)
        self._first(report)
        self._last(report)
        self._store(report.copy())

    def _complement(self, report: Report) -> None:
        if self._prev is None:
            return
        report_copy = report.copy()
        report.update(Report(task_id=report['task_id']))
        report.update(self._prev)
        report.update(report_copy)

    def _first(self, report: Report) -> None:
        if 'first' in report:
            return
        report['first'] = report['done'] == 0

    def _last(self, report: Report) -> None:
        if 'last' in report:
            return
        report['last'] = report['done'] >= report['total']

    def _store(self, report: Report) -> None:
        report.pop('first', None)
        report.pop('last', None)
        self._prev = report
