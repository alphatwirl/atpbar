[![PyPI version](https://badge.fury.io/py/atpbar.svg)](https://badge.fury.io/py/atpbar) [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.2567283.svg)](https://doi.org/10.5281/zenodo.2567283) [![Build Status](https://travis-ci.org/alphatwirl/atpbar.svg?branch=master)](https://travis-ci.org/alphatwirl/atpbar) [![codecov](https://codecov.io/gh/alphatwirl/atpbar/branch/master/graph/badge.svg)](https://codecov.io/gh/alphatwirl/atpbar)

# atpbar

_Progress bars_ for threading and multiprocessing tasks on terminal
and Jupyter Notebook.

```
 100.00% :::::::::::::::::::::::::::::::::::::::: |     7811 /     7811 |:  task 1
 100.00% :::::::::::::::::::::::::::::::::::::::: |    23258 /    23258 |:  task 0
  65.62% ::::::::::::::::::::::::::               |     8018 /    12219 |:  task 4
  60.89% ::::::::::::::::::::::::                 |    31083 /    51048 |:  task 2
  25.03% ::::::::::                               |    23884 /    95421 |:  task 3
```
  
_atpbar_ can display multiple progress bars simultaneously growing to
show the progresses of iterations of loops in
[threading](https://docs.python.org/3/library/threading.html) or
[multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
tasks. _atpbar_ can display progress bars on terminal and [Jupyter
Notebook](https://jupyter.org/). The code in _atpbar_ started its
development in 2015 as part of
[alphatwirl](https://github.com/alphatwirl/alphatwirl). It had been a
sub-package, _progressbar_, of alphatwirl until it became an
independent package in February 2019.

*****

- [**Requirement**](#requirement)
- [**Install**](#install)
- [**How to use**](#how-to-use)
    - [Import libraries](#import-libraries)
    - [One loop](#one-loop)
    - [Nested loops](#nested-loops)
    - [Threading](#threading)
    - [Multiprocessing](#multiprocessing)
- [**License**](#license)
- [**Contact**](#contact)

*****

## Requirement

- Python 2.7, 3.6, or 3.7

*****

## Install

You can install with `pip`.

```bash
$ pip install -U atpbar
```

*****

## How to use

I will show here how to use atpbar by simple examples.

These examples can be also run on Jupyter Notebook. <br />
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/alphatwirl/notebook-atpbar-001/master?filepath=atpbar.ipynb)


### Import libraries

To create simple loops in the examples, we use two python standard
libraries, [time](https://docs.python.org/3/library/time.html) and
[random](https://docs.python.org/3/library/random.html). Import the
two packages as well as `atpbar`.

```python
import time, random
from atpbar import atpbar
```

**Note**: import the object `atpbar` from the package `atpbar` rather
than importing the package `atpbar` itself.

### One loop

The object `atpbar` is an iterable that can wrap another iterable and
shows the progress bars for the iterations. (The idea of making the
interface iterable was inspired by
[tqdm](https://github.com/tqdm/tqdm).)


```python
n = random.randint(5, 10000)
for i in atpbar(range(n)):
    time.sleep(0.0001)
```

The task in the above code is to sleep for `0.0001` seconds in each
iteration of the loop. The number of the iterations of the loop is
randomly selected from between `5` and `10000`.

A progress bar will be shown by `atpbar`.

```
  51.25% ::::::::::::::::::::                     |     4132 /     8062 |:  range(0, 8062) 
```

In order for `atpbar` to show a progress bar, the wrapped iterable
needs to have a length. If the length cannot be obtained by `len()`,
`atpbar` won't show a progress bar.

### Nested loops

`atpbar` can show progress bars for nested loops as in the following
example.

```python
for i in atpbar(range(4), name='outer'):
    n = random.randint(5, 10000)
    for j in atpbar(range(n), name='inner {}'.format(i)):
        time.sleep(0.0001)
```

The outer loop iterates 4 times. The inner loop is similar to the loop
in the previous example---sleeps for `0.0001` seconds. You can
optionally give the keyword argument `name` to specify the label on
the progress bar.

```
 100.00% :::::::::::::::::::::::::::::::::::::::: |     3287 /     3287 |:  inner 0
 100.00% :::::::::::::::::::::::::::::::::::::::: |     5850 /     5850 |:  inner 1
  50.00% ::::::::::::::::::::                     |        2 /        4 |:  outer  
  34.42% :::::::::::::                            |     1559 /     4529 |:  inner 2
```

In the snapshot of the progress bars above, the outer loop is in its
3rd iteration. The inner loop has completed twice and is running the
third. The progress bars for the completed tasks move up. The progress
bars for the active tasks are growing at the bottom.

### Threading

`atpbar` can show multiple progress bars for loops concurrently
iterating in different threads.

The function `run_with_threading()` in the following code shows an
example.

```python
from atpbar import flush
import threading

def run_with_threading():
    def task(n, name):
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)
    nthreads = 5
    threads = [ ]
    for i in range(nthreads):
        name = 'thread {}'.format(i)
        n = random.randint(5, 100000)
        t = threading.Thread(target=task, args=(n, name))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    flush()

run_with_threading()
```

The task to sleep for `0.0001` seconds is defined as the function
`task`. The `task` is concurrently run 5 times with `threading`.
`atpbar` can be used in any threads. Five progress bars growing
simultaneously will be shown. The function `flush()` returns when the
progress bars have finished updating.

```
 100.00% :::::::::::::::::::::::::::::::::::::::: |     8042 /     8042 |:  thread 3 
  33.30% :::::::::::::                            |    31967 /    95983 |:  thread 0 
  77.41% ::::::::::::::::::::::::::::::           |    32057 /    41411 |:  thread 1 
  45.78% ::::::::::::::::::                       |    31816 /    69499 |:  thread 2 
  39.93% :::::::::::::::                          |    32373 /    81077 |:  thread 4 
```

As a task completes, the progress bar for the task moves up. The
progress bars for active tasks are at the bottom.

### Multiprocessing

`atpbar` can be used with `multiprocessing`.

The function `run_with_multiprocessing()` in the following code shows
an example.

```python
import multiprocessing
from atpbar import register_reporter, find_reporter, flush

def run_with_multiprocessing():
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
    processes = [ ]
    reporter = find_reporter()
    queue = multiprocessing.JoinableQueue()
    for i in range(nprocesses):
        p = multiprocessing.Process(target=worker, args=(reporter, task, queue))
        p.start()
        processes.append(p)
    ntasks = 10
    for i in range(ntasks):
        name = 'task {}'.format(i)
        n = random.randint(5, 100000)
        queue.put((n, name))
    for i in range(nprocesses):
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

```
 100.00% :::::::::::::::::::::::::::::::::::::::: |    44714 /    44714 |:  task 3
 100.00% :::::::::::::::::::::::::::::::::::::::: |    47951 /    47951 |:  task 2
 100.00% :::::::::::::::::::::::::::::::::::::::: |    21461 /    21461 |:  task 5
 100.00% :::::::::::::::::::::::::::::::::::::::: |    73721 /    73721 |:  task 1
 100.00% :::::::::::::::::::::::::::::::::::::::: |    31976 /    31976 |:  task 4
 100.00% :::::::::::::::::::::::::::::::::::::::: |    80765 /    80765 |:  task 0
  58.12% :::::::::::::::::::::::                  |    20133 /    34641 |:  task 6
  20.47% ::::::::                                 |    16194 /    79126 |:  task 7
  47.71% :::::::::::::::::::                      |    13072 /    27397 |:  task 8
  76.09% ::::::::::::::::::::::::::::::           |     9266 /    12177 |:  task 9
```

*****

## License

- atpbar is licensed under the BSD license.

*****

## Contact

- Tai Sakuma - tai.sakuma@gmail.com

