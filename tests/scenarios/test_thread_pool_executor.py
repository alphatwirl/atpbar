from concurrent.futures import ThreadPoolExecutor
from time import sleep

from hypothesis import given
from hypothesis import strategies as st

from atpbar import atpbar, flushing

from .utils import mock_presentations


def func(n: int, name: str) -> None:
    for _ in atpbar(range(n), name=name):
        sleep(0.0001)


@given(
    n_workers=st.integers(min_value=1, max_value=10),
    n_iterations=st.lists(
        st.integers(min_value=0, max_value=10), min_size=0, max_size=10
    ),
)
def test_thread_pool_executor(n_workers: int, n_iterations: list[int]) -> None:
    with mock_presentations() as presentations:
        with flushing(), ThreadPoolExecutor(max_workers=n_workers) as executor:
            for n in n_iterations:
                _ = executor.submit(func, n, name=f'Job {n}')

        n_jobs = len(n_iterations)

        if n_jobs == 0:
            assert len(presentations) == 1  # created by flushing()
            assert len(presentations[0].reports) == 0
            return

        assert len(presentations) == 2

        progressbar0 = presentations[0]
        assert len(progressbar0.reports) == sum(n_iterations) + n_jobs
        assert len(progressbar0.task_ids) == n_jobs
        assert progressbar0.n_firsts == n_jobs
        assert progressbar0.n_lasts == n_jobs

        progressbar1 = presentations[1]
        assert len(progressbar1.reports) == 0
