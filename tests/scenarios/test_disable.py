import itertools
import multiprocessing
import threading
import time
from typing import Callable

import pytest

from atpbar import atpbar, disable, find_reporter, flush, register_reporter
from atpbar.progress_report import ProgressReporter

from .conftest import MockCreatePresentation


@pytest.mark.parametrize('n_iterations', [10, 1, 0])
def test_one_loop(
    mock_create_presentation: MockCreatePresentation, n_iterations: int
) -> None:
    disable()
    for i in atpbar(range(n_iterations)):
        pass
    presentations = mock_create_presentation.presentations
    assert 0 == len(presentations)


def test_nested_loops(mock_create_presentation: MockCreatePresentation) -> None:
    disable()
    for i in atpbar(range(4)):
        for j in atpbar(range(3)):
            pass


def run_with_threading(n_threads: int = 3, n_iterations: list[int] = [5, 5, 5]) -> None:
    def task(n: int, name: str) -> None:
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)

    threads = []
    for i in range(n_threads):
        name = 'thread {}'.format(i)
        n = n_iterations[i]
        t = threading.Thread(target=task, args=(n, name))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    flush()


@pytest.mark.parametrize('n_iterations', [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize('n_threads', [3, 1, 0])
def test_threading(
    mock_create_presentation: MockCreatePresentation,
    n_threads: int,
    n_iterations: list[int],
) -> None:
    disable()

    # make n_iterations as long as n_threads. repeat if necessary
    n_iterations = list(
        itertools.chain(
            *itertools.repeat(n_iterations, n_threads // len(n_iterations) + 1)
        )
    )[:n_threads]

    run_with_threading(n_threads, n_iterations)

    presentations = mock_create_presentation.presentations
    assert 0 == len(presentations)


def run_with_multiprocessing(
    n_processes: int, n_tasks: int, n_iterations: list[int]
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
    for i in range(n_processes):
        p = multiprocessing.Process(target=worker, args=(reporter, task, queue))
        p.start()
    for i in range(n_tasks):
        name = 'task {}'.format(i)
        n = n_iterations[i]
        queue.put((n, name))
    for i in range(n_processes):
        queue.put(None)
        queue.join()
    flush()


@pytest.mark.xfail()
@pytest.mark.parametrize('n_iterations', [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize('n_tasks', [3, 1, 0])
@pytest.mark.parametrize('n_processes', [4, 1])
def test_multiprocessing(
    mock_create_presentation: MockCreatePresentation,
    n_processes: int,
    n_tasks: int,
    n_iterations: list[int],
) -> None:
    disable()

    # make n_iterations as long as n_tasks. repeat if necessary
    n_iterations = list(
        itertools.chain(
            *itertools.repeat(n_iterations, n_tasks // len(n_iterations) + 1)
        )
    )[:n_tasks]

    run_with_multiprocessing(n_processes, n_tasks, n_iterations)

    presentations = mock_create_presentation.presentations
    assert 0 == len(presentations)


def test_call_twice() -> None:
    disable()
    disable()
