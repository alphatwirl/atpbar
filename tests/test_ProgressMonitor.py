# Tai Sakuma <tai.sakuma@gmail.com>
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import Queue, ProgressMonitor
from alphatwirl import progressbar

##__________________________________________________________________||
@pytest.fixture()
def presentation():
    return mock.MagicMock()

@pytest.fixture()
def queue(presentation):
    return Queue(presentation)

@pytest.fixture()
def report():
    return mock.MagicMock()

##__________________________________________________________________||
def test_queue_put(queue, presentation, report):
    queue.put(report)
    presentation.present.assert_called_once_with(report)

##__________________________________________________________________||
@pytest.fixture()
def mock_queue():
    return mock.MagicMock()

@pytest.fixture()
def MockQueue(monkeypatch, mock_queue):
    module = sys.modules['alphatwirl.progressbar.ProgressMonitor']
    ret = mock.MagicMock()
    monkeypatch.setattr(module, 'Queue', ret)
    ret.return_value = mock_queue
    return ret

@pytest.fixture()
def mock_reporter():
    return mock.MagicMock()

@pytest.fixture()
def MockReporter(monkeypatch, mock_reporter):
    module = sys.modules['alphatwirl.progressbar.ProgressMonitor']
    ret = mock.MagicMock()
    monkeypatch.setattr(module, 'ProgressReporter', ret)
    ret.return_value = mock_reporter
    return ret

@pytest.fixture()
def monitor(presentation, MockReporter, MockQueue):
    return ProgressMonitor(presentation)

##__________________________________________________________________||
def test_init(monitor, mock_queue, MockQueue, presentation):
    assert [mock.call(presentation = presentation)] == MockQueue.call_args_list
    assert monitor.queue is mock_queue

def test_begin_end(monitor, MockReporter):
    monitor.begin()
    assert progressbar._progress_reporter is MockReporter()
    monitor.end()
    assert progressbar._progress_reporter is None

def test_create_reporter(monitor, mock_reporter, MockReporter, presentation):
    reporter = monitor.create_reporter()
    assert [mock.call(queue = monitor.queue)] == MockReporter.call_args_list
    assert reporter is mock_reporter

##__________________________________________________________________||
