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
        if not isinstance(s, str):
            # The same error message as `sys.stdout.write()`
            raise TypeError(f'write() argument must be str, not {type(s).__name__}')

        self.buffer += s
        if s.endswith('\n'):
            self.flush()
        return len(s)

    def flush(self) -> None:
        if not self.buffer:
            return
        self.queue.put((self.buffer, self.fd))
        self.buffer = ''
