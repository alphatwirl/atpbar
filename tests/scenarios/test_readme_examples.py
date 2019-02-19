# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import time, random
import threading
import multiprocessing

import pytest

from atpbar import atpbar
from atpbar import register_reporter, find_reporter, flush

##__________________________________________________________________||
def test_one_loop(mock_progressbar, wrap_end_pickup):
    for i in atpbar(range(4)):
        pass
    assert 1 == wrap_end_pickup.call_count
    assert len(mock_progressbar.present.call_args_list) >= 2

def test_nested_loops(mock_progressbar, wrap_end_pickup):
    for i in atpbar(range(4)):
        for j in atpbar(range(3)):
            pass
    assert 1 == wrap_end_pickup.call_count
    assert len(mock_progressbar.present.call_args_list) >= 2 + 2*3

##__________________________________________________________________||
def run_with_threading():
    def task(n, name):
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)
    nthreads = 3
    threads = [ ]
    for i in range(nthreads):
        name = 'thread {}'.format(i)
        n = random.randint(5, 10)
        t = threading.Thread(target=task, args=(n, name))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    flush()

def test_threading(mock_progressbar, wrap_end_pickup):
    run_with_threading()
    assert 1 == wrap_end_pickup.call_count
    assert len(mock_progressbar.present.call_args_list) >= 3*2

##__________________________________________________________________||
def run_with_multiprocessing():
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
    nprocesses = 3
    processes = [ ]
    reporter = find_reporter()
    queue = multiprocessing.JoinableQueue()
    for i in range(nprocesses):
        p = multiprocessing.Process(target=worker, args=(reporter, task, queue))
        p.start()
        processes.append(p)
    ntasks = 6
    for i in range(ntasks):
        name = 'task {}'.format(i)
        n = random.randint(5, 10)
        queue.put((n, name))
    for i in range(nprocesses):
        queue.put(None)
        queue.join()
    flush()

def test_multiprocessing(mock_progressbar, wrap_end_pickup):
    run_with_multiprocessing()
    assert 1 == wrap_end_pickup.call_count
    assert len(mock_progressbar.present.call_args_list) >= 6*2

##__________________________________________________________________||
