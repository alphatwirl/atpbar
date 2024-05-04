import os

try:
    import spyder  # type: ignore
except ImportError:
    spyder = None

try:
    from IPython import get_ipython
except ImportError:
    get_ipython = None  # type: ignore


def is_spyder_ide() -> bool:
    """Tests if on Spyder IDE

    Returns
    -------
    bool
        True if on Spyder IDE

    """

    if spyder is None:
        return False

    try:
        if "IPKernelApp" not in get_ipython().config:
            return False
    except:
        return False

    if "SPYDER_ARGS" not in os.environ:
        return False

    min_n_spy_var = 15  # A possible minimum number of the environmental
    # variables that start with "SPY_" on Spyder IDE.
    n_spy_var = len([k for k in os.environ.keys() if k.startswith("SPY_")])
    if n_spy_var < min_n_spy_var:
        return False

    return True
