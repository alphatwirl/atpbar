# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ProgressReport(object):
    """A progress report

    Parameters
    ----------
    name : str
        A name of the task. It will be use as the label on the
        progress bars.
    done : int
        The number of the iterations done so far
    total : int
        The total iterations to be done
    taskid : immutable
        The unique task ID.

    """

    def __init__(self, name, done, total, taskid):
        self.name = name
        self.done = done
        self.total = total
        self.taskid = taskid

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
