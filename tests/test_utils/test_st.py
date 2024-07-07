from hypothesis import given, settings

from .st import st_text


@settings(max_examples=500)
@given(text=st_text())
def test_st_text(text: str) -> None:
    assert not text.endswith('\n')
