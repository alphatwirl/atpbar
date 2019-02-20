# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ProgressReport(object):
    """A progress report

    Parameters
    ----------
    name : str
        A name of the task. It will be use as the label on the
        progress bars. If ``taskid`` is ``None``, it will be used to
        identify the task as well
    done : int
        The number of the iterations done so far
    total : int
        The total iterations to be done
    taskid : immutable, optional
        The task ID. If not given `name` will be used.

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
