# Tai Sakuma <tai.sakuma@gmail.com>
import os

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
    pid :
        The process ID, e.g., the value returned by `os.getpid()`
    in_main_thread : bool
        True if the task is running in the main thread of the process.
        False otherwise

    """

    def __init__(self, name, done, total, taskid, pid, in_main_thread):
        self.name = name
        self.done = done
        self.total = total
        self.taskid = taskid
        self.pid = pid
        self.in_main_thread = in_main_thread

    def __repr__(self):
        name_value_pairs = (
            ('taskid', self.taskid),
            ('name', self.name),
            ('done', self.done),
            ('total', self.total),
            ('pid', self.pid),
            ('in_main_thread', self.in_main_thread),
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
