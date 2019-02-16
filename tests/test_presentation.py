# Tai Sakuma <tai.sakuma@gmail.com>
import time
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressReport
from alphatwirl.progressbar.presentation import Presentation

##__________________________________________________________________||
class MockProgressBar(Presentation):
    def _present(self):
        pass

##__________________________________________________________________||
@pytest.fixture()
def mock_time(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(time, 'time', ret)
    ret.return_value = 1533374055.904203
    return ret

@pytest.fixture()
def obj(mock_time):
    return MockProgressBar()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
def test_present(obj):
    obj.present(ProgressReport('task1', 0, 10, 1))
    assert obj.active()
    obj.present(ProgressReport('task1', 2, 10, 1))
    assert obj.active()
    obj.present(ProgressReport('task1', 0, 10, 2))
    assert obj.active()
    obj.present(ProgressReport('task1', 2, 10, 2))
    assert obj.active()
    obj.present(ProgressReport('task1', 10, 10, 1))
    assert obj.active()
    obj.present(ProgressReport('task1', 10, 10, 2))
    assert not obj.active()

##__________________________________________________________________||
params = [

    ##
    pytest.param(
        ProgressReport('task1', 0, 10, 1),
        [ ], [ ], [ ], [ ],
        [1], [ ], [ ], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 0, 10, 1),
        [1], [ ], [ ], [ ],
        [1], [ ], [ ], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 0, 10, 1),
        [ ], [1], [ ], [ ],
        [ ], [1], [ ], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 0, 10, 1),
        [ ], [ ], [1], [ ],
        [ ], [ ], [1], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 0, 10, 1),
        [ ], [ ], [ ], [1],
        [ ], [ ], [ ], [1],
        False
    ),

    ##
    pytest.param(
        ProgressReport('task1', 2, 10, 1),
        [ ], [ ], [ ], [ ],
        [1], [ ], [ ], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 2, 10, 1),
        [1], [ ], [ ], [ ],
        [1], [ ], [ ], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 2, 10, 1),
        [ ], [1], [ ], [ ],
        [ ], [1], [ ], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 2, 10, 1),
        [ ], [ ], [1], [ ],
        [ ], [ ], [1], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 2, 10, 1),
        [ ], [ ], [ ], [1],
        [ ], [ ], [ ], [1],
        False
    ),

    ##
    pytest.param(
        ProgressReport('task1', 10, 10, 1),
        [ ], [ ], [ ], [ ],
        [ ], [ ], [1], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 10, 10, 1),
        [1], [ ], [ ], [ ],
        [ ], [ ], [1], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 10, 10, 1),
        [ ], [1], [ ], [ ],
        [ ], [ ], [1], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 10, 10, 1),
        [ ], [ ], [1], [ ],
        [ ], [ ], [1], [ ],
        True
    ),
    pytest.param(
        ProgressReport('task1', 10, 10, 1),
        [ ], [ ], [ ], [1],
        [ ], [ ], [ ], [1],
        False
    ),
]
param_names = (
    'report, '
    'initial_new_taskids, initial_active_taskids, '
    'initial_finishing_taskids, initial_complete_taskids, '
    'expected_new_taskids, expected_active_taskids, '
    'expected_finishing_taskids, expected_complete_taskids, '
    'expected_return'
)

@pytest.mark.parametrize(param_names, params)
def test_register_report(
        obj, report,
        initial_new_taskids, initial_active_taskids,
        initial_finishing_taskids, initial_complete_taskids,
        expected_new_taskids, expected_active_taskids,
        expected_finishing_taskids, expected_complete_taskids,
        expected_return):

    obj._new_taskids[:] = initial_new_taskids
    obj._active_taskids[:] = initial_active_taskids
    obj._finishing_taskids[:] = initial_finishing_taskids
    obj._complete_taskids[:] = initial_complete_taskids

    assert expected_return == obj._register_report(report)

    assert expected_new_taskids == obj._new_taskids
    assert expected_active_taskids == obj._active_taskids
    assert expected_finishing_taskids == obj._finishing_taskids
    assert expected_complete_taskids == obj._complete_taskids

##__________________________________________________________________||
params = [
    pytest.param(
        [ ], [ ], [ ], [ ],
        [ ], [ ], [ ], [ ],
    ),
    pytest.param(
        [ ], [10, 11, 12], [ ], [30, 31, 32],
        [ ], [10, 11, 12], [ ], [30, 31, 32],
    ),
    pytest.param(
        [1, 2], [10, 11, 12], [20, 21], [30, 31, 32],
        [ ], [10, 11, 12, 1, 2], [ ], [30, 31, 32, 20, 21],
    ),
]
param_names = (
    'initial_new_taskids, initial_active_taskids, '
    'initial_finishing_taskids, initial_complete_taskids, '
    'expected_new_taskids, expected_active_taskids, '
    'expected_finishing_taskids, expected_complete_taskids, '
)

@pytest.mark.parametrize(param_names, params)
def test_update_registry(
        obj,
        initial_new_taskids, initial_active_taskids,
        initial_finishing_taskids, initial_complete_taskids,
        expected_new_taskids, expected_active_taskids,
        expected_finishing_taskids, expected_complete_taskids):

    obj._new_taskids[:] = initial_new_taskids
    obj._active_taskids[:] = initial_active_taskids
    obj._finishing_taskids[:] = initial_finishing_taskids
    obj._complete_taskids[:] = initial_complete_taskids

    obj._update_registry()

    assert expected_new_taskids == obj._new_taskids
    assert expected_active_taskids == obj._active_taskids
    assert expected_finishing_taskids == obj._finishing_taskids
    assert expected_complete_taskids == obj._complete_taskids

##__________________________________________________________________||
params = [
    pytest.param([ ], [ ], 4.0, 2.0, 1.0, True),
    pytest.param([1], [ ], 4.0, 2.0, 1.0, True),
    pytest.param([ ], [1], 4.0, 2.0, 1.0, True),
    pytest.param([ ], [ ], 4.0, 2.0, 3.0, False),
]
param_names = (
    'new_taskids, finishing_taskids, '
    'current_time, last_time, interval, expected'
)

@pytest.mark.parametrize(param_names, params)
def test_need_to_present(
        obj, mock_time, new_taskids, finishing_taskids,
        current_time, last_time, interval, expected):

    obj._new_taskids[:] = new_taskids
    obj._finishing_taskids[:] = finishing_taskids

    mock_time.return_value = current_time
    obj.last_time = last_time
    obj.interval = interval

    assert expected == obj._need_to_present()

##__________________________________________________________________||
