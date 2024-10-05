import time
import unittest.mock as mock
import uuid

import pytest

from atpbar.presentation.base import Presentation
from atpbar.progress_report import Report


class MockProgressBar(Presentation):
    def _present(self, report: Report) -> None:
        pass


@pytest.fixture()
def mock_time(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
    from atpbar.presentation import base

    m = mock.Mock(wraps=time)
    m.time.return_value = 1533374055.904203
    monkeypatch.setattr(base, 'time', m)
    return m


@pytest.fixture()
def obj(mock_time: mock.Mock) -> MockProgressBar:
    return MockProgressBar()


def test_repr(obj: MockProgressBar) -> None:
    repr(obj)


def test_present(obj: Presentation) -> None:
    i = uuid.uuid4()
    j = uuid.uuid4()
    obj.present(dict(task_id=i, last=False))  # type: ignore
    assert obj.active()
    obj.present(dict(task_id=i, last=False))  # type: ignore
    assert obj.active()
    obj.present(dict(task_id=j, last=False))  # type: ignore
    assert obj.active()
    obj.present(dict(task_id=j, last=False))  # type: ignore
    assert obj.active()
    obj.present(dict(task_id=i, last=True))  # type: ignore
    assert obj.active()
    obj.present(dict(task_id=j, last=True))  # type: ignore
    assert not obj.active()


params = [
    ##
    pytest.param(dict(task_id=1, last=False), [], [], [], [], [1], [], [], [], True),
    pytest.param(dict(task_id=1, last=False), [1], [], [], [], [1], [], [], [], True),
    pytest.param(dict(task_id=1, last=False), [], [1], [], [], [], [1], [], [], True),
    pytest.param(dict(task_id=1, last=False), [], [], [1], [], [], [], [1], [], True),
    pytest.param(dict(task_id=1, last=False), [], [], [], [1], [], [], [], [1], False),
    ##
    pytest.param(dict(task_id=1, last=True), [], [], [], [], [], [], [1], [], True),
    pytest.param(dict(task_id=1, last=True), [1], [], [], [], [], [], [1], [], True),
    pytest.param(dict(task_id=1, last=True), [], [1], [], [], [], [], [1], [], True),
    pytest.param(dict(task_id=1, last=True), [], [], [1], [], [], [], [1], [], True),
    pytest.param(dict(task_id=1, last=True), [], [], [], [1], [], [], [], [1], False),
]
param_names = (
    'report, '
    'initial_new_task_ids, initial_active_task_ids, '
    'initial_finishing_task_ids, initial_complete_task_ids, '
    'expected_new_task_ids, expected_active_task_ids, '
    'expected_finishing_task_ids, expected_complete_task_ids, '
    'expected_return'
)


@pytest.mark.parametrize(param_names, params)
def test_register_report(  # type: ignore
    obj,
    report,
    initial_new_task_ids,
    initial_active_task_ids,
    initial_finishing_task_ids,
    initial_complete_task_ids,
    expected_new_task_ids,
    expected_active_task_ids,
    expected_finishing_task_ids,
    expected_complete_task_ids,
    expected_return,
):
    obj._new_task_ids[:] = initial_new_task_ids
    obj._active_task_ids[:] = initial_active_task_ids
    obj._finishing_task_ids[:] = initial_finishing_task_ids
    obj._complete_task_ids[:] = initial_complete_task_ids

    assert expected_return == obj._register_report(report)

    assert expected_new_task_ids == obj._new_task_ids
    assert expected_active_task_ids == obj._active_task_ids
    assert expected_finishing_task_ids == obj._finishing_task_ids
    assert expected_complete_task_ids == obj._complete_task_ids


params = [
    pytest.param(
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ),
    pytest.param(
        [],
        [10, 11, 12],
        [],
        [30, 31, 32],
        [],
        [10, 11, 12],
        [],
        [30, 31, 32],
    ),
    pytest.param(
        [1, 2],
        [10, 11, 12],
        [20, 21],
        [30, 31, 32],
        [],
        [10, 11, 12, 1, 2],
        [],
        [30, 31, 32, 20, 21],
    ),
]
param_names = (
    'initial_new_task_ids, initial_active_task_ids, '
    'initial_finishing_task_ids, initial_complete_task_ids, '
    'expected_new_task_ids, expected_active_task_ids, '
    'expected_finishing_task_ids, expected_complete_task_ids, '
)


@pytest.mark.parametrize(param_names, params)
def test_update_registry(  # type: ignore
    obj,
    initial_new_task_ids,
    initial_active_task_ids,
    initial_finishing_task_ids,
    initial_complete_task_ids,
    expected_new_task_ids,
    expected_active_task_ids,
    expected_finishing_task_ids,
    expected_complete_task_ids,
):
    obj._new_task_ids[:] = initial_new_task_ids
    obj._active_task_ids[:] = initial_active_task_ids
    obj._finishing_task_ids[:] = initial_finishing_task_ids
    obj._complete_task_ids[:] = initial_complete_task_ids

    obj._update_registry()

    assert expected_new_task_ids == obj._new_task_ids
    assert expected_active_task_ids == obj._active_task_ids
    assert expected_finishing_task_ids == obj._finishing_task_ids
    assert expected_complete_task_ids == obj._complete_task_ids


params = [
    pytest.param([], [], 4.0, 2.0, 1.0, True),
    pytest.param([1], [], 4.0, 2.0, 1.0, True),
    pytest.param([], [1], 4.0, 2.0, 1.0, True),
    pytest.param([], [], 4.0, 2.0, 3.0, False),
]
param_names = (
    'new_task_ids, finishing_task_ids, ' 'current_time, last_time, interval, expected'
)


@pytest.mark.parametrize(param_names, params)
def test_need_to_present(  # type: ignore
    obj,
    mock_time,
    new_task_ids,
    finishing_task_ids,
    current_time,
    last_time,
    interval,
    expected,
):
    obj._new_task_ids[:] = new_task_ids
    obj._finishing_task_ids[:] = finishing_task_ids

    mock_time.time.return_value = current_time
    obj.last_time = last_time
    obj.interval = interval

    assert expected == obj._need_to_present()
