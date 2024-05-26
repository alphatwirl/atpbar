import os
import unittest.mock as mock
from collections.abc import Iterator

import pytest

from atpbar.presentation.detect.spy import is_spyder_ide


@pytest.fixture()
def mock_spyder_module(monkeypatch: pytest.MonkeyPatch) -> Iterator[mock.Mock]:
    from atpbar.presentation.detect import spy

    ret = mock.Mock()
    monkeypatch.setattr(spy, 'spyder', ret)
    yield ret


@pytest.fixture()
def mock_get_ipython(monkeypatch: pytest.MonkeyPatch) -> Iterator[mock.Mock]:
    from atpbar.presentation.detect import spy

    mock_ipython = mock.Mock()
    mock_ipython.config = {
        'IPKernelApp': {
            'connection_file': '/some/path/kernel.json',
        },
    }
    ret = mock.Mock()
    ret.return_value = mock_ipython

    monkeypatch.setattr(spy, 'get_ipython', ret)
    yield ret


@pytest.fixture()
def mock_spyder_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    spyder_envs = [
        ('SPYDER_ARGS', '[]'),
        ('SPY_EXTERNAL_INTERPRETER', 'False'),
        ('SPY_UMR_ENABLED', 'True'),
        ('SPY_UMR_VERBOSE', 'True'),
        ('SPY_UMR_NAMELIST', ''),
        ('SPY_RUN_LINES_O', ''),
        ('SPY_PYLAB_O', 'True'),
        ('SPY_BACKEND_O', '0'),
        ('SPY_AUTOLOAD_PYLAB_O', 'False'),
        ('SPY_FORMAT_O', '0'),
        ('SPY_BBOX_INCHES_O', 'True'),
        ('SPY_RESOLUTION_O', '72'),
        ('SPY_WIDTH_O', '6'),
        ('SPY_HEIGHT_O', '4'),
        ('SPY_USE_FILE_O', 'False'),
        ('SPY_RUN_FILE_O', ''),
        ('SPY_AUTOCALL_O', '0'),
        ('SPY_GREEDY_O', 'False'),
        ('SPY_JEDI_O', 'False'),
        ('SPY_SYMPY_O', 'False'),
        ('SPY_TESTING', 'None'),
        ('SPY_HIDE_CMD', 'True'),
    ]
    for e, v in spyder_envs:
        monkeypatch.setenv(e, v)


@pytest.fixture()
def mock_spyder_ide(
    mock_spyder_module: mock.Mock,
    mock_get_ipython: mock.Mock,
    mock_spyder_env_vars: None,
) -> Iterator[None]:
    yield


def test_is_spyder_ide_true(mock_spyder_ide: None) -> None:
    assert is_spyder_ide()


@pytest.fixture()
def mock_del_spyder_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv('SPYDER_ARGS', raising=False)

    envs_to_delete = [e for e in os.environ.keys() if e.startswith('SPY_')]
    for e in envs_to_delete:
        monkeypatch.delenv(e, raising=False)


def test_is_spyder_ide_false(mock_del_spyder_env_vars: None) -> None:
    assert not is_spyder_ide()
