import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QSlider, QHBoxLayout \
    , QLabel, QPushButton, QCheckBox

from larry_common_usage.pyqt5.Custom_lbte import Custom_lbte
from larry_common_usage.pyqt5.DrawingFFT import Drawing_vitalsign
# from larry_common_usage.pyqt5.DrawingFFT import Drawing_vitalsign
from larry_common_usage.pyqt5.DrawingWidget import DrawingWidget
from larry_common_usage.pyqt5.Heatmap_widget import phase_map_widget


class WatchWidget(QWidget):
    def __init__(self, parent=None):
        super(WatchWidget, self).__init__(parent)  # parent

        self.ww = QWidget()
        self.hb = QHBoxLayout()
        self.hb.setSpacing(15)
        self.build_plotwdidget()
        self.build_te_gridlayout()
        self.build_btn_gridlayout()
        self.build_slider_gridlayout()
        self.hb.addLayout(self.slider_grid)
        self.hb.addLayout(self.text_grid)
        self.hb.addLayout(self.btn_grid)
        self.grid = QGridLayout()
        self.ww.setLayout(self.hb)
        self.setLayout(self.grid)
        self.grid.addWidget(self.phase_map_widget, 0, 0, 1, 2)
        self.grid.addWidget(self.phase_widget, 1, 0, 1, 1)
        self.grid.addWidget(self.psd_widget, 1, 1, 1, 1)

        self.grid.addWidget(self.ww, 2, 0, 1, 4)

    def build_plotwdidget(self):
        self.phase_map_widget = phase_map_widget("Phase map ")
        self.phase_widget = DrawingWidget("uwrapping filtered phase")  # plot3
        self.phase_plot_N = self.phase_widget.add_line_obj()
        self.phase_plot_phasediff = self.phase_widget.add_line_obj()
        self.phase_plot_cwt = self.phase_widget.add_line_obj()
        self.phase_plot_vmd = self.phase_widget.add_line_obj()
        self.phase_plot_phasecoheren = self.phase_widget.add_line_obj()
        self.phase_plot_simulation = self.phase_widget.add_line_obj()

        self.psd_widget = DrawingWidget("Phase PSD")  # plot4
        self.psd_plot_N = self.psd_widget.add_line_obj()
        self.psd_plot_phasediff = self.psd_widget.add_line_obj()
        self.psd_plot_cwt = self.psd_widget.add_line_obj()
        self.psd_plot_vmd = self.psd_widget.add_line_obj()
        self.psd_plot_phasecoheren = self.psd_widget.add_line_obj()
        self.psd_plot_gt = self.psd_widget.add_line_obj()
        self.psd_plot_simulation = self.psd_widget.add_line_obj()

    def build_slider_gridlayout(self):
        self.slider_grid = QGridLayout()
        lb_slider_index = QLabel("Current idx:")
        lb_slider_w_len = QLabel("window Len:")
        self.btn = QPushButton("update")
        self.nx_btn = QPushButton("Next")
        self.pre_btn = QPushButton("Pre")
        self.slider = QSlider(Qt.Horizontal)
        self.slider_w_len = QSlider(Qt.Horizontal)
        self.index = Custom_lbte("Index:", "0", 30, 60, 30, 100)
        self.window_len = Custom_lbte("Window len:", "0", 30, 60, 30, 100)
        self.slider_grid.addLayout(self.index, 0, 0, 1, 1)
        self.slider_grid.addLayout(self.window_len, 0, 2, 1, 1)
        self.slider_grid.addWidget(lb_slider_index, 1, 0, 1, 1)
        self.slider_grid.addWidget(self.slider, 1, 1, 1, 3)
        self.slider_grid.addWidget(lb_slider_w_len, 2, 0, 1, 1)
        self.slider_grid.addWidget(self.slider_w_len, 2, 1, 1, 3)
        self.slider_grid.addWidget(self.btn, 3, 2, 1, 1)
        self.slider_grid.addWidget(self.pre_btn, 3, 1, 1, 1)
        self.slider_grid.addWidget(self.nx_btn, 3, 3, 1, 1)

    def build_te_gridlayout(self):
        self.text_grid = QGridLayout()
        self.targetbin = Custom_lbte("targetbin:", "0", 30, 60, 30, 60)
        self.Arduino_HB = Custom_lbte("Ardiuno HB:", "0", 30, 60, 30, 60)
        self.Calc_RR = Custom_lbte("Calc RR:", "0", 30, 60, 30, 60)
        self.text_grid.addLayout(self.targetbin, 0, 0, 1, 1)
        self.text_grid.addLayout(self.Arduino_HB, 1, 0, 1, 1)
        self.text_grid.addLayout(self.Calc_RR, 2, 0, 1, 1)

    def build_btn_gridlayout(self):
        self.btn_grid = QGridLayout()

        self.cbbtn_nofilter = QCheckBox("show no filter spectral")
        self.cbbtn_phase_diff = QCheckBox("show phase diff spectral")
        self.cbbtn_cwt  = QCheckBox("show phase CWT spectral")
        self.cbbtn_vmd  = QCheckBox("show phase VMD spectral")
        self.cbbtn_phase_cohere = QCheckBox("show Phase-coherence method spectral")
        self.cbbtn_gt = QCheckBox("show Arduino HB")
        self.cbbtn_simulate = QCheckBox("show Simulation spectral")
        self.cbbtn_phase_window = QCheckBox("phase window process")

        self.btn_grid.addWidget(self.cbbtn_nofilter, 0, 1, 1, 1)
        self.btn_grid.addWidget(self.cbbtn_phase_diff, 1, 1, 1, 1)
        self.btn_grid.addWidget(self.cbbtn_cwt, 2, 1, 1, 1)
        self.btn_grid.addWidget(self.cbbtn_vmd, 3, 1, 1, 1)
        self.btn_grid.addWidget(self.cbbtn_phase_cohere, 4, 1, 1, 1)
        self.btn_grid.addWidget(self.cbbtn_phase_window, 0, 2, 1, 1)
        self.btn_grid.addWidget(self.cbbtn_simulate, 1, 2, 1, 1)
        self.btn_grid.addWidget(self.cbbtn_gt, 2, 2, 1, 1)


class Watch_single(QWidget):
    def __init__(self, parent=None):
        super(Watch_single, self).__init__(parent)  # parent

        self.plot1 = Drawing_vitalsign("")
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.plot1)


class Watch_eightwindow(QWidget):
    def __init__(self, parent=None):
        super(Watch_eightwindow, self).__init__(parent)  # parent

        self.plot1 = Drawing_vitalsign("")
        self.plot2 = Drawing_vitalsign("")
        self.plot3 = Drawing_vitalsign("")
        self.plot4 = Drawing_vitalsign("")
        self.plot5 = Drawing_vitalsign("")
        self.plot6 = Drawing_vitalsign("")
        self.plot7 = Drawing_vitalsign("")
        self.plot8 = Drawing_vitalsign("")
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.plot1)
        self.grid.addWidget(self.plot2)
        self.grid.addWidget(self.plot3)
        self.grid.addWidget(self.plot4)
        self.grid.addWidget(self.plot5)
        self.grid.addWidget(self.plot6)
        self.grid.addWidget(self.plot7)
        self.grid.addWidget(self.plot8)


if __name__ == "__main__":
    app = QApplication([])
    # w = Watch_eightwindow ()
    w = WatchWidget()
    w.show()
    sys.exit(app.exec_())
