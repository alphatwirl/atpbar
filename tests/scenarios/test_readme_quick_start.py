# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import time, random
import itertools
import threading
import multiprocessing

import pytest

from atpbar import atpbar
from atpbar import register_reporter, find_reporter, flush

##__________________________________________________________________||
@pytest.mark.parametrize('niterations', [10, 1, 0])
def test_one_loop(mock_create_presentation, wrap_end_pickup, niterations):

    #
    for i in atpbar(range(niterations)):
        pass

    ## print()
    ## print(mock_create_presentation)

    #
    assert 1 == wrap_end_pickup.call_count

    nreports_expected = niterations + 1
    presentations = mock_create_presentation.presentations

    #
    assert 2 == len(presentations) # created when atpbar started and ended

    progressbar0 = presentations[0]
    assert nreports_expected == len(progressbar0.reports)
    assert 1 == len(progressbar0.taskids)
    assert 1 == progressbar0.nfirsts
    assert 1 == progressbar0.nlasts

    #
    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)

##__________________________________________________________________||
def test_nested_loops(mock_create_presentation, wrap_end_pickup):
    for i in atpbar(range(4)):
        for j in atpbar(range(3)):
            pass

    ## print()
    ## print(mock_create_presentation)

    assert 1 == wrap_end_pickup.call_count

    presentations = mock_create_presentation.presentations
    assert 2 == len(presentations)

    progressbar0 = presentations[0]
    assert (3+1)*4 + 4+1 == len(progressbar0.reports)
    assert 5 == len(progressbar0.taskids)
    assert 5 == progressbar0.nfirsts
    assert 5 == progressbar0.nlasts

    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)

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

    # make niterations as long as nthreads. repeat if necessary
    niterations = list(itertools.chain(*itertools.repeat(niterations, nthreads//len(niterations)+1)))[:nthreads]

    run_with_threading(nthreads, niterations)

    ## print()
    ## print(mock_create_presentation)

    assert 1 == wrap_end_pickup.call_count

    nreports_expected = sum(niterations) + nthreads
    presentations = mock_create_presentation.presentations

    if nreports_expected == 0:
        assert 1 == len(presentations) # created by flush()
        assert 0 == len(presentations[0].reports)
        return

    assert 2 == len(presentations)

    progressbar0 = presentations[0]
    assert nreports_expected == len(progressbar0.reports)
    assert nthreads == len(progressbar0.taskids)
    assert nthreads == progressbar0.nfirsts
    assert nthreads == progressbar0.nlasts

    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)

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
@pytest.mark.parametrize('ntasks', [6, 3, 1, 0])
@pytest.mark.parametrize('nprocesses', [10, 6, 2, 1])
def test_multiprocessing(mock_create_presentation, wrap_end_pickup, nprocesses, ntasks, niterations):

    # make niterations as long as ntasks. repeat if necessary
    niterations = list(itertools.chain(*itertools.repeat(niterations, ntasks//len(niterations)+1)))[:ntasks]

    run_with_multiprocessing(nprocesses, ntasks, niterations)

    ## print()
    ## print(mock_create_presentation)

    assert 1 == wrap_end_pickup.call_count

    nreports_expected = sum(niterations) + ntasks
    presentations = mock_create_presentation.presentations

    assert 2 == len(presentations) # created by find_reporter() and flush()

    progressbar0 = presentations[0]
    assert nreports_expected == len(progressbar0.reports)
    assert ntasks == len(progressbar0.taskids)
    assert ntasks == progressbar0.nfirsts
    assert ntasks == progressbar0.nlasts

    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)

##__________________________________________________________________||
