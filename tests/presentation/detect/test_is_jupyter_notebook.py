import unittest.mock as mock
from collections.abc import Iterator

import pytest

from atpbar.presentation.detect.jupy import is_jupyter_notebook


@pytest.fixture()
def mock_widgets_module(monkeypatch: pytest.MonkeyPatch) -> Iterator[mock.Mock]:
    from atpbar.presentation.detect import jupy

    ret = mock.Mock()
    monkeypatch.setattr(jupy, 'widgets', ret)
    yield ret


@pytest.fixture()
def mock_display_module(monkeypatch: pytest.MonkeyPatch) -> Iterator[mock.Mock]:
    from atpbar.presentation.detect import jupy

    ret = mock.Mock()
    monkeypatch.setattr(jupy, 'display', ret)
    yield ret


@pytest.fixture()
def mock_get_ipython(monkeypatch: pytest.MonkeyPatch) -> Iterator[mock.Mock]:
    from atpbar.presentation.detect import jupy

    mock_ipython = mock.Mock()
    mock_ipython.config = {
        'IPKernelApp': {
            'connection_file': '/some/path/kernel.json',
        },
    }
    ret = mock.Mock()
    ret.return_value = mock_ipython
    monkeypatch.setattr(jupy, 'get_ipython', ret)
    yield ret


@pytest.fixture()
def mock_is_spyder_ide(monkeypatch: pytest.MonkeyPatch) -> Iterator[mock.Mock]:
    from atpbar.presentation.detect import jupy

    ret = mock.Mock()
    monkeypatch.setattr(jupy, 'is_spyder_ide', ret)
    yield ret


@pytest.fixture()
def mock_jupyter_notebook(
    mock_widgets_module: mock.Mock,
    mock_display_module: mock.Mock,
    mock_get_ipython: mock.Mock,
    mock_is_spyder_ide: mock.Mock,
) -> Iterator[None]:
    mock_is_spyder_ide.return_value = False
    yield


def test_is_jupyter_notebook_true(mock_jupyter_notebook: None) -> None:
    assert is_jupyter_notebook()


def test_is_jupyter_notebook_false(
    mock_jupyter_notebook: None, mock_is_spyder_ide: mock.Mock
) -> None:
    mock_is_spyder_ide.return_value = True
    assert not is_jupyter_notebook()
