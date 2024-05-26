import multiprocessing
import unittest.mock as mock
from collections.abc import Iterator

import pytest

from atpbar.progress_report.pickup import ProgressReportPickup


class TestStart:

    @pytest.fixture()
    def presentation(self) -> mock.Mock:
        return mock.Mock()

    @pytest.fixture()
    def queue(self) -> multiprocessing.Queue:
        return multiprocessing.Queue()

    @pytest.fixture()
    def pickup(
        self, queue: multiprocessing.Queue, presentation: mock.Mock
    ) -> ProgressReportPickup:
        presentation.active.return_value = True
        return ProgressReportPickup(queue, presentation)

    def test_end(
        self,
        pickup: ProgressReportPickup,
        queue: multiprocessing.Queue,
        presentation: mock.Mock,
    ) -> None:
        pickup.end()

    def test_daemon(
        self,
        pickup: ProgressReportPickup,
        queue: multiprocessing.Queue,
        presentation: mock.Mock,
    ) -> None:
        pass
        # it is ok not to execute `pickup.end()`.


class TestRunUntilTheEndOrderArrives:

    @pytest.fixture()
    def mock_thread_start(self, monkeypatch: pytest.MonkeyPatch) -> Iterator[mock.Mock]:
        y = mock.Mock()
        monkeypatch.setattr(ProgressReportPickup, 'start', y)
        yield y

    @pytest.fixture()
    def mock_queue(self) -> mock.Mock:
        return mock.Mock()

    @pytest.fixture()
    def presentation(self) -> mock.Mock:
        return mock.Mock()

    @pytest.fixture()
    def pickup(
        self,
        mock_queue: mock.Mock,
        presentation: mock.Mock,
        mock_thread_start: mock.Mock,
    ) -> Iterator[ProgressReportPickup]:
        y = ProgressReportPickup(mock_queue, presentation)
        yield y

    @pytest.fixture(autouse=True)
    def mock_short_sleep(
        self,
        pickup: ProgressReportPickup,
        monkeypatch: pytest.MonkeyPatch,
    ) -> Iterator[mock.Mock]:
        y = mock.Mock()
        monkeypatch.setattr(pickup, '_short_sleep', y)
        yield y

    def test_no_report(
        self,
        pickup: ProgressReportPickup,
        mock_queue: mock.Mock,
        presentation: mock.Mock,
    ) -> None:
        mock_queue.empty.side_effect = [False, True]
        mock_queue.get.side_effect = [None]
        pickup._run_until_the_end_order_arrives()
        assert [] == presentation.mock_calls
        assert [mock.call(), mock.call()] == mock_queue.empty.mock_calls
        assert 0 == pickup._short_sleep.call_count  # type: ignore

    def test_one_report(
        self,
        pickup: ProgressReportPickup,
        mock_queue: mock.Mock,
        presentation: mock.Mock,
    ) -> None:
        report = mock.MagicMock()
        mock_queue.empty.side_effect = [False, False, True]
        mock_queue.get.side_effect = [report, None]
        pickup._run_until_the_end_order_arrives()
        assert [mock.call.present(report)] == presentation.mock_calls
        assert 0 == pickup._short_sleep.call_count  # type: ignore

    def test_one_report_once_empty(
        self,
        pickup: ProgressReportPickup,
        mock_queue: mock.Mock,
        presentation: mock.Mock,
    ) -> None:
        report1 = mock.MagicMock()
        mock_queue.empty.side_effect = [
            False,
            True,
            False,
            True,
        ]  # it becomes empty once
        mock_queue.get.side_effect = [report1, None]
        pickup._run_until_the_end_order_arrives()
        assert [mock.call.present(report1)] == presentation.mock_calls
        assert 1 == pickup._short_sleep.call_count  # type: ignore

    def test_two_reports(
        self,
        pickup: ProgressReportPickup,
        mock_queue: mock.Mock,
        presentation: mock.Mock,
    ) -> None:
        report1 = mock.MagicMock()
        report2 = mock.MagicMock()
        mock_queue.empty.side_effect = [False, False, False, True]
        mock_queue.get.side_effect = [report1, None, report2]  # report2 arrives
        # after the end_order
        pickup._run_until_the_end_order_arrives()
        assert [
            mock.call.present(report1),
            mock.call.present(report2),
        ] == presentation.mock_calls
        assert 0 == pickup._short_sleep.call_count  # type: ignore


class TestRunUntilReportsStopComing:

    @pytest.fixture()
    def mock_thread_start(self, monkeypatch: pytest.MonkeyPatch) -> Iterator[mock.Mock]:
        y = mock.Mock()
        monkeypatch.setattr(ProgressReportPickup, 'start', y)
        yield y

    @pytest.fixture()
    def mock_queue(self) -> mock.Mock:
        return mock.Mock()

    @pytest.fixture()
    def presentation(self) -> mock.Mock:
        return mock.Mock()

    @pytest.fixture()
    def pickup(
        self,
        mock_queue: mock.Mock,
        presentation: mock.Mock,
        mock_thread_start: mock.Mock,
    ) -> ProgressReportPickup:
        return ProgressReportPickup(mock_queue, presentation)

    @pytest.fixture(autouse=True)
    def mock_short_sleep(
        self,
        pickup: ProgressReportPickup,
        monkeypatch: pytest.MonkeyPatch,
    ) -> Iterator[mock.Mock]:
        y = mock.Mock()
        monkeypatch.setattr(pickup, '_short_sleep', y)
        yield y

    @pytest.fixture(autouse=True)
    def mock_time(self, monkeypatch: pytest.MonkeyPatch) -> Iterator[mock.Mock]:
        ret = mock.Mock()
        ret.time.return_value = 1000.0
        from atpbar.progress_report import pickup as m

        monkeypatch.setattr(m, 'time', ret)
        return ret

    def test_no_report(
        self,
        pickup: ProgressReportPickup,
        mock_time: mock.Mock,
        presentation: mock.Mock,
    ) -> None:
        presentation.active.side_effect = [False]
        pickup._run_until_reports_stop_coming()
        assert [] == presentation.present.mock_calls
        assert 0 == pickup._short_sleep.call_count  # type: ignore

    def test_one_report(
        self,
        pickup: ProgressReportPickup,
        mock_time: mock.Mock,
        mock_queue: mock.Mock,
        presentation: mock.Mock,
    ) -> None:
        presentation.active.side_effect = [True, False]
        report = mock.MagicMock()
        mock_queue.empty.side_effect = [False, False, True]
        mock_queue.get.side_effect = [report, None]
        pickup._run_until_reports_stop_coming()
        assert [mock.call(report)] == presentation.present.mock_calls
        assert 1 == pickup._short_sleep.call_count  # type: ignore

    def test_one_report_timeout(
        self,
        pickup: ProgressReportPickup,
        mock_time: mock.Mock,
        mock_queue: mock.Mock,
        presentation: mock.Mock,
    ) -> None:
        presentation.active.return_value = True
        report = mock.MagicMock()
        mock_queue.empty.return_value = True
        mock_queue.get.side_effect = [report, None]
        mock_time.time.side_effect = [1000.0, 1000.2, 1003.0]
        pickup._run_until_reports_stop_coming()
        assert [] == presentation.present.mock_calls
        assert 1 == pickup._short_sleep.call_count  # type: ignore
