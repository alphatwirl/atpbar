#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
import multiprocessing
import time, random
import atpbar

##__________________________________________________________________||
class Task(multiprocessing.Process):
    def __init__(self, reporter, name):
        super(Task, self).__init__()
        self.reporter = reporter
        self.name = name

    def run(self):
        atpbar.register_reporter(self.reporter)

        n = random.randint(5, 100000)
        for i in atpbar.atpbar(range(n), name=self.name):
            time.sleep(0.0001)
        return None

##__________________________________________________________________||
reporter = atpbar.reporter()

##__________________________________________________________________||
ntasks = 5
tasks = [ ]

for i in range(ntasks):
    task_name = 'task {}'.format(i)
    task = Task(reporter=reporter, name=task_name)
    task.start()
    tasks.append(task)

for task in tasks:
    task.join()

##__________________________________________________________________||
