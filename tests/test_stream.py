# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import time

import pytest
from unittest.mock import Mock, call

from atpbar.stream import Stream

##__________________________________________________________________||
@pytest.fixture()
def mock_queue():
    return Mock()

@pytest.fixture()
def obj(mock_queue):
    y = Stream(mock_queue)
    yield y

##__________________________________________________________________||
def test_print(obj, mock_queue, monkeypatch):
    monkeypatch.setattr(sys, 'stdout', obj)

    print('abc')
    assert [call('abc\n')] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', 456)
    assert [call('abc 456\n')] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', 456, flush=True)
    assert [call('abc 456\n')] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', 456, end='')
    print()
    assert [call('abc 456\n')] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', 456, end='zzz', flush=True)
    assert [call('abc 456zzz')] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', end='')
    print(end='', flush=True)
    assert [call('abc')] == mock_queue.put.call_args_list

##__________________________________________________________________||
def test_print_bytes(obj, mock_queue, monkeypatch):
    monkeypatch.setattr(sys, 'stdout', obj)

    print(b'abc')
    assert [call("b'abc'\n")] == mock_queue.put.call_args_list

##__________________________________________________________________||
def test_stdout(obj, mock_queue, monkeypatch):
    monkeypatch.setattr(sys, 'stdout', obj)

    sys.stdout.write('abc')
    sys.stdout.flush()
    assert [call('abc')] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    sys.stdout.write(456)
    assert [call(456)] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    sys.stdout.write('abc')
    sys.stdout.write(456)
    assert [call('abc'), call(456)] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

##__________________________________________________________________||
