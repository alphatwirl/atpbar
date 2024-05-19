#!/usr/bin/env python

import traceback
from concurrent.futures import ThreadPoolExecutor
from random import randint
from time import sleep

from atpbar import atpbar, flushing

for i in atpbar(range(2000)):
    if i == 1234:
        break
    sleep(0.0001)
    # sleep(0.001)

try:
    for i in atpbar(range(2000)):
        if i == 1234:
            raise Exception
        sleep(0.0001)
        # sleep(0.001)
except Exception:
    traceback.print_exc()
    pass


def func(n, name):
    for i in atpbar(range(n), name=name):
        if i == 1234:
            break
        sleep(0.0001)
        # sleep(0.001)


n_workers = 5
n_jobs = 10

with flushing(), ThreadPoolExecutor(max_workers=n_workers) as executor:
    for i in range(n_jobs):
        n = randint(3000, 10000)
        f = executor.submit(func, n, name=f'Job {i}')
