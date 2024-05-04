#!/usr/bin/env python

import multiprocessing
import random
import time

multiprocessing.set_start_method("fork")

from atpbar import atpbar, find_reporter, flush, register_reporter


def task(n, name):
    for i in atpbar(range(n), name=name):
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


nprocesses = 4
processes = []

reporter = find_reporter()
queue = multiprocessing.JoinableQueue()

for i in range(nprocesses):
    p = multiprocessing.Process(target=worker, args=(reporter, task, queue))
    p.start()
    processes.append(p)


ntasks = 10
for i in range(ntasks):
    name = "task {}".format(i)
    n = random.randint(5, 10000)
    queue.put((n, name))


for i in range(nprocesses):
    queue.put(None)
queue.join()

flush()
