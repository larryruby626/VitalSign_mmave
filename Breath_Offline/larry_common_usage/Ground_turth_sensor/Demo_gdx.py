import sys
import numpy as np

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout,QLabel

from larry_common_usage.pyqt5.DrawingWidget import DrawingWidget
from larry_common_usage.Calc_heartbeat.IBI_process import Calc_groundtruth_HB
from larry_common_usage.Ground_turth_sensor.go_direct_sensor import  GoDirectSensor


class SinglePlotWidget(QWidget):
    def __init__(self,app, title=""):
        super(SinglePlotWidget, self).__init__()
        self.app = app
        self.plot_widget_gdx = DrawingWidget("Go direct")
        self.plot_widget_HB = DrawingWidget("HB")
        self.Layout = QGridLayout()
        self.lb_t = QLabel("Go direct Heartbeat")
        self.lb_v = QLabel("")
        self.HB = []
        self.time = np.linspace(0,600,600)/100
        self.Layout.addWidget(self.plot_widget_gdx,0,0)
        self.Layout.addWidget(self.plot_widget_HB,0,1)
        self.Layout.addWidget(self.lb_t,1,0,1,1)
        self.Layout.addWidget(self.lb_v,1,1,1,1)
        self.setLayout(self.Layout)
        self.gdx_line = self.plot_widget_gdx.add_line_obj("r")
        self.gdx_HB = self.plot_widget_HB.add_line_obj("w")

        self.th_gdx = GoDirectSensor(sensor_numb=1, samplerate=10, buffer_len=600)
        self.th_gdx.GoDirectSensor_V.connect(self.update_gdx)

    def update_gdx(self, buff_gdx):

        hz = Calc_groundtruth_HB(buff_gdx, self.time, "gdx")
        if hz is not None:
            self.HB.append((hz))
        else:
            self.HB.append(self.HB[-1])

        self.lb_v.setText(str(hz))
        self.plot_widget_gdx.line_obj_SetData(self.gdx_line, buff_gdx)
        self.plot_widget_HB.line_obj_SetData(self.gdx_HB, self.HB)

        self.app.processEvents()

if __name__ == '__main__':
    app = QApplication([])
    x = SinglePlotWidget(app)
    x.show()
    x.th_gdx.run()
    sys.exit(app.exec_())
