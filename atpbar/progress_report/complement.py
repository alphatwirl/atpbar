from uuid import UUID

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
        self.previous_reports = dict[UUID, Report]()

    def __call__(self, report: Report) -> None:
        task_id = report['task_id']
        if task_id in self.previous_reports:
            self._complement(task_id, report)
        self._first(report)
        self._last(report)
        self._store(task_id, report.copy())

    def _complement(self, task_id: UUID, report: Report) -> None:
        report_copy = report.copy()
        report.update(Report(task_id=task_id))
        report.update(self.previous_reports[task_id])
        report.update(report_copy)

    def _first(self, report: Report) -> None:
        if 'first' in report:
            return
        report['first'] = report['done'] == 0

    def _last(self, report: Report) -> None:
        if 'last' in report:
            return
        report['last'] = report['done'] >= report['total']

    def _store(self, task_id: UUID, report: Report) -> None:
        report.pop('first', None)
        report.pop('last', None)
        self.previous_reports[task_id] = report
