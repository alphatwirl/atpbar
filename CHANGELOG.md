# Changelog

## [Unreleased]

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.1.0...master))

## [1.1.0] - 2020-04-27

**PyPI**: https://pypi.org/project/atpbar/1.1.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.9...v1.1.0))
- reimplemented the logic in `funcs.py` with a state machine [#17](https://github.com/alphatwirl/atpbar/pull/17)
- optimized the brief sleep of pickup
- cleaned code
- updated `setup.py`, tests
- made the number of iterations in examples smaller
- set start method of `multiprocessing` in an example for Python 3.8
- removed code for Python 2.7

## [1.0.9] - 2020-04-19

**PyPI**: https://pypi.org/project/atpbar/1.0.9/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.8...v1.0.9))
- added the option to show time elapsed and remaining on Jupyter Notebook [#13](https://github.com/alphatwirl/atpbar/pull/13)
- moved the dependency list from `requirements` to `setup.py`
- updated `.travis.yml`, `.coveragerc`

## [1.0.8] - 2020-03-14

**PyPI**: https://pypi.org/project/atpbar/1.0.8/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.7...v1.0.8))
- stopped supporting Python 2.7

## [1.0.7] - 2020-02-29

**PyPI**: https://pypi.org/project/atpbar/1.0.7/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.6...v1.0.7))
- addressed the issue [#15](https://github.com/alphatwirl/atpbar/issues/15)
    - use `ProgressPrint` on Spyder IDE
- listed Python 3.8 in `setup.py`
- updated `.travis.yml`, allowing failure in Python 2.7

## [1.0.6] - 2020-02-15

**PyPI**: https://pypi.org/project/atpbar/1.0.6/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.5...v1.0.6))
- updated `travis.yml`
    - adding tests on Python 3.8
    - using Python 3.7 for deployment instead of 3.6

## [1.0.5] - 2020-01-03

**PyPI**: https://pypi.org/project/atpbar/1.0.5/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.4...v1.0.5))
- addressed the slowdown issue [#8](https://github.com/alphatwirl/atpbar/issues/8)

## [1.0.4] - 2019-04-23

**PyPI**: https://pypi.org/project/atpbar/1.0.4/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.3...v1.0.4))
- made the name field next to progress bars longer in wide terminals
  [#5](https://github.com/alphatwirl/atpbar/issues/5)
- updated tests, `README.md`

## [1.0.3] - 2019-03-15

**PyPI**: https://pypi.org/project/atpbar/1.0.3/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.2...v1.0.3))
- fixed the `EOFError` [#4](https://github.com/alphatwirl/atpbar/issues/4)

## [1.0.2] - 2019-03-08

**PyPI**: https://pypi.org/project/atpbar/1.0.2/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.1...v1.0.2))
- updated `README.md`, `MANIFEST.in`

## [1.0.1] - 2019-03-03

**PyPI**: https://pypi.org/project/atpbar/1.0.1/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v1.0.0...v1.0.1))
- updated `setup.py`, `travis.yml`

## [1.0.0] - 2019-03-03

**PyPI**: https://pypi.org/project/atpbar/1.0.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.9...v1.0.0))
- changed "Development Status" to "Production/Stable" in `setup.py`
- updated `.travis.yml`, not allowing failure in Python 3.7

## [0.9.9] - 2019-03-03

**PyPI**: https://pypi.org/project/atpbar/0.9.9/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.8...v0.9.9))
- confirmed `atpbar` works on Jupyter Notebook in Python 2.7 [#3](https://github.com/alphatwirl/atpbar/issues/3)
- updated `README.md`, `.travis.yml`
- added files in `requirements`

## [0.9.8] - 2019-03-03

**PyPI**: https://pypi.org/project/atpbar/0.9.8/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.7...v0.9.8))
- added `disable()`
- updated tests, `README.md`

## [0.9.7] - 2019-02-24

**PyPI**: https://pypi.org/project/atpbar/0.9.7/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.6...v0.9.7))
- fixed the problem of progress bars stopping in multiprocessing.
    - `atpbar` in sub-processes will not send the end order to the
      pickup.
- fixed the problem of duplicate progress bar for complete tasks.
    - The last report will be sent only once for each task regardless
      of whether the loop completes all iterations.
- updated `.travis.yml`, using 3.7-dev for python 3.7
- updated tests
- cleaned code

## [0.9.6] - 2019-02-22

**PyPI**: https://pypi.org/project/atpbar/0.9.6/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.5...v0.9.6))
- updated the feature
    - The progress bars will be updated with the last complete
      iteration even if the loop ends with `break` or an exception
- fixed the problem of a pickup not running after `flush()`.
- stopped `atpbar` waiting for all progress bars to finish updating if
  another `atpbar` starts in a sub-thread or sub-process.
- updated .travis.yml, adding a test without jupyter
- removed `ProgressReport`, replaced with `dict()`
- updated docstrings
- updated tests
- cleaned code

## [0.9.5] - 2019-02-18

**PyPI**: https://pypi.org/project/atpbar/0.9.5/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.4...v0.9.5))
- made the long description in `setup.py` load from `README.md`
- updated tests

## [0.9.4] - 2019-02-18

**PyPI**: https://pypi.org/project/atpbar/0.9.4/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.3...v0.9.4))
- fixed the problem whereby the pickup doesn't end if the loop ends
  with `break`.
- made a presentation every time a pickup is created.
- updated tests

## [0.9.3] - 2019-02-18

**PyPI**: https://pypi.org/project/atpbar/0.9.3/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.2...v0.9.3))
- fixed the problem of returning from the outermost `atpbar` too early
  in the single thread. This problem was causing, for example, the
  command prompt to already have appeared while the progress bars were
  still growing in the interactive mode.
- added a new function `flush()`, which returns after the progress
  bars finished updating -- useful for threading and multiprocessing

## [0.9.2] - 2019-02-17

**PyPI**: https://pypi.org/project/atpbar/0.9.2/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.1...v0.9.2))
- updated `README.md`
- updated the long description in `setup.py` for pypi

## [0.9.1] - 2019-02-17

**PyPI**: https://pypi.org/project/atpbar/0.9.1/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.0...v0.9.1))
- fixed a bug in `ProgressBarJupyter`
    - preventing scroll bars from being added to the output of a
      previous cell
- updated `README.md`

## [0.9.1] - 2019-02-17

**PyPI**: https://pypi.org/project/atpbar/0.9.0/

## [0.8.0] - 2019-02-17
