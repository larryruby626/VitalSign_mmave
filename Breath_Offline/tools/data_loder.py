import re

import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from tools.dataset_selector import LiesDataset,SeatDataset,AICAdjustDataset,SICAdjustDataset


class DataLoader(QWidget):
    cur_multi_dict = pyqtSignal(dict)

    def __init__(self, cfg):
        super(DataLoader, self).__init__()
        self.widget_cfg = cfg
        self.mode = self.widget_cfg["Mode"]
        if self.mode == "single":
            try:
                self.single_data()
            except Exception as e:
                print("file path is empty. PLZ select")
                print(e)


    def single_data(self):
        path = self.widget_cfg["single_file_path"]
        filename = re.search("/(\w*)_rangefft.npy", path)[0][1:-13]
        filepath = re.search(".*(?=range_fft_buf/\w*_rangefft.npy)", path)[0]
        self.fft_buffer = np.load(path, allow_pickle=True)
        self.HB_buffer = np.load(filepath + "/hb_gt/" + filename + "_HB_buf.npy", allow_pickle=True)
        print("Load the single file: {}".format(filename))

    def multidataset(self):
        """
        liedataset / seatdataset / aicadjust / sicadjust
        """
        dataset_list = self.widget_cfg["multi_dataset"]

        if dataset_list[0]:
            self.run_lie_dataset()
        if dataset_list[1]:
            self.run_seat_dataset()
        if dataset_list[2]:
            self.run_aic_adjust()
        if dataset_list[3]:
            self.run_sic_adjust()

    def run_lie_dataset(self):
        self.Lie_dataset = LiesDataset()

        for b_type_idx, b_type in enumerate(self.Lie_dataset.breath_type):
            for t_idx, t in enumerate(self.Lie_dataset.time):
                tmpname = "lie_" + b_type + "_p1_t" + t
                frame_buf, HB_GT = self.Lie_dataset.load_singe_processed_data(b_type_idx, t_idx)
                cur_dict = {"filename": tmpname, "radar": frame_buf, "gt": HB_GT}
                self.cur_multi_dict.emit(cur_dict)

    def run_seat_dataset(self):
        self.seat_dataset = SeatDataset()
        for r_idx,r in enumerate(self.seat_dataset.range):
            for p_idx,p in enumerate(self.seat_dataset.person):
                tmpname = "p" + p + "_" + r + "cm"
                frame_buf, HB_GT = self.seat_dataset.load_singe_processed_data(p_idx, r_idx)
                cur_dict = {"filename": tmpname, "radar": frame_buf, "gt": HB_GT}
                self.cur_multi_dict.emit(cur_dict)

    def run_aic_adjust(self):
        self.aic_dataset = AICAdjustDataset()
        for tia_idx,tia in enumerate(self.aic_dataset.TIA):
            for hp_idx,hp in enumerate(self.aic_dataset.HP):
                for t_idx,t in enumerate(self.aic_dataset.time):
                    tmpname = "40cm_TIA" + tia + "_HP" + hp + "_time" + t
                    frame_buf, HB_GT = self.aic_dataset.load_singe_processed_data(tia_idx,hp_idx,t_idx)
                    cur_dict = {"filename": tmpname, "radar": frame_buf, "gt": HB_GT}
                    self.cur_multi_dict.emit(cur_dict)

    def run_sic_adjust(self):
        self.sic_dataset = SICAdjustDataset()
        for d_t_idx,d_t in enumerate(self.sic_dataset.data_type):
            for r_idx,r in enumerate(self.sic_dataset.range):
                for t_idx,t in enumerate(self.sic_dataset.time):
                    tmpname = d_t + "_" + r + "cm_" + t
                    frame_buf, HB_GT = self.sic_dataset.load_singe_processed_data(d_t_idx,r_idx,t_idx)
                    cur_dict = {"filename": tmpname, "radar": frame_buf, "gt": HB_GT}
                    self.cur_multi_dict.emit(cur_dict)