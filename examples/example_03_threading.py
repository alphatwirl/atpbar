#!/usr/bin/env python

import time, random
import threading

from atpbar import atpbar, flush

##__________________________________________________________________||
def task(n, name):
    for i in atpbar(range(n), name=name):
        time.sleep(0.0001)

##__________________________________________________________________||
nthreads = 5
threads = [ ]

for i in range(nthreads):
    name = 'thread {}'.format(i)
    n = random.randint(5, 10000)
    t = threading.Thread(target=task, args=(n, name))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

flush()

##__________________________________________________________________||
