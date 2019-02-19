# Tai Sakuma <tai.sakuma@gmail.com>
import time, random
import threading

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

##__________________________________________________________________||
def test_launching_threads_in_monitored_loop(mock_progressbar, wrap_end_pickup):
    def run_with_threading():
        def task(n, name):
            for i in atpbar(range(n), name=name):
                time.sleep(0.0001)
        nthreads = 3
        threads = [ ]
        for i in atpbar(range(nthreads)):
            name = 'thread {}'.format(i)
            n = random.randint(5, 10)
            t = threading.Thread(target=task, args=(n, name))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        flush()

    run_with_threading()
    assert 1 == wrap_end_pickup.call_count
    assert len(mock_progressbar.present.call_args_list) >= 3*2

##__________________________________________________________________||
