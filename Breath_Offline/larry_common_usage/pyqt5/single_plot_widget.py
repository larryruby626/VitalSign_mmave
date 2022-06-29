import sys

from PyQt5.QtWidgets import QApplication, QWidget

from larry_common_usage.pyqt5.DrawingWidget import DrawingWidget


class SinglePlotWidget(QWidget):
    def __init__(self, title=""):
        super(SinglePlotWidget, self).__init__()

        self.plot_widget = DrawingWidget(title)
        self.plot_line = self.plot_widget.add_line_obj()

    def update(self, update_data):
        self.plot_widget.line_obj_SetData(self.plot_line, update_data)


if __name__ == '__main__':
    app = QApplication([])
    x = SinglePlotWidget()
    x.plot_widget.show()
    sys.exit(app.exec_())
