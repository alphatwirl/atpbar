import sys

import pytest

import unittest.mock as mock

from atpbar.progress_report.reporter import ProgressReporter


@pytest.fixture()
def mock_queue():
    return mock.Mock()


@pytest.fixture()
def mock_time(monkeypatch):
    ret = mock.Mock()
    module = sys.modules["atpbar.progress_report.reporter"]
    monkeypatch.setattr(module, "time", ret)
    return ret


@pytest.fixture()
def obj(mock_queue, mock_time):
    ret = ProgressReporter(
        mock_queue, notices_from_sub_processes=mock.Mock(), stream_queue=mock.Mock()
    )
    return ret


def test_repr(obj):
    repr(obj)


class TestReport:

    def test_report_need_to_report(self, obj, monkeypatch, mock_queue, mock_time):
        current_time = 15324.345
        taskid = 234
        mock_time.time.return_value = current_time
        monkeypatch.setattr(obj, "_need_to_report", mock.Mock(return_value=True))
        report = dict(taskid=taskid, done=0, total=10)
        obj.report(report)
        assert [mock.call(report)] == mock_queue.put.call_args_list
        assert {taskid: current_time} == obj.last_time

    def test_report_no_need_to_report(self, obj, monkeypatch, mock_queue, mock_time):
        current_time = 15324.345
        taskid = 234
        mock_time.time.return_value = current_time
        monkeypatch.setattr(obj, "_need_to_report", mock.Mock(return_value=False))
        report = dict(taskid=taskid, done=0, total=10)
        obj.report(report)
        assert [] == mock_queue.put.call_args_list
        assert {} == obj.last_time


params = [
    pytest.param(dict(taskid=1, first=True, last=False), {}, 10.0, True),
    pytest.param(dict(taskid=1, first=False, last=True), {}, 10.0, True),
    pytest.param(dict(taskid=1, first=True, last=False), {1: 10.0}, 10.0, True),
    pytest.param(dict(taskid=1, first=False, last=False), {1: 10.0}, 30.0, True),
    pytest.param(dict(taskid=1, first=False, last=False), {1: 10.0}, 15.0, False),
]
param_names = "report, last_time, current_time, " "expected"


@pytest.mark.parametrize(param_names, params)
def test_need_to_report(obj, mock_time, report, last_time, current_time, expected):

    obj.interval = 10
    obj.last_time = last_time
    mock_time.time.return_value = current_time
    assert expected == obj._need_to_report(report)
