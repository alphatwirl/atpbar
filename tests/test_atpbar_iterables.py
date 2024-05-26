import unittest.mock as mock
from collections.abc import Iterator, Sequence
from typing import Any, Generic, TypeVar

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
    monkeypatch.setattr(atpbar.main, 'fetch_reporter', ret)
    return ret


def test_mock_fetch_reporter(
    mock_fetch_reporter: mock.Mock, mock_reporter: mock.Mock
) -> None:
    with mock_fetch_reporter() as reporter:
        assert reporter is mock_reporter


class Iter(Generic[T]):
    def __init__(self, content: Sequence[T]) -> None:
        self.content = content

    def __len__(self) -> int:
        return len(self.content)

    def __iter__(self) -> Iterator[T]:
        for e in self.content:
            yield e


class GetItem(Generic[T]):
    def __init__(self, content: Sequence[T]) -> None:
        self.content = content

    def __len__(self) -> int:
        return len(self.content)

    def __getitem__(self, i: int) -> T:
        return self.content[i]


iterable_classes = list[type[Any]]([list, Iter, GetItem])

empty = list[Any]()
one = [mock.sentinel.item1]
three = [mock.sentinel.item1, mock.sentinel.item2, mock.sentinel.item3]
contents = [empty, one, three]
contents_ids = ['empty', 'one', 'three']


@pytest.mark.parametrize('content', contents, ids=contents_ids)
@pytest.mark.parametrize('iterable_class', iterable_classes)
def test_iterable(iterable_class: type[Any], content: list[Any]) -> None:
    iterable = iterable_class(content)
    assert content == [e for e in iterable]


@pytest.mark.parametrize('content', contents, ids=contents_ids)
@pytest.mark.parametrize('iterable_class', iterable_classes)
def test_atpbar_iterables(
    mock_reporter: mock.Mock, iterable_class: type[Any], content: list[Any]
) -> None:
    iterable = iterable_class(content)

    ##
    returned = []
    for e in atpbar.atpbar(iterable):
        returned.append(e)

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)

    # first report
    args, _ = mock_reporter.report.call_args_list[0]
    report = args[0]
    assert 0 == report['done']
    assert len(content) == report['total']

    #
    if content:
        for i, c in enumerate(mock_reporter.report.call_args_list[1:]):
            args, kwargs = c
            report = args[0]
            assert i + 1 == report['done']


@pytest.mark.parametrize('content', contents, ids=contents_ids)
@pytest.mark.parametrize('iterable_class', iterable_classes)
def test_atpbar_enumerate(
    mock_reporter: mock.Mock, iterable_class: type[Any], content: list[Any]
) -> None:
    iterable = iterable_class(content)

    ##
    returned = []
    for i, e in enumerate(atpbar.atpbar(iterable)):
        returned.append(e)

    ##
    assert content == returned

    ##
    assert len(content) + 1 == len(mock_reporter.report.call_args_list)

    # first report
    args, _ = mock_reporter.report.call_args_list[0]
    report = args[0]
    assert 0 == report['done']
    assert len(content) == report['total']
    #
    if content:
        for i, c in enumerate(mock_reporter.report.call_args_list[1:]):
            args, kwargs = c
            report = args[0]
            assert i + 1 == report['done']
