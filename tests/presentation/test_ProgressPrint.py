
import time
import pytest

import unittest.mock as mock

from atpbar.presentation.txtprint import ProgressPrint

##__________________________________________________________________||
@pytest.fixture(autouse=True)
def mock_time(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(time, 'time', ret)
    ret.return_value = 1533374055.904203
    return ret

##__________________________________________________________________||
def test_repr():
    obj = ProgressPrint()
    repr(obj)

def test_report(capsys):
    obj = ProgressPrint()
    report = dict(taskid=1, name='task1', done=0, total=10, first=True, last=False)
    obj.present(report)
    captured = capsys.readouterr()
    stdout_lines = captured.out.strip().split('\n')
    assert 1 == len(stdout_lines)
    assert (' :        0 /       10 (  0.00%): task1' in stdout_lines[0])

##__________________________________________________________________||
