from custom_label import CustomLabel
from CleanWidget import CustomWidget
import sys
from PyQt5.QtWidgets import QLabel, QApplication, QHBoxLayout, QWidget

class CustomChooser(QWidget):
    def __init__(self, lb_text, parent=None):
        super(CustomChooser, self).__init__(parent)
        pass
    def add_radio_btn(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    w = CustomWidget()
    H = QHBoxLayout()

    chooser = CustomChooser("hahaha")
    w.setLayout(H)
    H.addWidget(chooser)
    w.show()
    sys.exit(app.exec_())