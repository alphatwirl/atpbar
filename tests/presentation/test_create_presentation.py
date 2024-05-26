import sys
import unittest.mock as mock

import pytest

from atpbar.presentation.create import create_presentation

has_jupyter_notebook = False
try:
    import ipywidgets as widgets
    from IPython.display import display

    has_jupyter_notebook = True
except ImportError:
    pass


@pytest.fixture(params=[True, False])
def isatty(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> bool:
    ret = request.param
    org_stdout = sys.stdout
    f = mock.Mock(
        **{
            'stdout.isatty.return_value': ret,
            'stdout.write.side_effect': lambda x: org_stdout.write(x),
        }
    )
    module = sys.modules['atpbar.presentation.create']
    monkeypatch.setattr(module, 'sys', f)
    return ret


if has_jupyter_notebook:
    is_jupyter_notebook_parames = [True, False]
else:
    is_jupyter_notebook_parames = [False]


@pytest.fixture(params=is_jupyter_notebook_parames)
def is_jupyter_notebook(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> bool:
    ret = request.param
    f = mock.Mock()
    f.return_value = ret
    module = sys.modules['atpbar.presentation.create']
    monkeypatch.setattr(module, 'is_jupyter_notebook', f)
    return ret


@pytest.fixture(params=[True, False])
def del_ProgressBarJupyter(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> bool:
    ret = request.param
    module = sys.modules['atpbar.presentation.create']
    if ret:
        monkeypatch.delattr(module, 'ProgressBarJupyter', raising=False)
    else:
        m = mock.Mock()
        m().__class__.__name__ = 'ProgressBarJupyter'
        monkeypatch.setattr(module, 'ProgressBarJupyter', m, raising=False)
    return ret


def test_create_presentation(
    isatty: bool,
    is_jupyter_notebook: bool,
    del_ProgressBarJupyter: bool,
) -> None:
    actual = create_presentation()

    if isatty:
        assert 'ProgressBar' == actual.__class__.__name__
    elif is_jupyter_notebook:
        if del_ProgressBarJupyter:
            assert 'ProgressPrint' == actual.__class__.__name__
        else:
            assert 'ProgressBarJupyter' == actual.__class__.__name__
    else:
        assert 'ProgressPrint' == actual.__class__.__name__
