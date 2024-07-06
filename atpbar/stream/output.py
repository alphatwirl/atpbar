import sys
from io import TextIOBase

from .type import FD, StreamQueue


def register_stream_queue(queue: StreamQueue) -> None:
    if queue is None:
        return
    sys.stdout = OutputStream(queue, FD.STDOUT)  # type: ignore
    sys.stderr = OutputStream(queue, FD.STDERR)  # type: ignore


class OutputStream(TextIOBase):
    def __init__(self, queue: StreamQueue, fd: FD) -> None:
        self.fd = fd
        self.queue = queue
        self.buffer = ''

    def write(self, s: str) -> int:
        # sys.__stdout__.write(repr(s))
        # sys.__stdout__.write('\n')

        try:
            endswith_n = s.endswith('\n')
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
        self.buffer = ''
