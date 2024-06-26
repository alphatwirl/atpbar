#!/usr/bin/env python

from random import randint
from threading import Thread
from time import sleep

from atpbar import atpbar, flushing


def func(n, name):
    for _ in atpbar(range(n), name=name):
        sleep(0.0001)
        # sleep(0.001)


n_threads = 5

with flushing():
    threads = []
    for i in atpbar(range(n_threads)):
        n = randint(5, 1000)
        # n = randint(1000, 10000)
        t = Thread(target=func, args=(n, f'Thread {i}'))
        t.start()
        threads.append(t)
        sleep(0.01)
    for t in threads:
        t.join()
