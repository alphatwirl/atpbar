import collections
from typing import Literal

import pytest

from atpbar import atpbar

from .conftest import MockCreatePresentation


@pytest.mark.parametrize('method', ['break', 'exception'])
@pytest.mark.parametrize('n_iterations', [10, 1, 0])
@pytest.mark.parametrize('n_done', [10, 4, 1, 0])
def test_one_loop_break_exception(
    mock_create_presentation: MockCreatePresentation,
    n_iterations: int,
    n_done: int,
    method: Literal['break', 'exception'],
) -> None:
    n_done = min(n_done, n_iterations)

    def task_break(n_done: int, n_iterations: int) -> None:
        for i in atpbar(range(n_iterations)):
            if i == n_done:
                break

    def task_exception(n_done: int, n_iterations: int) -> None:
        for i in atpbar(range(n_iterations)):
            if i == n_done:
                raise Exception()

    #
    if method == 'break':
        task_break(n_done, n_iterations)
    else:
        if n_done < n_iterations:
            with pytest.raises(Exception):
                task_exception(n_done, n_iterations)
        else:
            task_exception(n_done, n_iterations)

    ## print()
    ## print(mock_create_presentation)

    n_reports_expected = n_done + 1 + bool(n_done < n_iterations)
    presentations = mock_create_presentation.presentations

    assert 2 == len(presentations)  # created when atpbar started and ended

    #
    progressbar0 = presentations[0]
    assert n_reports_expected == len(progressbar0.reports)
    assert 1 == len(progressbar0.task_ids)
    assert 1 == progressbar0.n_firsts
    assert 1 == progressbar0.n_lasts
    done_total_list_expected = [(n_done, n_iterations)]
    done_total_list_actual = [
        (d['done'], d['total']) for d in progressbar0._report_dict.values()
    ]
    assert collections.Counter(done_total_list_expected) == collections.Counter(
        done_total_list_actual
    )

    #
    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)
