[![PyPI version](https://badge.fury.io/py/atpbar.svg)](https://badge.fury.io/py/atpbar) [![DOI](https://zenodo.org/badge/171072963.svg)](https://zenodo.org/badge/latestdoi/171072963) [![Build Status](https://travis-ci.org/alphatwirl/atpbar.svg?branch=master)](https://travis-ci.org/alphatwirl/atpbar) [![codecov](https://codecov.io/gh/alphatwirl/atpbar/branch/master/graph/badge.svg)](https://codecov.io/gh/alphatwirl/atpbar)

# atpbar

Progress bars for threading and multiprocessing tasks on terminal and
Jupyter Notebook.

The code in _atpbar_ started its development in 2015 as part of
[alphatwirl](https://github.com/alphatwirl/alphatwirl). It has been a
sub-package, _progressbar_, of alphatwirl. It became an independent
package in February 2019. _atpbar_ can display multiple progress bars
simultaneously growing to show the progresses of iterations of loops
in [threading](https://docs.python.org/3/library/threading.html) or
[multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
tasks. _atpbar_ can display progress bars on terminal and [Jupyter
Notebook](https://jupyter.org/).

*****

## Requirement

- Python 2.7, 3.6, 3.7

*****

## Install

You can install with `pip`.

```bash
$ pip install -U atpbar
```

*****

## How to use

I will show here how to use atpbar by simple examples.

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


```python
import threading

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
```

The task to sleep for `0.0001` seconds is defined as the function
`task`. The `task` is concurrently run 5 times with `threading`.
`atpbar` can be used in any threads. Five progress bars growing
simultaneously will be shown.

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

`atpbar` can be used with `multiprocessing`. A few extra lines of code
need to be added.

```python
import multiprocessing
from atpbar import register_reporter, find_reporter

def task(n, name, reporter):
    register_reporter(reporter)
    for i in atpbar(range(n), name=name):
        time.sleep(0.0001)

reporter = find_reporter()

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
```

In order to use `atpbar` in a subprocess, the `reporter`, which can be
found in the main process by the function `find_reporter()`, needs to
be brought to the subprocess and registered there by the function
`register_reporter()`.

Simultaneously growing progress bars will be shown.

```
 100.00% :::::::::::::::::::::::::::::::::::::::: |    13110 /    13110 |:  process 1 
  61.88% ::::::::::::::::::::::::                 |    17957 /    29020 |:  process 0 
  19.37% :::::::                                  |    17982 /    92831 |:  process 2 
  21.49% ::::::::                                 |    17178 /    79939 |:  process 3 
  80.11% ::::::::::::::::::::::::::::::::         |    17187 /    21453 |:  process 4 
```

*****

## License

atpbar is licensed under the BSD license.

*****

## Contact

- Tai Sakuma - tai.sakuma@gmail.com

