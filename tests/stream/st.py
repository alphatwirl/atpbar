from hypothesis import strategies as st


def st_text() -> st.SearchStrategy[str]:
    '''A strategy for text without control characters.'''
    return st.text(alphabet=st.characters(blacklist_categories=['Cc', 'Cs']))
