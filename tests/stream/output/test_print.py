import sys
from typing import Literal
from unittest.mock import Mock, call

from hypothesis import given, settings
from hypothesis import strategies as st
from pytest import MonkeyPatch

from atpbar.stream import FD, OutputStream
from tests.stream.st import st_text


def st_end() -> st.SearchStrategy[str | None]:
    '''A strategy for the `end` parameter of the `print` function.'''
    return st.one_of(st.none(), st.just('\n'), st_text())


@settings(max_examples=500)
@given(
    texts=st.lists(st_text()),
    end=st_end(),
    flush=st.booleans(),
    fd_name=st.sampled_from(['stdout', 'stderr']),
)
def test_print(
    texts: list[str], end: str | None, flush: bool, fd_name: Literal['stdout', 'stderr']
) -> None:
    queue = Mock()
    stdout = OutputStream(queue, fd=FD.STDOUT)
    stderr = OutputStream(queue, fd=FD.STDERR)

    with MonkeyPatch.context() as m:
        m.setattr(sys, 'stdout', stdout)
        m.setattr(sys, 'stderr', stderr)

        file = {'stdout': sys.stdout, 'stderr': sys.stderr}[fd_name]
        fd = {'stdout': FD.STDOUT, 'stderr': FD.STDERR}[fd_name]

        print(*texts, end=end, flush=flush, file=file)
        joined = ' '.join(texts)
        match joined, end, flush:
            case '', None | '\n', _:
                expected = '\n'
                assert [call((expected, fd))] == queue.put.call_args_list
            case '', '', _:
                assert [] == queue.put.call_args_list
            case '', str(), False if end:
                assert [] == queue.put.call_args_list
                print(file=file)
                expected = f'{end}\n'
                assert [call((expected, fd))] == queue.put.call_args_list
            case '', str(), True if end:
                expected = f'{end}'
                assert [call((expected, fd))] == queue.put.call_args_list
            case str(), None | '\n', _ if joined:
                expected = f'{joined}\n'
                assert [call((expected, fd))] == queue.put.call_args_list
            case str(), str(), False if joined:
                assert [] == queue.put.call_args_list
                print(file=file)
                expected = f'{joined}{end}\n'
                assert [call((expected, fd))] == queue.put.call_args_list
            case str(), str(), True if joined:
                expected = f'{joined}{end}'
                assert [call((expected, fd))] == queue.put.call_args_list
            case _:  # pragma: no cover
                assert False, (joined, end, flush)
