# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import time, random
import itertools
import threading
import multiprocessing

import pytest

from atpbar import atpbar
from atpbar import register_reporter, find_reporter, flush, disable

##__________________________________________________________________||
@pytest.mark.parametrize('niterations', [10, 1, 0])
def test_one_loop(mock_create_presentation, wrap_end_pickup, niterations):

    #
    disable()

    #
    for i in atpbar(range(niterations)):
        pass

    print()
    print(mock_create_presentation)

    #
    assert 0 == wrap_end_pickup.call_count

    #
    presentations = mock_create_presentation.presentations
    assert 0 == len(presentations)


##__________________________________________________________________||
def test_nested_loops(mock_create_presentation, wrap_end_pickup):

    disable()

    for i in atpbar(range(4)):
        for j in atpbar(range(3)):
            pass

    ## print()
    ## print(mock_create_presentation)

    assert 0 == wrap_end_pickup.call_count

##__________________________________________________________________||
def run_with_threading(nthreads=3, niterations=[5, 5, 5]):
    def task(n, name):
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)
    threads = [ ]
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
def test_threading(mock_create_presentation, wrap_end_pickup, nthreads, niterations):

    disable()

    # make niterations as long as nthreads. repeat if necessary
    niterations = list(itertools.chain(*itertools.repeat(niterations, nthreads//len(niterations)+1)))[:nthreads]

    run_with_threading(nthreads, niterations)

    ## print()
    ## print(mock_create_presentation)

    assert 1 == wrap_end_pickup.call_count

    presentations = mock_create_presentation.presentations
    assert 0 == len(presentations)


##__________________________________________________________________||
def run_with_multiprocessing(nprocesses, ntasks, niterations):
    def task(n, name):
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)
    def worker(reporter, task, queue):
        register_reporter(reporter)
        while True:
            args = queue.get()
            if args is None:
                queue.task_done()
                break
            task(*args)
            queue.task_done()
    reporter = find_reporter()
    queue = multiprocessing.JoinableQueue()
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
def test_multiprocessing(mock_create_presentation, wrap_end_pickup, nprocesses, ntasks, niterations):

    disable()

    # make niterations as long as ntasks. repeat if necessary
    niterations = list(itertools.chain(*itertools.repeat(niterations, ntasks//len(niterations)+1)))[:ntasks]

    run_with_multiprocessing(nprocesses, ntasks, niterations)

    ## print()
    ## print(mock_create_presentation)

    assert 1 == wrap_end_pickup.call_count

    presentations = mock_create_presentation.presentations
    assert 0 == len(presentations)

##__________________________________________________________________||
