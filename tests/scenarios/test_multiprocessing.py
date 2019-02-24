# Tai Sakuma <tai.sakuma@gmail.com>
import time, random
import itertools
import multiprocessing

import pytest

from atpbar import atpbar
from atpbar import register_reporter, find_reporter, flush

##__________________________________________________________________||
def run_with_multiprocessing(nprocesses, ntasks, niterations, time_starting_task):

    def task(n, name, time_starting):
        time.sleep(time_starting)
        for i in atpbar(range(n), name=name):  # `atpbar` is used here
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

    for i in atpbar(range(ntasks)): # `atpbar` is used here
        name = 'task {}'.format(i)
        n = niterations[i]
        queue.put((n, name, time_starting_task))
        time.sleep(0.01)

    for i in range(nprocesses):
        queue.put(None)
        queue.join()

    flush()

@pytest.mark.xfail()
@pytest.mark.parametrize('time_starting_task', [0, 0.01, 0.2])
@pytest.mark.parametrize('niterations', [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize('ntasks', [3, 1, 0])
@pytest.mark.parametrize('nprocesses', [6, 2, 1])
def test_multiprocessing_from_loop(
        mock_create_presentation, wrap_end_pickup,
        nprocesses, ntasks, niterations, time_starting_task):

    # make niterations as long as ntasks. repeat if necessary
    niterations = list(itertools.chain(*itertools.repeat(niterations, ntasks//len(niterations)+1)))[:ntasks]

    run_with_multiprocessing(nprocesses, ntasks, niterations, time_starting_task)

    ## print()
    ## print(mock_create_presentation)

    nreports_expected_from_main = ntasks + 1
    nreports_expected_from_tasks = sum(niterations) + ntasks
    nreports_expected = nreports_expected_from_main + nreports_expected_from_tasks

    presentations = mock_create_presentation.presentations

    if nreports_expected_from_tasks == 0:
        assert 3 == len(presentations) # in find_reporter(), at the
                                       # end of `atpbar` in the main
                                       # process, and in flush().

        progressbar0 = presentations[0]
        assert nreports_expected == len(progressbar0.reports)
        # one report from `atpbar` in the main thread

        assert 1 == progressbar0.nfirsts
        assert 1 == progressbar0.nlasts
        assert 1 == len(progressbar0.taskids)

    else:
        if 2 == len(presentations):

            progressbar1 = presentations[1]
            assert 0 == len(progressbar1.reports)

            progressbar0 = presentations[0]
            assert ntasks + 1 == len(progressbar0.taskids)
            assert ntasks + 1 == progressbar0.nfirsts
            assert ntasks + 1 == progressbar0.nlasts
            assert nreports_expected == len(progressbar0.reports)

        else:
            assert 3 == len(presentations)

            progressbar2 = presentations[2]
            assert 0 == len(progressbar2.reports)

            progressbar0 = presentations[0]
            progressbar1 = presentations[1]

            assert ntasks + 1 == len(progressbar0.taskids) + len(progressbar1.taskids)
            assert ntasks + 1 == progressbar0.nfirsts + progressbar1.nfirsts
            assert ntasks + 1 == progressbar0.nlasts + progressbar1.nlasts
            assert nreports_expected == len(progressbar0.reports) + len(progressbar1.reports)

    # At this point the pickup shouldn't be owned. Therefore, a new
    # `atpbar` in the main thread should own it.
    npresentations = len(presentations)
    for i in atpbar(range(4)):
        pass
    assert npresentations + 1 == len(presentations)
    progressbar = presentations[-2]
    assert 1 == len(progressbar.taskids)
    assert 1 == progressbar.nfirsts
    assert 1 == progressbar.nlasts
    assert 4 + 1 == len(progressbar.reports)

##__________________________________________________________________||
