# Tai Sakuma <tai.sakuma@gmail.com>
import sys
from enum import Enum
import threading

##__________________________________________________________________||
class FD(Enum):
    STDOUT = 1
    STDERR = 2

##__________________________________________________________________||
class Stream:
    def __init__(self, queue, fd):
        self.fd = fd
        self.queue = queue
        self.buffer = ''
    def write(self, s):
        # sys.__stdout__.write(repr(s))
        # sys.__stdout__.write('\n')

        try:
            endswith_n = s.endswith('\n')
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
        self.buffer = ''

##__________________________________________________________________||
class StreamPickup(threading.Thread):
    def __init__(self, queue, send_stdout, send_stderr):
        super().__init__(daemon=True)
        self.queue = queue
        self.send_stdout = send_stdout
        self.send_stderr = send_stderr
    def run(self):
        try:
            while True:
                m = self.queue.get()
                if m is None:
                    break;
                s, f = m
                if f == FD.STDOUT:
                    self.send_stdout(s)
                elif f == FD.STDERR:
                    self.send_stderr(s)
                else:
                    raise ValueError('unknown fd: {!r}'.format(f))

        except EOFError:
            pass

##__________________________________________________________________||
