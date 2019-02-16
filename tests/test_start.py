# Tai Sakuma <tai.sakuma@gmail.com>
import itertools

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import _start_monitor_if_necessary
import alphatwirl

##__________________________________________________________________||
@pytest.fixture()
def mock_atexit(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(alphatwirl.progressbar, 'atexit', ret)
    return ret

@pytest.fixture()
def mock_presentation(monkeypatch):
    ret = mock.Mock()
    return ret

@pytest.fixture(autouse=True)
def mock_create_presentation(monkeypatch, mock_presentation):
    ret = mock.Mock()
    ret.return_value = mock_presentation
    monkeypatch.setattr(alphatwirl.progressbar, '_create_presentation', ret)
    return ret

@pytest.fixture()
def MockBProgressMonitor(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(alphatwirl.progressbar, 'BProgressMonitor', ret)
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

    monkeypatch.setattr(alphatwirl.progressbar, '_reporter', mock_reporter)
    monkeypatch.setattr(alphatwirl.progressbar, '_monitor', mock_monitor)
    monkeypatch.setattr(alphatwirl.progressbar, 'do_not_start_monitor', do_not_start_monitor)

def test_start_monitor_if_necessary(mock_atexit, MockBProgressMonitor, mock_presentation):

    org_reporter = alphatwirl.progressbar._reporter
    org_monitor = alphatwirl.progressbar._monitor
    org_do_not_start_monitor = alphatwirl.progressbar.do_not_start_monitor

    _start_monitor_if_necessary()

    assert org_do_not_start_monitor == alphatwirl.progressbar.do_not_start_monitor

    if org_do_not_start_monitor:
        assert alphatwirl.progressbar._reporter is org_reporter
        assert alphatwirl.progressbar._monitor is org_monitor
        assert not mock_atexit.register.call_args_list
        return

    if org_reporter:
        assert alphatwirl.progressbar._reporter is org_reporter
        assert alphatwirl.progressbar._monitor is org_monitor
        assert not mock_atexit.register.call_args_list
        return

    if org_monitor:
        assert [mock.call()] == org_monitor.end.call_args_list

    assert [mock.call(presentation=mock_presentation)] == MockBProgressMonitor.call_args_list
    assert [mock.call()] == MockBProgressMonitor().begin.call_args_list

    assert alphatwirl.progressbar._monitor is MockBProgressMonitor()
    assert alphatwirl.progressbar._reporter is MockBProgressMonitor().create_reporter()

    assert 1 == (len(mock_atexit.register.call_args_list))

##__________________________________________________________________||
