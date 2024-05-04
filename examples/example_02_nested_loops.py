#!/usr/bin/env python

import random
import time

from atpbar import atpbar

for i in atpbar(range(4)):
    n = random.randint(5, 10000)
    for j in atpbar(range(n)):
        time.sleep(0.0001)
