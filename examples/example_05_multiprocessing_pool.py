#!/usr/bin/env python

import multiprocessing
import random
import time

from atpbar import atpbar, find_reporter, flush, register_reporter


def task(n, name):
    for _ in atpbar(range(n), name=name):
        time.sleep(0.0001)


def run_with_multiprocessing_pool():

    n_processes = 4
    reporter = find_reporter()
    n_tasks = 10

    args = [(random.randint(5, 10000), 'Task {}'.format(i)) for i in range(n_tasks)]

    with multiprocessing.Pool(n_processes, register_reporter, (reporter,)) as pool:
        pool.starmap(task, args)

    flush()


run_with_multiprocessing_pool()
