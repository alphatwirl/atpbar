#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
import random
import time

from atpbar import atpbar

##__________________________________________________________________||
for i in atpbar(range(4)):
    n = random.randint(5, 10000)
    for j in atpbar(range(n)):
        time.sleep(0.0001)

##__________________________________________________________________||
