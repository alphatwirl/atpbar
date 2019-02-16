# Tai Sakuma <tai.sakuma@gmail.com>
from .ProgressReporter import ProgressReporter

import alphatwirl
from alphatwirl.misc.deprecation import _deprecated

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
        reporter = self.createReporter()
        alphatwirl.progressbar._progress_reporter = reporter

    def end(self):
        alphatwirl.progressbar._progress_reporter = None

    def create_reporter(self):
        reporter = ProgressReporter(queue=self.queue)
        return reporter

    @_deprecated(msg='use create_reporter() instead')
    def createReporter(self):
        return self.create_reporter()

##__________________________________________________________________||
