from PyQt5.QtWidgets import (QLabel, QRadioButton,
                             QPushButton, QHBoxLayout,
                             QApplication, QWidget,
                             QButtonGroup,QGridLayout,QGroupBox,QVBoxLayout)
from PyQt5.QtCore import pyqtSignal

class ProcessSelectWidget(QGridLayout):
    pass_cfg = pyqtSignal(dict)

    def __init__(self, cfg=None, parent=None):
        super(ProcessSelectWidget, self).__init__()
        self.widget_cfg = cfg

        self.setHorizontalSpacing(20)
        self.setContentsMargins(20,10,20,0)
        self.targetidx_search_group = QGroupBox("target index seacrh")
        self.phase_process_group = QGroupBox("phase process")
        self.calc_HB_group = QGroupBox("Calculate Heartbeat")
        self.build_targetidx()
        self.build_phase_process()
        self.build_Calc_HB_process()
        self.addWidget(self.targetidx_search_group,0,1)
        self.addWidget(self.phase_process_group,0,2)
        self.addWidget(self.calc_HB_group,0,3)
        self.rb_phasemap.setChecked(True)
        self.rb_normal.setChecked(True)
        self.rb_STFT.setChecked(True)

    def build_targetidx(self):
        self.rb_phasemap = QRadioButton("Phase Map Method")
        self.rb_phasemap.toggled.connect(self.update_processs_parameter)
        self.rb_maxrangebin = QRadioButton("Max Range bin")
        self.rb_maxrangebin.toggled.connect(self.update_processs_parameter)
        # self.rb_1d_cfar = QRadioButton("Cfar Method")
        # self.rb_1d_cfar.toggled.connect(self.update_processs_parameter)
        self.rbgroup_targetindx = QButtonGroup()
        self.rbgroup_targetindx.addButton(self.rb_phasemap)
        self.rbgroup_targetindx.addButton(self.rb_maxrangebin)
        # self.rbgroup_targetindx.addButton(self.rb_1d_cfar)
        layout = QVBoxLayout()
        layout.addWidget(self.rb_phasemap)
        layout.addWidget(self.rb_maxrangebin)
        # layout.addWidget(self.rb_1d_cfar)
        self.targetidx_search_group.setLayout(layout)


    def build_phase_process(self):
        self.rb_normal = QRadioButton("Normal Unwrap Phase")
        self.rb_normal.toggled.connect(self.update_processs_parameter)
        self.rb_phasediff = QRadioButton("Phase Difference")
        self.rb_phasediff.toggled.connect(self.update_processs_parameter)
        self.rb_cwt  = QRadioButton("CWT Method")
        self.rb_cwt.toggled.connect(self.update_processs_parameter)
        self.rb_phasecohere = QRadioButton("Phase Coherence")
        self.rb_phasecohere.toggled.connect(self.update_processs_parameter)
        self.rb_VMD  = QRadioButton("VMD　Method")
        self.rb_VMD.toggled.connect(self.update_processs_parameter)

        self.rbgroup_phase_process= QButtonGroup()
        self.rbgroup_phase_process.addButton(self.rb_normal)
        self.rbgroup_phase_process.addButton(self.rb_phasediff)
        self.rbgroup_phase_process.addButton(self.rb_cwt)
        self.rbgroup_phase_process.addButton(self.rb_VMD)
        self.rbgroup_phase_process.addButton(self.rb_phasecohere)
        layout =  QVBoxLayout()
        layout.addWidget(self.rb_normal)
        layout.addWidget(self.rb_phasediff)
        layout.addWidget(self.rb_cwt)
        layout.addWidget(self.rb_VMD)
        layout.addWidget(self.rb_phasecohere)
        self.phase_process_group.setLayout(layout)

    def build_Calc_HB_process(self):
        self.rb_STFT = QRadioButton("Short-time FT")
        self.rb_STFT.toggled.connect(self.update_processs_parameter)
        # self.rb_autocorr = QRadioButton("Autocorrelation")
        # self.rb_autocorr.toggled.connect(self.update_processs_parameter)
        self.rb_IBI  = QRadioButton("InterBeat Interval")
        self.rb_IBI.toggled.connect(self.update_processs_parameter)
        self.rbgroup_calc_hb= QButtonGroup()
        self.rbgroup_calc_hb.addButton(self.rb_STFT)
        # self.rbgroup_calc_hb.addButton(self.rb_autocorr)
        self.rbgroup_calc_hb.addButton(self.rb_IBI)
        layout =  QVBoxLayout()
        layout.addWidget(self.rb_STFT)
        # layout.addWidget(self.rb_autocorr)
        layout.addWidget(self.rb_IBI)
        self.calc_HB_group.setLayout(layout)


    def update_processs_parameter(self):
        targetidx = [self.rb_phasemap.isChecked(),
                     self.rb_maxrangebin.isChecked()]
                     # self.rb_1d_cfar.isChecked()]

        phaseprocess = [self.rb_normal.isChecked(),
                        self.rb_phasediff.isChecked(),
                        self.rb_cwt.isChecked(),
                        self.rb_VMD.isChecked(),
                        self.rb_phasecohere.isChecked()
                        ]
        HBCalc = [self.rb_STFT.isChecked(),
                  # self.rb_autocorr.isChecked(),
                  self.rb_IBI.isChecked()]

        self.widget_cfg["pw_targetidx"] = targetidx
        self.widget_cfg["pw_phaseprocess"] = phaseprocess
        self.widget_cfg["pw_HBCalc"] = HBCalc

        self.pass_cfg.emit(self.widget_cfg)










