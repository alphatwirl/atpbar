# Threading

An example with
[`threading.Thread`](https://docs.python.org/3/library/threading.html#thread-objects):

```python
from random import randint
from threading import Thread
from time import sleep

from atpbar import atpbar, flushing


def func(n, name):
    for _ in atpbar(range(n), name=name):
        sleep(0.001)


n_threads = 5

with flushing():
    threads = []
    for i in range(n_threads):
        n = randint(1000, 10000)
        t = Thread(target=func, args=(n, f'Thread {i}'))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
```
