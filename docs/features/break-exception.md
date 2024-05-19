# A `break` and an exception

When the loop ends with a `break` or an exception, the progress bar stops with
the last complete iteration.

For example, the loop in the following code breaks during the 1235th iteration.

```python
for i in atpbar(range(2000)):
    if i == 1234:
        break
    sleep(0.0001)
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
    sleep(0.001)
```

The progress bar stops at the last complete iteration, 1234.

```
  61.70% ::::::::::::::::::::::::                 |     1234 /     2000 |:  range(0, 2000)
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
Exception
```

This feature works as well with nested loops, threading, and multiprocessing.
For example, in the following code, the loops in threads break at 1235th
iteration.

```python
def func(n, name):
    for i in atpbar(range(n), name=name):
        if i == 1234:
            break
        sleep(0.001)


n_workers = 5
n_jobs = 10

with flushing(), ThreadPoolExecutor(max_workers=n_workers) as executor:
    for i in range(n_jobs):
        n = randint(3000, 10000)
        f = executor.submit(func, n, name=f'Job {i}')
```

All progress bars stop at 1234.

```plaintext
  23.97% :::::::::                                |     1234 /     5149 |:  Job 2
  33.32% :::::::::::::                            |     1234 /     3703 |:  Job 4
  35.09% ::::::::::::::                           |     1234 /     3517 |:  Job 0
  13.47% :::::                                    |     1234 /     9162 |:  Job 3
  27.35% ::::::::::                               |     1234 /     4512 |:  Job 1
  32.07% ::::::::::::                             |     1234 /     3848 |:  Job 6
  29.04% :::::::::::                              |     1234 /     4250 |:  Job 5
  21.01% ::::::::                                 |     1234 /     5872 |:  Job 8
  13.70% :::::                                    |     1234 /     9006 |:  Job 7
  36.51% ::::::::::::::                           |     1234 /     3380 |:  Job 9
```
