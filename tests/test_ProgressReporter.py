# Tai Sakuma <tai.sakuma@gmail.com>
import pytest
import time

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressReport
from alphatwirl.progressbar import ProgressReporter

##__________________________________________________________________||
@pytest.fixture()
def mock_queue():
    return mock.Mock()

@pytest.fixture()
def mock_time(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(time, 'time', ret)
    return ret

@pytest.fixture()
def obj(mock_queue, mock_time):
    ret = ProgressReporter(mock_queue)
    return ret

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
def test_report_need_to_report(obj, monkeypatch, mock_queue, mock_time):
    current_time = 15324.345
    taskid = 234
    mock_time.return_value = current_time
    monkeypatch.setattr(obj, '_need_to_report', mock.Mock(return_value=True))
    report = ProgressReport('task1', 0, 10, taskid)
    obj.report(report)
    assert [mock.call(report)] == mock_queue.put.call_args_list
    assert {taskid: current_time} == obj.last_time

def test_report_no_need_to_report(obj, monkeypatch, mock_queue, mock_time):
    current_time = 15324.345
    taskid = 234
    mock_time.return_value = current_time
    monkeypatch.setattr(obj, '_need_to_report', mock.Mock(return_value=False))
    report = ProgressReport('task1', 0, 10, taskid)
    obj.report(report)
    assert [ ] == mock_queue.put.call_args_list
    assert { } == obj.last_time

##__________________________________________________________________||
params = [
    pytest.param(ProgressReport('task1', 0, 10, 1), {}, 10.0, True),
    pytest.param(ProgressReport('task1', 10, 10, 1), {}, 10.0, True),
    pytest.param(ProgressReport('task1', 0, 10, 1), {1: 10.0}, 10.0, True),
    pytest.param(ProgressReport('task1', 1, 10, 1), {1: 10.0}, 30.0, True),
    pytest.param(ProgressReport('task1', 1, 10, 1), {1: 10.0}, 15.0, False),
]
param_names = (
    'report, last_time, current_time, '
    'expected'
)

@pytest.mark.parametrize(param_names, params)
def test_need_to_report(
        obj, mock_time, report,
        last_time, current_time, expected):

    obj.interval = 10
    obj.last_time = last_time
    mock_time.return_value = current_time
    assert expected == obj._need_to_report(report)

##__________________________________________________________________||
