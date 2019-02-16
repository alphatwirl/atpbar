# Tai Sakuma <tai.sakuma@gmail.com>
import time
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressPrint, ProgressReport

##__________________________________________________________________||
@pytest.fixture()
def mock_time(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(time, 'time', ret)
    ret.return_value = 1533374055.904203
    return ret

@pytest.fixture()
def obj(mock_time):
    return ProgressPrint()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_report(obj, capsys):
    report = ProgressReport('task1', 0, 10)
    obj.present(report)
    captured = capsys.readouterr()
    stdout_lines = captured.out.strip().split('\n')
    assert 2 == len(stdout_lines)
    assert '        0 /       10 (  0.00%) task1' == stdout_lines[1]

##__________________________________________________________________||
