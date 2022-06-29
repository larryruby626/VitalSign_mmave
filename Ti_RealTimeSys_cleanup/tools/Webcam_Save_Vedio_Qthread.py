import time
from time import time as timer
from threading import Thread
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import keyboard  # using module keyboard
import numpy as np
import cv2
import mediapipe as mp
from PyQt5.QtGui import QPixmap
from qimage2ndarray.dynqt import QtGui
from mediapipe_proecss import larry_draw


class RTSPVideoWriterObject(QThread):
    change_pixmap_signal = pyqtSignal(QPixmap)
    hand_points = pyqtSignal(list)

    def __init__(self, src=0, filename="", save_frame_len=0, mediapipe_mode=1):
        super(RTSPVideoWriterObject, self).__init__()
        # Create a VideoCapture object
        self.wc_number = src
        self.record_frame_len = save_frame_len
        self.capture = cv2.VideoCapture(src)
        # self.capture.set(cv2.CV_CAP_PROP_FPS, 25)
        self.capture.set(cv2.CAP_PROP_FPS, 20)
        print(self.capture.get(cv2.CAP_PROP_FPS))
        self.mode = mediapipe_mode
        self.capture.set(3, 640)  # 設定解析度
        self.capture.set(4, 480)
        self.record = False
        self.counter = 0
        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))
        # Set up codec and output video settings
        self.codec = cv2.VideoWriter_fourcc(*'mp4v')
        self.mp4_path = 'C:/Users/user/Desktop/thumouse_training_data_new/' + filename + ".mp4"
        self.output_video = cv2.VideoWriter(self.mp4_path, self.codec, 20, (self.frame_width, self.frame_height))
        self.readframe = 0
        self.fps_count = 0
        self.start_time = time.time()
        if self.mode == 1:
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)
        print("--- cam{} init work ---".format(self.wc_number))

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line,
                                            QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(cv_img.shape[1], cv_img.shape[0], Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def run(self):
        self.update()

    def update(self):
        # Read the next frame from the stream in a different thread
        timestart = time.time()
        while True:
            if self.capture.isOpened():

                (self.status, self.frame) = self.capture.read()
                if self.mode == 1:
                    print(self.frame)
                    image = cv2.cvtColor(self.frame.copy(), cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    if self.wc_number == 1:
                        image = cv2.flip(image, 1)
                        image = cv2.flip(image, 0)
                    results = self.hands.process(image)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(
                                image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        x, y = larry_draw(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                        scale_x1 = 56 / 640 * 0.015  # cm / pixel * (0.015 point/cm)
                        scale_y1 = 44 / 480 * 0.015
                        x1 = np.array(x)
                        y1 = np.array(y)
                        if (y1 != None).all() == True:
                            y1 = y1.astype(np.double)
                            y1 = np.round((y1 * scale_y1), 3)
                            y1 -= ((480 * scale_y1) / 2)
                            x1 = x1.astype(np.double)
                            x1 = np.round((x1 * scale_x1), 3)
                            x1 -= ((640 * scale_x1) / 2)
                            self.hand_points.emit([x1[8], y1[8]])
                        cv2.line(image, (0, 239), (640, 239), (0, 0, 255), 2)
                        cv2.line(image, (0, 240), (640, 240), (0, 0, 255), 2)
                        cv2.line(image, (319, 0), (319, 480), (0, 0, 255), 2)
                        cv2.line(image, (320, 0), (320, 480), (0, 0, 255), 2)

                        img = self.convert_cv_qt(image)
                        self.change_pixmap_signal.emit(img)
                    else:
                        if self.wc_number == 1:
                            image = cv2.flip(image, 1)
                            image = cv2.flip(image, 0)
                        img = self.convert_cv_qt(self.frame)
                        self.change_pixmap_signal.emit(img)
                else:
                    img = self.convert_cv_qt(self.frame)
                    self.change_pixmap_signal.emit(img)
                # print("cam1{} gogo ".format(self.wc_number))
                if self.record:
                    print("cam{} frame:{}".format(self.wc_number, self.readframe))
                    self.save_frame()
                    self.readframe += 1

                time_end = time.time() - timestart
                self.fps_count += 1
                fps = self.fps_count / time_end
                if self.fps_count % 200 == 0:
                    print(fps)

    def show_frame(self):
        # Display frames in main program
        if self.status:
            cv2.imshow('frame' + str(self.wc_number), self.frame)

    def line_up(self, image):
        cv2.line(image, (0, 240), (640, 240), (255, 0, 0), 1, 1)
        cv2.line(image, (0, 241), (640, 241), (255, 0, 0), 1, 1)
        cv2.line(image, (320, 0), (320, 480), (255, 0, 0), 1, 1)
        cv2.line(image, (321, 0), (321, 480), (255, 0, 0), 1, 1)
        return image

    def save_frame(self):
        # Save obtained frame into video output file
        self.output_video.write(self.frame)
        self.counter += 1

    def state_change(self):
        self.record = not self.record

    def release_video(self):
        # close the webcam process
        print("save the video")
        self.output_video.release()

    def get_fsp(self):
        if self.fps_count != 0:
            fps = self.fps_count / (time.time() - self.start_time)
            print("Time cam{} FPS is  : {} frame/perseconds".format(self.wc_number, fps))

    def restart_videowriter(self):
        self.output_video = cv2.VideoWriter(self.mp4_path, self.codec, 30, (self.frame_width, self.frame_height))
        self.readframe = 0


if __name__ == '__main__':
    rtsp_stream_link = 0
    rtsp_stream_link1 = 1
    save_frame_len = 120


    # video_stream_widget = RTSPVideoWriterObject(rtsp_stream_link, "vedio1",save_frame_len=save_frame_len)
    # video_stream_widget2 = RTSPVideoWriterObject(rtsp_stream_link1, "vedio2",save_frame_len=save_frame_len)
    # print("start")
    # while(1):
    #     print(video_stream_widget2.counter)
    #     if keyboard.is_pressed('s'):  # if key 'q' is pressed
    #         video_stream_widget.record = True
    #         video_stream_widget2.record = True
    #     if video_stream_widget.counter >= 120:
    #         video_stream_widget.close_webcam()
    #         print(type(video_stream_widget2.frame))
    #
    #         video_stream_widget.record = False
    #     if video_stream_widget2.counter >= 120:
    #         video_stream_widget2.close_webcam()
    #         video_stream_widget2.record = False
    #     if  not(video_stream_widget.record & video_stream_widget2.record):
    #         break
    def update_image(img):
        cv2.imshow("mats", img)


    video_stream_widget = RTSPVideoWriterObject(rtsp_stream_link, "vedio1", save_frame_len=save_frame_len)
    video_stream_widget.start()
    video_stream_widget.change_pixmap_signal.connect(update_image)
    video_stream_widget.record = True

    # while True:
    #     if keyboard.is_pressed('s'):  # if key 'q' is pressed
    #         video_stream_widget.record = False
    #         video_stream_widget.close_webcam()
    #         break
