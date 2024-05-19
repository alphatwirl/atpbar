import atexit
import contextlib
import multiprocessing
from collections.abc import Iterator

from .machine import StateMachine
from .progressreport import ProgressReporter

_machine = StateMachine()


def find_reporter() -> ProgressReporter | None:
    """returns the progress reporter

    This function is to be called in the main process of a
    multiprocessing program. The reporter should be registered in
    sub-processes with the function `register_reporter()`

    Returns
    -------
    object
        The progress reporter

    """
    return _machine.find_reporter()


def register_reporter(reporter: ProgressReporter) -> None:
    """registers a reporter

    This function is to be called in sub-processes of a
    multiprocessing program.

    Parameters
    ----------
    reporter : object
        The reporter obtained in the main process by the function
        `find_reporter()`


    Returns
    -------
    None

    """
    _machine.register_reporter(reporter)


def flush() -> None:
    """flushes progress bars

    This function flushes all active progress bars. It returns when
    the progress bars finish updating.

    Returns
    -------
    None

    """
    _machine.flush()


@contextlib.contextmanager
def flushing() -> Iterator[None]:
    '''Flushes progress bars on exit'''
    try:
        yield
    finally:
        flush()


def disable() -> None:
    """disables progress bars

    This function needs to be called in the main process before
    `atpbar()` or `find_reporter()` is used.

    Returns
    -------
    None

    """
    _machine.disable()


def shutdown() -> None:
    """shutdowns the progress bars

    Returns
    -------
    None

    """
    _machine.shutdown()


# This import prevents the issue
# https://github.com/alphatwirl/atpbar/issues/4
import multiprocessing.queues  # noqa: E402 F401

atexit.register(shutdown)


@contextlib.contextmanager
def fetch_reporter() -> Iterator[ProgressReporter | None]:
    yield from _machine.fetch_reporter()
