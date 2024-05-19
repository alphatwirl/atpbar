#!/usr/bin/env python


from multiprocessing import Pool, set_start_method
from random import randint
from time import sleep

from atpbar import atpbar, find_reporter, flushing, register_reporter

set_start_method('fork', force=True)


def func(n, name):
    for _ in atpbar(range(n), name=name):
        sleep(0.0001)
        # sleep(0.001)


n_processes = 4
n_jobs = 10

args = [(randint(5, 1000), f'Job {i}') for i in range(n_jobs)]
# args = [(randint(1000, 10000), f'Job {i}') for i in range(n_jobs)]

with (
    flushing(),
    Pool(
        n_processes,
        initializer=register_reporter,
        initargs=(find_reporter(),),
    ) as pool,
):
    pool.starmap(func, args)
