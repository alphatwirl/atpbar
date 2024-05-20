import unittest.mock as mock
from collections.abc import Iterator, Sequence
from typing import Generic, TypeVar

import pytest

import atpbar

T = TypeVar('T')


@pytest.fixture()
def mock_reporter(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
    ret = mock.Mock()
    return ret


@pytest.fixture(autouse=True)
def mock_fetch_reporter(
    monkeypatch: pytest.MonkeyPatch, mock_reporter: mock.Mock
) -> mock.Mock:
    ret = mock.Mock()
    ret.return_value.__enter__ = mock.Mock()
    ret.return_value.__enter__.return_value = mock_reporter
    ret.return_value.__exit__ = mock.Mock()
    monkeypatch.setattr(atpbar.main, "fetch_reporter", ret)
    return ret


@pytest.fixture(autouse=True)
def mock_fetch_reporter_raise(
    monkeypatch: pytest.MonkeyPatch, mock_reporter: mock.Mock
) -> mock.Mock:
    mock_reporter.report.side_effect = Exception
    ret = mock.Mock()
    ret.return_value.__enter__ = mock.Mock()
    ret.return_value.__enter__.return_value = mock_reporter
    ret.return_value.__exit__ = mock.Mock()
    monkeypatch.setattr(atpbar.main, "fetch_reporter", ret)
    return ret


class Iter(Generic[T]):
    def __init__(self, content: Sequence[T]) -> None:
        self.content = content

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __len__(self) -> int:
        return len(self.content)

    def __iter__(self) -> Iterator[T]:
        for e in self.content:
            yield e


content = [mock.sentinel.item1, mock.sentinel.item2, mock.sentinel.item3]


def test_atpbar_name_repr(
    mock_fetch_reporter: mock.Mock,
    mock_reporter: mock.Mock,
    caplog: pytest.LogCaptureFixture,
) -> None:

    iterable = Iter(content)
    returned = [e for e in atpbar.atpbar(iterable)]

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)

    # first report
    args, _ = mock_reporter.report.call_args_list[0]
    report = args[0]
    assert 0 == report["done"]
    assert len(content) == report["total"]
    assert "Iter" == report["name"]  # repr(iterable)


def test_atpbar_name_given(
    mock_fetch_reporter: mock.Mock,
    mock_reporter: mock.Mock,
    caplog: pytest.LogCaptureFixture,
) -> None:

    iterable = Iter(content)
    returned = [e for e in atpbar.atpbar(iterable, name="given")]

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)

    # first report
    args, _ = mock_reporter.report.call_args_list[0]
    report = args[0]
    assert 0 == report["done"]
    assert len(content) == report["total"]
    assert "given" == report["name"]


def test_atpbar_raise(
    mock_fetch_reporter_raise: mock.Mock,
    mock_reporter: mock.Mock,
    caplog: pytest.LogCaptureFixture,
) -> None:

    iterable = Iter(content)
    returned = [e for e in atpbar.atpbar(iterable, name="given")]

    ##
    assert content == returned
