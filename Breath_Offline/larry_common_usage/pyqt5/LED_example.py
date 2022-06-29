import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
from pyqt_led import Led

class Demo(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._shape = np.array(['capsule', 'circle', 'rectangle'])
        self._color = np.array(['blue', 'green', 'orange', 'purple', 'red',
                                'yellow'])
        self._layout = QGridLayout(self)
        self._create_leds()
        self._arrange_leds()
        self.resize(400, 200)
        self.setWindowTitle('pyqt-led Demo')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def _create_leds(self):
        for s in self._shape:
            for c in self._color:
                exec('self._{}_{} = Led(self, on_color=Led.{}, shape=Led.{}, build="debug")'
                     .format(s, c, c, s))
                exec('self._{}_{}.setFocusPolicy(Qt.NoFocus)'.format(s, c))
                exec('self._{}_{}.turn_on(True)'.format(s, c))

    def _arrange_leds(self):
        for r in range(3):
            for c in range(6):
                exec('self._layout.addWidget(self._{}_{}, {}, {}, 1, 1, \
                      Qt.AlignCenter)'
                     .format(self._shape[r], self._color[c], r, c))

app = QApplication(sys.argv)
demo = Demo()
demo.show()
sys.exit(app.exec_())