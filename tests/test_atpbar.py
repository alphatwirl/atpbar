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

@pytest.fixture()
def mock_find_reporter(monkeypatch, mock_reporter):
    ret = mock.Mock()
    ret.return_value = mock_reporter
    monkeypatch.setattr(atpbar.main, 'find_reporter', ret)
    return ret

@pytest.fixture()
def mock_find_reporter_raise(monkeypatch, mock_reporter):
    ret = mock.Mock()
    mock_reporter.report.side_effect = Exception
    ret.return_value = mock_reporter
    monkeypatch.setattr(atpbar.main, 'find_reporter', ret)
    return ret

##__________________________________________________________________||
class Iter(object):
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
def test_atpbar_name_repr(mock_find_reporter, mock_reporter, caplog):

    iterable = Iter(content)
    returned = [e for e in atpbar.atpbar(iterable)]

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)
    for i, c in enumerate(mock_reporter.report.call_args_list):
        args, kwargs = c
        report = args[0]
        assert i == report.done
        assert len(content) == report.total
        assert 'Iter' == report.name # repr(iterable)

##__________________________________________________________________||
def test_atpbar_name_given(mock_find_reporter, mock_reporter, caplog):

    iterable = Iter(content)
    returned = [e for e in atpbar.atpbar(iterable, name='given')]

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)
    for i, c in enumerate(mock_reporter.report.call_args_list):
        args, kwargs = c
        report = args[0]
        assert i == report.done
        assert len(content) == report.total
        assert 'given' == report.name

##__________________________________________________________________||
def test_atpbar_raise(mock_find_reporter_raise, mock_reporter, caplog):

    iterable = Iter(content)
    returned = [e for e in atpbar.atpbar(iterable, name='given')]

    ##
    assert content == returned

##__________________________________________________________________||
