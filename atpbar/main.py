# Tai Sakuma <tai.sakuma@gmail.com>
import uuid
import logging

from .report import ProgressReport
from .funcs import find_reporter

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
        self.reporter = find_reporter()
        self._report_progress(-1)
        for i, e in enumerate(self. iterable):
            yield e
            self._report_progress(i)

    def _report_progress(self, i):
        if self.reporter is None:
            return
        try:
            report = ProgressReport(
                name=self.name, done=(i+1),
                total=self.len_, taskid=self.id_)
            self.reporter.report(report)
        except:
            pass

##__________________________________________________________________||
