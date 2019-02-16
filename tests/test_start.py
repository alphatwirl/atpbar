# Tai Sakuma <tai.sakuma@gmail.com>
import itertools

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import atpbar
from atpbar.funcs import _start_monitor_if_necessary

##__________________________________________________________________||
@pytest.fixture()
def mock_atexit(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(atpbar.funcs, 'atexit', ret)
    return ret

@pytest.fixture()
def mock_lock(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(atpbar.funcs, '_lock', ret)
    return ret

@pytest.fixture()
def mock_presentation(monkeypatch):
    ret = mock.Mock()
    return ret

@pytest.fixture(autouse=True)
def mock_create_presentation(monkeypatch, mock_presentation):
    ret = mock.Mock()
    ret.return_value = mock_presentation
    monkeypatch.setattr(atpbar.funcs, '_create_presentation', ret)
    return ret

@pytest.fixture()
def MockProgressMonitor(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(atpbar.funcs, 'ProgressMonitor', ret)
    return ret

@pytest.fixture(
    autouse=True,
    params=itertools.product([True, False], [True, False], [True, False])
)
def global_variables(monkeypatch, request):
    was_reporter, was_monitor, do_not_start_monitor = request.param

    if was_reporter:
        mock_reporter = mock.Mock()
    else:
        mock_reporter = None

    if was_monitor:
        mock_monitor = mock.Mock()
    else:
        mock_monitor = None

    monkeypatch.setattr(atpbar.funcs, '_reporter', mock_reporter)
    monkeypatch.setattr(atpbar.funcs, '_monitor', mock_monitor)
    monkeypatch.setattr(atpbar.funcs, 'do_not_start_monitor', do_not_start_monitor)

def test_start_monitor_if_necessary(mock_atexit, mock_lock, MockProgressMonitor, mock_presentation):

    org_reporter = atpbar.funcs._reporter
    org_monitor = atpbar.funcs._monitor
    org_do_not_start_monitor = atpbar.funcs.do_not_start_monitor

    _start_monitor_if_necessary()

    assert [mock.call.acquire(), mock.call.release()] == mock_lock.method_calls

    assert org_do_not_start_monitor == atpbar.funcs.do_not_start_monitor

    if org_do_not_start_monitor:
        assert atpbar.funcs._reporter is org_reporter
        assert atpbar.funcs._monitor is org_monitor
        assert not mock_atexit.register.call_args_list
        return

    if org_reporter:
        assert atpbar.funcs._reporter is org_reporter
        assert atpbar.funcs._monitor is org_monitor
        assert not mock_atexit.register.call_args_list
        return

    if org_monitor:
        assert [mock.call()] == org_monitor.end.call_args_list

    assert [mock.call(presentation=mock_presentation)] == MockProgressMonitor.call_args_list
    assert [mock.call()] == MockProgressMonitor().begin.call_args_list

    assert atpbar.funcs._monitor is MockProgressMonitor()
    assert atpbar.funcs._reporter is MockProgressMonitor().create_reporter()

    assert 1 == (len(mock_atexit.register.call_args_list))

##__________________________________________________________________||
