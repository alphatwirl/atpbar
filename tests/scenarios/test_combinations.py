# Tai Sakuma <tai.sakuma@gmail.com>
import time, random
import threading

import pytest

from atpbar import atpbar
from atpbar import register_reporter, find_reporter, flush

##__________________________________________________________________||
def test_one_loop_break(mock_progressbar, wrap_end_pickup):
    for i in atpbar(range(4)):
        if i == 2:
            break
    assert 1 == wrap_end_pickup.call_count

    # assert len(mock_progressbar.present.call_args_list) >= 2
    # FIXME: when the loop breaks, the progress bar should be updated
    # with the last complete loop

def test_one_loop_raise(mock_progressbar, wrap_end_pickup):
    with pytest.raises(Exception):
        for i in atpbar(range(4)):
            if i == 2:
                raise Exception()
    assert 1 == wrap_end_pickup.call_count
    # assert len(mock_progressbar.present.call_args_list) >= 2


##__________________________________________________________________||
def test_launching_threads_in_monitored_loop(mock_progressbar, wrap_end_pickup):
    def run_with_threading():

        def task(n, name):
            for i in atpbar(range(n), name=name):
                time.sleep(0.0001)

        nthreads = 3
        threads = [ ]

        for i in atpbar(range(nthreads)):
            # `atpbar` is used to show a progress bar for the progress
            # of launching threads in which `atpbar` is also used.
            # This loop should ends without waiting for all progress
            # bars to finish updating.

            name = 'thread {}'.format(i)
            n = random.randint(5, 10)
            t = threading.Thread(target=task, args=(n, name))
            t.start()
            threads.append(t)

            time.sleep(0.0001)
            # sleep sometime so this loop doesn't end too quickly. If
            # the loop ends before `atpbar()` is called in any of the
            # threads, `_end_pickup()` will be called twice and the
            # test fails.

        for t in threads:
            t.join()

        flush()

    run_with_threading()

    assert 1 == wrap_end_pickup.call_count

    assert len(mock_progressbar.present.call_args_list) >= 3*2

    for i in atpbar(range(4)):
        pass
    assert 2 == wrap_end_pickup.call_count

##__________________________________________________________________||
