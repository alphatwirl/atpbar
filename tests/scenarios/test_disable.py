import itertools
import multiprocessing
import threading
import time
from typing import Callable

import pytest

from atpbar import atpbar, disable, find_reporter, flush, register_reporter
from atpbar.progress_report import ProgressReporter

from .conftest import MockCreatePresentation


@pytest.mark.parametrize('niterations', [10, 1, 0])
def test_one_loop(
    mock_create_presentation: MockCreatePresentation, niterations: int
) -> None:
    disable()
    for i in atpbar(range(niterations)):
        pass
    presentations = mock_create_presentation.presentations
    assert 0 == len(presentations)


def test_nested_loops(mock_create_presentation: MockCreatePresentation) -> None:
    disable()
    for i in atpbar(range(4)):
        for j in atpbar(range(3)):
            pass


def run_with_threading(nthreads: int = 3, niterations: list[int] = [5, 5, 5]) -> None:
    def task(n: int, name: str) -> None:
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)

    threads = []
    for i in range(nthreads):
        name = 'thread {}'.format(i)
        n = niterations[i]
        t = threading.Thread(target=task, args=(n, name))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    flush()


@pytest.mark.parametrize('niterations', [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize('nthreads', [3, 1, 0])
def test_threading(
    mock_create_presentation: MockCreatePresentation,
    nthreads: int,
    niterations: list[int],
) -> None:
    disable()

    # make niterations as long as nthreads. repeat if necessary
    niterations = list(
        itertools.chain(
            *itertools.repeat(niterations, nthreads // len(niterations) + 1)
        )
    )[:nthreads]

    run_with_threading(nthreads, niterations)

    presentations = mock_create_presentation.presentations
    assert 0 == len(presentations)


def run_with_multiprocessing(
    nprocesses: int, ntasks: int, niterations: list[int]
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
        name = 'task {}'.format(i)
        n = niterations[i]
        queue.put((n, name))
    for i in range(nprocesses):
        queue.put(None)
        queue.join()
    flush()


@pytest.mark.xfail()
@pytest.mark.parametrize('niterations', [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize('ntasks', [3, 1, 0])
@pytest.mark.parametrize('nprocesses', [4, 1])
def test_multiprocessing(
    mock_create_presentation: MockCreatePresentation,
    nprocesses: int,
    ntasks: int,
    niterations: list[int],
) -> None:
    disable()

    # make niterations as long as ntasks. repeat if necessary
    niterations = list(
        itertools.chain(*itertools.repeat(niterations, ntasks // len(niterations) + 1))
    )[:ntasks]

    run_with_multiprocessing(nprocesses, ntasks, niterations)

    presentations = mock_create_presentation.presentations
    assert 0 == len(presentations)


def test_call_twice() -> None:
    disable()
    disable()
