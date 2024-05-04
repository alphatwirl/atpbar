#!/usr/bin/env python

import time, random

from atpbar import atpbar

##__________________________________________________________________||
for i in atpbar(range(4)):
    n = random.randint(5, 10000)
    for j in atpbar(range(n)):
        time.sleep(0.0001)

##__________________________________________________________________||
