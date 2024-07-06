from enum import Enum
from multiprocessing import Queue
from typing import TypeAlias


class FD(Enum):
    STDOUT = 1
    STDERR = 2


StreamQueue: TypeAlias = 'Queue[tuple[str, FD] | None]'
