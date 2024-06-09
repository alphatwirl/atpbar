#!/usr/bin/env python

from random import randint
from time import sleep

from atpbar import atpbar

for i in atpbar(range(4), name='Outer'):
    n = randint(5, 1000)
    # n = randint(1000, 10000)
    for _ in atpbar(range(n), name=f'Inner {i}'):
        sleep(0.0001)
        # sleep(0.001)
