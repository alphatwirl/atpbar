# A `break` and an exception

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
