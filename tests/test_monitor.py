# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from atpbar.monitor import BProgressMonitor
from atpbar.presentation import Presentation

##__________________________________________________________________||
class MockProgressBar(Presentation):
    def _present(self):
        pass

##__________________________________________________________________||
def build_BProgressMonitor():
    return BProgressMonitor(presentation=MockProgressBar())

builds = [build_BProgressMonitor]
build_ids = ['BProgressMonitor']

##__________________________________________________________________||
@pytest.mark.parametrize('build', builds, ids=build_ids)
def test_monitor(build):
    obj = build()
    obj.begin()
    obj.create_reporter()
    obj.end()

##__________________________________________________________________||
