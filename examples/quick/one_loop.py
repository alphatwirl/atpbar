#!/usr/bin/env python

from random import randint
from time import sleep

from atpbar import atpbar

n = randint(5, 1000)
# n = randint(1000, 10000)
for _ in atpbar(range(n)):
    sleep(0.0001)
    # sleep(0.001)
