# Changelog

## [Unreleased]

#### Changs from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.2...master))
- fixed the problem of returning from the outermost `atpbar` in the
  single thread. This problem was causing, for example, the command
  prompt to already have appeared while the progress bars were still
  growing in the interactive mode.
- added a new function `flush()`, which returns after the progress
  bars finished updating -- useful for threading and multiprocessing

## [0.9.2] - 2019-02-17

**PyPI**: https://pypi.org/project/atpbar/0.9.2/

#### Changs from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.1...v0.9.2))
- updated `README.md`
- updated the long description in `setup.py` for pypi

## [0.9.1] - 2019-02-17

**PyPI**: https://pypi.org/project/atpbar/0.9.1/

#### Changs from the previous release: ([diff](https://github.com/alphatwirl/atpbar/compare/v0.9.0...v0.9.1))
- fixed a bug in `ProgressBarJupyter`
    - preventing scroll bars from being added to the output of a
      previous cell
- updated `README.md`

## [0.9.1] - 2019-02-17

**PyPI**: https://pypi.org/project/atpbar/0.9.0/

## [0.8.0] - 2019-02-17
