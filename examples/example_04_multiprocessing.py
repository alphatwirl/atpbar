#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
import multiprocessing
import time, random
import atpbar

##__________________________________________________________________||
atpbar._start_monitor_if_necessary()
reporter = atpbar._reporter

##__________________________________________________________________||
class Task(multiprocessing.Process):
    def __init__(self, reporter, name):
        super(Task, self).__init__()
        self.reporter = reporter
        self.name = name

    def run(self):
        atpbar._reporter = self.reporter
        atpbar.do_not_start_monitor = True

        n = random.randint(5, 100000)
        time.sleep(random.randint(0, 3))
        for i in atpbar.atpbar(range(n), name=self.name):
            time.sleep(0.0001)
        return None

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
