from hypothesis import given
from hypothesis import strategies as st

from atpbar.progress_report import Report
from atpbar.progress_report.complement import ProgressReportComplementer
from tests.test_utils.st import st_text


@given(data=st.data())
def test_complement(data: st.DataObject) -> None:
    obj = ProgressReportComplementer()

    id_ = data.draw(st.uuids(version=4))
    name = data.draw(st_text())
    total = data.draw(st.integers(min_value=0, max_value=10))

    report = Report(task_id=id_, name=name, done=0, total=total)
    obj(report)
    assert report['first']

    for i in range(total):
        done = i + 1
        report = Report(task_id=id_, done=done, total=total)
        obj(report)
        assert not report['first']
        assert report['last'] is (done == total)
    else:
        assert report['last']


@given(data=st.data())
def test_first(data: st.DataObject) -> None:
    obj = ProgressReportComplementer()

    id_ = data.draw(st.uuids(version=4))
    name = data.draw(st_text())
    total = data.draw(st.integers(min_value=0, max_value=10))

    first = data.draw(st.booleans())

    report = Report(task_id=id_, name=name, done=0, total=total, first=first)
    obj(report)
    assert report['first'] is first


@given(data=st.data())
def test_last(data: st.DataObject) -> None:
    obj = ProgressReportComplementer()

    id_ = data.draw(st.uuids(version=4))
    name = data.draw(st_text())
    total = data.draw(st.integers(min_value=0, max_value=10))
    done = data.draw(st.integers(min_value=0, max_value=total))

    last = data.draw(st.booleans())

    report = Report(task_id=id_, name=name, done=done, total=total, last=last)
    obj(report)
    assert report['last'] is last
