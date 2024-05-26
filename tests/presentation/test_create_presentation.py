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
    from atpbar.presentation import create

    ret = request.param
    org_stdout = sys.stdout
    m = mock.Mock(wraps=sys)
    m.stdout.isatty.return_value = ret
    m.stdout.write.side_effect = lambda x: org_stdout.write(x)
    monkeypatch.setattr(create, 'sys', m)
    return ret


if has_jupyter_notebook:
    is_jupyter_notebook_parames = [True, False]
else:
    is_jupyter_notebook_parames = [False]


@pytest.fixture(params=is_jupyter_notebook_parames)
def is_jupyter_notebook(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> bool:
    from atpbar.presentation import create

    ret = request.param
    m = mock.Mock(wraps=create.is_jupyter_notebook)
    m.return_value = ret
    monkeypatch.setattr(create, 'is_jupyter_notebook', m)
    return ret


@pytest.fixture(params=[True, False])
def del_ProgressBarJupyter(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> bool:
    from atpbar.presentation import create

    ret = request.param
    if ret:
        monkeypatch.delattr(create, 'ProgressBarJupyter', raising=False)
    else:
        m = mock.Mock()
        m().__class__.__name__ = 'ProgressBarJupyter'
        monkeypatch.setattr(create, 'ProgressBarJupyter', m, raising=False)
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
