# Quick Start

I will show you how to use the atpbar using simple examples.

#### Import libraries

To create simple loops in the examples, we use two Python standard
libraries, [time](https://docs.python.org/3/library/time.html) and
[random](https://docs.python.org/3/library/random.html). Import the
two packages as well as `atpbar`.

```python
import time, random
from atpbar import atpbar
```

#### One loop

The object `atpbar` is an iterable that can wrap another iterable and shows the
progress bars for the iterations. (The idea of making the interface iterable
was inspired by [tqdm](https://github.com/tqdm/tqdm).)

```python
n = random.randint(1000, 10000)
for i in atpbar(range(n)):
    time.sleep(0.0001)
```

The task in the above code is to sleep for `0.0001` seconds in each iteration
of the loop. The number of the iterations of the loop is randomly selected from
between `1000` and `10000`.

A progress bar will be shown by `atpbar`.

```plaintext
  51.25% ::::::::::::::::::::                     |     4132 /     8062 |:  range(0, 8062)
```

In order for `atpbar` to show a progress bar, the wrapped iterable needs to
have a length. If the length cannot be obtained by `len()`, `atpbar` won't show
a progress bar.

#### Nested loops

`atpbar` can show progress bars for nested loops as in the following example.

```python
for i in atpbar(range(4), name='Outer'):
    n = random.randint(1000, 10000)
    for j in atpbar(range(n), name='Inner {}'.format(i)):
        time.sleep(0.0001)
```

The outer loop iterates 4 times. The inner loop is similar to the loop
in the previous example---sleeps for `0.0001` seconds. You can
optionally give the keyword argument `name` to specify the label on
the progress bar.

```plaintext
 100.00% :::::::::::::::::::::::::::::::::::::::: |     3287 /     3287 |:  Inner 0
 100.00% :::::::::::::::::::::::::::::::::::::::: |     5850 /     5850 |:  Inner 1
  50.00% ::::::::::::::::::::                     |        2 /        4 |:  Outer
  34.42% :::::::::::::                            |     1559 /     4529 |:  Inner 2
```

In the snapshot of the progress bars above, the outer loop is in its 3rd
iteration. The inner loop has been completed twice and is running the third.
The progress bars for the completed tasks move up. The progress bars for the
active tasks are growing at the bottom.

#### Threading

`atpbar` can show multiple progress bars for loops concurrently iterating in
different threads.

The function `run_with_threading()` in the following code shows an
example.

```python
from atpbar import flush
import threading

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
```

The task to sleep for `0.0001` seconds is defined as the function `task`. The
`task` is concurrently run five times with `threading`. `atpbar` can be used in
any thread. Five progress bars growing simultaneously will be shown. The
function `flush()` returns when the progress bars have finished updating.

```plaintext
 100.00% :::::::::::::::::::::::::::::::::::::::: |     8042 /     8042 |:  Thread 3
  33.30% :::::::::::::                            |    31967 /    95983 |:  Thread 0
  77.41% ::::::::::::::::::::::::::::::           |    32057 /    41411 |:  Thread 1
  45.78% ::::::::::::::::::                       |    31816 /    69499 |:  Thread 2
  39.93% :::::::::::::::                          |    32373 /    81077 |:  Thread 4
```

As a task completes, the progress bar for the task moves up. The
progress bars for active tasks are at the bottom.

#### Multiprocessing

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

#### Multiprocessing.Pool

To use `atpbar` with
[`multiprocessing.Pool`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool),
use `find_reporter` as the initializer and give the `reporter` as an argument
to the initializer.

```python
def task(n, name):
    for _ in atpbar(range(n), name=name):
        time.sleep(0.0001)


def run_with_multiprocessing_pool():

    n_processes = 4
    reporter = find_reporter()
    n_tasks = 10

    args = [(random.randint(5, 10000), 'Task {}'.format(i)) for i in range(n_tasks)]

    with multiprocessing.Pool(n_processes, register_reporter, (reporter,)) as pool:
        pool.starmap(task, args)

    flush()


run_with_multiprocessing_pool()
```

#### ThreadPoolExecutor

An example with [`concurrent.futures.ThreadPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor):

```python
def task(n, name):
    for _ in atpbar(range(n), name=name):
        time.sleep(0.0001)


def run_with_thread_pool():

    n_workers = 5
    n_tasks = 10

    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        for i in range(n_tasks):
            name = 'Task {}'.format(i)
            n = random.randint(5, 1000)
            executor.submit(task, n, name)

    flush()


run_with_thread_pool()
```

#### ProcessPoolExecutor

An example with [`concurrent.futures.ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor):

```python
def task(n, name):
    for _ in atpbar(range(n), name=name):
        time.sleep(0.0001)


def run_with_process_pool():

    n_workers = 5
    n_tasks = 10

    reporter = find_reporter()

    with ProcessPoolExecutor(
        max_workers=n_workers, initializer=register_reporter, initargs=(reporter,)
    ) as executor:
        for i in range(n_tasks):
            name = 'Task {}'.format(i)
            n = random.randint(5, 1000)
            executor.submit(task, n, name)

    flush()


run_with_process_pool()
```
