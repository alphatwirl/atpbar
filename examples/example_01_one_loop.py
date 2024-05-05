#!/usr/bin/env python

import random
import time

from atpbar import atpbar

n = random.randint(5, 1000)
for i in atpbar(range(n)):
    time.sleep(0.0001)
