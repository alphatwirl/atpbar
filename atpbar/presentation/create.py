# Tai Sakuma <tai.sakuma@gmail.com>
import sys

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

def is_jupyter_notebook():
    try:
        from IPython import get_ipython
        if 'IPKernelApp' in get_ipython().config:
            return True
    except:
        pass
    return False

##__________________________________________________________________||
