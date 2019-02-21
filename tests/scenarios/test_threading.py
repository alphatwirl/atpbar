# Tai Sakuma <tai.sakuma@gmail.com>
import time, random
import threading

import pytest

from atpbar import atpbar
from atpbar import flush

##__________________________________________________________________||
def test_threading_from_loop(mock_progressbar, wrap_end_pickup):

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

        time.sleep(0.01)
        # sleep sometime so this loop doesn't end too quickly. If
        # the loop ends before `atpbar()` is called in any of the
        # threads, `_end_pickup()` will be called twice and the
        # test fails.

    for t in threads:
        t.join()

    flush()

    assert 1 == wrap_end_pickup.call_count

    assert len(mock_progressbar.present.call_args_list) >= 3*2

    for i in atpbar(range(4)):
        pass
    assert 2 == wrap_end_pickup.call_count

##__________________________________________________________________||
