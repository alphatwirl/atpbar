# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import atpbar

##__________________________________________________________________||
@pytest.fixture()
def mock_report_progress(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(atpbar, 'report_progress', ret)
    return ret

##__________________________________________________________________||
class Iter(object):
    def __init__(self, content):
        self.content = content

    def __iter__(self):
        for e in self.content:
            yield e

##__________________________________________________________________||
content = [mock.sentinel.item1, mock.sentinel.item2, mock.sentinel.item3]

##__________________________________________________________________||
def test_atpbar_no_len(mock_report_progress, caplog):
    iterable = Iter(content)

    ##
    returned = [ ]
    with caplog.at_level(logging.WARNING):
        for e in atpbar.atpbar(iterable):
            returned.append(e)

    ##
    assert content == returned

    ##
    assert not mock_report_progress.call_args_list

    ##
    assert 2 == len(caplog.records)
    assert 'WARNING' == caplog.records[0].levelname
    assert 'length is unknown' in caplog.records[0].msg

##__________________________________________________________________||
