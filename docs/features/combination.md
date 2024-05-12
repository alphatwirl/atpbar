# Progress of starting threads and processes with progress bars

`atpbar` can be used for a loop that starts sub-threads or sub-processes in
which `atpbar` is also used.

```python
from atpbar import flush
import threading

def run_with_threading():
    def task(n, name):
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)

    n_threads = 5
    threads = []

    for i in atpbar(range(n_threads)):
        name = 'Thread {}'.format(i)
        n = random.randint(200, 1000)
        t = threading.Thread(target=task, args=(n, name))
        t.start()
        threads.append(t)
        time.sleep(0.1)

    for t in threads:
        t.join()

    flush()

run_with_threading()
```

```
 100.00% :::::::::::::::::::::::::::::::::::::::: |      209 /      209 |:  Thread 1
 100.00% :::::::::::::::::::::::::::::::::::::::: |      699 /      699 |:  Thread 0
 100.00% :::::::::::::::::::::::::::::::::::::::: |      775 /      775 |:  Thread 2
 100.00% :::::::::::::::::::::::::::::::::::::::: |      495 /      495 |:  Thread 3
 100.00% :::::::::::::::::::::::::::::::::::::::: |        5 /        5 |:  range(0, 5)
 100.00% :::::::::::::::::::::::::::::::::::::::: |      647 /      647 |:  Thread 4
```

The `atpbar` sensibly works regardless of the order in which multiple instances
of `atpbar` in multiple threads and multiple processes start and end. The
progress bars in the example above indicate that the loops in four threads
have already ended before the loop in the main threads ended; the loop in the
last thread ended afterward.
