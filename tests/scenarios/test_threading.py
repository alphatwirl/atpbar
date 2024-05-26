import itertools
import threading
import time

import pytest

from atpbar import atpbar, flush

from .conftest import MockCreatePresentation


@pytest.mark.parametrize('time_starting_task', [0, 0.01, 0.2])
@pytest.mark.parametrize('n_iterations', [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize('n_threads', [3, 1, 0])
def test_threading_from_loop(
    mock_create_presentation: MockCreatePresentation,
    n_threads: int,
    n_iterations: list[int],
    time_starting_task: float,
) -> None:

    # make n_iterations as long as n_threads. repeat if necessary
    n_iterations = list(
        itertools.chain(
            *itertools.repeat(n_iterations, n_threads // len(n_iterations) + 1)
        )
    )[:n_threads]

    def run_with_threading(
        n_threads: int = 3,
        n_iterations: list[int] = [5, 5, 5],
        time_starting_task: float = 0,
    ) -> None:

        def task(
            n: int,
            name: str,
            time_starting: float,
        ) -> None:
            # When starting time is long, the loop in the main thread might
            # already end by the time the loop in this task starts.
            time.sleep(time_starting)
            for i in atpbar(range(n), name=name):
                time.sleep(0.0001)

        threads = []
        # `atpbar` is used here while `atpbar` is also used in threads being
        # launched in this loop. If none of the `atpbar`s in threads has
        # started by the end of this loop, the `atpbar` for this loop waits
        # until the progress bar for this loop finish updating. Otherwise,
        # progress bars from threads are being updated together with the
        # progress bar for this loop and the `atpbar` will not wait.
        for i in atpbar(range(n_threads)):

            name = 'thread {}'.format(i)
            n = n_iterations[i]
            t = threading.Thread(target=task, args=(n, name, time_starting_task))
            t.start()
            threads.append(t)

            time.sleep(0.01)
            # sleep sometime so this loop doesn't end too quickly. Without this
            # sleep, this loop could end before an `atpbar` in any of the
            # threads start even if `time_starting_task` is zero.

        for t in threads:
            t.join()

        flush()

    run_with_threading(n_threads, n_iterations, time_starting_task)

    ## print()
    ## print(mock_create_presentation)

    n_reports_expected_from_main = n_threads + 1
    n_reports_expected_from_threads = sum(n_iterations) + n_threads
    n_reports_expected = n_reports_expected_from_main + n_reports_expected_from_threads

    presentations = mock_create_presentation.presentations

    if n_reports_expected_from_threads == 0:
        assert 3 == len(presentations)  # when `atpbar` in the main thread
        # starts and end and when flush() is
        # called

        progressbar0 = presentations[0]
        assert n_reports_expected == len(progressbar0.reports)
        # one report from `atpbar` in the main thread

        assert 1 == len(progressbar0.task_ids)
        assert 1 == progressbar0.n_firsts
        assert 1 == progressbar0.n_lasts

    else:

        if 2 == len(presentations):

            progressbar0 = presentations[0]
            assert n_reports_expected == len(progressbar0.reports)
            assert n_threads + 1 == len(progressbar0.task_ids)
            assert n_threads + 1 == progressbar0.n_firsts
            assert n_threads + 1 == progressbar0.n_lasts

            progressbar1 = presentations[1]
            assert 0 == len(progressbar1.reports)

        else:
            assert 3 == len(presentations)

            progressbar0 = presentations[0]
            progressbar1 = presentations[1]

            assert n_reports_expected == len(progressbar0.reports) + len(
                progressbar1.reports
            )
            assert n_threads + 1 == len(progressbar0.task_ids) + len(
                progressbar1.task_ids
            )
            assert n_threads + 1 == progressbar0.n_firsts + progressbar1.n_firsts
            assert n_threads + 1 == progressbar0.n_lasts + progressbar1.n_lasts

            progressbar2 = presentations[2]
            assert 0 == len(progressbar2.reports)

    # At this point the pickup shouldn't be owned. Therefore, a new
    # `atpbar` in the main thread should own it.
    n_presentations = len(presentations)
    for i in atpbar(range(4)):
        pass
    assert n_presentations + 1 == len(presentations)
    progressbar = presentations[-2]
    assert 4 + 1 == len(progressbar.reports)
    assert 1 == len(progressbar.task_ids)
    assert 1 == progressbar.n_firsts
    assert 1 == progressbar.n_lasts
