from collections.abc import Iterator
from contextlib import contextmanager
from uuid import UUID

from pytest import MonkeyPatch

from atpbar import callback, funcs
from atpbar.funcs import StateMachine, shutdown
from atpbar.presentation.base import Presentation
from atpbar.progress_report import Report, reporter


class MockProgressBar(Presentation):
    def __init__(self) -> None:
        super().__init__()
        self.reports = list[Report]()
        self.task_ids = set[UUID]()
        self.n_firsts = 0
        self.n_lasts = 0

    def __str__(self) -> str:
        lines = []
        l = '{}: # reports: {}, # task_ids: {}, # firsts: {}, # lasts: {}'.format(
            self.__class__.__name__,
            len(self.reports),
            len(self.task_ids),
            self.n_firsts,
            self.n_lasts,
        )
        lines.append(l)
        lines.extend(['  {}'.format(r) for r in self.reports])
        return '\n'.join(lines)

    def present(self, report: Report) -> None:
        super().present(report)
        self.reports.append(report)
        self.task_ids.add(report['task_id'])
        self.n_firsts += report['first']
        self.n_lasts += report['last']

    def _present(self, report: Report) -> None:
        pass


class MockCreatePresentation:
    '''A functor to mock `create_presentation()`.

    It keeps returned values so they can be examined later.
    '''

    def __init__(self) -> None:
        self.presentations = list[MockProgressBar]()

    def __str__(self) -> str:
        lines = []
        lines.append('{}:'.format(self.__class__.__name__))
        lines.extend(
            ['  {}'.format('\n  '.join(str(p).split('\n'))) for p in self.presentations]
        )
        return '\n'.join(lines)

    def __call__(self) -> MockProgressBar:
        ret = MockProgressBar()
        self.presentations.append(ret)
        return ret


@contextmanager
def monkeypatch_machine() -> Iterator[StateMachine]:
    with MonkeyPatch.context() as m:
        _machine = StateMachine(callback=callback.CallbackImp())
        m.setattr(funcs, '_machine', _machine)
        try:
            yield _machine
        finally:
            shutdown()


@contextmanager
def monkeypatch_reporter_interval() -> Iterator[None]:
    interval = 0
    with MonkeyPatch.context() as m:
        m.setattr(reporter, 'DEFAULT_INTERVAL', interval)
        yield


@contextmanager
def mock_create_presentation() -> Iterator[MockCreatePresentation]:
    y = MockCreatePresentation()
    with MonkeyPatch.context() as m:
        m.setattr(callback, 'create_presentation', y)
        yield y


@contextmanager
def mock_presentations() -> Iterator[list[MockProgressBar]]:
    with (
        monkeypatch_machine(),
        monkeypatch_reporter_interval(),
        mock_create_presentation() as y,
    ):
        yield y.presentations
