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
    """Create a presentation of progress report, e.g., progress bars

    Returns
    -------
    object
        an instance of ProgressBar if on TTY
        an instance of ProgressBarJupyter if on Jupyter Notebook
        an instance of ProgressPrint otherwise

    """

    if sys.stdout.isatty():
        return ProgressBar()

    if is_jupyter_notebook():
        try:
            return ProgressBarJupyter()
        except:
            pass

    return ProgressPrint()

##__________________________________________________________________||
