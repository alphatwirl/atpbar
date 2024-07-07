import contextlib
import logging
import uuid
from collections.abc import Iterable, Iterator
from typing import Generic, Optional, TypeVar

from .funcs import fetch_reporter
from .progress_report import Report

T = TypeVar('T')


def atpbar(iterable: Iterable[T], /, name: Optional[str] = None) -> Iterable[T]:
    '''returns an instance of `Atpbar`

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

    '''
    try:
        len_ = len(iterable)  # type: ignore
    except TypeError:
        logger = logging.getLogger(__name__)
        logger.warning('length is unknown: {!r}'.format(iterable))
        logger.warning('atpbar is turned off')
        return iterable

    if name is None:
        name = repr(iterable)

    return Atpbar(iterable, name=name, len_=len_)


class Atpbar(Generic[T]):
    '''Progress bar

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

    '''

    def __init__(self, iterable: Iterable[T], name: str, len_: int):
        self.iterable = iterable
        self.name = name
        self.len_ = len_
        self.id_ = uuid.uuid4()
        self._done = 0

    def __iter__(self) -> Iterator[T]:
        with fetch_reporter() as reporter:
            if reporter is None:
                yield from self.iterable
                return
            self.reporter = reporter
            self.loop_complete = False
            self._report_start()
            with self._report_last():
                for i, e in enumerate(self.iterable):
                    yield e
                    self._done = i + 1
                    self._report_progress()
                else:
                    self.loop_complete = True

    def _report_start(self) -> None:
        report = Report(
            task_id=self.id_,
            name=self.name,
            done=0,
            total=self.len_,
            first=True,
            last=self._done == self.len_,
        )
        self._submit(report)

    def _report_progress(self) -> None:
        report = Report(
            task_id=self.id_,
            name=self.name,
            done=self._done,
            total=self.len_,
            first=self._done == 0,
            last=self._done == self.len_,
        )
        self._submit(report)

    @contextlib.contextmanager
    def _report_last(self) -> Iterator[None]:
        '''send a last report

        This function sends the last report of the task when the loop ends with
        `break` or an exception so that the progress bar will be updated with
        the last complete iteration.

        '''
        try:
            yield
        finally:
            if self.loop_complete:
                return
            report = Report(
                task_id=self.id_,
                name=self.name,
                done=self._done,
                total=self.len_,
                first=False,
                last=True,
            )
            self._submit(report)

    def _submit(self, report: Report) -> None:
        try:
            self.reporter.report(report)
        except BaseException:
            pass
