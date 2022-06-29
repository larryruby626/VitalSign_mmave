import sys
from PyQt5.QtWidgets import (QLabel, QRadioButton,
                             QPushButton, QVBoxLayout,
                             QApplication, QWidget,
                             QButtonGroup)

class basicRadiobuttonExample(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.label = QLabel('Which city do you live in?')
        self.rbtn1 = QRadioButton('New York')
        self.rbtn2 = QRadioButton('Houston')
        self.label2 = QLabel("")

        self.label3 = QLabel('Which state do you live in?')
        self.rbtn3 = QRadioButton('New York')
        self.rbtn4 = QRadioButton('Texas')
        self.label4 = QLabel("")

        self.btngroup1 = QButtonGroup()
        self.btngroup2 = QButtonGroup()

        self.btngroup1.addButton(self.rbtn1)
        self.btngroup1.addButton(self.rbtn2)
        self.btngroup2.addButton(self.rbtn3)
        self.btngroup2.addButton(self.rbtn4)

        self.rbtn1.toggled.connect(self.onClickedCity)
        self.rbtn2.toggled.connect(self.onClickedCity)

        self.rbtn3.toggled.connect(self.onClickedState)
        self.rbtn4.toggled.connect(self.onClickedState)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.rbtn1)
        layout.addWidget(self.rbtn2)
        layout.addWidget(self.label2)

        layout.addWidget(self.label3)
        layout.addWidget(self.rbtn3)
        layout.addWidget(self.rbtn4)
        layout.addWidget(self.label4)

        self.setGeometry(200, 200, 300, 300)

        self.setLayout(layout)
        self.setWindowTitle('PyQt5 Radio Button Example')

        self.show()

    def onClickedCity(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.label2.setText("You live in " + radioBtn.text())

    def onClickedState(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.label4.setText("You live in " + radioBtn.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = basicRadiobuttonExample()
    sys.exit(app.exec_())