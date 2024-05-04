#!/usr/bin/env python

import time, random

from atpbar import atpbar


n = random.randint(5, 10000)
for i in atpbar(range(n)):
    time.sleep(0.0001)


