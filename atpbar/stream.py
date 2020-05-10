# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import threading

##__________________________________________________________________||
class Stream:
    def __init__(self, queue):
        self.buffer = ''

        self.queue = queue
    def write(self, s):
        # sys.__stdout__.write(repr(s))
        # sys.__stdout__.write('\n')

        try:
            endswith_n = s.endswith('\n')
        except:
            self.flush()
            self.queue.put(s)
            return

        if endswith_n:
            self.buffer += s
            self.flush()
            return

        self.buffer += s

    def flush(self):
        if not self.buffer:
            return
        self.queue.put(self.buffer)
        self.buffer = ''

##__________________________________________________________________||
class StreamPickup(threading.Thread):
    def __init__(self, queue, send):
        super().__init__(daemon=True)
        self.queue = queue
        self.send = send
    def run(self):
        try:
            while True:
                s = self.queue.get()
                if s is None:
                    break;
                self.send(s)
        except EOFError:
            pass

##__________________________________________________________________||
