from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QGridLayout, QPushButton, QGroupBox, QCheckBox


class MultiDatasetLayout(QGridLayout):
    pass_cfg = pyqtSignal(dict)
    processbar_max_v = pyqtSignal(int)

    def __init__(self, cfg=None, parent=None):
        super(MultiDatasetLayout, self).__init__()
        self.widget_cfg = cfg
        self.setRowMinimumHeight(10, 20)
        self.build_checK_box_widget()
        self.pb_comfire = QPushButton("Comfirm")
        self.pb_comfire.clicked.connect(self.update_cfg)
        self.addWidget(self.checkbox_group, 1, 0, 1, 2)
        self.addWidget(self.pb_comfire, 2, 0, 1, 2)

    def build_checK_box_widget(self):
        self.checkbox_group = QGroupBox("Dataset")
        self.checkbox_grid = QGridLayout()
        self.ch_liedataset = QCheckBox("Lie Dataset")
        self.ch_seatdatast = QCheckBox("Seat Dataset")
        self.ch_sicadjust = QCheckBox("SIC Adjust Dataset")
        self.ch_aicadjust = QCheckBox("AIC Adjust Dataset")
        self.ch_liedataset.clicked.connect(self.state_changed)
        self.ch_seatdatast.clicked.connect(self.state_changed)
        self.ch_sicadjust.clicked.connect(self.state_changed)
        self.ch_aicadjust.clicked.connect(self.state_changed)

        self.checkbox_grid.addWidget(self.ch_liedataset, 0, 0)
        self.checkbox_grid.addWidget(self.ch_seatdatast, 1, 0)
        self.checkbox_grid.addWidget(self.ch_aicadjust, 0, 1)
        self.checkbox_grid.addWidget(self.ch_sicadjust, 1, 1)
        self.checkbox_group.setLayout(self.checkbox_grid)

    def state_changed(self, int):
        self.dataset_state = [self.ch_liedataset.isChecked(),
                              self.ch_seatdatast.isChecked(),
                              self.ch_aicadjust.isChecked(),
                              self.ch_sicadjust.isChecked()]
        self.widget_cfg["multi_dataset"] = self.dataset_state
        self.count_multifile_num()
        self.update_cfg()
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

    def update_cfg(self):
        self.pass_cfg.emit(self.widget_cfg)
