import os

import pytest


@pytest.mark.script_launch_mode("subprocess")
def test_run(script_runner):

    cwd = os.path.dirname(os.path.abspath(__file__))

    script_path = os.path.join(".", "script.py")
    args = []
    ret = script_runner.run(script_path, *args, cwd=cwd)
    assert ret.success
    assert "" == ret.stderr
    assert ":       10 /       10 (100.00%):" in ret.stdout
