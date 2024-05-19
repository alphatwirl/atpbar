import uuid

import pytest

from atpbar.progress_report import Report
from atpbar.progress_report.complement import ProgressReportComplementer


@pytest.fixture()
def obj() -> ProgressReportComplementer:
    ret = ProgressReportComplementer()
    return ret


def test_repr(obj: ProgressReportComplementer) -> None:
    repr(obj)


def test_complement(obj: ProgressReportComplementer) -> None:

    task_id = uuid.uuid4()
    report0 = Report(taskid=task_id, done=0, total=10, name="task1")
    expected0 = Report(
        taskid=task_id, done=0, total=10, first=True, last=False, name="task1"
    )
    obj(report0)
    assert expected0 == report0

    report1 = Report(taskid=task_id, done=1, total=12)
    expected1 = Report(
        taskid=task_id, done=1, total=12, first=False, last=False, name="task1"
    )
    obj(report1)
    assert expected0 == report0
    assert expected1 == report1

    report2 = Report(taskid=task_id, done=2)
    expected2 = Report(
        taskid=task_id, done=2, total=12, first=False, last=False, name="task1"
    )
    obj(report2)
    assert expected0 == report0
    assert expected1 == report1
    assert expected2 == report2

    report3 = Report(taskid=task_id, done=12)
    expected3 = Report(
        taskid=task_id, done=12, total=12, first=False, last=True, name="task1"
    )
    obj(report3)
    assert expected0 == report0
    assert expected1 == report1
    assert expected2 == report2
    assert expected3 == report3


def test_volatile_fileds(obj: ProgressReportComplementer) -> None:

    task_id = uuid.uuid4()
    report0 = Report(taskid=task_id, done=0, total=10, first=True)
    expected0 = Report(taskid=task_id, done=0, total=10, first=True, last=False)
    obj(report0)
    assert expected0 == report0

    # manually set `first`
    report1 = Report(taskid=task_id, done=1, total=12, first=True, last=False)
    expected1 = Report(taskid=task_id, done=1, total=12, first=True, last=False)
    obj(report1)
    assert expected0 == report0
    assert expected1 == report1

    # doesn't remember previously manually set `first`
    report2 = Report(taskid=task_id, done=2)
    expected2 = Report(taskid=task_id, done=2, total=12, first=False, last=False)
    obj(report2)
    assert expected0 == report0
    assert expected1 == report1
    assert expected2 == report2


def test_first(obj: ProgressReportComplementer) -> None:

    task_id_1 = uuid.uuid4()
    report0 = Report(taskid=task_id_1, done=0, total=10)
    expected0 = Report(taskid=task_id_1, done=0, total=10, first=True, last=False)
    obj(report0)
    assert expected0 == report0

    report1 = Report(taskid=task_id_1, done=1, total=12)
    expected1 = Report(taskid=task_id_1, done=1, total=12, first=False, last=False)
    obj(report1)
    assert expected1 == report1

    report2 = Report(taskid=task_id_1, done=2, first=True)
    expected2 = Report(taskid=task_id_1, done=2, total=12, first=True, last=False)
    obj(report2)
    assert expected2 == report2

    report3 = Report(taskid=task_id_1, done=3)
    expected3 = Report(taskid=task_id_1, done=3, total=12, first=False, last=False)
    obj(report3)
    assert expected3 == report3

    # different taskid, both done and total are 0
    task_id_2 = uuid.uuid4()
    report4 = Report(taskid=task_id_2, done=0, total=0)
    expected4 = Report(taskid=task_id_2, done=0, total=0, first=True, last=True)
    obj(report4)
    assert expected4 == report4


def test_last(obj: ProgressReportComplementer) -> None:

    task_id_1 = uuid.uuid4()
    report0 = Report(taskid=task_id_1, done=0, total=10)
    expected0 = Report(taskid=task_id_1, done=0, total=10, first=True, last=False)
    obj(report0)
    assert expected0 == report0

    # set `last` manually
    report1 = Report(taskid=task_id_1, done=1, total=12, last=True)
    expected1 = Report(taskid=task_id_1, done=1, total=12, first=False, last=True)
    obj(report1)
    assert expected1 == report1

    task_id_2 = uuid.uuid4()
    report2 = Report(taskid=task_id_2, done=0, total=10)
    expected2 = Report(taskid=task_id_2, done=0, total=10, first=True, last=False)
    obj(report2)
    assert expected2 == report2

    # done = total
    report3 = Report(taskid=task_id_2, done=10, total=10)
    expected3 = Report(taskid=task_id_2, done=10, total=10, first=False, last=True)
    obj(report3)
    assert expected3 == report3
