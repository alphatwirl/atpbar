# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from atpbar.BProgressMonitor import BProgressMonitor
from atpbar.ProgressMonitor import ProgressMonitor
from atpbar.presentation import Presentation

##__________________________________________________________________||
class MockProgressBar(Presentation):
    def _present(self):
        pass

##__________________________________________________________________||
def build_BProgressMonitor():
    return BProgressMonitor(presentation=MockProgressBar())

def build_ProgressMonitor():
    return ProgressMonitor(presentation=MockProgressBar)

builds = [build_BProgressMonitor, build_ProgressMonitor]
build_ids = ['BProgressMonitor', 'ProgressMonitor']

##__________________________________________________________________||
@pytest.mark.parametrize('build', builds, ids=build_ids)
def test_monitor(build):
    obj = build()
    obj.begin()
    obj.create_reporter()
    obj.end()

##__________________________________________________________________||
