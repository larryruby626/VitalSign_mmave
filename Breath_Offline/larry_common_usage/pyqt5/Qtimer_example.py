#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('my window')
        self.setGeometry(50, 50, 200, 150)

        self.mylabel = QLabel('timer', self)
        self.mylabel.setFont(QFont('Arial', 24))
        self.mylabel.move(60, 50)

        self.counter = 0

        self.mytimer = QTimer(self)
        self.mytimer.timeout.connect(self.onTimer)
        self.mytimer.start(1000)

    def onTimer(self):
        self.counter += 1
        self.mylabel.setText(str(self.counter))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())