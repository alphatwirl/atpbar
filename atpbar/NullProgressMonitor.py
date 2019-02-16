# Tai Sakuma <tai.sakuma@gmail.com>

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

##__________________________________________________________________||
