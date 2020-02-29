# Tai Sakuma <tai.sakuma@gmail.com>
import sys

from .detect.jupy import is_jupyter_notebook

from .bartty import ProgressBar
from .txtprint import ProgressPrint

try:
    from .barjupyter import ProgressBarJupyter
except ImportError:
    pass

##__________________________________________________________________||
def create_presentation():
    if sys.stdout.isatty():
        return ProgressBar()
    if is_jupyter_notebook():
        return ProgressBarJupyter()
    return ProgressPrint()

##__________________________________________________________________||
