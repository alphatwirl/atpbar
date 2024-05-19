'''Test if example scripts run

'''

from pathlib import Path

import pytest

here = Path(__file__).resolve().parent
example_dir = here.parent / 'examples'

exclude = [  # type: ignore
    'break_exception.py',
]

script_paths = list(example_dir.glob('**/*.py'))
script_paths = [p for p in script_paths if p.name not in exclude]
print(script_paths)


@pytest.mark.parametrize('script_path', script_paths)
@pytest.mark.script_launch_mode('subprocess')
def test_run_example_script(script_runner, script_path):
    ret = script_runner.run(script_path)
    assert ret.success
    assert ret.stderr == ''
