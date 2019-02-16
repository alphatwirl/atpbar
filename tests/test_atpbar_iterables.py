# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
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
def test_atpbar_iterables(mock_report_progress, iterable_class, content):
    iterable = iterable_class(content)

    ##
    returned = [ ]
    for e in atpbar(iterable):
        returned.append(e)

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_report_progress.call_args_list)
    for i, c in enumerate(mock_report_progress.call_args_list):
        args, kwargs = c
        report = args[0]
        assert i == report.done
        assert len(content) == report.total

##__________________________________________________________________||
@pytest.mark.parametrize('content', contents, ids=contents_ids)
@pytest.mark.parametrize('iterable_class', iterable_classes)
def test_atpbar_enumerate(mock_report_progress, iterable_class, content):
    iterable = iterable_class(content)

    ##
    returned = [ ]
    for i, e in enumerate(atpbar(iterable)):
        returned.append(e)

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_report_progress.call_args_list)
    for i, c in enumerate(mock_report_progress.call_args_list):
        args, kwargs = c
        report = args[0]
        assert i == report.done
        assert len(content) == report.total


##__________________________________________________________________||
