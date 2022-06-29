import sys
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
                             QGridLayout,QMessageBox)
from larry_common_usage.vitalsign.Filter_struct_point_8_7 import Filter_struct_point_8_7
from larry_common_usage.vitalsign.config import build_config
from larry_common_usage.vitalsign.fft_buf_process import fft_buf_process
from larry_common_usage.vitalsign.object_location import Oject_Location
from larry_common_usage.DSP.get_fft_spectral import spectral_abs
from larry_common_usage.pyqt5.DrawingWidget import DrawingWidget
from larry_common_usage.pyqt5.Heatmap_widget import CustomWidget
from tools.data_loder import DataLoader
from tools.target_index_processor import TargetIdxProcessor
from tools.phase_processor import PhaseProcessor
from tools.CalcHB_processor import CalcHBProcessor
from PyQt5.QtCore import pyqtSignal

class OfflineSystemWidget(QWidget):
    pass_cfg = pyqtSignal(dict)
    def __init__(self,app,cfg=None):
        super().__init__()
        self.app = app
        self.widget_cfg = cfg
        self.buf, self.cfg = build_config()

        self.idx1 = 0
        self.HB_GT = []
        self.frame_buf= []
        self.HB_out = []
        self.fft_buf = np.array([])
        self.range_idx_buf = np.array([])
        self.smooth_filter = Filter_struct_point_8_7(1)
        self.set_vital_sign_widget()

    def cfg_update_event(self):
        if self.widget_cfg["vitalsign_mode"] == "breath":
            self.psd_plot_w.setYRange(0, 800)
            self.psd_plot_w.setXRange(0, 60)
            self.phase_plot_w.setYRange(-8, 8)
            self.bpm_plot_w.setYRange(0, 30)

        elif self.widget_cfg["vitalsign_mode"] == "heart":
            self.psd_plot_w.setYRange(0, 40)
            self.psd_plot_w.setXRange(0, 160)
            self.phase_plot_w.setYRange(-1, 1)
            self.bpm_plot_w.setYRange(50, 120)
        self.file_init()

    def file_init(self):
        self.buf.fft_buf = np.array([])
        self.buf.out_breath_rate_buffer = []
        self.phase_plot.setData([])
        self.psd_plot.setData([])
        self.bpm_plot.setData([])


        if self.widget_cfg["Mode"] == "single":
            if self.state_check():
                self.data_loader = DataLoader(self.widget_cfg)
                self.frame_buf = self.data_loader.fft_buffer
                self.HB_GT = self.data_loader.HB_buffer
        # print(len(self.frame_buf))
        if self.widget_cfg["pw_targetidx"][0] == True and self.widget_cfg["current_wiget"] == "1":

            self.heatmap = CustomWidget()
            self.heatmap.show()
        self.targetidx_processor =TargetIdxProcessor(self.widget_cfg)
        self.phase_processor = PhaseProcessor(self.widget_cfg)
        self.calchb_processor = CalcHBProcessor(self.widget_cfg)

    def state_check(self):
        if self.widget_cfg["single_file_path"] == "":
            QMessageBox.information(None, 'Error Message', "Single file path is empty !!! ")
            return False
        else:
            return True


    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.process)
        self.timer.start()

    def start_process(self):
        if self.state_check():
            self.idx1 = 0
            self.buf.fft_buf = np.array([])
            self.buf.out_breath_rate_buffer = []
            self.bpm_gt.setData([])
            self.bpm_plot.setData([])
            self.phase_plot.setData([])
            self.psd_plot.setData([])
            self.run()

    def detect_none_bearth(self, phase_RR):

        if np.max(spectral_abs(phase_RR[-120:])) < 20:
            self.buf.stop_B_c += 1
        else:
            self.buf.stop_B_c = 0

    def process(self):
        print(self.idx1)
        # for i in range(self.frame_buf.shape[0]):
        rangefft= self.frame_buf[self.idx1]
        fft_std, rawfft = Oject_Location(rangefft, show_searchbin_plot=True, \
                                      buf_cfg=self.buf)
        if fft_std is not None:
            self.FFT_plot_w.line_obj_SetData(self.FFT_plot,abs(fft_std) ,np.linspace(0,128,128)/128*240)

        if self.buf.obj_state == "Objected":

            if True:
                self.led_moving.set_on_color(self.led_moving.green)
                self.led_moving.turn_on()
                self.lbte_moving.te.setPlainText("Person Detected")

                self.buf.fft_buf, self.cfg = fft_buf_process(self.buf.fft_buf, \
                                                             rangefft, \
                                                             self.cfg)  # print(self.buf.fft_buf.shape)
                self.cfg.buf_state = True

                if self.buf.fft_buf.shape[0] >= self.cfg.w_l:

                    """
                    process the fft_buff to hearbeat 
                    """
                    targeidx, phasemap = self.targetidx_processor.run_process(self.buf.fft_buf)
                    phase = self.phase_processor.run_process(self.buf.fft_buf,targeidx)
                    HB,spectral = self.calchb_processor.run_process(phase)
                    # BR = self.smooth_filter.run(BR)

                    if self.buf.stop_B_c > 5:
                        self.led_no.turn_on()
                        self.led_yes.turn_off()
                        self.lbte_current_bpm.te.setPlainText("---stoping breath---")
                        self.buf.out_breath_rate_buffer.append(0)
                    #
                    else:
                        self.led_no.turn_off()
                        self.led_yes.turn_on()
                        self.lbte_current_bpm.te.setPlainText(str(HB))
                        self.buf.out_breath_rate_buffer.append(HB)
                    if phasemap is not None:
                        self.heatmap.set_image_data(phasemap)
                    self.phase_plot.setData(phase)
                    self.psd_plot_w.line_obj_SetData(self.psd_plot, spectral,
                                                         np.linspace(0, 512, 512) / 512 * 600)
                    self.bpm_plot.setData(self.buf.out_breath_rate_buffer)
                    self.bpm_plot_w.setData_with_color(self.bpm_gt,self.HB_GT[self.idx1-len(self.buf.out_breath_rate_buffer):self.idx1],
                                                       c="r")
            else:
                self.led_no.turn_off()
                self.led_yes.turn_off()
                self.buf.fft_buf = np.array([])
                self.buf.out_breath_rate_buffer = []
                self.led_moving.set_on_color(self.led_moving.red)
                self.led_moving.turn_on()
                self.lbte_moving.te.setPlainText("Person Moving")
        else:

            self.led_moving.turn_off()
            self.led_no.turn_off()
            self.led_yes.turn_off()
            self.lbte_moving.te.setPlainText("--Empty-- NO Person")
            self.lbte_current_bpm.te.setPlainText(str(""))
            self.buf.out_breath_rate_buffer = []
        self.app.processEvents()

        self.idx1 += 1
        if self.idx1 >=len(self.frame_buf):
            self.timer.stop()
    #
    def clean_BPM(self):
        self.buf.out_breath_rate_buffer=  []

    def set_vital_sign_widget(self):
        from pyqt_led import Led
        from larry_common_usage.pyqt5.Custom_lbte import Custom_lbte
        self.resize(800, 600)
        self.grid_layout = QGridLayout()
        self.FFT_plot_w = DrawingWidget("Range profile")
        self.FFT_plot_w.setYRange(0, 30000)
        self.FFT_plot_w.setlb(xlabel="cm",ylabel="amplitude")
        self.FFT_plot =self.FFT_plot_w.add_line_obj()
        self.FFT_plot_raw = self.FFT_plot_w.add_line_obj()


        self.phase_plot_w = DrawingWidget("targe phase")
        self.phase_plot_w.setYRange(-8, 8)
        self.phase_plot_w.setlb(xlabel="th-time phase of window",ylabel="Radius")
        self.phase_plot =self.phase_plot_w.add_line_obj()

        self.psd_plot_w = DrawingWidget("Phase PSD")
        self.psd_plot_w.setYRange(0, 300)
        self.psd_plot_w.setlb(xlabel="BPM", ylabel="Spectral amplitude")
        self.psd_plot = self.psd_plot_w.add_line_obj()

        self.bpm_plot_w = DrawingWidget("BPM")
        self.bpm_plot_w.setlb(xlabel="time", ylabel="BPM")
        self.psd_plot_w.setXRange(0, 60)

        self.bpm_plot_w.setYRange(0, 30)
        self.bpm_plot = self.bpm_plot_w.add_line_obj()
        self.bpm_gt = self.bpm_plot_w.add_line_obj(c='r')


        self.box_H1 = QHBoxLayout()
        self.box_H2 = QHBoxLayout()
        self.box_H3 = QHBoxLayout()
        self.box_H4 = QHBoxLayout()
        self.box_H5 = QHBoxLayout()
        self.box_H1.addWidget(self.FFT_plot_w)
        self.box_H1.addWidget(self.phase_plot_w)
        self.box_H2.addWidget(self.psd_plot_w)
        self.box_H2.addWidget(self.bpm_plot_w)
        self.lb_bpm_state = QLabel("Breath state:")
        self.lb_breath = QLabel("(Breathing)")
        self.lb_nobreath = QLabel("(No Breathing)")
        self.led_yes = Led(self, on_color=Led.green, shape=Led.capsule, build="debug")
        self.led_no  = Led(self, on_color=Led.red, shape=Led.capsule, build="debug")
        self.pb_start = QPushButton("Start")
        self.pb_start.clicked.connect(self.start_process)
        self.pb_clean_BPM = QPushButton("Clean BPM")
        self.pb_clean_BPM.clicked.connect(self.clean_BPM)


        self.box_H3.addWidget(self.lb_bpm_state)
        self.box_H3.addWidget(self.led_yes)
        self.box_H3.addWidget(self.lb_breath)
        self.box_H3.addWidget(self.led_no)
        self.box_H3.addWidget(self.lb_nobreath)
        self.box_H3.addWidget(self.pb_start)
        self.box_H3.addWidget(self.pb_clean_BPM)

        self.box_H3.addWidget(self.lb_nobreath)
        self.lbte_current_bpm = Custom_lbte("Current BPM:","---init---",50,200,50,600)
        self.lbte_current_bpm.change_font(self.lbte_current_bpm.te,20,bold=True)
        self.lbte_current_bpm.change_font(self.lbte_current_bpm.lb,15,bold=True)
        self.lbte_current_bpm.change_font(self.lb_bpm_state,15,bold=True)
        self.lbte_current_bpm.change_font(self.lb_breath,12)
        self.lbte_current_bpm.change_font(self.lb_nobreath,12)
        self.box_H4.addLayout(self.lbte_current_bpm)
        self.lbte_moving = Custom_lbte("OBJ state:","---init---",50,200,50,600)
        self.led_moving = Led(self, on_color=Led.black, shape=Led.circle, build="debug")
        self.lbte_current_bpm.change_font(self.lbte_moving.te,20,bold=True)
        self.lbte_current_bpm.change_font(self.lbte_moving.lb,15,bold=True)

        self.box_H5.addLayout(self.lbte_moving)
        self.box_H5.addWidget(self.led_moving)

        self.grid_layout.addLayout(self.box_H1,0,0,1,2)
        self.grid_layout.addLayout(self.box_H2,1,0,1,2)
        self.grid_layout.addLayout(self.box_H3,2,0,1,2)
        self.grid_layout.addLayout(self.box_H4,3,0,1,1)
        self.grid_layout.addLayout(self.box_H5,3,1,1,1)
        self.setLayout(self.grid_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    x = OfflineBreathWidget()
    x.show()
    sys.exit(app.exec_())
