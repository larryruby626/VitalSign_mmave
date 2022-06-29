import tkinter as tk
from tkinter import filedialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QGroupBox, QPushButton
from larry_common_usage.pyqt5.Custom_lbte import Custom_lbte


class SaverResultWidget(QGridLayout):
    pass_cfg = pyqtSignal(dict)

    def __init__(self, cfg=None, parent=None):
        super(SaverResultWidget, self).__init__()
        self.widget_cfg = cfg
        self.save_path = []
        self.setRowMinimumHeight(10, 20)
        self.build_savetype_groupbox()
        self.state_changed()
        self.ch_suresave = QCheckBox("Sure Save")
        self.ch_suresave.stateChanged.connect(self.save_checkbox_state_change)
        self.addWidget(self.ch_suresave, 0, 0, 1, 1)
        self.addWidget(self.savetype_group, 0, 1, 1, 6)


    def save_checkbox_state_change(self):

        if self.ch_suresave.isChecked():
            self.savetype_group.setEnabled(True)
        else:
            self.savetype_group.setEnabled(False)
        self.update_cfg()

    def build_savetype_groupbox(self):
        self.savetype_group = QGroupBox("Save Output type")
        self.ch_save_xls = QCheckBox("Save as .xlsx")
        self.ch_save_xls.stateChanged.connect(self.state_changed)
        self.ch_save_npy = QCheckBox("Save as .npy")
        self.ch_save_npy.stateChanged.connect(self.state_changed)
        self.ch_save_fig = QCheckBox("Save as .jpeg")
        self.ch_save_fig.stateChanged.connect(self.state_changed)
        self.save_result = Custom_lbte("save path: ", "", 30, 60, 30, 500)
        self.pb_save_path = QPushButton("Load Path")

        self.pb_save_path.clicked.connect(self.Load_save_path)
        layout = QGridLayout()

        layout.addLayout(self.save_result, 0, 0, 1, 2)
        layout.addWidget(self.pb_save_path, 0, 2, 1, 1)
        layout.addWidget(self.ch_save_xls, 1, 0, 1, 1)
        layout.addWidget(self.ch_save_npy, 1, 1, 1, 1)
        layout.addWidget(self.ch_save_fig, 1, 2, 1, 1)
        self.savetype_group.setLayout(layout)
        self.savetype_group.setEnabled(False)

    def Load_save_path(self):
        root = tk.Tk()
        root.withdraw()
        # self.file_path_cam2 = filedialog.askopenfilename(parent=root, initialdir=self.path)
        self.save_path = filedialog.askdirectory(parent=root)
        self.save_result.te.setPlainText(str(self.save_path))
        self.update_cfg()

    def state_changed(self):
        self.save_type = [self.ch_save_xls.isChecked(),
                          self.ch_save_npy.isChecked(),
                          self.ch_save_fig.isChecked()]
        self.update_cfg()

    def update_cfg(self):
        self.widget_cfg["save_type"] = self.save_type
        self.widget_cfg["save_result_path"] = self.save_path
        self.pass_cfg.emit(self.widget_cfg)
