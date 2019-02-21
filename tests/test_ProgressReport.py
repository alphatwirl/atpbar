# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from atpbar.report import ProgressReport

##__________________________________________________________________||
def test_repr():
    obj = ProgressReport(name='task1', done=124, total=1552, taskid=1212, pid=2342, in_main_thread=True)
    repr(obj)

def test_init():
    obj = ProgressReport(name='task1', done=124, total=1552, taskid=1212, pid=2342, in_main_thread=True)

params = [
    (ProgressReport(name='task1', done=124, total=1552, taskid=1, pid=2342, in_main_thread=True), False),
    (ProgressReport(name='task1', done=1552, total=1552, taskid=1, pid=2342, in_main_thread=True), True),
    (ProgressReport(name='task1', done=0, total=0, taskid=1, pid=2342, in_main_thread=True), True),
]
@pytest.mark.parametrize('obj, expected', params)
def test_last(obj, expected):
    assert expected == obj.last()

params = [
    (ProgressReport(name='task1', done=124, total=1552, taskid=1, pid=2342, in_main_thread=True), False),
    (ProgressReport(name='task1', done=0, total=1552, taskid=1, pid=2342, in_main_thread=True), True),
    (ProgressReport(name='task1', done=0, total=0, taskid=1, pid=2342, in_main_thread=True), True),
]
@pytest.mark.parametrize('obj, expected', params)
def test_first(obj, expected):
    assert expected == obj.first()

##__________________________________________________________________||
