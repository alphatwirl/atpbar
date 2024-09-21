import os
import sys
from pathlib import Path

import pytest
from hypothesis import settings

if os.getenv('GITHUB_ACTIONS') == 'true':
    settings.register_profile('ci', deadline=None)
    settings.load_profile('ci')


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool:
    if collection_path.name == 'test_state.py' and sys.version_info < (3, 10):
        return True
    return False
