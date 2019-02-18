# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import atpbar

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

def test_mock_fetch_reporter(mock_fetch_reporter, mock_reporter):
    with mock_fetch_reporter() as reporter:
        assert reporter is mock_reporter

##__________________________________________________________________||
class Iter(object):
    def __init__(self, content):
        self.content = content

    def __len__(self):
        return len(self.content)

    def __iter__(self):
        for e in self.content:
            yield e

class GetItem(object):
    def __init__(self, content):
        self.content = content

    def __len__(self):
        return len(self.content)

    def __getitem__(self, i):
        return self.content[i]

##__________________________________________________________________||
iterable_classes = [list, Iter, GetItem]

empty = [ ]
one = [mock.sentinel.item1]
three = [mock.sentinel.item1, mock.sentinel.item2, mock.sentinel.item3]
contents = [empty, one, three]
contents_ids = ['empty', 'one', 'three']

##__________________________________________________________________||
@pytest.mark.parametrize('content', contents, ids=contents_ids)
@pytest.mark.parametrize('iterable_class', iterable_classes)
def test_iterable(iterable_class, content):
    iterable = iterable_class(content)
    assert content == [e for e in iterable]

##__________________________________________________________________||
@pytest.mark.parametrize('content', contents, ids=contents_ids)
@pytest.mark.parametrize('iterable_class', iterable_classes)
def test_atpbar_iterables(mock_reporter, iterable_class, content):
    iterable = iterable_class(content)

    ##
    returned = [ ]
    for e in atpbar.atpbar(iterable):
        returned.append(e)

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)
    for i, c in enumerate(mock_reporter.report.call_args_list):
        args, kwargs = c
        report = args[0]
        assert i == report.done
        assert len(content) == report.total

##__________________________________________________________________||
@pytest.mark.parametrize('content', contents, ids=contents_ids)
@pytest.mark.parametrize('iterable_class', iterable_classes)
def test_atpbar_enumerate(mock_reporter, iterable_class, content):
    iterable = iterable_class(content)

    ##
    returned = [ ]
    for i, e in enumerate(atpbar.atpbar(iterable)):
        returned.append(e)

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)
    for i, c in enumerate(mock_reporter.report.call_args_list):
        args, kwargs = c
        report = args[0]
        assert i == report.done
        assert len(content) == report.total


##__________________________________________________________________||
