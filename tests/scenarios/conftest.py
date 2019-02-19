# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import threading

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from atpbar import flush
from atpbar.presentation.base import Presentation

##__________________________________________________________________||
@pytest.fixture()
def mock_progressbar():
    ret = mock.Mock(spec=Presentation)
    return ret

@pytest.fixture(autouse=True)
def mock_create_presentation(monkeypatch, mock_progressbar):
    ret = mock.Mock()
    ret.return_value = mock_progressbar
    module = sys.modules['atpbar.funcs']
    monkeypatch.setattr(module, 'create_presentation', ret)
    return ret

##__________________________________________________________________||
@pytest.fixture(autouse=True)
def global_variables(monkeypatch):
    module = sys.modules['atpbar.funcs']
    monkeypatch.setattr(module, '_presentation', None)
    monkeypatch.setattr(module, '_reporter', None)
    monkeypatch.setattr(module, '_pickup', None)
    monkeypatch.setattr(module, '_lock', threading.Lock())
    yield
    flush()

##__________________________________________________________________||
