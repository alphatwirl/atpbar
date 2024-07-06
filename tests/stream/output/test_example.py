import sys
from unittest.mock import Mock, call

from pytest import MonkeyPatch, fixture

from atpbar.stream import FD, OutputStream


@fixture()
def mock_queue() -> Mock:
    return Mock()


@fixture()
def obj(mock_queue: Mock) -> OutputStream:
    return OutputStream(mock_queue, FD.STDOUT)


def test_print(mock_queue: Mock, obj: OutputStream, monkeypatch: MonkeyPatch) -> None:
    with monkeypatch.context() as m:
        m.setattr(sys, 'stdout', obj)

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
        assert [] == mock_queue.put.call_args_list
        print()
        assert [call(('abc 456\n', FD.STDOUT))] == mock_queue.put.call_args_list

        mock_queue.reset_mock()

        print('abc', 456, end='zzz', flush=True)
        assert [call(('abc 456zzz', FD.STDOUT))] == mock_queue.put.call_args_list

        mock_queue.reset_mock()

        print('abc', end='')
        assert [] == mock_queue.put.call_args_list
        print(end='', flush=True)
        assert [call(('abc', FD.STDOUT))] == mock_queue.put.call_args_list


def test_print_bytes(
    mock_queue: Mock, obj: OutputStream, monkeypatch: MonkeyPatch
) -> None:
    with monkeypatch.context() as m:
        m.setattr(sys, 'stdout', obj)

        print(b'abc')
        assert [call(("b'abc'\n", FD.STDOUT))] == mock_queue.put.call_args_list


def test_stdout(mock_queue: Mock, obj: OutputStream, monkeypatch: MonkeyPatch) -> None:
    with monkeypatch.context() as m:
        m.setattr(sys, 'stdout', obj)

        sys.stdout.write('abc')
        sys.stdout.flush()
        assert [call(('abc', FD.STDOUT))] == mock_queue.put.call_args_list

        mock_queue.reset_mock()

        sys.stdout.write('abc')
        sys.stdout.flush()
        assert [call(('abc', FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()
