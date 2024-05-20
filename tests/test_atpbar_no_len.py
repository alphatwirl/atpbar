import logging
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


def test_mock_fetch_reporter(
    mock_fetch_reporter: mock.Mock, mock_reporter: mock.Mock
) -> None:
    with mock_fetch_reporter() as reporter:
        assert reporter is mock_reporter


class Iter(Generic[T]):
    def __init__(self, content: Sequence[T]) -> None:
        self.content = content

    def __iter__(self) -> Iterator[T]:
        for e in self.content:
            yield e


content = [mock.sentinel.item1, mock.sentinel.item2, mock.sentinel.item3]


def test_atpbar_no_len(
    mock_reporter: mock.Mock, caplog: pytest.LogCaptureFixture
) -> None:
    iterable = Iter(content)

    ##
    returned = []
    with caplog.at_level(logging.WARNING):
        for e in atpbar.atpbar(iterable):
            returned.append(e)

    ##
    assert content == returned

    ##
    assert not mock_reporter.report.call_args_list

    ##
    assert 2 == len(caplog.records)
    assert "WARNING" == caplog.records[0].levelname
    assert "length is unknown" in caplog.records[0].msg
