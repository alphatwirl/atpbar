import uuid

import pytest

from atpbar.presentation.bartty import ProgressBar
from atpbar.presentation.base import Presentation
from atpbar.presentation.txtprint import ProgressPrint

has_jupyter_notebook = False
try:
    import ipywidgets as widgets
    from IPython.display import display

    has_jupyter_notebook = True
except ImportError:
    pass

if has_jupyter_notebook:
    from atpbar.presentation.barjupyter import ProgressBarJupyter


classes = [ProgressBar, ProgressPrint]

if has_jupyter_notebook:
    classes.append(ProgressBarJupyter)

class_ids = [c.__name__ for c in classes]


@pytest.mark.parametrize('Class', classes, ids=class_ids)
def test_presentation(Class: type[Presentation]) -> None:
    i = uuid.uuid4()
    j = uuid.uuid4()
    obj = Class()
    repr(obj)
    obj.active()
    obj.present(dict(name='task1', done=0, total=10, task_id=i, first=True, last=False))
    obj.present(
        dict(name='task1', done=2, total=10, task_id=i, first=False, last=False)
    )
    obj.active()
    obj.present(dict(name='task1', done=0, total=5, task_id=j, first=True, last=False))
    obj.present(dict(name='task1', done=3, total=5, task_id=j, first=False, last=False))
    obj.active()
    obj.present(
        dict(name='task1', done=10, total=10, task_id=i, first=False, last=True)
    )
    obj.active()
    obj.present(dict(name='task1', done=5, total=5, task_id=j, first=False, last=True))
    obj.active()
    obj.active()
    obj.present(
        dict(name='task1', done=10, total=10, task_id=i, first=False, last=True)
    )
    obj.active()


@pytest.mark.parametrize('Class', classes, ids=class_ids)
def test_time_track(Class: type[Presentation]) -> None:
    i = uuid.uuid4()
    obj = Class()
    repr(obj)
    obj.active()
    obj.present(
        dict(
            name='task1',
            done=0,
            total=10,
            task_id=i,
            first=True,
            last=False,
        )
    )
    obj.present(
        dict(
            name='task1',
            done=2,
            total=10,
            task_id=i,
            first=False,
            last=False,
        )
    )
    obj.present(
        dict(
            name='task1',
            done=10,
            total=10,
            task_id=i,
            first=False,
            last=True,
        )
    )
    obj.active()
