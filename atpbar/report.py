# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ProgressReport(object):
    """A progress report

    Args:
        name (str): the name of the task. if ``taskid`` is ``None``, used to identify the task
        done (int): the number of the iterations done so far
        total (int): the total iterations to be done
        taskid (immutable, optional): if given, used to identify the task. useful if multiple tasks have the same name
    """

    def __init__(self, name, done, total, taskid=None):
        self.taskid = taskid if taskid is not None else name
        self.name = name
        self.done = done
        self.total = total

    def __repr__(self):
        name_value_pairs = (
            ('taskid', self.taskid),
            ('name', self.name),
            ('done', self.done),
            ('total', self.total),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def last(self):
         return self.done == self.total

    def first(self):
         return self.done == 0

##__________________________________________________________________||
