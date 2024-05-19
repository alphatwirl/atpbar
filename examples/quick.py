#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
from random import randint
from time import sleep

from atpbar import atpbar, flushing

n = randint(5, 1000)
# n = randint(1000, 10000)
for _ in atpbar(range(n)):
    sleep(0.0001)
    # sleep(0.001)


for i in atpbar(range(4), name='Outer'):
    n = randint(5, 1000)
    # n = randint(1000, 10000)
    for _ in atpbar(range(n), name=f'Inner {i}'):
        sleep(0.0001)
        # sleep(0.001)


def func(n, name):
    for _ in atpbar(range(n), name=name):
        sleep(0.0001)
        # sleep(0.001)


n_workers = 5
n_jobs = 10

with flushing(), ThreadPoolExecutor(max_workers=n_workers) as executor:
    for i in range(n_jobs):
        n = randint(5, 1000)
        # n = randint(1000, 10000)
        f = executor.submit(func, n, name=f'Job {i}')
