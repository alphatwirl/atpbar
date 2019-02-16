# Tai Sakuma <tai.sakuma@gmail.com>

from alphatwirl.progressbar import ProgressReport

##__________________________________________________________________||
def test_repr():
    obj = ProgressReport(name = 'dataset1', done = 124, total = 1552, taskid = 1212)
    repr(obj)

def test_init():
    obj = ProgressReport(name = 'dataset1', done = 124, total = 1552, taskid = 1212)

def test_init_no_taskid():
    obj = ProgressReport(name = 'dataset1', done = 124, total = 1552)
    assert obj.taskid == 'dataset1'

def test_last():
    obj = ProgressReport(name = 'dataset1', done = 124, total = 1552)
    assert not obj.last()

    obj = ProgressReport(name = 'dataset1', done = 1552, total = 1552)
    assert obj.last()

    obj = ProgressReport(name = 'dataset1', done = 0, total = 0)
    assert obj.last()

def test_first():
    obj = ProgressReport(name = 'dataset1', done = 124, total = 1552)
    assert not obj.last()

    obj = ProgressReport(name = 'dataset1', done = 0, total = 1552)
    assert obj.first()

    obj = ProgressReport(name = 'dataset1', done = 0, total = 0)
    assert obj.first()

##__________________________________________________________________||
