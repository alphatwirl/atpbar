from typing import TypedDict
from uuid import UUID


class Report(TypedDict, total=False):
    '''Progress report

    Parameters
    ----------
    taskid : immutable
        The unique task ID.
    done : int
        The number of the iterations done so far
    total : int
            The total iterations to be done
    name : str
            A name of the task. It will be use as the label on the
            progress bars.
    first : bool
            `True` if the first report for the task. If not given,
            automatically determined from `done`; `True` if `done` is
            0, `False` otherwise
    last : bool
            `True` if the last report for the task. If not given,
            automatically determined from `done` and `total`; `True`
            if `done` equals `total`, `False` otherwise

    Notes:
    ------
    TODO: Use typing.Required for Python 3.11 and above
    '''

    taskid: UUID
    done: int
    total: int
    name: str
    first: bool
    last: bool
