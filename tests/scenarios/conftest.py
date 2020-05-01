# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import threading

import pytest

import unittest.mock as mock

from atpbar.presentation.base import Presentation

from atpbar.funcs import shutdown

##__________________________________________________________________||
class MockProgressBar(Presentation):
    def __init__(self):
        super().__init__()
        self.reports = [ ]
        self.taskids = set()
        self.nfirsts = 0
        self.nlasts = 0

    def __str__(self):
        lines = [ ]
        l = '{}: # reports: {}, # taskids: {}, # firsts: {}, # lasts: {}'.format(
            self.__class__.__name__,
            len(self.reports), len(self.taskids), self.nfirsts, self.nlasts
        )
        lines.append(l)
        lines.extend(['  {}'.format(r) for r in self.reports])
        return '\n'.join(lines)

    def present(self, report):
        super().present(report)
        self.reports.append(report)
        self.taskids.add(report['taskid'])
        self.nfirsts += report['first']
        self.nlasts += report['last']

    def _present(self):
        pass

class MockCreatePresentation:
    """A functor to mock `create_presentation()`.

    It keeps returned values so they can be examined later.
    """
    def __init__(self):
        self.presentations = [ ]

    def __str__(self):
        lines = [ ]
        lines.append('{}:'.format(self.__class__.__name__))
        lines.extend(['  {}'.format('\n  '.join(str(p).split('\n'))) for p in self.presentations])
        return '\n'.join(lines)

    def __call__(self):
        ret = MockProgressBar()
        self.presentations.append(ret)
        return ret

@pytest.fixture(autouse=True)
def mock_create_presentation(monkeypatch):
    ret = MockCreatePresentation()
    module = sys.modules['atpbar.machine']
    monkeypatch.setattr(module, 'create_presentation', ret)
    return ret

##__________________________________________________________________||
@pytest.fixture(autouse=True)
def machine(monkeypatch):
    module = sys.modules['atpbar.funcs']
    y = module.StateMachine()
    monkeypatch.setattr(module, '_machine', y)
    yield
    shutdown()

##__________________________________________________________________||
@pytest.fixture(autouse=True)
def reporter_interval(monkeypatch):
    module = sys.modules['atpbar.reporter']
    monkeypatch.setattr(module, 'DEFAULT_INTERVAL', 0)
    yield

##__________________________________________________________________||
