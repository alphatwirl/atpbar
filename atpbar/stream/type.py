import sys
from enum import Enum
from multiprocessing import Queue

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias


class FD(Enum):
    STDOUT = 1
    STDERR = 2


StreamQueue: TypeAlias = 'Queue[tuple[str, FD] | None]'
