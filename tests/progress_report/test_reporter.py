import time
import unittest.mock as mock
import uuid
from typing import Any

import pytest

from atpbar.progress_report import ProgressReporter, Report


@pytest.fixture()
def mock_queue() -> mock.Mock:
    return mock.Mock()


@pytest.fixture()
def mock_time(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
    from atpbar.progress_report import reporter

    m = mock.Mock(wraps=time)
    monkeypatch.setattr(reporter, 'time', m)
    return m


@pytest.fixture()
def obj(mock_queue: mock.Mock, mock_time: mock.Mock) -> ProgressReporter:
    ret = ProgressReporter()
    ret.queue = mock_queue
    return ret


def test_repr(obj: ProgressReporter) -> None:
    repr(obj)


class TestReport:
    def test_report_need_to_report(
        self,
        obj: ProgressReporter,
        monkeypatch: pytest.MonkeyPatch,
        mock_queue: mock.Mock,
        mock_time: mock.Mock,
    ) -> None:
        current_time = 15324.345
        task_id = uuid.uuid4()
        mock_time.time.return_value = current_time
        monkeypatch.setattr(obj, '_need_to_report', mock.Mock(return_value=True))
        report = Report(
            task_id=task_id,
            name='',
            done=0,
            total=10,
            first=True,
            last=False,
        )
        obj.report(report)
        assert [mock.call(report)] == mock_queue.put.call_args_list
        assert {task_id: current_time} == obj.last_time

    def test_report_no_need_to_report(
        self,
        obj: ProgressReporter,
        monkeypatch: pytest.MonkeyPatch,
        mock_queue: mock.Mock,
        mock_time: mock.Mock,
    ) -> None:
        current_time = 15324.345
        task_id = uuid.uuid4()
        mock_time.time.return_value = current_time
        monkeypatch.setattr(obj, '_need_to_report', mock.Mock(return_value=False))
        report = Report(
            task_id=task_id,
            name='',
            done=0,
            total=10,
            first=True,
            last=False,
        )
        obj.report(report)
        assert [] == mock_queue.put.call_args_list
        assert {} == obj.last_time


task_id = uuid.uuid4()

params = [
    pytest.param(
        Report(
            task_id=task_id,
            name='',
            done=0,
            total=10,
            first=True,
            last=False,
        ),
        {},
        10.0,
        True,
    ),
    pytest.param(
        Report(
            task_id=task_id,
            name='',
            done=10,
            total=10,
            first=False,
            last=True,
        ),
        {},
        10.0,
        True,
    ),
    pytest.param(
        Report(
            task_id=task_id,
            name='',
            done=0,
            total=10,
            first=True,
            last=False,
        ),
        {task_id: 10.0},
        10.0,
        True,
    ),
    pytest.param(
        Report(
            task_id=task_id,
            name='',
            done=5,
            total=10,
            first=False,
            last=False,
        ),
        {task_id: 10.0},
        30.0,
        True,
    ),
    pytest.param(
        Report(
            task_id=task_id,
            name='',
            done=5,
            total=10,
            first=False,
            last=False,
        ),
        {task_id: 10.0},
        15.0,
        False,
    ),
]
param_names = 'report, last_time, current_time, expected'


@pytest.mark.parametrize(param_names, params)
def test_need_to_report(
    obj: ProgressReporter,
    mock_time: mock.Mock,
    report: Report,
    last_time: dict[uuid.UUID, float],
    current_time: Any,
    expected: bool,
) -> None:
    obj.interval = 10
    obj.last_time = last_time
    mock_time.time.return_value = current_time
    assert expected == obj._need_to_report(report)
