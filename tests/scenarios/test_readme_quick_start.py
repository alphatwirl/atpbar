import itertools
import multiprocessing
import threading
import time
from collections.abc import Callable

import pytest

from atpbar import atpbar, find_reporter, flush, register_reporter
from atpbar.progress_report import ProgressReporter

from .conftest import MockCreatePresentation


@pytest.mark.parametrize('n_iterations', [10, 1, 0])
def test_one_loop(
    mock_create_presentation: MockCreatePresentation,
    n_iterations: int,
) -> None:

    for i in atpbar(range(n_iterations)):
        pass

    #
    n_reports_expected = n_iterations + 1
    presentations = mock_create_presentation.presentations

    #
    assert 2 == len(presentations)  # created when atpbar started and ended

    #
    progressbar0 = presentations[0]
    assert n_reports_expected == len(progressbar0.reports)
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

    # make n_iterations as long as n_threads. repeat if necessary
    n_iterations = list(
        itertools.chain(
            *itertools.repeat(n_iterations, n_threads // len(n_iterations) + 1)
        )
    )[:n_threads]

    run_with_threading(n_threads, n_iterations)

    n_reports_expected = sum(n_iterations) + n_threads
    presentations = mock_create_presentation.presentations

    if n_reports_expected == 0:
        assert 1 == len(presentations)  # created by flush()
        assert 0 == len(presentations[0].reports)
        return

    assert 2 == len(presentations)

    progressbar0 = presentations[0]
    assert n_reports_expected == len(progressbar0.reports)
    assert n_threads == len(progressbar0.task_ids)
    assert n_threads == progressbar0.n_firsts
    assert n_threads == progressbar0.n_lasts

    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)


def run_with_multiprocessing(
    n_processes: int,
    n_tasks: int,
    n_iterations: list[int],
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
@pytest.mark.parametrize('n_tasks', [6, 3, 1, 0])
@pytest.mark.parametrize('n_processes', [10, 6, 2, 1])
def test_multiprocessing(
    mock_create_presentation: MockCreatePresentation,
    n_processes: int,
    n_tasks: int,
    n_iterations: list[int],
) -> None:

    # make n_iterations as long as n_tasks. repeat if necessary
    n_iterations = list(
        itertools.chain(
            *itertools.repeat(n_iterations, n_tasks // len(n_iterations) + 1)
        )
    )[:n_tasks]

    run_with_multiprocessing(n_processes, n_tasks, n_iterations)

    n_reports_expected = sum(n_iterations) + n_tasks
    presentations = mock_create_presentation.presentations

    assert 2 == len(presentations)  # created by find_reporter() and flush()

    progressbar0 = presentations[0]
    assert n_reports_expected == len(progressbar0.reports)
    assert n_tasks == len(progressbar0.task_ids)
    assert n_tasks == progressbar0.n_firsts
    assert n_tasks == progressbar0.n_lasts

    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)
