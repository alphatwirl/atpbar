import time
import unittest.mock as mock
import uuid

import pytest

from atpbar.presentation.txtprint import ProgressPrint
from atpbar.progress_report import Report


@pytest.fixture(autouse=True)
def mock_time(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
    ret = mock.Mock()
    monkeypatch.setattr(time, 'time', ret)
    ret.return_value = 1533374055.904203
    return ret


def test_repr() -> None:
    obj = ProgressPrint()
    repr(obj)


def test_report(capsys: pytest.CaptureFixture) -> None:
    obj = ProgressPrint()
    i = uuid.uuid4()
    report = Report(taskid=i, name='task1', done=0, total=10, first=True, last=False)
    obj.present(report)
    captured = capsys.readouterr()
    stdout_lines = captured.out.strip().split('\n')
    assert 1 == len(stdout_lines)
    assert ' :        0 /       10 (  0.00%): task1' in stdout_lines[0]
