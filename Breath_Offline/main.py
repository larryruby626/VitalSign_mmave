from PyQt5.QtWidgets import *
from Layout_Widget.phase_watch_widget import PhaseWatchingTools
from Layout_Widget.offline_system_widget import OfflineSystemWidget
from Layout_Widget.setting_widget import SettingWidget
from Layout_Widget.parm_side_pannel_widget import ParmAdjustSidepanel
from Layout_Widget.widget_cfg import build_config
import sys

class Window(QMainWindow):
    def __init__(self,app):
        super().__init__()

        # set the title of main window
        self.setWindowTitle('Larry Vital Sign - GUI')
        self.widget_cfg = build_config()
        self.app = app
        # set the size of window
        self.Width = 1200
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = QPushButton('Setting', self)
        self.btn_2 = QPushButton('Offline System', self)
        self.btn_3 = QPushButton('Phase watching tool', self)
        self.btn_4 = QPushButton('future...', self)

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()

        self.initUI()

    def initUI(self):
        self.ParmAdjust_group = QGroupBox("Parm Adjust")
        self.ParmAdjust_widget = ParmAdjustSidepanel(cfg=self.widget_cfg)
        self.ParmAdjust_group.setLayout(self.ParmAdjust_widget)
        self.ParmAdjust_widget.pass_cfg.connect(self.update_cfg)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addWidget(self.ParmAdjust_group)

        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        # -----------------
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(0)
        self.widget_cfg["current_wiget"] = "0"

    def button2(self):
        self.right_widget.setCurrentIndex(1)
        self.widget_cfg["current_wiget"] = "1"
        self.offlinesystem.file_init()

    def button3(self):
        self.right_widget.setCurrentIndex(2)
        self.widget_cfg["current_wiget"] = "2"
        self.phase_watching_tools.file_init()
    def button4(self):
        self.right_widget.setCurrentIndex(3)

    # ----------------- 
    # pages

    def ui1(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 1'))
        main_layout.addStretch(5)
        self.setting_widget = SettingWidget(cfg = self.widget_cfg,app=self.app)
        self.setting_widget.pass_cfg.connect(self.update_cfg)
        return self.setting_widget

    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 2'))
        main_layout.addStretch(5)
        self.offlinesystem = OfflineSystemWidget(app,cfg=self.widget_cfg)
        return self.offlinesystem

    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 3'))
        main_layout.addStretch(5)
        self.phase_watching_tools =PhaseWatchingTools(app,cfg=self.widget_cfg)
        return self.phase_watching_tools
    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 4'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    # ----- motion
    def update_cfg(self):
        if self.widget_cfg["Mode"] == "single":
            self.btn_2.setEnabled(True)
            self.btn_3.setEnabled(True)
            self.ParmAdjust_group.setEnabled(True)
        elif self.widget_cfg["Mode"] == "multiple":
            self.btn_2.setEnabled(False)
            self.btn_3.setEnabled(False)
            self.ParmAdjust_group.setEnabled(False)

        self.offlinesystem.cfg_update_event()
        self.phase_watching_tools.cfg_update_event()
        self.ParmAdjust_widget.cfg_update_event()
        self.setting_widget.cfg_update_event()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window(app)
    ex.show()
    sys.exit(app.exec_())