# Tai Sakuma <tai.sakuma@gmail.com>
import uuid
import logging

from .report import ProgressReport
from .funcs import fetch_reporter

##__________________________________________________________________||
def atpbar(iterable, name=None):
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

    return Atpbar(iterable, name=name, len_=len_)

##__________________________________________________________________||
class Atpbar(object):
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

    def __init__(self, iterable, name, len_):
        self.iterable = iterable
        self.name = name
        self.len_ = len_
        self.id_ = uuid.uuid4()

    def __iter__(self):
        with fetch_reporter() as reporter:
            self.reporter = reporter
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
