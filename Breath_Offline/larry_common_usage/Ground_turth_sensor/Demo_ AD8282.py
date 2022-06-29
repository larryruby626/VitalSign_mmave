import sys

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from larry_common_usage.Calc_heartbeat.IBI_process import Calc_groundtruth_HB
from larry_common_usage.Ground_turth_sensor.AD8232 import AD8232
from larry_common_usage.pyqt5.DrawingWidget import DrawingWidget


class SinglePlotWidget(QWidget):
    def __init__(self, app, title=""):
        super(SinglePlotWidget, self).__init__()
        self.app = app
        self.plot_widget_ard = DrawingWidget("AD8232")
        self.plot_widget_HB = DrawingWidget("HB")
        self.Layout = QGridLayout()
        self.lb_t = QLabel("AD8232 Heartbeat")
        self.lb_v = QLabel("")
        self.HB = []
        self.Layout.addWidget(self.plot_widget_ard, 0, 0)
        self.Layout.addWidget(self.plot_widget_HB, 0, 1)
        self.Layout.addWidget(self.lb_t, 1, 0, 1, 0)
        self.Layout.addWidget(self.lb_v, 1, 0, 1, 1)
        self.setLayout(self.Layout)
        self.ad8232_line = self.plot_widget_ard.add_line_obj("w")
        self.ad8232_HB = self.plot_widget_HB.add_line_obj("w")
        self.th_ad8232 = AD8232(buffer_len=600)
        self.th_ad8232.AD8232_V.connect(self.update_ad8232)

    def update_ad8232(self, buff, time):
        hz = Calc_groundtruth_HB(buff, time, "ecg")
        if hz is not None:
            self.HB.append((hz))
        else:
            self.HB.append(self.HB[-1])
        self.lb_v.setText(str(hz))
        # print(self.HB)
        self.plot_widget_ard.line_obj_SetData(self.ad8232_line, buff)
        self.plot_widget_HB.line_obj_SetData(self.ad8232_HB, self.HB )

        self.app.processEvents()


if __name__ == '__main__':
    app = QApplication([])
    x = SinglePlotWidget(app)
    x.show()
    x.th_ad8232.run()
    sys.exit(app.exec_())
