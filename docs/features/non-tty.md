# Non TTY device

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
