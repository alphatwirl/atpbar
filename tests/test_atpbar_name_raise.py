# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

import atpbar

try:
    import unittest.mock as mock
except ImportError:
    import mock

##__________________________________________________________________||
@pytest.fixture()
def mock_reporter(monkeypatch):
    ret = mock.Mock()
    return ret

@pytest.fixture(autouse=True)
def mock_fetch_reporter(monkeypatch, mock_reporter):
    ret = mock.Mock()
    ret.return_value.__enter__ = mock.Mock()
    ret.return_value.__enter__.return_value = mock_reporter
    ret.return_value.__exit__ = mock.Mock()
    monkeypatch.setattr(atpbar.main, 'fetch_reporter', ret)
    return ret

@pytest.fixture(autouse=True)
def mock_fetch_reporter_raise(monkeypatch, mock_reporter):
    mock_reporter.report.side_effect = Exception
    ret = mock.Mock()
    ret.return_value.__enter__ = mock.Mock()
    ret.return_value.__enter__.return_value = mock_reporter
    ret.return_value.__exit__ = mock.Mock()
    monkeypatch.setattr(atpbar.main, 'fetch_reporter', ret)
    return ret

##__________________________________________________________________||
class Iter:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return self.__class__.__name__

    def __len__(self):
        return len(self.content)

    def __iter__(self):
        for e in self.content:
            yield e

##__________________________________________________________________||
content = [mock.sentinel.item1, mock.sentinel.item2, mock.sentinel.item3]

##__________________________________________________________________||
def test_atpbar_name_repr(mock_fetch_reporter, mock_reporter, caplog):

    iterable = Iter(content)
    returned = [e for e in atpbar.atpbar(iterable)]

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)

    # first report
    args, _ = mock_reporter.report.call_args_list[0]
    report = args[0]
    assert 0 == report['done']
    assert len(content) == report['total']
    assert 'Iter' == report['name'] # repr(iterable)

##__________________________________________________________________||
def test_atpbar_name_given(mock_fetch_reporter, mock_reporter, caplog):

    iterable = Iter(content)
    returned = [e for e in atpbar.atpbar(iterable, name='given')]

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)

    # first report
    args, _ = mock_reporter.report.call_args_list[0]
    report = args[0]
    assert 0 == report['done']
    assert len(content) == report['total']
    assert 'given' == report['name']

##__________________________________________________________________||
def test_atpbar_raise(mock_fetch_reporter_raise, mock_reporter, caplog):

    iterable = Iter(content)
    returned = [e for e in atpbar.atpbar(iterable, name='given')]

    ##
    assert content == returned

##__________________________________________________________________||
