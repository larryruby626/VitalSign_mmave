import re
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget
from scipy import signal
from sklearn.metrics import mean_squared_error

from larry_common_usage.xlsx_writer import XlsxWriter
from tools.CalcHB_processor import CalcHBProcessor
from tools.data_loder import DataLoader
from tools.phase_processor import PhaseProcessor
from tools.target_index_processor import TargetIdxProcessor
import time

class EstimateRunner(QWidget):
    processbar_v = pyqtSignal(int)
    processbar_max_v = pyqtSignal(int)

    def __init__(self, cfg=None,app=None):
        super(EstimateRunner, self).__init__()
        self.widget_cfg = cfg
        self.app = app
    def start(self):
        self.targetidx_processor = TargetIdxProcessor(self.widget_cfg)
        self.phase_processor = PhaseProcessor(self.widget_cfg)
        self.calchb_processor = CalcHBProcessor(self.widget_cfg)
        if self.state_check():
            if self.widget_cfg["Mode"] == "single":
                self.data_loader = DataLoader(self.widget_cfg)
                self.frame_buf = self.data_loader.fft_buffer
                self.HB_GT = self.data_loader.HB_buffer
                self.processbar_max_v.emit(len(self.frame_buf) - self.widget_cfg["vital_sign_window_len"])
                filename = str(re.search("/(\w*)_rangefft.npy", self.widget_cfg["single_file_path"])[0][1:-13])
                self.xlsx_writer = XlsxWriter(
                    self.widget_cfg["save_result_path"] + "/" + filename + "_" + self.get_process_name() + ".xlsx")
                self.process(self.frame_buf, self.HB_GT, filename)
                self.single_file_save()
                self.xlsx_writer.save()

            elif self.widget_cfg["Mode"] == "multiple":
                filename = time.strftime("%Y_%m_%d_%H_%M")+"_multidataset"
                self.xlsx_writer = XlsxWriter(
                    self.widget_cfg["save_result_path"] + "/" + filename + "_" + self.get_process_name() + ".xlsx")
                self.data_loader = DataLoader(self.widget_cfg)
                self.data_loader.cur_multi_dict.connect(self.multi_process)
                self.multi_bar_count = 0
                self.count_multifile_num()
                self.data_loader.multidataset()
                self.xlsx_writer.save()

    def state_check(self):
        if self.widget_cfg["single_file_path"] == []:
            QMessageBox.information(None, 'Error Message', "Single file path is empty !!! ")
            return False
        elif self.widget_cfg["save_result_path"] == []:
            QMessageBox.information(None, 'Error Message', "Save path is empty !!! ")
            return False
        elif all(i == False for i in self.widget_cfg["save_type"]):
            QMessageBox.information(None, 'Error Message', "You didn't select any save type!!! ")
            return False
        elif self.widget_cfg["vitalsign_mode"] == "breath":
            QMessageBox.information(None, 'Error Message',
                                    "Current don't provide breath ground!!! \n PLZ set vital sign mode as heart Rate type")
            return False
        else:
            return True

    def process(self, fft_buff, hb_gt, filename):

        self.w_len = self.widget_cfg["vital_sign_window_len"]
        self.cur_hb_list = []
        self.file_name = filename

        for i in range(len(fft_buff) - self.w_len):
            if i % self.widget_cfg["vital_sign_shfit_len"] == 0:
                tmp_fft = fft_buff[i:i + self.w_len]
                targeidx, phasemap = self.targetidx_processor.run_process(tmp_fft)
                phase = self.phase_processor.run_process(tmp_fft, targeidx)
                HB, spectral = self.calchb_processor.run_process(phase)
                self.cur_hb_list.append(HB)
            if self.widget_cfg["Mode"]=="single":
                self.processbar_v.emit(i + 1)
        self.ds_hb_gt = signal.resample(hb_gt, len(self.cur_hb_list))
        self.rmse = self.calc_rmse(self.cur_hb_list, self.ds_hb_gt)
        self.mape = self.calc_mape(self.cur_hb_list, self.ds_hb_gt)

    def multi_process(self, data_dict):
        fft_buff = data_dict["radar"]
        hb_gt = data_dict["gt"]
        filename = data_dict["filename"]
        print("------ process : {} ------".format(filename))
        self.process( fft_buff, hb_gt, filename)
        self.multi_file_save()
        self.multi_bar_count+=1
        self.processbar_v.emit(self.multi_bar_count)

    def count_multifile_num(self):
        count = 0
        if self.widget_cfg["multi_dataset"][0]:
            count +=12
        if self.widget_cfg["multi_dataset"][1]:
            count += 12
        if self.widget_cfg["multi_dataset"][2]:
            count += 18
        if self.widget_cfg["multi_dataset"][3]:
            count += 27
        self.processbar_max_v.emit(count)

    def single_file_save(self):
        save_list = self.widget_cfg["save_type"]
        save_path = self.widget_cfg["save_result_path"] + "/" + self.file_name + "_" + self.get_process_name()
        if save_list[0]:
            self.xlsx_writer.addline([self.file_name, self.get_process_name()])
            self.xlsx_writer.addline(["rmse", "mape"])
            self.xlsx_writer.addline([self.rmse, self.mape])
        if save_list[1]:
            out_dic = {"radar": self.cur_hb_list,
                       "gt": self.ds_hb_gt,
                       "rmse": self.rmse,
                       "mape": self.mape,
                       "pw_targetidx": self.widget_cfg["pw_targetidx"],
                       "pw_phaseprocess": self.widget_cfg["pw_phaseprocess"],
                       "pw_HBCalc": self.widget_cfg["pw_HBCalc"],
                       }
            np.save(save_path + ".npy", out_dic)
        if save_list[2]:
            font = {'family': 'sans-serif',
                    'color': 'Black',
                    'weight': 'normal',
                    'size': 16,
                    }
            p1, = plt.plot(self.cur_hb_list)
            p2, = plt.plot(self.ds_hb_gt)
            plt.ylim([50, 120])
            plt.legend([p1, p2], ["Radar estiate", "Ground truth"])
            plt.text(2, 110, "RMSE : {}".format(np.round(self.rmse, 2)), fontdict=font)
            plt.text(2, 105, "MAPE : {} %".format(np.round(self.mape, 2)), fontdict=font)
            plt.title(self.file_name + "-" + self.get_process_name())
            plt.ylabel("BPM")
            plt.savefig(save_path + ".jpg")
            plt.cla()

    def multi_file_save(self):
        save_list = self.widget_cfg["save_type"]
        save_path = self.widget_cfg["save_result_path"] + "/" + self.file_name + "_" + self.get_process_name()
        if save_list[0]:
            self.xlsx_writer.addline([self.file_name, self.get_process_name()])
            self.xlsx_writer.addline(["rmse", "mape"])
            self.xlsx_writer.addline([self.rmse, self.mape])
        if save_list[1]:
            out_dic = {"radar": self.cur_hb_list,
                       "gt": self.ds_hb_gt,
                       "rmse": self.rmse,
                       "mape": self.mape,
                       "pw_targetidx": self.widget_cfg["pw_targetidx"],
                       "pw_phaseprocess": self.widget_cfg["pw_phaseprocess"],
                       "pw_HBCalc": self.widget_cfg["pw_HBCalc"],
                       }
            np.save(save_path + ".npy", out_dic)
        if save_list[2]:
            font = {'family': 'sans-serif',
                    'color': 'Black',
                    'weight': 'normal',
                    'size': 16,
                    }
            p1, = plt.plot(self.cur_hb_list)
            p2, = plt.plot(self.ds_hb_gt)
            plt.ylim([50, 120])
            plt.legend([p1, p2], ["Radar estiate", "Ground truth"])
            plt.text(2, 110, "RMSE : {}".format(np.round(self.rmse, 2)), fontdict=font)
            plt.text(2, 105, "MAPE : {} %".format(np.round(self.mape, 2)), fontdict=font)
            plt.title(self.file_name + "-" + self.get_process_name())
            plt.ylabel("BPM")
            plt.savefig(save_path + ".jpg")
            plt.cla()

    def get_process_name(self):
        search_bin = {'0': "searchbin_",
                      '1': "maxpower_"}
        phase_pro = {'0': "normal_",
                     '1': "phasediff_",
                     '2': "cwt_",
                     '3': "vmd_",
                     '4': "phase_coherence_", }
        calc = {'0': "STFT",
                '1': "IBI", }

        search_bin_str = search_bin[str(np.where(self.widget_cfg["pw_targetidx"])[0][0])]
        phase_str = phase_pro[str(np.where(self.widget_cfg["pw_phaseprocess"])[0][0])]
        calc_str = calc[str(np.where(self.widget_cfg["pw_HBCalc"])[0][0])]

        return search_bin_str + phase_str + calc_str

    def calc_rmse(self, y_true, y_pred):
        rms = sqrt(mean_squared_error(y_true, y_pred))
        return rms

    def calc_mape(self, y_true, y_pred):
        '''
        引數:
        y_true -- 測試集目標真實值
        y_pred -- 測試集目標預測值
        返回:
        mape -- MAPE 評價指標
        '''
        return np.round(np.mean(np.abs((y_true - y_pred) / y_true)) * 100, 2)
