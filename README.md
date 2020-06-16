[![PyPI version](https://badge.fury.io/py/atpbar.svg)](https://badge.fury.io/py/atpbar) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/atpbar/badges/version.svg)](https://anaconda.org/conda-forge/atpbar) [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.2567283.svg)](https://doi.org/10.5281/zenodo.2567283) [![Build Status](https://travis-ci.org/alphatwirl/atpbar.svg?branch=master)](https://travis-ci.org/alphatwirl/atpbar) [![codecov](https://codecov.io/gh/alphatwirl/atpbar/branch/master/graph/badge.svg)](https://codecov.io/gh/alphatwirl/atpbar)

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
Notebook](https://jupyter.org/). _atpbar_ can be used with
[_Mantichora_](https://github.com/alphatwirl/mantichora).

_atpbar_ started its development in 2015 as part of
[_alphatwirl_](https://github.com/alphatwirl/alphatwirl). _atpbar_
prevented physicists from terminating their running analysis codes,
which would take many hours to complete, by showing progress bars
indicating their codes were actually running. The progress bars have
saved the physicists countless hours total. _atpbar_ had been the
sub-package
[_progressbar_](https://github.com/alphatwirl/alphatwirl/tree/v0.22.0/alphatwirl/progressbar)
of alphatwirl until it became an independent package, with the name
_atpbar_, in February 2019.


You can try it on Jupyter Notebook online: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/alphatwirl/notebook-atpbar-001/master?filepath=atpbar.ipynb)

*****

- [**Requirement**](#requirement)
- [**Install**](#install)
- [**User guide**](#user-guide)
    - [**Quick start**](#quick-start)
        - [Import libraries](#import-libraries)
        - [One loop](#one-loop)
        - [Nested loops](#nested-loops)
        - [Threading](#threading)
        - [Multiprocessing](#multiprocessing)
        - [With Mantichora](#with-mantichora)
    - [**Features**](#features)
        - [A `break` and an exception](#a-break-and-an-exception)
        - [Progress of starting threads and processes with progress bars](#progress-of-starting-threads-and-processes-with-progress-bars)
        - [On Jupyter Notebook](#on-jupyter-notebook)
        - [Non TTY device](#non-tty-device)
        - [How to disable progress bars](#how-to-disable-progress-bars)
- [**License**](#license)
- [**Contact**](#contact)

*****

## Requirement

- Python 3.6, 3.7, or 3.8

*****

## Install

You can install with `conda` from conda-forge:

```bash
conda install -c conda-forge atpbar
```

or with `pip`:

```bash
pip install -U atpbar
```

*****

## User guide

### Quick start

I will show here how to use atpbar by simple examples.

#### Import libraries

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

#### One loop

The object `atpbar` is an iterable that can wrap another iterable and
shows the progress bars for the iterations. (The idea of making the
interface iterable was inspired by
[tqdm](https://github.com/tqdm/tqdm).)


```python
n = random.randint(1000, 10000)
for i in atpbar(range(n)):
    time.sleep(0.0001)
```

The task in the above code is to sleep for `0.0001` seconds in each
iteration of the loop. The number of the iterations of the loop is
randomly selected from between `1000` and `10000`.

A progress bar will be shown by `atpbar`.

```
  51.25% ::::::::::::::::::::                     |     4132 /     8062 |:  range(0, 8062) 
```

In order for `atpbar` to show a progress bar, the wrapped iterable
needs to have a length. If the length cannot be obtained by `len()`,
`atpbar` won't show a progress bar.

#### Nested loops

`atpbar` can show progress bars for nested loops as in the following
example.

```python
for i in atpbar(range(4), name='outer'):
    n = random.randint(1000, 10000)
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

#### Threading

`atpbar` can show multiple progress bars for loops concurrently
iterating in different threads.

The function `run_with_threading()` in the following code shows an
example.

```python
from atpbar import flush
import threading

def run_with_threading():
    nthreads = 5
    def task(n, name):
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)
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

#### Multiprocessing

`atpbar` can be used with `multiprocessing`.

The function `run_with_multiprocessing()` in the following code shows
an example.

```python
import multiprocessing
multiprocessing.set_start_method('fork', force=True)

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
    ntasks = 10
    reporter = find_reporter()
    queue = multiprocessing.JoinableQueue()
    for i in range(nprocesses):
        p = multiprocessing.Process(target=worker, args=(reporter, task, queue))
        p.start()
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

#### With Mantichora

[_Mantichora_](https://github.com/alphatwirl/mantichora) provides a
simple interface to _multiprocessing_ and _threading_.

With Mantichora, `task()` can be concurrently run with multiprocessing or threading with as simple code as the following example:

```python
from mantichora import mantichora

def task(name):
    n = random.randint(1000, 10000)
    for i in atpbar(range(n), name=name):
        time.sleep(0.0001)

with mantichora() as mcore:
    mcore.run(task, 'task 1')
    mcore.run(task, 'task 2')
    mcore.run(task, 'task 3')
    mcore.run(task, 'task 4')
    mcore.run(task, 'task 5')
    returns = mcore.returns()
```

This example uses multiprocessing. To use threading, set the option `mode` to `threading` (the default is
`multiprocessing`), i.e., `mantichora(mode='threading')`

`atpbar` can be used in the task function.

```
 100.00% :::::::::::::::::::::::::::::::::::::::: |     2288 /     2288 |:  task 3
 100.00% :::::::::::::::::::::::::::::::::::::::: |     3964 /     3964 |:  task 4
 100.00% :::::::::::::::::::::::::::::::::::::::: |     4207 /     4207 |:  task 2
 100.00% :::::::::::::::::::::::::::::::::::::::: |     8519 /     8519 |:  task 1
 100.00% :::::::::::::::::::::::::::::::::::::::: |     6595 /     6595 |:  task 5
```

*****

### Features

#### A `break` and an exception

When the loop ends with a `break` or an exception, the progress bar stops with
the last complete iteration.

For example, the loop in the following code breaks during the 1235th iteration.
```python
for i in atpbar(range(2000)):
    if i == 1234:
        break
    time.sleep(0.0001)
```

Since `i` starts with `0`, when `i` is `1234`, the loop is in its 1235th
iteration. The last complete iteration is 1234. The progress bar stops at 1234.

```
  61.70% ::::::::::::::::::::::::                 |     1234 /     2000 |:  range(0, 2000)
```

As an example of an exception, in the following code, an exception is
thrown during the 1235th iteration.
```python
for i in atpbar(range(2000)):
    if i == 1234:
        raise Exception
    time.sleep(0.0001)
```
The progress bar stops at the last complete iteration, 1234.

```
  61.70% ::::::::::::::::::::::::                 |     1234 /     2000 |:  range(0, 2000)
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
Exception
```

This feature works as well with nested loops, threading, and
multiprocessing. For example, in the following code, the loops in five
threads break at 1235th iteration.

```python
from atpbar import flush
import threading

def run_with_threading():
    def task(n, name):
        for i in atpbar(range(n), name=name):
            if i == 1234:
                break
            time.sleep(0.0001)
    nthreads = 5
    threads = [ ]
    for i in range(nthreads):
        name = 'thread {}'.format(i)
        n = random.randint(3000, 10000)
        t = threading.Thread(target=task, args=(n, name))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    flush()

run_with_threading()
```

All progress bars stop at 1234.

```
  18.21% :::::::                                  |     1234 /     6777 |:  thread 0
  15.08% ::::::                                   |     1234 /     8183 |:  thread 2
  15.25% ::::::                                   |     1234 /     8092 |:  thread 1
  39.90% :::::::::::::::                          |     1234 /     3093 |:  thread 4
  19.67% :::::::                                  |     1234 /     6274 |:  thread 3
```

#### Progress of starting threads and processes with progress bars

`atpbar` can be used for a loop that starts sub-threads or
sub-processes in which `atpbar` is also used.

```python
from atpbar import flush
import threading

def run_with_threading():
    def task(n, name):
        for i in atpbar(range(n), name=name):
            time.sleep(0.0001)
    nthreads = 5
    threads = [ ]
    for i in atpbar(range(nthreads)):
        name = 'thread {}'.format(i)
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
 100.00% :::::::::::::::::::::::::::::::::::::::: |      209 /      209 |:  thread 1
 100.00% :::::::::::::::::::::::::::::::::::::::: |      699 /      699 |:  thread 0
 100.00% :::::::::::::::::::::::::::::::::::::::: |      775 /      775 |:  thread 2
 100.00% :::::::::::::::::::::::::::::::::::::::: |      495 /      495 |:  thread 3
 100.00% :::::::::::::::::::::::::::::::::::::::: |        5 /        5 |:  range(0, 5)
 100.00% :::::::::::::::::::::::::::::::::::::::: |      647 /      647 |:  thread 4 
```

The `atpbar` sensibly works regardless of the order in which multiple
instances of `atpbar` in multiple threads and multiple processes start
and end. The progress bars in the example above indicates that the
loops in four threads have already ended before the loop in the main
threads ended; the loop in the last thread ended afterwards.

*****

#### On Jupyter Notebook

On Jupyter Notebook, `atpbar` shows progress bars based on
[widgets](https://ipywidgets.readthedocs.io).

<img src="https://raw.githubusercontent.com/alphatwirl/notebook-atpbar-001/v1.0.1/images/20190304_01_atpbar_jupyter.gif" width="800">

You can try interactively online:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/alphatwirl/notebook-atpbar-001/master?filepath=atpbar.ipynb)

*****

#### Non TTY device

If neither on Jupyter Notebook or on a TTY device, `atpbar` is not
able to show progress bars. `atpbar` occasionally prints the status.

```
03/04 09:17 :     1173 /     7685 ( 15.26%): thread 0 
03/04 09:17 :     1173 /     6470 ( 18.13%): thread 3 
03/04 09:17 :     1199 /     1199 (100.00%): thread 4 
03/04 09:18 :     1756 /     2629 ( 66.79%): thread 2 
03/04 09:18 :     1757 /     7685 ( 22.86%): thread 0 
03/04 09:18 :     1757 /     6470 ( 27.16%): thread 3 
03/04 09:19 :     2342 /     2629 ( 89.08%): thread 2 
```

*****

#### How to disable progress bars

The function `disable()` disables `atpbar`; progress bars will not be shown.

```python
from atpbar import disable

disable()
```

This function needs to be called before `atpbar` or `find_reporter()` is used,
typically at the beginning of the program.

*****

## License

- _atpbar_ is licensed under the BSD license.

*****

## Contact

- <span itemscope itemtype="https://schema.org/Person"><a itemprop="sameAs" content="https://orcid.org/0000-0003-3225-9861" href="https://orcid.org/0000-0003-3225-9861" target="orcid.widget" rel="me noopener noreferrer" style="vertical-align:text-top;"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png" style="width:1em;margin-right:.5em;" alt="ORCID iD icon"></a></span>Tai Sakuma - tai.sakuma@gmail.com

