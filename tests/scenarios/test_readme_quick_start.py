from collections.abc import Callable
import itertools
import multiprocessing
import threading
import time

import pytest

from atpbar import atpbar, find_reporter, flush, register_reporter
from atpbar.progress_report import ProgressReporter

from .conftest import MockCreatePresentation


@pytest.mark.parametrize("niterations", [10, 1, 0])
def test_one_loop(
    mock_create_presentation: MockCreatePresentation,
    niterations: int,
) -> None:

    for i in atpbar(range(niterations)):
        pass

    #
    nreports_expected = niterations + 1
    presentations = mock_create_presentation.presentations

    #
    assert 2 == len(presentations)  # created when atpbar started and ended

    #
    progressbar0 = presentations[0]
    assert nreports_expected == len(progressbar0.reports)
    assert 1 == len(progressbar0.task_ids)
    assert 1 == progressbar0.n_firsts
    assert 1 == progressbar0.n_lasts

    #
    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)


def test_nested_loops(mock_create_presentation: MockCreatePresentation) -> None:

    for i in atpbar(range(4)):
        for j in atpbar(range(3)):
            pass

    presentations = mock_create_presentation.presentations
    assert 2 == len(presentations)

    progressbar0 = presentations[0]
    assert (3 + 1) * 4 + 4 + 1 == len(progressbar0.reports)
    assert 5 == len(progressbar0.task_ids)
    assert 5 == progressbar0.n_firsts
    assert 5 == progressbar0.n_lasts

    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)


def run_with_threading(nthreads: int = 3, niterations: list[int] = [5, 5, 5]) -> None:
    def task(n: int, name: str) -> None:
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)

    threads = []
    for i in range(nthreads):
        name = "thread {}".format(i)
        n = niterations[i]
        t = threading.Thread(target=task, args=(n, name))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    flush()


@pytest.mark.parametrize("niterations", [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize("nthreads", [3, 1, 0])
def test_threading(
    mock_create_presentation: MockCreatePresentation,
    nthreads: int,
    niterations: list[int],
) -> None:

    # make niterations as long as nthreads. repeat if necessary
    niterations = list(
        itertools.chain(
            *itertools.repeat(niterations, nthreads // len(niterations) + 1)
        )
    )[:nthreads]

    run_with_threading(nthreads, niterations)

    nreports_expected = sum(niterations) + nthreads
    presentations = mock_create_presentation.presentations

    if nreports_expected == 0:
        assert 1 == len(presentations)  # created by flush()
        assert 0 == len(presentations[0].reports)
        return

    assert 2 == len(presentations)

    progressbar0 = presentations[0]
    assert nreports_expected == len(progressbar0.reports)
    assert nthreads == len(progressbar0.task_ids)
    assert nthreads == progressbar0.n_firsts
    assert nthreads == progressbar0.n_lasts

    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)


def run_with_multiprocessing(
    nprocesses: int,
    ntasks: int,
    niterations: list[int],
) -> None:
    def task(n: int, name: str) -> None:
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)

    def worker(
        reporter: ProgressReporter,
        task: Callable[[int, str], None],
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
    for i in range(ntasks):
        name = "task {}".format(i)
        n = niterations[i]
        queue.put((n, name))
    for i in range(nprocesses):
        queue.put(None)
        queue.join()
    flush()


@pytest.mark.xfail()
@pytest.mark.parametrize("niterations", [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize("ntasks", [6, 3, 1, 0])
@pytest.mark.parametrize("nprocesses", [10, 6, 2, 1])
def test_multiprocessing(
    mock_create_presentation: MockCreatePresentation,
    nprocesses: int,
    ntasks: int,
    niterations: list[int],
) -> None:

    # make niterations as long as ntasks. repeat if necessary
    niterations = list(
        itertools.chain(*itertools.repeat(niterations, ntasks // len(niterations) + 1))
    )[:ntasks]

    run_with_multiprocessing(nprocesses, ntasks, niterations)

    nreports_expected = sum(niterations) + ntasks
    presentations = mock_create_presentation.presentations

    assert 2 == len(presentations)  # created by find_reporter() and flush()

    progressbar0 = presentations[0]
    assert nreports_expected == len(progressbar0.reports)
    assert ntasks == len(progressbar0.task_ids)
    assert ntasks == progressbar0.n_firsts
    assert ntasks == progressbar0.n_lasts

    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)
