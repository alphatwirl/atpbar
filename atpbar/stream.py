import sys
import threading
from collections.abc import Callable
from enum import Enum
from io import TextIOBase
from multiprocessing import Queue
from typing import Any, TypeAlias

from .presentation import Presentation


class FD(Enum):
    STDOUT = 1
    STDERR = 2


StreamQueue: TypeAlias = 'Queue[tuple[str, FD] | None]'


class StreamRedirection:
    def __init__(self, queue: StreamQueue, presentation: Presentation) -> None:
        self.disabled = not presentation.stdout_stderr_redrection
        if self.disabled:
            return

        self.queue = queue
        self.presentation = presentation

        self.stdout = Stream(self.queue, FD.STDOUT)
        self.stderr = Stream(self.queue, FD.STDERR)

    def start(self) -> None:
        if self.disabled:
            return

        self.pickup = StreamPickup(
            self.queue, self.presentation.stdout_write, self.presentation.stderr_write
        )
        self.pickup.start()

        self.stdout_org = sys.stdout
        sys.stdout = self.stdout  # type: ignore

        self.stderr_org = sys.stderr
        sys.stderr = self.stderr  # type: ignore

    def end(self) -> None:
        if self.disabled:
            return

        sys.stdout = self.stdout_org
        sys.stderr = self.stderr_org
        self.queue.put(None)
        self.pickup.join()


def register_stream_queue(queue: StreamQueue) -> None:
    if queue is None:
        return
    sys.stdout = Stream(queue, FD.STDOUT)  # type: ignore
    sys.stderr = Stream(queue, FD.STDERR)  # type: ignore


class Stream(TextIOBase):
    def __init__(self, queue: StreamQueue, fd: FD) -> None:
        self.fd = fd
        self.queue = queue
        self.buffer = ""

    def write(self, s: str) -> int:
        # sys.__stdout__.write(repr(s))
        # sys.__stdout__.write('\n')

        try:
            endswith_n = s.endswith("\n")
        except:
            self.flush()
            self.queue.put((s, self.fd))
            return len(s)

        if endswith_n:
            self.buffer += s
            self.flush()
            return len(s)

        self.buffer += s
        return len(s)

    def flush(self) -> None:
        if not self.buffer:
            return
        self.queue.put((self.buffer, self.fd))
        self.buffer = ""


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
                    raise ValueError("unknown fd: {!r}".format(f))

        except EOFError:
            pass
