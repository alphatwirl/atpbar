#!/usr/bin/env python

import random
import time
from concurrent.futures import ThreadPoolExecutor

from atpbar import atpbar, flush


def task(n, name):
    for _ in atpbar(range(n), name=name):
        time.sleep(0.0001)


def run_with_thread_pool():

    n_workers = 5
    n_tasks = 10

    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        for i in range(n_tasks):
            name = 'Task {}'.format(i)
            n = random.randint(5, 1000)
            executor.submit(task, n, name)

    flush()


run_with_thread_pool()
