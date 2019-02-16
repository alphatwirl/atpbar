# Tai Sakuma <tai.sakuma@gmail.com>
from .ProgressReporter import ProgressReporter

import atpbar

##__________________________________________________________________||
class Queue(object):

    def __init__(self, presentation):
        self.presentation = presentation

    def put(self, report):
        self.presentation.present(report)

##__________________________________________________________________||
class ProgressMonitor(object):
    def __init__(self, presentation):
        self.presentation = presentation
        self.queue = Queue(presentation=presentation)

    def begin(self):
        reporter = self.create_reporter()
        atpbar._progress_reporter = reporter

    def end(self):
        atpbar._progress_reporter = None

    def create_reporter(self):
        reporter = ProgressReporter(queue=self.queue)
        return reporter

##__________________________________________________________________||
