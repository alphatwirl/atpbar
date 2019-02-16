# Tai Sakuma <tai.sakuma@gmail.com>
import uuid
import logging

import alphatwirl
from .ProgressReport import ProgressReport

##__________________________________________________________________||
def atpbar(iterable, name=None):
    """Progress bar

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

    return Atpbar(iterable, name=name, len_=len_)

##__________________________________________________________________||
class Atpbar(object):
    def __init__(self, iterable, name, len_):
        self.iterable = iterable
        self.name = name
        self.len_ = len_
        self.id_ = uuid.uuid4()

    def __iter__(self):
        alphatwirl.progressbar._start_monitor_if_necessary()
        self._report_progress(-1)
        for i, e in enumerate(self. iterable):
            yield e
            self._report_progress(i)

    def _report_progress(self, i):
        try:
            report = ProgressReport(
                name=self.name, done=(i+1),
                total=self.len_, taskid=self.id_)
            alphatwirl.progressbar.report_progress(report)
        except:
            pass

##__________________________________________________________________||
