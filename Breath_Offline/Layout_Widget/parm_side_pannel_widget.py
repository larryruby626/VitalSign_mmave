import re
import tkinter as tk
from tkinter import filedialog

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QLabel, QRadioButton,
                             QPushButton, QGridLayout,QComboBox)

from larry_common_usage.pyqt5.Custom_lbte import Custom_lbte


class ParmAdjustSidepanel(QGridLayout):
    pass_cfg = pyqtSignal(dict)

    def __init__(self, cfg=None, parent=None):
        super(ParmAdjustSidepanel, self).__init__()
        self.widget_cfg = cfg
        vital_select_panel = self.build_vitalsign_mode_select_rb()
        file_loader_panel = self.build_file_load()
        process_select_panel = self.build_combox_process_selector()
        self.setVerticalSpacing(30)

        self.addLayout(vital_select_panel, 0, 0)
        self.addLayout(file_loader_panel, 2, 0)
        self.addLayout(process_select_panel, 4, 0)

        self.rb_respiration.setChecked(True)

    def cfg_update_event(self):
        self.file_path = self.widget_cfg["single_file_path"]
        if self.file_path !="":
            self.dataloader.te.setPlainText(str(re.search("/(\w*)_rangefft.npy", self.file_path)[0][1:-13]))
        if self.widget_cfg["vitalsign_mode"] == "breath":
            self.rb_respiration.setChecked(True)
        else:
            self.rb_heart.setChecked(True)

    def update_cfg(self):

        if self.rb_respiration.isChecked():
            self.widget_cfg["vitalsign_mode"] = "breath"
        else:
                self.widget_cfg["vitalsign_mode"] = "heart"

        self.pass_cfg.emit(self.widget_cfg)

    def build_vitalsign_mode_select_rb(self):

        grid = QGridLayout()
        grid.setVerticalSpacing(10)
        self.rb_respiration = QRadioButton("Respiration Mode")
        self.rb_heart = QRadioButton("Heart Rate")
        self.rb_respiration.toggled.connect(self.update_cfg)
        self.rb_heart.toggled.connect(self.update_cfg)
        self.lb_vitalmode = QLabel("Vital sign mode:")
        grid.addWidget(self.lb_vitalmode, 0, 0, 1, 3)
        grid.addWidget(self.rb_respiration, 1, 1, 1, 3)
        grid.addWidget(self.rb_heart, 2, 1, 1, 2)
        return grid

    def build_file_load(self):
        grid = QGridLayout()
        grid.setVerticalSpacing(10)
        self.dataloader = Custom_lbte("File: ", "", 40, 20, 40, 400)
        self.save_result = Custom_lbte("save path: ", "", 40, 20, 40, 400)
        self.pb_load_data = QPushButton("Load File")
        self.pb_load_data.clicked.connect(self.Load_File)
        self.lb_dataloader = QLabel("Load Data:")

        grid.addWidget(self.lb_dataloader, 0, 0, 1, 1)
        grid.addLayout(self.dataloader, 1, 0, 1, 1)
        grid.addWidget(self.pb_load_data, 2, 0, 1, 1)
        return grid

    def Load_File(self):
        root = tk.Tk()
        root.withdraw()
        # self.file_path_cam2 = filedialog.askopenfilename(parent=root, initialdir=self.path)
        self.file_path = filedialog.askopenfilename(parent=root)
        self.dataloader.te.setPlainText(str(re.search("/(\w*)_rangefft.npy", self.file_path)[0][1:-13]))
        self.widget_cfg["single_file_path"] = self.file_path
        self.update_cfg()

    def build_combox_process_selector(self):
        grid = QGridLayout()
        grid.setVerticalSpacing(8)

        self.lb_targetidx = QLabel("target index seacrh:")
        self.cb_targetidx = QComboBox()
        targetidx_list = ['Phase Map Method',
                          'Max Range bin']
        self.cb_targetidx.addItems(targetidx_list)
        self.lb_phase_process = QLabel("phase process:")
        self.cb_phase_process = QComboBox()

        phase_processlist = ['Normal Unwrap Phase',
                             "Phase Difference",
                             "CWT Method",
                             "VMD　Method",
                             "Phase Coherence",

                             ]
        self.cb_phase_process.addItems(phase_processlist)
        self.lb_calchb = QLabel("Calc HB process:")
        self.cb_calchb  = QComboBox()

        phase_calchb  = ['Short-time FT',
                         'InterBeat Interval']
        self.cb_calchb .addItems(phase_calchb)
        self.cb_phase_process.currentIndexChanged.connect(self.ComboBox_evnet)
        self.cb_calchb.currentIndexChanged.connect(self.ComboBox_evnet)
        self.cb_targetidx.currentIndexChanged.connect(self.ComboBox_evnet)

        grid.addWidget(self.lb_targetidx, 0, 1, 1, 1)
        grid.addWidget(self.cb_targetidx, 1, 1, 1, 1)
        grid.addWidget(self.lb_phase_process, 2, 1, 1, 1)
        grid.addWidget(self.cb_phase_process, 3 ,1, 1, 1)
        grid.addWidget(self.lb_calchb, 4, 1, 1, 1)
        grid.addWidget(self.cb_calchb, 5, 1, 1, 1)
        return grid

    def ComboBox_evnet(self):
        targetidx_cfg = [False for i in range(self.cb_targetidx.count())]
        phase_process_cfg = [False for i in range(self.cb_phase_process.count())]
        calchb_cfg = [False for i in range(self.cb_calchb.count())]

        targetidx_cfg[self.cb_targetidx.currentIndex()] = True
        phase_process_cfg[self.cb_phase_process.currentIndex()] = True
        calchb_cfg[self.cb_calchb.currentIndex()] = True

        self.widget_cfg["pw_targetidx"] = targetidx_cfg
        self.widget_cfg["pw_phaseprocess"] = phase_process_cfg
        self.widget_cfg["pw_HBCalc"] = calchb_cfg
        self.update_cfg()
