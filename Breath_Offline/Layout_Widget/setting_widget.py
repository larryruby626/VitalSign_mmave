from PyQt5.QtWidgets import (QWidget, QGroupBox, QGridLayout
, QPushButton, QCheckBox, QProgressBar, QLabel)
from PyQt5.QtWidgets import (QWidget, QGroupBox, QGridLayout
, QPushButton, QCheckBox, QProgressBar, QLabel)
from PyQt5.QtCore import pyqtSignal

from Layout_Widget.multi_data_widget import MultiDatasetLayout
from Layout_Widget.process_select_widget import ProcessSelectWidget
from Layout_Widget.save_result_widget import SaverResultWidget
from Layout_Widget.singe_data_widget import SingleDatasetLayout
from tools.estiamte_runner import EstimateRunner


class SettingWidget(QWidget):
    pass_cfg = pyqtSignal(dict)

    def __init__(self, cfg=None, app=None, parent=None):
        super(SettingWidget, self).__init__(parent)  # parent
        self.main_gridlayout = QGridLayout()
        self.widget_cfg = cfg
        self.app = app
        self.build_dataset_box()
        self.build_process_box()
        self.build_saver_box()
        self.estimate_runner = EstimateRunner(self.widget_cfg,app = self.app)
        self.estimate_runner.processbar_max_v.connect(self.set_process_bar_max_value)
        self.estimate_runner.processbar_v.connect(self.set_process_bar_value)
        self.pb_start_estimate = QPushButton("Start Estimate")
        self.pb_start_estimate.setEnabled(False)
        self.pb_start_estimate.clicked.connect(self.estimate_runner.start)
        self.main_gridlayout.addWidget(self.data_set_group, 0, 0)
        self.main_gridlayout.addWidget(self.process_group, 1, 0)
        self.main_gridlayout.addWidget(self.save_group, 2, 0)
        self.main_gridlayout.addWidget(self.pb_start_estimate, 3, 0)

        self.setLayout(self.main_gridlayout)
        self.multi_file_group.setEnabled(False)
        self.pb_single_file.setEnabled(False)

    def build_dataset_box(self):
        self.data_set_group = QGroupBox("Data Set Loader")
        self.data_set_group.setFixedHeight(250)
        self.pb_single_file = QPushButton("Single file")
        self.pb_single_file.clicked.connect(self.change_dataset_sate)
        self.pb_multiple = QPushButton("Multiple file")
        self.pb_multiple.clicked.connect(self.change_dataset_sate)
        self.pb_breath = QPushButton("breath")
        self.pb_breath.setEnabled(False)
        self.pb_breath.clicked.connect(self.change_type_sate)
        self.pb_heart = QPushButton("heart")
        self.pb_heart.clicked.connect(self.change_type_sate)
        self.single_file_group = QGroupBox("Select single data ")
        self.single_file_group.setFixedHeight(150)
        self.single_widget = SingleDatasetLayout(cfg=self.widget_cfg)
        self.single_widget.pass_cfg.connect(self.update_cfg)
        self.single_file_group.setLayout(self.single_widget)

        self.multi_file_group = QGroupBox("Select Multidata set ")
        self.multi_file_group.setFixedHeight(150)
        self.multi_widget = MultiDatasetLayout(cfg=self.widget_cfg)
        self.multi_widget.processbar_max_v.connect(self.set_process_bar_max_value)
        self.multi_widget.pass_cfg.connect(self.update_cfg)
        self.multi_file_group.setLayout(self.multi_widget)
        self.process_bar = QProgressBar()
        self.process_bar.setMinimum(0)
        self.lb_process_bar = QLabel("Process:")

        layout = QGridLayout()
        layout.addWidget(self.pb_single_file, 0, 0, 1, 1)
        layout.addWidget(self.pb_multiple, 0, 1, 1, 1)
        layout.addWidget(self.pb_breath, 0, 3, 1, 1)
        layout.addWidget(self.pb_heart, 0, 4, 1, 1)
        layout.addWidget(self.lb_process_bar, 0, 6, 1, 1)
        layout.addWidget(self.process_bar, 0, 7, 1, 1)

        layout.addWidget(self.single_file_group, 1, 0, 1, 4)
        layout.addWidget(self.multi_file_group, 1, 4, 1, 4)
        self.data_set_group.setLayout(layout)

    def set_process_bar_value(self, v):
        self.process_bar.setValue(v)
        if v == self.process_bar.maximum():
            self.process_bar.setValue(0)
            self.setEnabled(True)
        else:
            self.setEnabled(False)
        self.app.processEvents()
    def set_process_bar_max_value(self, v):
        self.process_bar.setMaximum(v)

    def build_saver_box(self):
        self.save_group = QGroupBox("Save Option")
        self.save_group.setFixedHeight(150)
        self.saver_widget = SaverResultWidget(cfg=self.widget_cfg)
        self.saver_widget.pass_cfg.connect(self.update_cfg)
        self.save_group.setLayout(self.saver_widget)

    def build_process_box(self):
        self.process_group = QGroupBox("Vitalsign process")
        self.process_group.setFixedHeight(200)
        self.process_widget = ProcessSelectWidget(cfg=self.widget_cfg)
        self.process_widget.pass_cfg.connect(self.update_cfg)
        self.process_group.setLayout(self.process_widget)

    def change_dataset_sate(self):
        if self.pb_single_file.isEnabled():
            self.pb_multiple.setEnabled(True)
            self.multi_file_group.setEnabled(False)
            self.pb_single_file.setEnabled(False)
            self.single_file_group.setEnabled(True)
            self.widget_cfg["Mode"] = "single"
        else:
            self.pb_multiple.setEnabled(False)
            self.multi_file_group.setEnabled(True)
            self.pb_single_file.setEnabled(True)
            self.single_file_group.setEnabled(False)
            self.widget_cfg["Mode"] = "multiple"

        self.update_cfg()

    def change_type_sate(self):
        if self.pb_breath.isEnabled():
            self.pb_breath.setEnabled(False)
            self.pb_heart.setEnabled(True)
            self.widget_cfg["vitalsign_mode"] = "breath"
        elif self.pb_heart.isEnabled():
            self.pb_breath.setEnabled(True)
            self.pb_heart.setEnabled(False)
            self.widget_cfg["vitalsign_mode"] = "heart"
        self.update_cfg()

    def save_result_chooser(self):
        self.save_result_chooser_group = QGroupBox("save type")
        layout = QGridLayout()
        self.ch_suresave = QCheckBox()

    def update_cfg(self):
        if self.saver_widget.ch_suresave.isChecked():
            self.pb_start_estimate.setEnabled(True)
        else:
            self.pb_start_estimate.setEnabled(False)
        self.pass_cfg.emit(self.widget_cfg)

    def cfg_update_event(self):

        self.single_widget.dataloader.te.setPlainText(self.widget_cfg["single_file_path"])
        if self.widget_cfg["vitalsign_mode"] == "breath":
            self.pb_breath.setEnabled(False)
            self.pb_heart.setEnabled(True)
        else:
            self.pb_breath.setEnabled(True)
            self.pb_heart.setEnabled(False)
