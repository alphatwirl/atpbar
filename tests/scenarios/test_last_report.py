import collections
from multiprocessing import set_start_method
from typing import Literal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from atpbar import atpbar

from .utils import mock_presentations

set_start_method('fork', force=True)


def func_break(n_done: int, n_iterations: int) -> None:
    for i in atpbar(range(n_iterations)):
        if i == n_done:
            break


def func_exception(n_done: int, n_iterations: int) -> None:
    for i in atpbar(range(n_iterations)):
        if i == n_done:
            raise Exception()


@given(
    method=st.sampled_from(['break', 'exception']),
    n_iterations=st.integers(min_value=0, max_value=10),
    n_done=st.integers(min_value=0, max_value=10),
)
def test_multiprocessing_process(
    method: Literal['break', 'exception'], n_iterations: int, n_done: int
) -> None:
    n_done = min(n_done, n_iterations)

    with mock_presentations() as presentations:
        if method == 'break':
            func_break(n_done, n_iterations)
        else:
            if n_done < n_iterations:
                with pytest.raises(Exception):
                    func_exception(n_done, n_iterations)
            else:
                func_exception(n_done, n_iterations)

        assert len(presentations) == 2

        progressbar0 = presentations[0]
        assert len(progressbar0.reports) == n_done + 1 + bool(n_done < n_iterations)
        assert len(progressbar0.task_ids) == 1
        assert progressbar0.n_firsts == 1
        assert progressbar0.n_lasts == 1

        done_total_list_expected = [(n_done, n_iterations)]
        done_total_list_actual = [
            (d['done'], d['total']) for d in progressbar0._report_dict.values()
        ]
        assert collections.Counter(done_total_list_expected) == collections.Counter(
            done_total_list_actual
        )

        progressbar1 = presentations[1]
        assert len(progressbar1.reports) == 0
