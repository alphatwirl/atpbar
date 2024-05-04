
"""Test if an example script runs

"""
from pathlib import Path

import pytest

here = Path(__file__).resolve().parent
example_dir = here.parent.joinpath('examples')


params = [
    'example_01_one_loop.py',
    'example_02_nested_loops.py',
    'example_03_threading.py',
    'example_04_multiprocessing.py',
]
@pytest.mark.parametrize('script_name', params)
@pytest.mark.script_launch_mode('subprocess')
def test_run_example_script(script_runner, script_name):
    script_path = example_dir.joinpath(script_name)
    ret = script_runner.run(script_path)
    assert ret.success
    assert ret.stderr == ''


