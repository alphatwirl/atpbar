# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import threading
from enum import Enum


##__________________________________________________________________||
class StreamRedirection:
    def __init__(self, queue, presentation):
        self.disabled = not presentation.stdout_stderr_redrection
        if self.disabled:
            return

        self.queue = queue
        self.presentation = presentation

        self.stdout = Stream(self.queue, FD.STDOUT)
        self.stderr = Stream(self.queue, FD.STDERR)

    def start(self):
        if self.disabled:
            return

        self.pickup = StreamPickup(self.queue, self.presentation.stdout_write, self.presentation.stderr_write)
        self.pickup.start()

        self.stdout_org = sys.stdout
        sys.stdout = self.stdout

        self.stderr_org = sys.stderr
        sys.stderr = self.stderr

    def end(self):
        if self.disabled:
            return

        sys.stdout = self.stdout_org
        sys.stderr = self.stderr_org
        self.queue.put(None)
        self.pickup.join()


##__________________________________________________________________||
def register_stream_queue(queue):
    if queue is None:
        return
    sys.stdout = Stream(queue, FD.STDOUT)
    sys.stderr = Stream(queue, FD.STDERR)


##__________________________________________________________________||
class FD(Enum):
    STDOUT = 1
    STDERR = 2


##__________________________________________________________________||
class Stream:
    def __init__(self, queue, fd):
        self.fd = fd
        self.queue = queue
        self.buffer = ""

    def write(self, s):
        # sys.__stdout__.write(repr(s))
        # sys.__stdout__.write('\n')

        try:
            endswith_n = s.endswith("\n")
        except:
            self.flush()
            self.queue.put((s, self.fd))
            return

        if endswith_n:
            self.buffer += s
            self.flush()
            return

        self.buffer += s

    def flush(self):
        if not self.buffer:
            return
        self.queue.put((self.buffer, self.fd))
        self.buffer = ""


##__________________________________________________________________||
class StreamPickup(threading.Thread):
    def __init__(self, queue, stdout_write, stderr_write):
        super().__init__(daemon=True)
        self.queue = queue
        self.stdout_write = stdout_write
        self.stderr_write = stderr_write

    def run(self):
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


##__________________________________________________________________||
