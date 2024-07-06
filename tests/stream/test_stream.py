from unittest.mock import sentinel

from hypothesis import given, settings
from hypothesis import strategies as st

from atpbar.stream import Queue, Stream, StreamQueue

from .st import st_text


class StatefulTest:
    def __init__(self, data: st.DataObject) -> None:
        self.draw = data.draw
        self.queue: StreamQueue = Queue()
        self.fd = sentinel.fd
        self.stream = Stream(self.queue, self.fd)
        self.written = list[str]()

    def write(self) -> None:
        text = self.draw(st_text())
        self.stream.write(text)
        self.written.append(text)

    def write_with_newline(self) -> None:
        text = self.draw(st_text())
        text += '\n'
        self.stream.write(text)
        self.written.append(text)
        expected = ''.join(self.written)
        assert self.queue.get() == (expected, self.fd)
        self.written.clear()

    def flush(self) -> None:
        self.stream.flush()
        expected = ''.join(self.written)
        if not expected:
            return
        assert self.queue.get() == (expected, self.fd)
        self.written.clear()


@settings(max_examples=200)
@given(data=st.data())
def test_stream(data: st.DataObject) -> None:
    test = StatefulTest(data=data)
    METHODS = [test.write, test.write_with_newline, test.flush]
    methods = data.draw(st.lists(st.sampled_from(METHODS)))
    for method in methods:
        method()
