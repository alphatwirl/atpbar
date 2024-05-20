import sys
from collections.abc import Iterator
from unittest.mock import Mock, call

import pytest

from atpbar.stream import FD, Stream


@pytest.fixture()
def mock_queue() -> Mock:
    return Mock()


@pytest.fixture()
def obj(mock_queue: Mock) -> Iterator[Stream]:
    y = Stream(mock_queue, FD.STDOUT)
    yield y


def test_print(obj: Stream, mock_queue: Mock, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "stdout", obj)

    print("abc")
    assert [call(("abc\n", FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print("abc", 456)
    assert [call(("abc 456\n", FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print("abc", 456, flush=True)
    assert [call(("abc 456\n", FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print("abc", 456, end="")
    print()
    assert [call(("abc 456\n", FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print("abc", 456, end="zzz", flush=True)
    assert [call(("abc 456zzz", FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    print("abc", end="")
    print(end="", flush=True)
    assert [call(("abc", FD.STDOUT))] == mock_queue.put.call_args_list


def test_print_bytes(
    obj: Stream, mock_queue: Mock, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, "stdout", obj)

    print(b"abc")
    assert [call(("b'abc'\n", FD.STDOUT))] == mock_queue.put.call_args_list


def test_stdout(obj: Stream, mock_queue: Mock, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "stdout", obj)

    sys.stdout.write("abc")
    sys.stdout.flush()
    assert [call(("abc", FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()

    sys.stdout.write("abc")
    sys.stdout.flush()
    assert [call(("abc", FD.STDOUT))] == mock_queue.put.call_args_list

    mock_queue.reset_mock()
