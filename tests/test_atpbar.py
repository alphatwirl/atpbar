# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

import alphatwirl
from alphatwirl.progressbar import atpbar

try:
    import unittest.mock as mock
except ImportError:
    import mock

##__________________________________________________________________||
@pytest.fixture()
def mock_report_progress(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(alphatwirl.progressbar, 'report_progress', ret)
    return ret

@pytest.fixture()
def mock_report_progress_raise(monkeypatch):
    ret = mock.Mock()
    ret.side_effect = Exception
    monkeypatch.setattr(alphatwirl.progressbar, 'report_progress', ret)
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
def test_atpbar_name_repr(mock_report_progress, caplog):

    iterable = Iter(content)
    returned = [e for e in atpbar(iterable)]

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_report_progress.call_args_list)
    for i, c in enumerate(mock_report_progress.call_args_list):
        args, kwargs = c
        report = args[0]
        assert i == report.done
        assert len(content) == report.total
        assert 'Iter' == report.name # repr(iterable)
        print(report)

##__________________________________________________________________||
def test_atpbar_name_given(mock_report_progress, caplog):

    iterable = Iter(content)
    returned = [e for e in atpbar(iterable, name='given')]

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_report_progress.call_args_list)
    for i, c in enumerate(mock_report_progress.call_args_list):
        args, kwargs = c
        report = args[0]
        assert i == report.done
        assert len(content) == report.total
        assert 'given' == report.name
        print(report)

##__________________________________________________________________||
def test_atpbar_raise(mock_report_progress_raise, caplog):

    iterable = Iter(content)
    returned = [e for e in atpbar(iterable, name='given')]

    ##
    assert content == returned

##__________________________________________________________________||
