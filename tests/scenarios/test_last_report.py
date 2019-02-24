# Tai Sakuma <tai.sakuma@gmail.com>
import time, random
import collections

import pytest

from atpbar import atpbar
from atpbar import flush

##__________________________________________________________________||
@pytest.mark.parametrize('method', ['break', 'exception'])
@pytest.mark.parametrize('niterations', [10, 1, 0])
@pytest.mark.parametrize('ndones', [10, 4, 1, 0])
def test_one_loop_break_exception(mock_create_presentation, wrap_end_pickup, niterations, ndones, method):
    ndones = min(ndones, niterations)

    def task_break(ndones, niterations):
        for i in atpbar(range(niterations)):
            if i == ndones:
                break

    def task_exception(ndones, niterations):
        for i in atpbar(range(niterations)):
            if i == ndones:
                raise Exception()

    #
    if method == 'break':
        task_break(ndones, niterations)
    else:
        if ndones < niterations:
            with pytest.raises(Exception):
                task_exception(ndones, niterations)
        else:
            task_exception(ndones, niterations)

    ## print()
    ## print(mock_create_presentation)

    #
    assert 1 == wrap_end_pickup.call_count

    nreports_expected = ndones + 1 + bool(ndones<niterations)
    presentations = mock_create_presentation.presentations

    assert 2 == len(presentations) # created when atpbar started and ended

    #
    progressbar0 = presentations[0]
    assert nreports_expected == len(progressbar0.reports)
    assert 1 == len(progressbar0.taskids)
    assert 1 == progressbar0.nfirsts
    assert 1 == progressbar0.nlasts
    done_total_list_expected = [(ndones, niterations)]
    done_total_list_actual = [(d['done'], d['total']) for d in progressbar0._report_dict.values()]
    assert collections.Counter(done_total_list_expected) == collections.Counter(done_total_list_actual)

    #
    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)

##__________________________________________________________________||
