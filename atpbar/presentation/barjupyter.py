from uuid import UUID

import ipywidgets as widgets
from IPython.display import display

from .base import Presentation, Report


class ProgressBarJupyter(Presentation):
    def __init__(self) -> None:
        super().__init__()
        self.interval = 0.05  # [second]

        self.container_widget = None
        self.active_box_list = list[widgets.HBox]()
        self.complete_box_list = list[widgets.HBox]()
        self.widget_dict = dict[
            UUID, tuple[widgets.HBox, widgets.IntProgress, widgets.HTML]
        ]()

    def __repr__(self) -> str:
        return '{}()'.format(self.__class__.__name__)

    def _present(self, report: Report) -> None:
        self._create_widgets()
        self._update_widgets()

    def _create_widgets(self) -> None:
        if self.container_widget is None:
            self.container_widget = widgets.VBox()
            display(self.container_widget)

        for task_id in self._new_task_ids:
            report = self._report_dict[task_id]
            self._create_widget(report)

    def _create_widget(self, report: Report) -> None:
        bar = widgets.IntProgress(
            value=report['done'],
            min=0,
            max=report['total'],
            description='',
            bar_style='',  # 'success', 'info', 'warning', 'danger' or ''
            orientation='horizontal',
        )
        label = widgets.HTML(value='')
        box = widgets.HBox([bar, label])
        self.active_box_list.append(box)
        if self.container_widget is not None:
            self.container_widget.children = (
                self.complete_box_list + self.active_box_list
            )
        self.widget_dict[report['task_id']] = (box, bar, label)

    def _update_widgets(self) -> None:
        for task_id in (
            self._finishing_task_ids + self._active_task_ids + self._new_task_ids
        ):
            report = self._report_dict[task_id]
            self._update_widget(report)

        self._reorder_widgets(report)

        if not self._new_task_ids and not self._active_task_ids:
            self.container_widget = None
            self.active_box_list[:] = []
            self.complete_box_list[:] = []
            self.widget_dict.clear()

    def _update_widget(self, report: Report) -> None:
        percent = float(report['done']) / report['total'] if report['total'] > 0 else 1
        percent = round(percent * 100, 2)
        percent_fmt = '{:6.2f}%'.format(percent)

        box = self.widget_dict[report['task_id']][0]
        box  # to silence not-used warning

        bar = self.widget_dict[report['task_id']][1]
        bar.value = report['done']
        bar.max = report['total']
        bar.description = percent_fmt
        if report['last']:
            bar.bar_style = 'success'

        label = self.widget_dict[report['task_id']][2]
        name_field_length = 32
        percent = float(report['done']) / report['total'] if report['total'] > 0 else 1
        bar = (':' * int(percent * 40)).ljust(40, ' ')
        percent = round(percent * 100, 2)
        name = report['name'][0:name_field_length]
        label.value = '<pre> | {:8d} / {:8d} |: {:<{}s}</pre>'.format(
            report['done'], report['total'], name, name_field_length
        )

    def _reorder_widgets(self, report: Report) -> None:
        for task_id in self._finishing_task_ids:
            box, bar, label = self.widget_dict[task_id]
            if box in self.active_box_list:
                self.active_box_list.remove(box)
                self.complete_box_list.append(box)
                if self.container_widget is not None:
                    self.container_widget.children = (
                        self.complete_box_list + self.active_box_list
                    )
