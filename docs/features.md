# Features

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

```plaintext
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

    n_threads = 5
    threads = []

    for i in range(n_threads):
        name = 'Thread {}'.format(i)
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
  18.21% :::::::                                  |     1234 /     6777 |:  Thread 0
  15.08% ::::::                                   |     1234 /     8183 |:  Thread 2
  15.25% ::::::                                   |     1234 /     8092 |:  Thread 1
  39.90% :::::::::::::::                          |     1234 /     3093 |:  Thread 4
  19.67% :::::::                                  |     1234 /     6274 |:  Thread 3
```

#### Progress of starting threads and processes with progress bars

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

---

#### On Jupyter Notebook

On Jupyter Notebook, `atpbar` shows progress bars based on
[widgets](https://ipywidgets.readthedocs.io).

<img src="https://raw.githubusercontent.com/alphatwirl/notebook-atpbar-001/v1.0.1/images/20190304_01_atpbar_jupyter.gif" width="800">

You can try interactively online:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/alphatwirl/notebook-atpbar-001/master?filepath=atpbar.ipynb)

---

#### Non TTY device

If neither on Jupyter Notebook or on a TTY device, `atpbar` is not able to show
progress bars. `atpbar` occasionally prints the status.

```
03/04 09:17 :     1173 /     7685 ( 15.26%): Thread 0
03/04 09:17 :     1173 /     6470 ( 18.13%): Thread 3
03/04 09:17 :     1199 /     1199 (100.00%): Thread 4
03/04 09:18 :     1756 /     2629 ( 66.79%): Thread 2
03/04 09:18 :     1757 /     7685 ( 22.86%): Thread 0
03/04 09:18 :     1757 /     6470 ( 27.16%): Thread 3
03/04 09:19 :     2342 /     2629 ( 89.08%): Thread 2
```

---

#### How to disable progress bars

The function `disable()` disables `atpbar`; progress bars will not be shown.

```python
from atpbar import disable

disable()
```

This function needs to be called before `atpbar` or `find_reporter()` is used,
typically at the beginning of the program.
