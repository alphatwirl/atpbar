# How to disable progress bars

The function `disable()` disables `atpbar`; progress bars will not be shown.

```python
from atpbar import disable

disable()
```

This function needs to be called before `atpbar` or `find_reporter()` is used,
typically at the beginning of the program.
