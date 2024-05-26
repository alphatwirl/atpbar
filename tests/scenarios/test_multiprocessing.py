import itertools
import multiprocessing
import time
from collections.abc import Callable

import pytest

from atpbar import atpbar, find_reporter, flush, register_reporter
from atpbar.progress_report import ProgressReporter

from .conftest import MockCreatePresentation


def run_with_multiprocessing(
    nprocesses: int, ntasks: int, niterations: list[int], time_starting_task: float
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

    for i in range(nprocesses):
        p = multiprocessing.Process(target=worker, args=(reporter, task, queue))
        p.start()

    for i in atpbar(range(ntasks)):  # `atpbar` is used here
        name = "task {}".format(i)
        n = niterations[i]
        queue.put((n, name, time_starting_task))
        time.sleep(0.01)

    for i in range(nprocesses):
        queue.put(None)
        queue.join()

    flush()


@pytest.mark.xfail()
@pytest.mark.parametrize("time_starting_task", [0, 0.01, 0.2])
@pytest.mark.parametrize("niterations", [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize("ntasks", [3, 1, 0])
@pytest.mark.parametrize("nprocesses", [6, 2, 1])
def test_multiprocessing_from_loop(
    mock_create_presentation: MockCreatePresentation,
    nprocesses: int,
    ntasks: int,
    niterations: list[int],
    time_starting_task: float,
) -> None:

    # make niterations as long as ntasks. repeat if necessary
    niterations = list(
        itertools.chain(*itertools.repeat(niterations, ntasks // len(niterations) + 1))
    )[:ntasks]

    run_with_multiprocessing(nprocesses, ntasks, niterations, time_starting_task)

    ## print()
    ## print(mock_create_presentation)

    nreports_expected_from_main = ntasks + 1
    nreports_expected_from_tasks = sum(niterations) + ntasks
    nreports_expected = nreports_expected_from_main + nreports_expected_from_tasks

    presentations = mock_create_presentation.presentations

    if nreports_expected_from_tasks == 0:
        assert 3 == len(presentations)  # in find_reporter(), at the
        # end of `atpbar` in the main
        # process, and in flush().

        progressbar0 = presentations[0]
        assert nreports_expected == len(progressbar0.reports)
        # one report from `atpbar` in the main thread

        assert 1 == progressbar0.n_firsts
        assert 1 == progressbar0.nlasts
        assert 1 == len(progressbar0.task_ids)

    else:
        if 2 == len(presentations):

            progressbar1 = presentations[1]
            assert 0 == len(progressbar1.reports)

            progressbar0 = presentations[0]
            assert ntasks + 1 == len(progressbar0.task_ids)
            assert ntasks + 1 == progressbar0.n_firsts
            assert ntasks + 1 == progressbar0.nlasts
            assert nreports_expected == len(progressbar0.reports)

        else:
            assert 3 == len(presentations)

            progressbar2 = presentations[2]
            assert 0 == len(progressbar2.reports)

            progressbar0 = presentations[0]
            progressbar1 = presentations[1]

            assert ntasks + 1 == len(progressbar0.task_ids) + len(progressbar1.task_ids)
            assert ntasks + 1 == progressbar0.n_firsts + progressbar1.n_firsts
            assert ntasks + 1 == progressbar0.nlasts + progressbar1.nlasts
            assert nreports_expected == len(progressbar0.reports) + len(
                progressbar1.reports
            )

    # At this point the pickup shouldn't be owned. Therefore, a new
    # `atpbar` in the main thread should own it.
    npresentations = len(presentations)
    for i in atpbar(range(4)):
        pass
    assert npresentations + 1 == len(presentations)
    progressbar = presentations[-2]
    assert 1 == len(progressbar.task_ids)
    assert 1 == progressbar.n_firsts
    assert 1 == progressbar.nlasts
    assert 4 + 1 == len(progressbar.reports)
