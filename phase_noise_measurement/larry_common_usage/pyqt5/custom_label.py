from larry_common_usage.pyqt5.CleanWidget import CustomWidget
import sys
from PyQt5.QtWidgets import QLabel, QApplication, QHBoxLayout

class CustomLabel(QLabel):
    def __init__(self, width, height, init_text, parent=None):
        super(CustomLabel, self).__init__(parent)           # parent
        self.setText(init_text)
        self.resize(width, height)

    def setborder(self):
        self.setStyleSheet("border: 1px solid black;")


if __name__ == "__main__":
    app = QApplication([])
    w = CustomWidget()
    H = QHBoxLayout()
    lb = CustomLabel(200, 100, "fuckworld")
    lb.setborder()
    w.setLayout(H)
    H.addWidget(lb)
    w.show()
    sys.exit(app.exec_())