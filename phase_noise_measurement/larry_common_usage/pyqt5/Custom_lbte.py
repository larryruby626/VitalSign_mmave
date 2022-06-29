from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtGui import QFont

class Custom_lbte(QHBoxLayout):
    def __init__(self, lb_text, de_text, lb_mh, lb_mw, te_mh, te_mw, parent=None):
        super(Custom_lbte, self).__init__(parent)
        self.lb = QLabel(lb_text)
        self.te = QPlainTextEdit(de_text)
        self.lb.setMaximumSize(lb_mw, lb_mh)
        self.te.setMaximumSize(te_mw, te_mh)
        self.addWidget(self.lb)
        self.addWidget(self.te)

    def change_font(self, obj, size, bold=False):
        is_label = isinstance(obj, QLabel)
        if is_label:
            tmp_text = obj.text()
        else:
            tmp_text = obj.toPlainText()
        if bold:
            custom_font = QFont(tmp_text, size,QFont.Bold)
        else:
            custom_font = QFont(tmp_text,size)

        obj.setFont(custom_font)
