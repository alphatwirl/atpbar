# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from atpbar.monitor import ProgressMonitor
from atpbar.presentation.base import Presentation

##__________________________________________________________________||
class MockProgressBar(Presentation):
    def _present(self):
        pass

##__________________________________________________________________||
def build_ProgressMonitor():
    return ProgressMonitor(presentation=MockProgressBar())

builds = [build_ProgressMonitor]
build_ids = ['ProgressMonitor']

##__________________________________________________________________||
@pytest.mark.parametrize('build', builds, ids=build_ids)
def test_monitor(build):
    obj = build()
    obj.begin()
    obj.create_reporter()
    obj.end()

##__________________________________________________________________||
