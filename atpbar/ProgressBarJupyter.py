# Tai Sakuma <tai.sakuma@gmail.com>
import ipywidgets as widgets
from IPython.display import display

from .presentation import Presentation

##__________________________________________________________________||
class ProgressBarJupyter(Presentation):
    def __init__(self):
        super(ProgressBarJupyter, self).__init__()
        self.interval = 0.05 # [second]

        self.container_widget = None
        self.active_box_list = [ ]
        self.complete_box_list = [ ]
        self.widget_dict = { } # {taskid: [box, bar, label]}

        self._read_time()

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def _present(self):
        self._create_widgets()
        self._update_widgets()

    def _create_widgets(self):
        if self.container_widget is None:
            self.container_widget = widgets.VBox()
            display(self.container_widget)

        for taskid in self._new_taskids:
            report = self._report_dict[taskid]
            self._create_widget(report)

    def _create_widget(self, report):
        bar = widgets.IntProgress(
            value=report.done, min=0, max=report.total,
            description='',
            bar_style='', # 'success', 'info', 'warning', 'danger' or ''
            orientation='horizontal'
         )
        label = widgets.HTML(value='')
        box = widgets.HBox([bar, label])
        self.active_box_list.append(box)
        self.container_widget.children = self.complete_box_list + self.active_box_list
        self.widget_dict[report.taskid] = [box, bar, label]

    def _update_widgets(self):
        for taskid in self._finishing_taskids + self._active_taskids + self._new_taskids:
            report = self._report_dict[taskid]
            self._update_widget(report)

        self._reorder_widgets(report)

    def _update_widget(self, report):

        percent = float(report.done)/report.total if report.total > 0 else 1
        percent = round(percent * 100, 2)
        percent = '<pre>{:6.2f}%</pre>'.format(percent)

        box = self.widget_dict[report.taskid][0]

        bar = self.widget_dict[report.taskid][1]
        bar.value = report.done
        bar.max = report.total
        bar.description = percent
        if report.done >= report.total:
            bar.bar_style = 'success'

        label = self.widget_dict[report.taskid][2]
        name_field_length = 32
        percent = float(report.done)/report.total if report.total > 0 else 1
        bar = (':' * int(percent * 40)).ljust(40, " ")
        percent = round(percent * 100, 2)
        name = report.name[0:name_field_length]
        label.value = '<pre> | {:8d} / {:8d} |:  {:<{}s}</pre>'.format(report.done, report.total, name, name_field_length)

    def _reorder_widgets(self, report):
        for taskid in self._finishing_taskids:
            box, bar, label = self.widget_dict[taskid]
            if box in self.active_box_list:
                self.active_box_list.remove(box)
                self.complete_box_list.append(box)
                self.container_widget.children = self.complete_box_list + self.active_box_list

##__________________________________________________________________||
