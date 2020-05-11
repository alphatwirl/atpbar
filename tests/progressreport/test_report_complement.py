# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from atpbar.progressreport.complement import ProgressReportComplementer

##__________________________________________________________________||
@pytest.fixture()
def obj():
    ret = ProgressReportComplementer()
    return ret

def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
def test_complement(obj):

    report0 = dict(taskid=5355, done=0, total=10, name='task1')
    expected0 = dict(taskid=5355, done=0, total=10, first=True, last=False, name='task1')
    assert obj(report0) is None
    assert expected0 == report0

    report1 = dict(taskid=5355, done=1, total=12)
    expected1 = dict(taskid=5355, done=1, total=12, first=False, last=False, name='task1')
    assert obj(report1) is None
    assert expected0 == report0
    assert expected1 == report1

    report2 = dict(taskid=5355, done=2)
    expected2 = dict(taskid=5355, done=2, total=12, first=False, last=False, name='task1')
    assert obj(report2) is None
    assert expected0 == report0
    assert expected1 == report1
    assert expected2 == report2

    report3 = dict(taskid=5355, done=12)
    expected3 = dict(taskid=5355, done=12, total=12, first=False, last=True, name='task1')
    assert obj(report3) is None
    assert expected0 == report0
    assert expected1 == report1
    assert expected2 == report2
    assert expected3 == report3

##__________________________________________________________________||
def test_volatile_fileds(obj):

    report0 = dict(taskid=5355, done=0, total=10, first=True)
    expected0 = dict(taskid=5355, done=0, total=10, first=True, last=False)
    assert obj(report0) is None
    assert expected0 == report0

    # manually set `first`
    report1 = dict(taskid=5355, done=1, total=12, first=True, last=False)
    expected1 = dict(taskid=5355, done=1, total=12, first=True, last=False)
    assert obj(report1) is None
    assert expected0 == report0
    assert expected1 == report1

    # doesn't remember previously manually set `first`
    report2 = dict(taskid=5355, done=2)
    expected2 = dict(taskid=5355, done=2, total=12, first=False, last=False)
    assert obj(report2) is None
    assert expected0 == report0
    assert expected1 == report1
    assert expected2 == report2

##__________________________________________________________________||
def test_first(obj):

    report0 = dict(taskid=5355, done=0, total=10)
    expected0 = dict(taskid=5355, done=0, total=10, first=True, last=False)
    assert obj(report0) is None
    assert expected0 == report0

    report1 = dict(taskid=5355, done=1, total=12)
    expected1 = dict(taskid=5355, done=1, total=12, first=False, last=False)
    assert obj(report1) is None
    assert expected1 == report1

    report2 = dict(taskid=5355, done=2, first=True)
    expected2 = dict(taskid=5355, done=2, total=12, first=True, last=False)
    assert obj(report2) is None
    assert expected2 == report2

    report3 = dict(taskid=5355, done=3)
    expected3 = dict(taskid=5355, done=3, total=12, first=False, last=False)
    assert obj(report3) is None
    assert expected3 == report3

    # different taskid, both done and total are 0
    report4 = dict(taskid=9222, done=0, total=0)
    expected4 = dict(taskid=9222, done=0, total=0, first=True, last=True)
    assert obj(report4) is None
    assert expected4 == report4

##__________________________________________________________________||
def test_last(obj):

    report0 = dict(taskid=5355, done=0, total=10)
    expected0 = dict(taskid=5355, done=0, total=10, first=True, last=False)
    assert obj(report0) is None
    assert expected0 == report0

    # set `last` manually
    report1 = dict(taskid=5355, done=1, total=12, last=True)
    expected1 = dict(taskid=5355, done=1, total=12, first=False, last=True)
    assert obj(report1) is None
    assert expected1 == report1

    report2 = dict(taskid=9222, done=0, total=10)
    expected2 = dict(taskid=9222, done=0, total=10, first=True, last=False)
    assert obj(report2) is None
    assert expected2 == report2

    # done = total
    report3 = dict(taskid=9222, done=10, total=10)
    expected3 = dict(taskid=9222, done=10, total=10, first=False, last=True)
    assert obj(report3) is None
    assert expected3 == report3

##__________________________________________________________________||
