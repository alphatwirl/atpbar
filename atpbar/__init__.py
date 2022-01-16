# Tai Sakuma <tai.sakuma@gmail.com>
##__________________________________________________________________||
from ._version import get_versions
from .funcs import disable, find_reporter, flush, register_reporter
from .main import atpbar

__version__ = get_versions()["version"]
del get_versions

##__________________________________________________________________||
