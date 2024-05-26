import sys
from collections.abc import Iterator
from uuid import UUID

import pytest

from atpbar.funcs import shutdown
from atpbar.presentation.base import Presentation
from atpbar.progress_report import Report


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
        self.task_ids.add(report['taskid'])
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


@pytest.fixture(autouse=True)
def mock_create_presentation(monkeypatch: pytest.MonkeyPatch) -> MockCreatePresentation:
    ret = MockCreatePresentation()
    module = sys.modules['atpbar.machine']
    monkeypatch.setattr(module, 'create_presentation', ret)
    return ret


@pytest.fixture(autouse=True)
def machine(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    module = sys.modules['atpbar.funcs']
    y = module.StateMachine()
    monkeypatch.setattr(module, '_machine', y)
    yield
    shutdown()


@pytest.fixture(autouse=True)
def reporter_interval(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    module = sys.modules['atpbar.progress_report.reporter']
    monkeypatch.setattr(module, 'DEFAULT_INTERVAL', 0)
    yield
