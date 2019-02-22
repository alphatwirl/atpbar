# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

has_jupyter_notebook = False
try:
    import ipywidgets as widgets
    from IPython.display import display
    has_jupyter_notebook = True
except ImportError:
    pass

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
    obj.present(dict(name='task1', done=0, total=10, taskid=1, first=True, last=False))
    obj.present(dict(name='task1', done=2, total=10, taskid=1, first=False, last=False))
    obj.active()
    obj.present(dict(name='task1', done=0, total=5, taskid=2, first=True, last=False))
    obj.present(dict(name='task1', done=3, total=5, taskid=2, first=False, last=False))
    obj.active()
    obj.present(dict(name='task1', done=10, total=10, taskid=1, first=False, last=True))
    obj.active()
    obj.present(dict(name='task1', done=5, total=5, taskid=2, first=False, last=True))
    obj.active()
    obj.active()
    obj.present(dict(name='task1', done=10, total=10, taskid=1, first=False, last=True))
    obj.active()

##__________________________________________________________________||
