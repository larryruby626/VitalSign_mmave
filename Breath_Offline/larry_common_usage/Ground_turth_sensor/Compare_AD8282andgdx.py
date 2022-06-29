import sys

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

from larry_common_usage.pyqt5.DrawingWidget import DrawingWidget
from larry_common_usage.Ground_turth_sensor.AD8232 import  AD8232
from larry_common_usage.Ground_turth_sensor.go_direct_sensor import  GoDirectSensor


class SinglePlotWidget(QWidget):
    def __init__(self,app, title=""):
        super(SinglePlotWidget, self).__init__()
        self.app = app
        self.plot_widget_ard = DrawingWidget("AD8232")
        self.plot_widget_gdx = DrawingWidget("Go direct")
        self.plot_widget_HB = DrawingWidget("HB")
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.plot_widget_ard,0,0)
        self.Layout.addWidget(self.plot_widget_gdx,0,1)
        self.Layout.addWidget(self.plot_widget_HB,1,0,1,2)
        self.setLayout(self.Layout)
        self.ad8232_line = self.plot_widget_ard.add_line_obj("w")
        self.gdx_line = self.plot_widget_gdx.add_line_obj("r")
        self.ad8232_HB = self.plot_widget_ard.add_line_obj("w")
        self.gdx_HB = self.plot_widget_gdx.add_line_obj("r")
        self.th_ad8232 = AD8232(buffer_len=256)
        self.th_gdx = GoDirectSensor(sensor_numb=1, samplerate= 10, buffer_len=256)

        self.th_gdx.GoDirectSensor_V.connect(self.update_gdx)
        self.th_ad8232.AD8232_V.connect(self.update_ad8232)

    #
    # def start_run_thread(self):


    def update_gdx(self, buff_gdx):
        self.plot_widget_gdx.line_obj_SetData(self.gdx_line, buff_gdx)
        self.app.processEvents()

    def update_ad8232(self, buff):
        self.plot_widget_ard.line_obj_SetData(self.ad8232_line, buff)
        self.app.processEvents()

if __name__ == '__main__':
    app = QApplication([])
    x = SinglePlotWidget(app)
    x.show()
    x.th_ad8232.run()
    x.th_gdx.run()
    sys.exit(app.exec_())
