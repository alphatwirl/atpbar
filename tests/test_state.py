from unittest.mock import MagicMock, Mock, call

from hypothesis import given, settings
from hypothesis import strategies as st

from atpbar.machine import (
    Active,
    Callback,
    Disabled,
    Initial,
    Lock,
    ProgressReporter,
    Registered,
    State,
    Yielded,
)


class StatefulTest:
    def __init__(self) -> None:
        self.callback = MagicMock(spec=Callback)
        self.reporter = Mock(spec=ProgressReporter)
        self.callback.reporter = self.reporter
        self.state: State = Initial(callback=self.callback)

    def prepare_reporter(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.prepare_reporter()
        match prev:
            case Initial():
                assert isinstance(self.state, Active)
                assert self.callback.mock_calls == [call.on_active()]
            case _:
                assert self.state is prev
                assert self.callback.mock_calls == []

    def register_reporter(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        reporter = Mock(spec=ProgressReporter)
        self.state = prev.register_reporter(reporter)
        assert isinstance(self.state, Registered)
        assert self.callback.mock_calls == [call.on_registered(reporter)]

    def disable(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.disable()
        assert isinstance(self.state, Disabled)
        assert self.callback.mock_calls == [call.on_disabled()]

    def fetch_reporter(self) -> None:
        prev = self.state
        self.callback.reset_mock()

        lock = Lock()

        with prev.fetch_reporter(lock=lock) as reporter:
            match prev:
                case Active():
                    assert self.callback.mock_calls == [
                        call.fetch_reporter_in_active(lock=lock),
                        call.fetch_reporter_in_active(lock=lock).__enter__(),
                    ]
                    assert (
                        reporter
                        is self.callback.fetch_reporter_in_active.return_value.__enter__.return_value
                    )
                case Yielded():
                    assert self.callback.mock_calls == [
                        call.fetch_reporter_in_yielded(lock=lock),
                        call.fetch_reporter_in_yielded(lock=lock).__enter__(),
                    ]
                    assert (
                        reporter
                        is self.callback.fetch_reporter_in_yielded.return_value.__enter__.return_value
                    )
                case Registered():
                    assert self.callback.mock_calls == [
                        call.fetch_reporter_in_registered(lock=lock),
                        call.fetch_reporter_in_registered(lock=lock).__enter__(),
                    ]
                    assert (
                        reporter
                        is self.callback.fetch_reporter_in_registered.return_value.__enter__.return_value
                    )
                case Disabled():
                    assert self.callback.mock_calls == [
                        call.fetch_reporter_in_disabled(lock=lock),
                        call.fetch_reporter_in_disabled(lock=lock).__enter__(),
                    ]
                    assert (
                        reporter
                        is self.callback.fetch_reporter_in_disabled.return_value.__enter__.return_value
                    )
                case _:
                    assert self.callback.mock_calls == []
                    assert reporter is self.reporter

    def on_yielded(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.on_yielded()
        match prev:
            case Active():
                assert isinstance(self.state, Yielded)
            case _:
                assert self.state is prev
        assert self.callback.mock_calls == []

    def on_resumed(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.on_resumed()
        match prev:
            case Yielded():
                assert isinstance(self.state, Active)
                assert self.state is prev._active
            case _:
                assert self.state is prev
        assert self.callback.mock_calls == []

    def flush(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.flush()
        match prev:
            case Initial():
                assert isinstance(self.state, Active)
                assert self.callback.mock_calls == [call.on_active()]
            case Active():
                assert self.state is prev
                assert self.callback.mock_calls == [call.flush_in_active()]
            case _:
                assert self.state is prev
                assert self.callback.mock_calls == []

    def shutdown(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.shutdown()
        assert isinstance(self.state, Initial)
        match prev:
            case Active():
                assert self.callback.mock_calls == [call.shutdown_in_active()]
            case _:
                assert self.callback.mock_calls == []


@settings(max_examples=500)
@given(data=st.data())
def test_state(data: st.DataObject) -> None:
    test = StatefulTest()

    METHODS = [
        test.prepare_reporter,
        test.register_reporter,
        test.disable,
        test.fetch_reporter,
        test.on_yielded,
        test.on_resumed,
        test.flush,
        test.shutdown,
    ]

    methods = data.draw(st.lists(st.sampled_from(METHODS)))

    for method in methods:
        method()
