# Multiprocessing

`atpbar` can be used with `multiprocessing`.

The function `run_with_multiprocessing()` in the following code shows an
example.

```python
import multiprocessing
multiprocessing.set_start_method('fork', force=True)

from atpbar import register_reporter, find_reporter, flush

def run_with_multiprocessing():

    def task(n, name):
        for _ in atpbar(range(n), name=name):
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

    n_processes = 4
    processes = []

    reporter = find_reporter()
    queue = multiprocessing.JoinableQueue()

    for i in range(n_processes):
        p = multiprocessing.Process(target=worker, args=(reporter, task, queue))
        p.start()
        processes.append(p)

    n_tasks = 10
    for i in range(n_tasks):
        name = 'Task {}'.format(i)
        n = random.randint(5, 10000)
        queue.put((n, name))

    for i in range(n_processes):
        queue.put(None)
        queue.join()

    flush()


run_with_multiprocessing()
```

It starts four workers in subprocesses with `multiprocessing` and have
them run ten tasks.

In order to use `atpbar` in a subprocess, the `reporter`, which can be
found in the main process by the function `find_reporter()`, needs to
be brought to the subprocess and registered there by the function
`register_reporter()`.

Simultaneously growing progress bars will be shown.

```plaintext
 100.00% :::::::::::::::::::::::::::::::::::::::: |    44714 /    44714 |:  Task 3
 100.00% :::::::::::::::::::::::::::::::::::::::: |    47951 /    47951 |:  Task 2
 100.00% :::::::::::::::::::::::::::::::::::::::: |    21461 /    21461 |:  Task 5
 100.00% :::::::::::::::::::::::::::::::::::::::: |    73721 /    73721 |:  Task 1
 100.00% :::::::::::::::::::::::::::::::::::::::: |    31976 /    31976 |:  Task 4
 100.00% :::::::::::::::::::::::::::::::::::::::: |    80765 /    80765 |:  Task 0
  58.12% :::::::::::::::::::::::                  |    20133 /    34641 |:  Task 6
  20.47% ::::::::                                 |    16194 /    79126 |:  Task 7
  47.71% :::::::::::::::::::                      |    13072 /    27397 |:  Task 8
  76.09% ::::::::::::::::::::::::::::::           |     9266 /    12177 |:  Task 9
```
