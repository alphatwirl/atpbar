from unittest.mock import sentinel

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from atpbar.stream import OutputStream, Queue, StreamQueue
from tests.test_utils.st import st_text


def test_type_error() -> None:
    stream = OutputStream(Queue(), sentinel.fd)
    with pytest.raises(TypeError):
        stream.write(123)  # type: ignore


class StatefulTest:
    def __init__(self, data: st.DataObject) -> None:
        self.draw = data.draw
        self.queue: StreamQueue = Queue()
        self.fd = sentinel.fd
        self.stream = OutputStream(self.queue, self.fd)
        self.written = list[str]()

    def write(self) -> None:
        text = self.draw(st_text())
        assert self.stream.write(text) == len(text)
        self.written.append(text)

    def write_with_newline(self) -> None:
        text = self.draw(st_text())
        text += '\n'
        assert self.stream.write(text) == len(text)
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
def test_stateful(data: st.DataObject) -> None:
    test = StatefulTest(data=data)
    METHODS = [test.write, test.write_with_newline, test.flush]
    methods = data.draw(st.lists(st.sampled_from(METHODS)))
    for method in methods:
        method()
