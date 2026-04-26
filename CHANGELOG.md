# Changelog

All notable changes to this project will be documented in this file.

## [2.0.9] - 2026-04-26

### Build & CI

- Adopt Conventional Commits and automated release flow ([#79](https://github.com/alphatwirl/atpbar/pull/79))

## [2.0.8] - 2026-04-26

## [2.0.7] - 2025-11-09

### Changes 🚀

- Stop supporting Python 3.9 ([#76](https://github.com/alphatwirl/atpbar/pull/76))

## [2.0.6] - 2025-10-19

### Changes 🚀

- Add Python 3.14 to tests on GitHub Actions ([#74](https://github.com/alphatwirl/atpbar/pull/74))
- Support Python 3.14 ([#75](https://github.com/alphatwirl/atpbar/pull/75))

## [2.0.5] - 2024-10-19

### Changes 🚀

- Format code with `ruff` ([#65](https://github.com/alphatwirl/atpbar/pull/65))
- Add tests on Python 3.13 in GitHub Actions ([#66](https://github.com/alphatwirl/atpbar/pull/66))
- Support Python 3.13 ([#67](https://github.com/alphatwirl/atpbar/pull/67))

## [2.0.4] - 2024-09-21

### Changes 🚀

- Update tests on `Stream` ([#61](https://github.com/alphatwirl/atpbar/pull/61))
- Clean code ([#62](https://github.com/alphatwirl/atpbar/pull/62))
- Remove `ProgressReportComplementer` ([#63](https://github.com/alphatwirl/atpbar/pull/63))
- Support Python 3.9 ([#64](https://github.com/alphatwirl/atpbar/pull/64))

## [2.0.3] - 2024-07-04

### Changes 🚀

- Rewrite tests in `tests/scenarios/` with Hypothesis ([#50](https://github.com/alphatwirl/atpbar/pull/50))
- Split the `Active` state into two states in the state machine ([#51](https://github.com/alphatwirl/atpbar/pull/51))
- Rename `taskid` to `task_id` for spellchecker ([#52](https://github.com/alphatwirl/atpbar/pull/52))
- Clean code ([#53](https://github.com/alphatwirl/atpbar/pull/53))
- Move `.coveragerc` to `pyproject.toml` ([#54](https://github.com/alphatwirl/atpbar/pull/54))
- Add test for state transitions ([#55](https://github.com/alphatwirl/atpbar/pull/55))
- Update the state diagram in docstring ([#56](https://github.com/alphatwirl/atpbar/pull/56))
- Update state transitions ([#57](https://github.com/alphatwirl/atpbar/pull/57))
- Clean code ([#58](https://github.com/alphatwirl/atpbar/pull/58))
- Rename `threading.py` to distinguish from the system module ([#59](https://github.com/alphatwirl/atpbar/pull/59))
- Clean code ([#60](https://github.com/alphatwirl/atpbar/pull/60))

## [2.0.2] - 2024-06-01

### Changes 🚀

- Rename `progressreport` to `progress_report` ([#40](https://github.com/alphatwirl/atpbar/pull/40))
- Add type hints to `tests` ([#41](https://github.com/alphatwirl/atpbar/pull/41))
- Fix type, linter, and spell checker errors ([#42](https://github.com/alphatwirl/atpbar/pull/42))
- Replace double quotes with single quotes ([#43](https://github.com/alphatwirl/atpbar/pull/43))
- Replace sys.modules with the import statement ([#47](https://github.com/alphatwirl/atpbar/pull/47))
- Fix spell checker errors ([#48](https://github.com/alphatwirl/atpbar/pull/48))
- Change license to MIT License ([#49](https://github.com/alphatwirl/atpbar/pull/49))

## [2.0.1] - 2024-05-19

### Changes 🚀

- Add the context manager `flushing()` ([#38](https://github.com/alphatwirl/atpbar/pull/38))
- Add documentation ([#39](https://github.com/alphatwirl/atpbar/pull/39))

## [2.0.0] - 2024-05-05

### Changes 🚀

- Switch from `setup.py` to `pyproject.toml` ([#31](https://github.com/alphatwirl/atpbar/pull/31))
- Require Python 3.10 and above ([#32](https://github.com/alphatwirl/atpbar/pull/32))
- Remove support for `Mantichora` ([#33](https://github.com/alphatwirl/atpbar/pull/33))
- Format code with black and isort ([#34](https://github.com/alphatwirl/atpbar/pull/34))
- Make the first argument of `atpbar` positional only ([#35](https://github.com/alphatwirl/atpbar/pull/35))
- Add type hints ([#36](https://github.com/alphatwirl/atpbar/pull/36))
- Remove the option time_track ([#37](https://github.com/alphatwirl/atpbar/pull/37))

## [1.1.4] - 2021-05-08

### Changes 🚀

- No change in the code
- Moved from Tavis-CI to GitHub Actions to publish to PyPI

## [1.1.3] - 2020-05-09

### Changes 🚀

- Made the option `time_track` effective on terminal as well [#19](https://github.com/alphatwirl/atpbar/pull/19)

## [1.1.2] - 2020-05-03

### Changes 🚀

- Updated escape code for moving cursor and clearing lines [#18](https://github.com/alphatwirl/atpbar/pull/18)
- Cleaned code
- Updated tests

## [1.1.1] - 2020-05-02

### Changes 🚀

- Cleaned code
- Updated tests

## [1.1.0] - 2020-04-28

### Changes 🚀

- Reimplemented the logic in `funcs.py` with a state machine [#17](https://github.com/alphatwirl/atpbar/pull/17)
- Optimized the brief sleep of pickup
- Cleaned code
- Updated `setup.py`, tests
- Made the number of iterations in examples smaller
- Set start method of `multiprocessing` in an example for Python 3.8
- Removed code for Python 2.7

## [1.0.9] - 2020-04-19

### Changes 🚀

- Added the option to show time elapsed and remaining on Jupyter Notebook [#13](https://github.com/alphatwirl/atpbar/pull/13)
- Moved the dependency list from `requirements` to `setup.py`
- Updated `.travis.yml`, `.coveragerc`

## [1.0.8] - 2020-03-14

### Changes 🚀

- Stopped supporting Python 2.7

## [1.0.7] - 2020-02-29

### Changes 🚀

- Addressed the issue [#15](https://github.com/alphatwirl/atpbar/issues/15)
  - Use `ProgressPrint` on Spyder IDE
- Listed Python 3.8 in `setup.py`
- Updated `.travis.yml`, allowing failure in Python 2.7

## [1.0.6] - 2020-02-15

### Changes 🚀

- Updated `travis.yml`
  - Adding tests on Python 3.8
  - Using Python 3.7 for deployment instead of 3.6

## [1.0.5] - 2020-01-03

### Changes 🚀

- Addressed the slowdown issue [#8](https://github.com/alphatwirl/atpbar/issues/8)

## [1.0.4] - 2019-04-23

### Changes 🚀

- Made the name field next to progress bars longer in wide terminals [#5](https://github.com/alphatwirl/atpbar/issues/5)
- Updated tests, `README.md`

## [1.0.3] - 2019-03-15

### Changes 🚀

- Fixed the `EOFError` [#4](https://github.com/alphatwirl/atpbar/issues/4)

## [1.0.2] - 2019-03-08

### Changes 🚀

- Updated `README.md`, `MANIFEST.in`

## [1.0.1] - 2019-03-03

### Changes 🚀

- Updated `setup.py`, `travis.yml`

## [1.0.0] - 2019-03-03

### Changes 🚀

- Changed "Development Status" to "Production/Stable" in `setup.py`
- Updated `.travis.yml`, not allowing failure in Python 3.7

## [0.9.9] - 2019-03-03

### Changes 🚀

- Confirmed `atpbar` works on Jupyter Notebook in Python 2.7 (https://github.com/alphatwirl/atpbar/issues/3)
- Updated `README.md`, `.travis.yml`
- Added files in `requirements`

## [0.9.8] - 2019-03-03

### Changes 🚀

- Updated tests, `README.md`
- Added `disable()`

## [0.9.7] - 2019-02-24

### Changes 🚀

- Fixed the problem of progress bars stopping in multiprocessing.
  - `atpbar` in sub-processes will not send the end order to the pickup.
- Fixed the problem of duplicate progress bar for complete tasks.
  - The last report will be sent only once for each task regardless of whether the loop completes all iterations.
- Updated .travis.yml, using 3.7-dev for python 3.7
- Updated tests
- Cleaned code

## [0.9.6] - 2019-02-22

### Changes 🚀

- Updated the feature
  - The progress bars will be updated with the last complete iteration even if the loop ends with `break` or an exception
- Fixed the problem of a pickup not running after `flush()`.
- Stopped `atpbar` waiting for all progress bars to finish updating if another `atpbar` starts in a sub-thread or sub-process.
- Updated .travis.yml, adding a test without jupyter
- Removed `ProgressReport`, replaced with `dict()`
- Updated docstrings
- Updated tests
- Cleaned code

## [0.9.5] - 2019-02-19

### Changes 🚀

- Made the long description in `setup.py` load from `README.md`
- Updated tests

## [0.9.4] - 2019-02-18

### Changes 🚀

- Fixed the problem whereby the pickup doesn't end if the loop ends with `break`.
- Made a presentation every time a pickup is created.
- Updated tests

## [0.9.3] - 2019-02-18

### Changes 🚀

- Fixed the problem of returning from the outermost `atpbar` in the single thread. This problem was causing, for example, the command prompt to already have appeared while the progress bars were still growing in the interactive mode.
- Added a new function `flush()`, which returns after the progress bars finished updating -- useful for threading and multiprocessing

## [0.9.2] - 2019-02-17

### Changes 🚀

- Updated `README.md`
- Updated the long description in `setup.py` for pypi

## [0.9.1] - 2019-02-17

### Changes 🚀

- Fixed a bug in `ProgressBarJupyter`
  - Preventing scroll bars from being added to the output of a previous cell
- Updated `README.md`

## [0.9.0] - 2019-02-17
