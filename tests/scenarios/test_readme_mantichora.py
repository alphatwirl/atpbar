# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import time, random
import itertools
import threading
import multiprocessing

import pytest

from atpbar import atpbar
from mantichora import mantichora

##__________________________________________________________________||
def task(n, name):
    for i in atpbar(range(n), name=name):
        time.sleep(0.0001)

def run_with_mantichora(nprocesses, ntasks, niterations):
    # print(nprocesses, ntasks, niterations)
    with mantichora(nworkers=nprocesses) as mcore:
        for i in range(ntasks):
            name = 'task {}'.format(i)
            n = niterations[i]
            mcore.run(task, n, name)
        returns = mcore.returns()

# @pytest.mark.xfail()
@pytest.mark.parametrize('niterations', [[5, 4, 3], [5, 0, 1], [0], [1]])
@pytest.mark.parametrize('ntasks', [6, 3, 1, 0])
@pytest.mark.parametrize('nprocesses', [10, 6, 2, 1])
def test_mantichora(mock_create_presentation, wrap_end_pickup, nprocesses, ntasks, niterations):

    # make niterations as long as ntasks. repeat if necessary
    niterations = list(itertools.chain(*itertools.repeat(niterations, ntasks//len(niterations)+1)))[:ntasks]

    run_with_mantichora(nprocesses, ntasks, niterations)

    print()
    print(mock_create_presentation)

    assert 2 == wrap_end_pickup.call_count

    nreports_expected = sum(niterations) + ntasks
    presentations = mock_create_presentation.presentations

    assert 3 == len(presentations)

    progressbar0 = presentations[0]
    assert nreports_expected == len(progressbar0.reports)
    assert ntasks == len(progressbar0.taskids)
    assert ntasks == progressbar0.nfirsts
    assert ntasks == progressbar0.nlasts

    progressbar1 = presentations[1]
    assert 0 == len(progressbar1.reports)

    progressbar2 = presentations[2]
    assert 0 == len(progressbar2.reports)

##__________________________________________________________________||
