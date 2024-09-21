import sys
from pathlib import Path

import pytest


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool:
    if collection_path.name == 'test_print.py' and sys.version_info < (3, 10):
        return True
    return False
