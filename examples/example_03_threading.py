#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
import threading
import time, random
import atpbar

##__________________________________________________________________||
class Task(threading.Thread):
    def __init__(self, name):
        super(Task, self).__init__()
        self.name = name

    def run(self):
        n = random.randint(5, 100000)
        for i in atpbar.atpbar(range(n), name=self.name):
            time.sleep(0.0001)
        return None

##__________________________________________________________________||
ntasks = 5
tasks = [ ]

for i in range(ntasks):
    task_name = 'task {}'.format(i)
    task = Task(name=task_name)
    task.start()
    tasks.append(task)

for task in tasks:
    task.join()

##__________________________________________________________________||
