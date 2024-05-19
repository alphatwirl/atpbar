# atpbar

_Progress bars_ for threading and multiprocessing tasks on the terminal and
Jupyter Notebook.

![Demo](demo.svg)

## Introduction

_atpbar_ can display multiple progress bars simultaneously growing to show the
progress of each iteration of loops in
[threading](https://docs.python.org/3/library/threading.html) or
[multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
tasks. _atpbar_ can display progress bars on the terminal and [Jupyter
Notebook](https://jupyter.org/).

_atpbar_ started its development in 2015 and was the sub-package
[_progressbar_](https://github.com/alphatwirl/alphatwirl/tree/v0.22.0/alphatwirl/progressbar)
of alphatwirl. It became an independent package in 2019.

You can try it on Jupyter Notebook online:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/alphatwirl/notebook-atpbar-001/master?filepath=atpbar.ipynb)

## Install

You can install with `pip` from [PyPI](https://pypi.org/project/atpbar/):

```bash
pip install -U atpbar
```

To install with Jupyter Notebook support, use the following command:

```bash
pip install -U atpbar[jupyter]
```
