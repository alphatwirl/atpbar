import os

from hypothesis import settings

if os.getenv('GITHUB_ACTIONS') == 'true':
    settings.register_profile('ci', deadline=None)
    settings.load_profile('ci')
