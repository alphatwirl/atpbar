#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
import time, random
import atpbar

##__________________________________________________________________||
for i in atpbar.atpbar(range(4)):
    n = random.randint(5, 10000)
    for j in atpbar.atpbar(range(n)):
        time.sleep(0.0001)

##__________________________________________________________________||
