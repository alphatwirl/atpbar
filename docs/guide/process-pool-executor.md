# ProcessPoolExecutor

An example with [`concurrent.futures.ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor):

```python
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from random import randint
from time import sleep

from atpbar import atpbar, find_reporter, flushing, register_reporter

multiprocessing.set_start_method('fork', force=True)


def func(n, name):
    for _ in atpbar(range(n), name=name):
        sleep(0.001)


n_workers = 5
n_jobs = 10

with (
    flushing(),
    ProcessPoolExecutor(
        max_workers=n_workers,
        initializer=register_reporter,
        initargs=(find_reporter(),),
    ) as executor,
):
    for i in range(n_jobs):
        n = randint(1000, 10000)
        f = executor.submit(func, n, name=f'Job {i}')
```
