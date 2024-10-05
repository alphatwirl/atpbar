from hypothesis import given
from hypothesis import strategies as st

from atpbar import atpbar, disable

from .utils import mock_presentations


@given(
    n_outer=st.integers(min_value=0, max_value=5),
    n_inner=st.integers(min_value=0, max_value=5),
    to_disable=st.booleans(),
)
def test_nested_loop(n_outer: int, n_inner: int, to_disable: bool) -> None:
    with mock_presentations() as presentations:
        if to_disable:
            disable()

        for _ in atpbar(range(n_outer)):
            for _ in atpbar(range(n_inner)):
                pass

        if to_disable:
            assert len(presentations) == 0
            return

        assert len(presentations) == 2

        progressbar0 = presentations[0]
        assert len(progressbar0.reports) == (n_inner + 1 + 1) * n_outer + 1
        assert len(progressbar0.task_ids) == n_outer + 1
        assert progressbar0.n_firsts == n_outer + 1
        assert progressbar0.n_lasts == n_outer + 1

        progressbar1 = presentations[1]
        assert len(progressbar1.reports) == 0
