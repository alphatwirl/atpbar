import sys

from .bartty import ProgressBar
from .base import Presentation
from .detect.jupy import is_jupyter_notebook
from .txtprint import ProgressPrint

try:
    from .barjupyter import ProgressBarJupyter
except ImportError:
    pass


def create_presentation() -> Presentation:
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
