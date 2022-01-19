# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import unittest.mock as mock

import pytest

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
    monkeypatch.setattr(atpbar.main, "fetch_reporter", ret)
    return ret


def test_mock_fetch_reporter(mock_fetch_reporter, mock_reporter):
    with mock_fetch_reporter() as reporter:
        assert reporter is mock_reporter


##__________________________________________________________________||
class Iter:
    def __init__(self, content):
        self.content = content

    def __iter__(self):
        for e in self.content:
            yield e


##__________________________________________________________________||
content = [mock.sentinel.item1, mock.sentinel.item2, mock.sentinel.item3]

##__________________________________________________________________||
def test_atpbar_no_len(mock_reporter, caplog):
    iterable = Iter(content)

    ##
    returned = []
    with caplog.at_level(logging.WARNING):
        for e in atpbar.atpbar(iterable):
            returned.append(e)

    ##
    assert content == returned

    ##
    assert not mock_reporter.report.call_args_list

    ##
    assert 2 == len(caplog.records)
    assert "WARNING" == caplog.records[0].levelname
    assert "length is unknown" in caplog.records[0].msg


##__________________________________________________________________||
