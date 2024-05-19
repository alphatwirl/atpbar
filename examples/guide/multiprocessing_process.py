#!/usr/bin/env python

from multiprocessing import Process, set_start_method
from random import randint
from time import sleep

from atpbar import atpbar, find_reporter, flushing, register_reporter

set_start_method('fork', force=True)


def func(n, name, reporter):
    register_reporter(reporter)
    for _ in atpbar(range(n), name=name):
        sleep(0.0001)
        # sleep(0.001)


n_processes = 5

with flushing():
    processes = []
    for i in range(n_processes):
        n = randint(5, 1000)
        # n = randint(1000, 10000)
        p = Process(target=func, args=(n, f'Job {i}', find_reporter()))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
