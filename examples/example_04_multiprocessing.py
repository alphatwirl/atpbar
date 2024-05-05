#!/usr/bin/env python

import multiprocessing
import random
import time

multiprocessing.set_start_method('fork', force=True)

from atpbar import atpbar, find_reporter, flush, register_reporter


def run_with_multiprocessing():

    def task(n, name):
        for _ in atpbar(range(n), name=name):
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

    n_processes = 4
    processes = []

    reporter = find_reporter()
    queue = multiprocessing.JoinableQueue()

    for i in range(n_processes):
        p = multiprocessing.Process(target=worker, args=(reporter, task, queue))
        p.start()
        processes.append(p)

    n_tasks = 10
    for i in range(n_tasks):
        name = 'Task {}'.format(i)
        n = random.randint(5, 1000)
        queue.put((n, name))

    for i in range(n_processes):
        queue.put(None)
        queue.join()

    flush()


run_with_multiprocessing()
