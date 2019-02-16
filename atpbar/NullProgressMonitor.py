# Tai Sakuma <tai.sakuma@gmail.com>

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
class NullProgressMonitor(object):
    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def begin(self):
        pass

    def end(self):
        pass

    def create_reporter(self):
        return None

    @_deprecated(msg='use create_reporter() instead')
    def createReporter(self):
        return self.create_reporter()


##__________________________________________________________________||
