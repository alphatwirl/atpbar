# Tai Sakuma <tai.sakuma@gmail.com>
import time, random

import pytest

from atpbar import atpbar
from atpbar import flush

##__________________________________________________________________||
def test_one_loop_break(mock_progressbar, wrap_end_pickup):
    for i in atpbar(range(4)):
        if i == 2:
            break
    assert 1 == wrap_end_pickup.call_count
    assert len(mock_progressbar.present.call_args_list) >= 2

def test_one_loop_raise(mock_progressbar, wrap_end_pickup):
    with pytest.raises(Exception):
        for i in atpbar(range(4)):
            if i == 2:
                raise Exception()
    assert 1 == wrap_end_pickup.call_count
    assert len(mock_progressbar.present.call_args_list) >= 2


##__________________________________________________________________||
