import threading
from collections.abc import Callable
from typing import Any

from .type import FD, StreamQueue


class StreamPickup(threading.Thread):
    def __init__(
        self,
        queue: StreamQueue,
        stdout_write: Callable[[str], Any],
        stderr_write: Callable[[str], Any],
    ) -> None:
        super().__init__(daemon=True)
        self.queue = queue
        self.stdout_write = stdout_write
        self.stderr_write = stderr_write

    def run(self) -> None:
        try:
            while True:
                m = self.queue.get()
                if m is None:
                    break
                s, f = m
                if f == FD.STDOUT:
                    self.stdout_write(s)
                elif f == FD.STDERR:
                    self.stderr_write(s)
                else:
                    raise ValueError('unknown fd: {!r}'.format(f))

        except EOFError:
            pass
