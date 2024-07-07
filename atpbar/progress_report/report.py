from typing import TypedDict
from uuid import UUID


class Report(TypedDict):
    '''Progress report

    Parameters
    ----------
    task_id
        The unique task ID.
    done
        The number of the iterations done so far
    total
        The total iterations to be done
    name
        A name of the task. It will be use as the label on the progress bars.
    first : bool
       `True` if the first report for the task.
    last : bool
       `True` if the last report for the task.

    '''

    task_id: UUID
    done: int
    total: int
    name: str
    first: bool
    last: bool
