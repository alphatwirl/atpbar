import itertools
import multiprocessing
import time
from collections.abc import Callable

import pytest

from atpbar import atpbar, find_reporter, flush, register_reporter
from atpbar.progress_report import ProgressReporter

from .conftest import MockCreatePresentation


def run_with_multiprocessing(
    n_processes: int, n_tasks: int, n_iterations: list[int], time_starting_task: float
) -> None:

    def task(n: int, name: str, time_starting: float) -> None:
        time.sleep(time_starting)
        for i in atpbar(range(n), name=name):  # `atpbar` is used here
            time.sleep(0.0001)

    def worker(
        reporter: ProgressReporter,
        task: Callable[[int, str, float], None],
        queue: multiprocessing.JoinableQueue,
    ) -> None:
        register_reporter(reporter)
        while True:
            args = queue.get()
            if args is None:
                queue.task_done()
                break
            task(*args)
            queue.task_done()

    reporter = find_reporter()
    queue = multiprocessing.JoinableQueue()  # type: ignore

    for i in range(n_processes):
        p = multiprocessing.Process(target=worker, args=(reporter, task, queue))
        p.start()

    for i in atpbar(range(n_tasks)):  # `atpbar` is used here
        name = 'task {}'.format(i)
        n = n_iterations[i]
        queue.put((n, name, time_starting_task))
        time.sleep(0.01)

    for i in range(n_processes):
        queue.put(None)
        queue.join()

    flush()


@pytest.mark.xfail()
@pytest.mark.parametrize('time_starting_task', [0, 0.01, 0.2])
@pytest.mark.parametrize('n_iterations', [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize('n_tasks', [3, 1, 0])
@pytest.mark.parametrize('n_processes', [6, 2, 1])
def test_multiprocessing_from_loop(
    mock_create_presentation: MockCreatePresentation,
    n_processes: int,
    n_tasks: int,
    n_iterations: list[int],
    time_starting_task: float,
) -> None:

    # make n_iterations as long as n_tasks. repeat if necessary
    n_iterations = list(
        itertools.chain(
            *itertools.repeat(n_iterations, n_tasks // len(n_iterations) + 1)
        )
    )[:n_tasks]

    run_with_multiprocessing(n_processes, n_tasks, n_iterations, time_starting_task)

    ## print()
    ## print(mock_create_presentation)

    n_reports_expected_from_main = n_tasks + 1
    n_reports_expected_from_tasks = sum(n_iterations) + n_tasks
    n_reports_expected = n_reports_expected_from_main + n_reports_expected_from_tasks

    presentations = mock_create_presentation.presentations

    if n_reports_expected_from_tasks == 0:
        assert 3 == len(presentations)  # in find_reporter(), at the
        # end of `atpbar` in the main
        # process, and in flush().

        progressbar0 = presentations[0]
        assert n_reports_expected == len(progressbar0.reports)
        # one report from `atpbar` in the main thread

        assert 1 == progressbar0.n_firsts
        assert 1 == progressbar0.n_lasts
        assert 1 == len(progressbar0.task_ids)

    else:
        if 2 == len(presentations):

            progressbar1 = presentations[1]
            assert 0 == len(progressbar1.reports)

            progressbar0 = presentations[0]
            assert n_tasks + 1 == len(progressbar0.task_ids)
            assert n_tasks + 1 == progressbar0.n_firsts
            assert n_tasks + 1 == progressbar0.n_lasts
            assert n_reports_expected == len(progressbar0.reports)

        else:
            assert 3 == len(presentations)

            progressbar2 = presentations[2]
            assert 0 == len(progressbar2.reports)

            progressbar0 = presentations[0]
            progressbar1 = presentations[1]

            assert n_tasks + 1 == len(progressbar0.task_ids) + len(
                progressbar1.task_ids
            )
            assert n_tasks + 1 == progressbar0.n_firsts + progressbar1.n_firsts
            assert n_tasks + 1 == progressbar0.n_lasts + progressbar1.n_lasts
            assert n_reports_expected == len(progressbar0.reports) + len(
                progressbar1.reports
            )

    # At this point the pickup shouldn't be owned. Therefore, a new
    # `atpbar` in the main thread should own it.
    n_presentations = len(presentations)
    for i in atpbar(range(4)):
        pass
    assert n_presentations + 1 == len(presentations)
    progressbar = presentations[-2]
    assert 1 == len(progressbar.task_ids)
    assert 1 == progressbar.n_firsts
    assert 1 == progressbar.n_lasts
    assert 4 + 1 == len(progressbar.reports)
