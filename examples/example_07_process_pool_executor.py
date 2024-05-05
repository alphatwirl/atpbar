#!/usr/bin/env python

import multiprocessing
import random
import time
from concurrent.futures import ProcessPoolExecutor

multiprocessing.set_start_method('fork', force=True)

from atpbar import atpbar, find_reporter, flush, register_reporter


def task(n, name):
    for _ in atpbar(range(n), name=name):
        time.sleep(0.0001)


def run_with_process_pool():

    n_workers = 5
    n_tasks = 10

    reporter = find_reporter()

    with ProcessPoolExecutor(
        max_workers=n_workers, initializer=register_reporter, initargs=(reporter,)
    ) as executor:
        for i in range(n_tasks):
            name = 'Task {}'.format(i)
            n = random.randint(5, 1000)
            executor.submit(task, n, name)

    flush()


run_with_process_pool()
