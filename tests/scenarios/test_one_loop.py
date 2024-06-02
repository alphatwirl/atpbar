from hypothesis import given
from hypothesis import strategies as st

from atpbar import atpbar, disable

from .utils import mock_presentations


@given(n_iterations=st.integers(min_value=0, max_value=10), to_disable=st.booleans())
def test_one_loop(n_iterations: int, to_disable: bool) -> None:

    with mock_presentations() as presentations:

        if to_disable:
            disable()

        for _ in atpbar(range(n_iterations)):
            pass

        if to_disable:
            assert len(presentations) == 0
            return

        assert len(presentations) == 2

        progressbar0 = presentations[0]
        assert len(progressbar0.reports) == n_iterations + 1
        assert len(progressbar0.task_ids) == 1
        assert progressbar0.n_firsts == 1
        assert progressbar0.n_lasts == 1

        progressbar1 = presentations[1]
        assert len(progressbar1.reports) == 0
