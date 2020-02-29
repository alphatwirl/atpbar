
##__________________________________________________________________||
try:
    import ipywidgets as widgets
except ImportError:
    widgets = None

try:
    from IPython.display import display
except ImportError:
    display = None

try:
    from IPython import get_ipython
except ImportError:
    get_ipython = None


from .spy import is_spyder_ide

##__________________________________________________________________||
def is_jupyter_notebook():
    """Tests if on Jupyter Notebook

    Returns
    -------
    bool
        True if on Jupyter Notebook

    """

    if widgets is None:
        return False

    if display is None:
        return False

    try:
        if 'IPKernelApp' not in get_ipython().config:
            return False
    except:
        return False

    if is_spyder_ide():
        return False

    return True

##__________________________________________________________________||
