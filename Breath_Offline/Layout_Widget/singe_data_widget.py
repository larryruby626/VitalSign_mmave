import tkinter as tk
from tkinter import filedialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QPushButton
from larry_common_usage.pyqt5.Custom_lbte import Custom_lbte



class SingleDatasetLayout(QGridLayout):
    pass_cfg = pyqtSignal(dict)

    def __init__(self, cfg=None, parent=None):
        super(SingleDatasetLayout, self).__init__()
        self.widget_cfg = cfg
        self.setRowMinimumHeight(10, 20)
        self.dataloader = Custom_lbte("File: ", "", 40, 20, 40, 400)
        self.save_result = Custom_lbte("save path: ", "", 40, 20, 40, 400)
        self.pb_load_data = QPushButton("Load File")
        self.pb_comfire = QPushButton("Comfirm")
        self.pb_comfire.clicked.connect(self.update_cfg)
        self.pb_load_data.clicked.connect(self.Load_File)
        self.addLayout(self.dataloader, 0, 0, 1, 1)
        self.addWidget(self.pb_load_data, 0, 1, 1, 1)
        self.addWidget(self.pb_comfire, 1, 0, 1, 2)
        self.pb_comfire.click()

    def Load_File(self):
        root = tk.Tk()
        root.withdraw()
        # self.file_path_cam2 = filedialog.askopenfilename(parent=root, initialdir=self.path)
        self.file_path = filedialog.askopenfilename(parent=root)
        self.dataloader.te.setPlainText(str(self.file_path))
        self.pb_comfire.click()

    def update_cfg(self):
        if self.widget_cfg["single_file_path"] != "":
            self.widget_cfg["single_file_path"] = self.file_path
        self.pass_cfg.emit(self.widget_cfg)
