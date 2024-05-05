#!/usr/bin/env python

import random
import time

from atpbar import atpbar

for i in atpbar(range(4), name='Outer'):
    n = random.randint(5, 1000)
    for j in atpbar(range(n), name='Inner {}'.format(i)):
        time.sleep(0.0001)
