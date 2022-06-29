from PyQt5.QtWidgets import QWidget, QApplication
import sys

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)  # parent



if __name__ == "__main__":
    app = QApplication([])
    w = CustomWidget()
    w.show()
    sys.exit(app.exec_())