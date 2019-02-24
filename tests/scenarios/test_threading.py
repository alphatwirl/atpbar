# Tai Sakuma <tai.sakuma@gmail.com>
import time, random
import itertools
import threading

import pytest

from atpbar import atpbar
from atpbar import flush

##__________________________________________________________________||
@pytest.mark.parametrize('time_starting_task', [0, 0.01, 0.2])
@pytest.mark.parametrize('niterations', [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize('nthreads', [3, 1, 0])
def test_threading_from_loop(mock_create_presentation, wrap_end_pickup, nthreads, niterations, time_starting_task):

    # make niterations as long as nthreads. repeat if necessary
    niterations = list(itertools.chain(*itertools.repeat(niterations, nthreads//len(niterations)+1)))[:nthreads]

    def run_with_threading(nthreads=3, niterations=[5, 5, 5], time_starting_task=0):

        def task(n, name, time_starting):
            time.sleep(time_starting) # When starting time is long, the loop in
                                      # the main thread might already end by the
                                      # time the loop in this task starts.
            for i in atpbar(range(n), name=name):
                time.sleep(0.0001)

        threads = [ ]
        for i in atpbar(range(nthreads)): # `atpbar` is used here while `atpbar`
                                          # is also used in threads being
                                          # launched in this loop. If none of
                                          # the `atpbar`s in threads has started
                                          # by the end of this loop, the
                                          # `atpbar` for this loop waits until
                                          # the progress bar for this loop
                                          # finish updating. Otherwise, progress
                                          # bars from threads are being updated
                                          # together with the progress bar for
                                          # this loop and the `atpbar` will not
                                          # wait.

            name = 'thread {}'.format(i)
            n = niterations[i]
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

    run_with_threading(nthreads, niterations, time_starting_task)

    ## print()
    ## print(mock_create_presentation)

    ## assert 1 == wrap_end_pickup.call_count # 1 or 2 depending on how quickly the loop ends

    nreports_expected_from_main = nthreads + 1
    nreports_expected_from_threads = sum(niterations) + nthreads
    nreports_expected = nreports_expected_from_main + nreports_expected_from_threads

    presentations = mock_create_presentation.presentations

    if nreports_expected_from_threads == 0:
        assert 3 == len(presentations) # when `atpbar` in the main thread
                                       # starts and end and when flush() is
                                       # called

        progressbar0 = presentations[0]
        assert nreports_expected == len(progressbar0.reports)
        # one report from `atpbar` in the main thread

        assert 1 == len(progressbar0.taskids)
        assert 1 == progressbar0.nfirsts
        assert 1 == progressbar0.nlasts

    else:

        if 2 == len(presentations):

            progressbar0 = presentations[0]
            assert nreports_expected == len(progressbar0.reports)
            assert nthreads + 1 == len(progressbar0.taskids)
            assert nthreads + 1 == progressbar0.nfirsts
            assert nthreads + 1 == progressbar0.nlasts

            progressbar1 = presentations[1]
            assert 0 == len(progressbar1.reports)

        else:
            assert 3 == len(presentations)

            progressbar0 = presentations[0]
            progressbar1 = presentations[1]

            assert nreports_expected == len(progressbar0.reports) + len(progressbar1.reports)
            assert nthreads + 1 == len(progressbar0.taskids) + len(progressbar1.taskids)
            assert nthreads + 1 == progressbar0.nfirsts + progressbar1.nfirsts
            assert nthreads + 1 == progressbar0.nlasts + progressbar1.nlasts

            progressbar2 = presentations[2]
            assert 0 == len(progressbar2.reports)

    # At this point the pickup shouldn't be owned. Therefore, a new
    # `atpbar` in the main thread should own it.
    npresentations = len(presentations)
    for i in atpbar(range(4)):
        pass
    assert npresentations + 1 == len(presentations)
    progressbar = presentations[-2]
    assert 4 + 1 == len(progressbar.reports)
    assert 1 == len(progressbar.taskids)
    assert 1 == progressbar.nfirsts
    assert 1 == progressbar.nlasts

##__________________________________________________________________||
