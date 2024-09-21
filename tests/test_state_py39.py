import sys
from unittest.mock import MagicMock, Mock, call

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from atpbar.machine import (
    Active,
    Callback,
    Disabled,
    Initial,
    ProgressReporter,
    Registered,
    State,
    Yielded,
)

pytestmark = pytest.mark.skipif(sys.version_info >= (3, 10), reason='for Python 3.9')


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
        if isinstance(prev, Initial):
            assert isinstance(self.state, Active)
            assert self.callback.mock_calls == [call.on_active()]
        else:
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

        with prev.fetch_reporter() as reporter:
            if isinstance(prev, Active):
                assert self.callback.mock_calls == [
                    call.fetch_reporter_in_active(),
                    call.fetch_reporter_in_active().__enter__(),
                ]
                assert (
                    reporter
                    is self.callback.fetch_reporter_in_active.return_value.__enter__.return_value
                )
            elif isinstance(prev, Yielded):
                assert self.callback.mock_calls == [
                    call.fetch_reporter_in_yielded(),
                    call.fetch_reporter_in_yielded().__enter__(),
                ]
                assert (
                    reporter
                    is self.callback.fetch_reporter_in_yielded.return_value.__enter__.return_value
                )
            elif isinstance(prev, Registered):
                assert self.callback.mock_calls == [
                    call.fetch_reporter_in_registered(),
                    call.fetch_reporter_in_registered().__enter__(),
                ]
                assert (
                    reporter
                    is self.callback.fetch_reporter_in_registered.return_value.__enter__.return_value
                )
            elif isinstance(prev, Disabled):
                assert self.callback.mock_calls == [
                    call.fetch_reporter_in_disabled(),
                    call.fetch_reporter_in_disabled().__enter__(),
                ]
                assert (
                    reporter
                    is self.callback.fetch_reporter_in_disabled.return_value.__enter__.return_value
                )
            else:
                assert self.callback.mock_calls == []
                assert reporter is self.reporter

    def on_yielded(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.on_yielded()
        if isinstance(prev, Active):
            assert isinstance(self.state, Yielded)
        else:
            assert self.state is prev
        assert self.callback.mock_calls == []

    def on_resumed(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.on_resumed()
        if isinstance(prev, Yielded):
            assert isinstance(self.state, Active)
            assert self.state is prev._active
        else:
            assert self.state is prev
        assert self.callback.mock_calls == []

    def flush(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.flush()
        if isinstance(prev, Initial):
            assert isinstance(self.state, Active)
            assert self.callback.mock_calls == [call.on_active()]
        elif isinstance(prev, Active):
            assert self.state is prev
            assert self.callback.mock_calls == [call.flush_in_active()]
        else:
            assert self.state is prev
            assert self.callback.mock_calls == []

    def shutdown(self) -> None:
        prev = self.state
        self.callback.reset_mock()
        self.state = prev.shutdown()
        assert isinstance(self.state, Initial)
        if isinstance(prev, Active):
            assert self.callback.mock_calls == [call.shutdown_in_active()]
        else:
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
