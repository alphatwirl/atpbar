# Threading

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
