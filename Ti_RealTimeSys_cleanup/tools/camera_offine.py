import cv2
import threading as th
import time
import mediapipe as mp
import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread

class CamCapture():

    def __init__(self, path):
        super(CamCapture, self).__init__()
        self.path = path
        self.capture = cv2.VideoCapture(path)
        length = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        print(" frame len is {}".format(length))
        print(self.capture)
        print("{} frame com is {}".format(path,self.capture.get(7)))
        self.disply_width = 640
        self.display_height = 480

    def get_frame(self):

        ret,frame  = self.capture.read()

        if ret == True :
            # frame = np.rot90(frame,2)

            qt_img = self.convert_cv_qt(frame)

            return  qt_img

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line,
                                            QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

# path = "D:/kaiku_report/2021-0418for_posheng/larry_test1.mp4"
# x1= CamCapture(path)
# while True:
#     x1.get_frame()
