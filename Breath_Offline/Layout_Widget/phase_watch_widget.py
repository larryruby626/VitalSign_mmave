import numpy as np
from larry_common_usage.DSP.get_fft_spectral import spectral_abs
from larry_common_usage.pyqtgraph.watching_Widget import *
from tools.CalcHB_processor import CalcHBProcessor
from tools.data_loder import DataLoader
from tools.phase_processor import PhaseProcessor
from tools.target_index_processor import TargetIdxProcessor
from tools.wave_simulate import wave_sumlate_process
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

class PhaseWatchingTools(WatchWidget):
    pass_cfg = pyqtSignal(dict)

    def __init__(self, app, cfg=None):
        super(PhaseWatchingTools, self).__init__()
        self.app = app
        self.widget_cfg = cfg

    def file_init(self):

        if self.widget_cfg["Mode"] == "single":
            if self.state_check():
                self.data_loader = DataLoader(self.widget_cfg)
                self.frame_buf = self.data_loader.fft_buffer
                self.HB_GT = self.data_loader.HB_buffer
                self.targetidx_processor = TargetIdxProcessor(self.widget_cfg)
                self.phase_processor = PhaseProcessor(self.widget_cfg)
                self.calchb_processor = CalcHBProcessor(self.widget_cfg)
                self.init_layout()

    def state_check(self):
        if self.widget_cfg["single_file_path"] == "":
            QMessageBox.information(None, 'Error Message', "Single file path is empty !!! ")
            return False
        else:
            return True

    def init_layout(self):
        self.slider.valueChanged.connect(self.slider_update_plot)
        self.slider_w_len.valueChanged.connect(self.slider_update_W_len)
        self.slider_w_len.setMaximum(self.frame_buf.shape[0] - 1)
        self.slider_w_len.setMinimum(1)
        self.slider_w_len.setValue(256)
        self.btn.clicked.connect(self.btn_update_plot)
        self.nx_btn.clicked.connect(self.nx_update_plot)
        self.pre_btn.clicked.connect(self.pre_update_plot)
        self.cbbtn_nofilter.stateChanged.connect(self.btn_update_plot)
        self.cbbtn_phase_diff.stateChanged.connect(self.btn_update_plot)
        self.cbbtn_cwt.stateChanged.connect(self.btn_update_plot)
        self.cbbtn_vmd.stateChanged.connect(self.btn_update_plot)
        self.cbbtn_phase_cohere.stateChanged.connect(self.btn_update_plot)
        self.cbbtn_simulate.stateChanged.connect(self.btn_update_plot)
        self.cbbtn_gt.stateChanged.connect(self.btn_update_plot)
        self.cbbtn_phase_cohere.stateChanged.connect(self.btn_update_plot)
        self.cbbtn_phase_window.stateChanged.connect(self.btn_update_plot)

    def cfg_update_event(self):
        if self.widget_cfg["vitalsign_mode"] == "breath":
            self.psd_widget.setYRange(0, 800)
            self.psd_widget.setXRange(0, 60)
            self.phase_widget.setYRange(-8, 8)
            self.cbbtn_cwt.setEnabled(False)
            self.cbbtn_vmd.setEnabled(False)
            self.gt_len = 800

        elif self.widget_cfg["vitalsign_mode"] == "heart":
            self.psd_widget.setYRange(0, 40)
            self.psd_widget.setXRange(0, 160)
            self.phase_widget.setYRange(-1, 1)
            self.cbbtn_cwt.setEnabled(True)
            self.cbbtn_vmd.setEnabled(True)
            self.gt_len = 800
        self.file_init()

    def single_plot(self):

        self.targetbin.te.setPlainText(str(self.target_idx))
        self.Arduino_HB.te.setPlainText(str(np.round(self.HB_GT[int(self.slider.value())], 2)))
        self.tmp_buf = self.update_cur_frame_buff()
        self.phase_processor.fft_frame_buf = self.tmp_buf
        self.phase_processor.target_idx = self.target_idx
        if self.cbbtn_nofilter.isChecked():
            raw_phase = self.phase_processor.raw_phase_process(self.tmp_buf, self.target_idx)
            raw_phase = raw_phase * np.hanning(
                len(raw_phase)) if self.cbbtn_phase_window.isChecked() == True else raw_phase
            self.phase_plot_N.setData(raw_phase)
            self.psd_plot_N.setData(spectral_abs(raw_phase))
        else:
            self.phase_plot_N.setData([])
            self.psd_plot_N.setData([])

        if self.cbbtn_phase_diff.isChecked():
            phasediff = self.phase_processor.phasediff_method()
            phasediff = phasediff * np.hanning(
                len(phasediff)) if self.cbbtn_phase_window.isChecked() == True else phasediff
            self.phase_widget.setData_with_color(self.phase_plot_phasediff,phasediff,"g")
            self.psd_widget.setData_with_color(self.psd_plot_phasediff,
                                                       spectral_abs(phasediff),"g")
        else:
            self.phase_plot_phasediff.setData([])
            self.psd_plot_phasediff.setData([])

        if self.cbbtn_vmd.isChecked():
            phasevmd = self.phase_processor.vmd_method()
            phasevmd = phasevmd * np.hanning(
                len(phasevmd)) if self.cbbtn_phase_window.isChecked() == True else phasevmd
            self.phase_widget.setData_with_color(self.phase_plot_vmd, phasevmd, "c")
            self.psd_widget.setData_with_color(self.psd_plot_vmd,
                                               spectral_abs(phasevmd), "c")
        else:
            self.phase_plot_vmd.setData([])
            self.psd_plot_vmd.setData([])

        if self.cbbtn_cwt.isChecked():
            phasecwt = self.phase_processor.cwt_method()
            phasecwt = phasecwt * np.hanning(
                len(phasecwt)) if self.cbbtn_phase_window.isChecked() == True else phasecwt
            self.phase_widget.setData_with_color(self.phase_plot_cwt, phasecwt, "m")
            self.psd_widget.setData_with_color(self.psd_plot_cwt,spectral_abs(phasecwt), "m")
        else:
            self.phase_plot_cwt.setData([])
            self.psd_plot_cwt.setData([])

        if self.cbbtn_phase_cohere.isChecked():
            phase_coheren = self.phase_processor.phase_coherence_method()
            phase_coheren = phase_coheren * np.hanning(
                len(phase_coheren)) if self.cbbtn_phase_window.isChecked() == True else phase_coheren
            self.phase_widget.setData_with_color(self.phase_plot_phasecoheren, phase_coheren, "y")
            self.psd_widget.setData_with_color(self.psd_plot_phasecoheren, spectral_abs(phase_coheren), "y")
        else:
            self.phase_plot_phasecoheren.setData([])
            self.psd_plot_phasecoheren.setData([])

        if self.cbbtn_gt.isChecked():
            hb = [np.round(self.HB_GT[int(self.slider.value())], 2),np.round(self.HB_GT[int(self.slider.value())], 2)]
            self.psd_plot_gt.setData(x=hb,y=np.array(np.linspace(1,self.gt_len,2)),)
        else:
            self.psd_plot_gt.setData([])

        if self.cbbtn_simulate.isChecked():
            RR = self.phase_processor.calc_RR(self.tmp_buf, self.target_idx)

            simulate_wave = wave_sumlate_process(len(self.tmp_buf), RR / 60,
                                            np.round(self.HB_GT[int(self.slider.value())], 2)/ 60,
                                            fft_point=int(512 * 2))
            simulate_wave = simulate_wave * np.hanning(
                len(simulate_wave)) if self.cbbtn_phase_window.isChecked() == True else simulate_wave

            self.phase_widget.setData_with_color(self.phase_plot_simulation, simulate_wave, "b")
            self.psd_widget.setData_with_color(self.psd_plot_simulation, spectral_abs(simulate_wave), "b")

        else:
            self.phase_plot_simulation.setData([])
            self.psd_plot_simulation.setData([])

    def slider_update_W_len(self):
        if self.state_check():
            tmp_window_len = self.slider_w_len.value()
            self.slider.setMaximum(self.frame_buf.shape[0] - tmp_window_len)
            self.window_len.te.setPlainText(str(tmp_window_len))

            self.target_idx, self.phasemap = self.targetidx_processor.run_process(
                self.update_cur_frame_buff())
            self.phase_map_widget.set_image_data(self.phasemap)
            self.single_plot()

    def slider_update_plot(self):
        if self.state_check():
            self.index.te.setPlainText(str(self.slider.value()))

            self.target_idx, self.phasemap = self.targetidx_processor.run_process(
                self.update_cur_frame_buff())
            self.phase_map_widget.set_image_data(self.phasemap)
            self.single_plot()

    def btn_update_plot(self):
        if self.state_check():
            index = int(self.index.te.toPlainText())
            self.slider.setValue(index)
            self.single_plot()


    def nx_update_plot(self):
        if self.state_check():
            index = int(self.index.te.toPlainText())
            if index <= 3600 - 256:
                index = index + 1
                self.update_state(index)
                self.single_plot()

    def pre_update_plot(self):
        if self.state_check():
            index = int(self.index.te.toPlainText())
            if index >= 1:
                index = index - 1
                self.update_state(index)
                self.single_plot()

    def update_state(self, index):
        if self.state_check():
            self.index.te.setPlainText(str(index))
            self.slider_update_plot()
            self.slider.setValue(index)

    def update_cur_frame_buff(self):
        if self.state_check():
            idx = int(self.slider.value())
            w_len = int(self.slider_w_len.value())
            return self.frame_buf[idx:idx + w_len]


if __name__ == "__main__":
    app = QApplication([])
    xxx = PhaseWatchingTools(app)
    xxx.show()
    sys.exit(app.exec_())
