# Tai Sakuma <tai.sakuma@gmail.com>
import pytest
import time
import multiprocessing

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressReportPickup

##__________________________________________________________________||
@pytest.fixture()
def presentation():
    return mock.MagicMock()

##__________________________________________________________________||
@pytest.fixture()
def queue():
    return multiprocessing.Queue()

@pytest.fixture()
def pickup(queue, presentation):
    return ProgressReportPickup(queue, presentation)

##__________________________________________________________________||
def test_start_join(pickup, queue, presentation):
    presentation.active.return_value = True
    pickup.start()
    queue.put(None)
    pickup.join()

##__________________________________________________________________||
@pytest.fixture()
def mock_queue():
    return mock.MagicMock()

@pytest.fixture()
def pickup0(mock_queue, presentation):
    return ProgressReportPickup(mock_queue, presentation)

##__________________________________________________________________||
def test_run_until_the_end_order_arrives_no_report(pickup0, mock_queue, presentation):

    mock_queue.empty.side_effect = [False, True]
    mock_queue.get.side_effect = [None]
    pickup0._run_until_the_end_order_arrives()

    assert [] == presentation.mock_calls

def test_run_until_the_end_order_arrives_one_report(pickup0, mock_queue, presentation):

    report = mock.MagicMock()
    mock_queue.empty.side_effect = [False, False, True]
    mock_queue.get.side_effect = [report, None]
    pickup0._run_until_the_end_order_arrives()

    assert [mock.call.present(report)] == presentation.mock_calls

def test_run_until_the_end_order_arrives_one_report_once_empty(pickup0, mock_queue, presentation):

    report1 = mock.MagicMock()
    mock_queue.empty.side_effect = [False, True, False, True] # it becomes empty once
    mock_queue.get.side_effect = [report1, None]
    pickup0._run_until_the_end_order_arrives()

    assert [mock.call.present(report1)] == presentation.mock_calls

def test_run_until_the_end_order_arrives_two_reports(pickup0, mock_queue, presentation):

    report1 = mock.MagicMock()
    report2 = mock.MagicMock()
    mock_queue.empty.side_effect = [False, False, False, True]
    mock_queue.get.side_effect = [report1, None, report2] # report2 arrives
                                                          # after the end_order
    pickup0._run_until_the_end_order_arrives()

    assert [mock.call.present(report1), mock.call.present(report2)] == presentation.mock_calls

##__________________________________________________________________||
@pytest.fixture()
def mocktime(monkeypatch):
    ret = mock.MagicMock(return_value = 1000.0)
    monkeypatch.setattr(time, 'time', ret)
    return ret

def test_run_until_reports_stop_coming_no_report(pickup0, mock_queue, presentation, mocktime):
    presentation.active.side_effect = [False]
    pickup0._run_until_reports_stop_coming()
    assert [] == presentation.present.mock_calls

def test_run_until_reports_stop_coming_one_report(pickup0, mock_queue, presentation, mocktime):
    presentation.active.side_effect = [True, False]
    report = mock.MagicMock()
    mock_queue.empty.side_effect = [False, False, True]
    mock_queue.get.side_effect = [report, None]
    pickup0._run_until_reports_stop_coming()
    assert [mock.call(report)] == presentation.present.mock_calls

def test_run_until_reports_stop_coming_one_report_timeout(pickup0, mock_queue, presentation, mocktime):
    presentation.active.return_value = True
    report = mock.MagicMock()
    mock_queue.empty.return_value = True
    mock_queue.get.side_effect = [report, None]
    mocktime.side_effect = [1000.0, 1003.0]
    pickup0._run_until_reports_stop_coming()
    assert [ ] == presentation.present.mock_calls

##__________________________________________________________________||
