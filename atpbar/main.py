# Tai Sakuma <tai.sakuma@gmail.com>
import os, uuid
import logging
import time

import contextlib

from .funcs import fetch_reporter

##__________________________________________________________________||
def atpbar(iterable, name=None, time_track=False):
    """returns an instance of `Atpbar`

    Parameters
    ----------
    iterable : iterable
        An iterable whose progress of the iterations is to be shown
    name : str
        A label to be shown on the progress bar

    Returns
    -------
    iterable
        An instance of `Atpbar` if successfully instantiated.
        Otherwise, the object received as the parameter `iterable`.

    """
    try:
        len_ = len(iterable)
    except TypeError:
        logger = logging.getLogger(__name__)
        logging.warning('length is unknown: {!r}'.format(iterable))
        logging.warning('atpbar is turned off')
        return iterable

    if name is None:
        name = repr(iterable)

    return Atpbar(iterable, name=name, len_=len_, time_track=time_track)

##__________________________________________________________________||
class Atpbar:
    """Progress bar

    An iterable that wraps another iterable and shows the progress
    bars for the iterations. The class is usually instantiated by the
    function `atpbar`.

    Parameters
    ----------
    iterable : iterable
        An iterable whose progress of the iterations is to be shown
    name : str
        A label to be shown on the progress bar
    len_ : int
        The length of the iterable

    """

    def __init__(self, iterable, name, len_, time_track=False):
        self.iterable = iterable
        self.name = name
        self.len_ = len_
        self.id_ = uuid.uuid4()
        self.time_track = time_track

    def __iter__(self):
        with fetch_reporter() as reporter:
            self.reporter = reporter
            self.loop_complete = False
            self._report_start()
            with report_last(pbar=self):
                for i, e in enumerate(self. iterable):
                    yield e
                    self._report_progress(i)
                else:
                    self.loop_complete = True

    def _report_start(self):
        if self.reporter is None:
            return
        try:
            report = dict(
                taskid=self.id_, name=self.name,
                done=0, total=self.len_)
            if self.time_track:
                report['start_time'] = start_time=time.time()
            self.reporter.report(report)
        except:
            pass

    def _report_progress(self, i):
        if self.reporter is None:
            return
        try:
            report = dict(taskid=self.id_, done=(i+1))
            self.reporter.report(report)
        except:
            pass

@contextlib.contextmanager
def report_last(pbar):
    """send a last report

    This function sends the last report of the task when the loop ends
    with `break` or an exception so that the progress bar will be
    updated with the last complete iteration.

    """
    try:
        yield
    finally:
        if pbar.loop_complete:
            return
        if pbar.reporter is None:
            return
        try:
            report = dict(taskid=pbar.id_, first=False, last=True)
            pbar.reporter.report(report)
        except:
            pass

##__________________________________________________________________||
