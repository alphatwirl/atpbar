#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
import time, random
import multiprocessing

from atpbar import atpbar, register_reporter, find_reporter

##__________________________________________________________________||
def task(n, name, reporter):
    register_reporter(reporter)
    for i in atpbar(range(n), name=name):
        time.sleep(0.0001)

##__________________________________________________________________||
reporter = find_reporter()

##__________________________________________________________________||
nprocesses = 5
processes = [ ]

for i in range(nprocesses):
    name = 'process {}'.format(i)
    n = random.randint(5, 100000)
    p = multiprocessing.Process(target=task, args=(n, name, reporter))
    p.start()
    processes.append(p)

for p in processes:
    p.join()

##__________________________________________________________________||
