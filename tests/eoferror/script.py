#!/usr/bin/env python
import atpbar

# This simple script always ends with an error in a certain
# environment in atpbar 1.0.2 as described in
# https://github.com/alphatwirl/atpbar/issues/4


for i in atpbar.atpbar(range(10)):
    pass


