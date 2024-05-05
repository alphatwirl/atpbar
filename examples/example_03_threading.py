#!/usr/bin/env python

import random
import threading
import time

from atpbar import atpbar, flush


def run_with_threading():
    def task(n, name):
        for _ in atpbar(range(n), name=name):
            time.sleep(0.0001)

    n_threads = 5
    threads = []

    for i in range(n_threads):
        name = 'Thread {}'.format(i)
        n = random.randint(5, 10000)
        t = threading.Thread(target=task, args=(n, name))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    flush()


run_with_threading()
