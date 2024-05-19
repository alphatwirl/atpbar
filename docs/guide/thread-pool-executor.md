# ThreadPoolExecutor

An example with
[`concurrent.futures.ThreadPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor):

```python
from concurrent.futures import ThreadPoolExecutor
from random import randint
from time import sleep

from atpbar import atpbar, flushing


def func(n, name):
    for _ in atpbar(range(n), name=name):
        sleep(0.001)


n_workers = 5
n_jobs = 10

with flushing(), ThreadPoolExecutor(max_workers=n_workers) as executor:
    for i in range(n_jobs):
        n = randint(1000, 10000)
        f = executor.submit(func, n, name=f'Job {i}')

```
