from atpbar import callback, funcs
from atpbar.progress_report import reporter

from .utils import mock_presentations


def test_mock_presentations() -> None:

    class MockException(Exception):
        pass

    func_machine = funcs._machine
    interval = reporter.DEFAULT_INTERVAL
    create_presentation = callback.create_presentation
    try:
        with mock_presentations() as presentations:
            assert func_machine is not funcs._machine
            assert interval != reporter.DEFAULT_INTERVAL
            assert create_presentation is not callback.create_presentation
            presentations
            raise MockException()
    except MockException:
        pass
    finally:
        assert func_machine is funcs._machine
        assert interval == reporter.DEFAULT_INTERVAL
        assert create_presentation is callback.create_presentation
