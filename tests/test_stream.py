# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import time

import pytest
from unittest.mock import Mock, call

from atpbar.stream import Stream, FD

##__________________________________________________________________||
@pytest.fixture()
def mock_queue():
    return Mock()

@pytest.fixture()
def obj(mock_queue):
    y = Stream(mock_queue, FD.STDOUT)
    yield y

##__________________________________________________________________||
def test_print(obj, mock_queue, monkeypatch):
    monkeypatch.setattr(sys, 'stdout', obj)

    print('abc')
    assert [call(('abc\n', FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', 456)
    assert [call(('abc 456\n', FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', 456, flush=True)
    assert [call(('abc 456\n', FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', 456, end='')
    print()
    assert [call(('abc 456\n', FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', 456, end='zzz', flush=True)
    assert [call(('abc 456zzz', FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print('abc', end='')
    print(end='', flush=True)
    assert [call(('abc', FD.STDOUT))] == mock_queue.put.call_args_list

##__________________________________________________________________||
def test_print_bytes(obj, mock_queue, monkeypatch):
    monkeypatch.setattr(sys, 'stdout', obj)

    print(b'abc')
    assert [call(("b'abc'\n", FD.STDOUT))] == mock_queue.put.call_args_list

##__________________________________________________________________||
def test_stdout(obj, mock_queue, monkeypatch):
    monkeypatch.setattr(sys, 'stdout', obj)

    sys.stdout.write('abc')
    sys.stdout.flush()
    assert [call(('abc', FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    sys.stdout.write(456)
    assert [call((456, FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    sys.stdout.write('abc')
    sys.stdout.write(456)
    assert [call(('abc', FD.STDOUT)), call((456, FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

##__________________________________________________________________||
