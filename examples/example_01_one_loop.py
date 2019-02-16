#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
import time, random
import atpbar

##__________________________________________________________________||
n = random.randint(5, 10000)
for i in atpbar.atpbar(range(n)):
    time.sleep(0.0001)

##__________________________________________________________________||
