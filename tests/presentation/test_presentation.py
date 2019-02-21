# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

has_jupyter_notebook = False
try:
    import ipywidgets as widgets
    from IPython.display import display
    has_jupyter_notebook = True
except ImportError:
    pass

from atpbar.report import ProgressReport
from atpbar.presentation.bartty import ProgressBar
from atpbar.presentation.txtprint import ProgressPrint

if has_jupyter_notebook:
    from atpbar.presentation.barjupyter import ProgressBarJupyter

##__________________________________________________________________||
classes = [ProgressBar, ProgressPrint]

if has_jupyter_notebook:
    classes.append(ProgressBarJupyter)

classe_ids = [c.__name__ for c in classes]

@pytest.mark.parametrize('Class', classes, ids=classe_ids)
def test_presentation(Class):
    obj = Class()
    repr(obj)
    obj.active()
    obj.present(ProgressReport('task1', 0, 10, 1, 2342, True))
    obj.present(ProgressReport('task1', 2, 10, 1, 2342, True))
    obj.active()
    obj.present(ProgressReport('task1', 0, 5, 2, 2342, True))
    obj.present(ProgressReport('task1', 3, 5, 2, 2342, True))
    obj.active()
    obj.present(ProgressReport('task1', 10, 10, 1, 2342, True))
    obj.active()
    obj.present(ProgressReport('task1', 5, 5, 2, 2342, True))
    obj.active()
    obj.active()
    obj.present(ProgressReport('task1', 10, 10, 1, 2342, True))
    obj.active()

##__________________________________________________________________||
