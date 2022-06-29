from tkinter import filedialog
from PyQt5.QtCore import QThread, pyqtSignal
from scipy.signal import savgol_filter
import sys
import time
import socket
import numpy as np
import threading
from queue import Queue
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
# -----------------------------------------------
from tools.real_time_pd_qthread import UdpListener, DataProcessor
from radar_config import SerialConfig
from tools.ultis import send_cmd, get_color, ConnectDca
from tools.Webcam_Save_Vedio_Qthread import RTSPVideoWriterObject
# -----------------------------------------------
from layout.app_layout_2t4r_predict import Ui_MainWindow

set_radar = SerialConfig(name='ConnectRadar', CLIPort='COM30', BaudRate=115200)  # connect to your comport
config = '../radar_config/xwr68xx_profile_2021_03_23T08_12_36_405.cfg'

class Realtime_sys():

    def __init__(self):
        adc_sample = 64
        chirp = 16
        tx_num = 3
        rx_num = 4
        self.radar_config = [adc_sample, chirp, tx_num, rx_num]
        frame_length = adc_sample * chirp * tx_num * rx_num * 2
        # Host setting
        address = ('192.168.33.30', 4098)
        buff_size = 2097152
        self.save_frame_len = 1000
        # call class
        self.bindata = Queue()
        self.rawdata = Queue()
        self.predict_data = Queue()
        self.collector = UdpListener('Listener', frame_length, address, buff_size, self.bindata, self.rawdata)
        self.processor = DataProcessor('Processor', self.radar_config, self.bindata, "0105", status=0)
        self.processor.data_signal.connect(self.Qthreadupdate_fig)
        self.pd_save_status = 0
        self.pd_save = []
        self.pd = []
        self.rdi = []
        self.rai = []
        self.raw = []

        self.btn_status = False
        self.run_state = False
        self.camera = True
        self.sure_next = True
        self.sure_image = True
        self.sure_start_predict = False
        self.frame_count = 0
        # ----- for test Usage ----
        self.sure_select = False
        self.realtime_mdoe = True
        self.rai_mode = 0
        #   ----- Qthread ------
        self.preprocesser = DataPreprocess()
        self.preprocesser.pysig_sliding_voxel.connect(self.show_trajectory)
        path = "D:\\thumouse_new_dataset_32_32\\model\\voxel.h5"
        self.model = load_model(path)  # Load a HDF5 file
        self.TracjectPredict = TracjectPredict(self.model)
        self.TracjectPredict.preidct_xyz.connect(self.slot_tracject)
        self.current_status = True

    def predict_start(self):
        if self.current_status == True:
            self.cam_plane_x = []
            self.cam_plane_y = []
            self.predict_data = Queue()
            self.sure_start_predict = True
            self.current_status = False
            self.start_predict.setText("STOP")
        else:
            self.predict_stop()
            self.current_status = True
            self.start_predict.setText("Start predict")

    def predict_stop(self):
        self.sure_start_predict = False
        self.preprocesser.sliding_voxel_process(self.predict_data)

    def smooth(self, data):
        window = 9
        order = 3
        y_sf = savgol_filter(data, window, order)
        return y_sf

    def smooth1(self, data):
        window = 9
        order = 3
        y_sf = savgol_filter(data, window, order)
        return y_sf

    def slot_tracject(self, out_xyz):
        self.xy_plane_x = out_xyz[:, 0] * -1
        self.xy_plane_y = out_xyz[:, 1] * -1
        self.xy_plane.setData(self.smooth(self.xy_plane_x), self.smooth(self.xy_plane_y))
        self.cam_plane_x = np.array(self.cam_plane_x) * -1
        self.cam_plane_y = np.array(self.cam_plane_y) * -1
        self.cam_plane.setData(self.smooth1((self.cam_plane_x)), self.smooth((self.cam_plane_y)))

    def show_trajectory(self, data):
        data = np.reshape(data, [-1, 3, 1, 32, 32, 32])
        self.TracjectPredict.predict(data)

    def restart(self):
        self.cam1_thread.restart_videowriter()
        self.cam2_thread.restart_videowriter()

    def restart_radar(self):
        set_radar.StopRadar()

    def append_rawdata(self, rawdata):
        self.raw.append(rawdata)

    def Qthreadupdate_fig(self, rdi, rai, pd):
        self.processor.Sure_staic_RM = self.static_rm.isChecked()
        self.pd = pd
        if self.pd_save_status == 1:
            self.raw.append(self.rawdata.get())
            self.frame_count += 1
            if self.frame_count >= self.save_frame_len:
                self.StopRecord()
                self.SaveData()\

        self.img_rdi.setImage(np.rot90(rdi, 1))
        self.img_rai.setImage(np.fliplr(np.flip(rai, axis=0)).T)
        pos = np.transpose(pd, [1, 0])

        if self.sure_start_predict:
            self.predict_data.put(pos)
            print(self.predict_data.qsize())

        p13d.setData(pos=pos[:, :3], color=[1, 0.35, 0.02, 1], pxMode=True)

    def save_process(self):
        self.raw = np.append(self.raw, self.rawData.get())
        self.frame_count += 1
        if self.frame_count >= self.save_frame_len:
            self.StopRecord()

    def update_cam1(self, img):
        self.image_label1.setPixmap(img)

    def update_cam2(self, img):
        self.image_label2.setPixmap(img)

    def slot(self, object):
        print("Key was pressed, id is:", self.radio_group.id(object))

        self.rai_mode = self.radio_group.id(object)

        if self.rai_mode == 1:
            self.view_rai.setRange(QtCore.QRectF(10, 0, 170, 80))
        else:
            self.view_rai.setRange(QtCore.QRectF(-5, 0, 100, 60))

    def StartRecord(self):
        self.starttime = time.time()
        self.processor.status = 1
        self.collector.status = 1
        if self.camera == True:
            self.cam1_thread.record = True
            self.cam2_thread.record = True
        self.pd_save_status = 1
        print('Start Record Time:', (time.ctime(time.time())))
        print('=======================================')

    def StopRecord(self):
        total = time.time() - self.starttime
        fps = self.save_frame_len / total
        print("FPS is {}".format(fps))
        self.processor.status = 0
        self.collector.status = 0
        self.pd_save_status = 0
        if self.camera == True:
            self.cam1_thread.record = False
            self.cam2_thread.record = False
            self.cam1_thread.release_video()
            self.cam2_thread.release_video()
        print('Stop Record Time:', (time.ctime(time.time())))
        print('=======================================')

    def ConnectDca1000(self):
        # dca1000  = ConnectDca()
        # dca1000.start()
        global sockConfig, FPGA_address_cfg
        print('Connect to DCA1000')
        print('=======================================')
        config_address = ('192.168.33.30', 4096)
        FPGA_address_cfg = ('192.168.33.180', 4096)
        cmd_order = ['9', 'E', '3', 'B', '5', '6']
        sockConfig = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockConfig.bind(config_address)
        for k in range(5):
            # Send the command
            sockConfig.sendto(send_cmd(cmd_order[k]), FPGA_address_cfg)
            time.sleep(0.1)
            # Request data back on the config port
            msg, server = sockConfig.recvfrom(2048)
            # print('receive command:', msg.hex())
        sockConfig.close()

    def openradar(self):
        set_radar.StopRadar()
        set_radar.SendConfig(config)
        self.collector.start()
        self.processor.start()

        # self.update_figure()
        print('=============openradar=================')

    def exit(self):
        if self.camera == True:
            self.cam1_thread.quit()
            self.cam2_thread.quit()
        set_radar.StopRadar()

        self.app.instance().exit()

    def SaveData(self):
        print("save the npy")
        np.save("C:/Users/user/Desktop/thumouse_dataset_index_Enhance/raw.npy", self.raw)
        self.raw = []
        self.frame_count = 0

    def calulate1(self, arr):
        x = arr[0]
        y = arr[1]
        if self.sure_start_predict == True:
            self.cam_plane_x.append(x)
            self.cam_plane_y.append(y)

    def calulate2(self, arr):  # cam1--> above camera x2{x},y2{y}
        scale_x2 = 45 / 640 * 0.015
        scale_y2 = 33 / 480 * 0.015
        x2 = np.array(arr[0])
        y2 = np.array(arr[1])
        x2 = np.where(x2 is not None, x2, np.double(320))
        x2 = x2.astype(np.double)
        x2 = (x2 * scale_x2)
        x2 -= ((640 * scale_x2) / 2)
        x2 = np.round(x2, 3)
        x2 += 0.015

        y2 = np.where(y2 is not None, y2, np.double(480))
        y2 = y2.astype(np.double)
        y2 = (y2 * scale_y2)
        y2 = (y2 * -1) + ((480 * scale_y2)) + 0.015 * 8
        y2 = np.round(y2, 3)
        # y2 = y2 + 0.30

        if self.pd != []:
            tmp = np.mean(self.pd, axis=1)
            difx = (tmp[0] - x2[8] * -1)
            dify = (tmp[1] - y2[8])
            yy = np.min(self.pd[1, :])
            # print("\n ================")
            # print("校正x:{}  radarx:{}  camx:{}".format(difx/0.015  ,tmp[0], x2[8]*-1/0.015))
            # print("\n校正y:{}  radary:{}  camy:{}".format(dify/0.015,yy, y2[8]/0.015))

    def open_camera(self):
        self.save_frame_len = int(self.camera_frame_count_lb.toPlainText())
        self.cam1_thread = RTSPVideoWriterObject(0, "vedio1", save_frame_len=self.save_frame_len, mediapipe_mode=1)
        self.cam2_thread = RTSPVideoWriterObject(1, "vedio2", save_frame_len=self.save_frame_len, mediapipe_mode=0)
        self.cam1_thread.change_pixmap_signal.connect(self.update_cam1)  # Qthread link slot
        self.cam2_thread.change_pixmap_signal.connect(self.update_cam2)
        self.cam1_thread.hand_points.connect(self.calulate1)  # Qthread link slot
        self.cam2_thread.hand_points.connect(self.calulate2)  # Qthread link slot
        self.cam1_thread.start()
        self.cam2_thread.start()

        self.camera = True

    def build_GLline(self, p1, p2):
        x1 = p1[0];
        y1 = p1[1];
        z1 = p1[2]
        x2 = p2[0];
        y2 = p2[1];
        z2 = p2[2]
        return gl.GLLinePlotItem(pos=np.array([[[x1, y1, z1], [x2, y2, z2]]]), color=[128, 255, 128, 255],
                                 antialias=False)

    def bounding_box(self, view_PD):
        all_len = 0.234375
        half_len = all_len / 2
        self.line1 = self.build_GLline([half_len, 0, half_len], [-1 * half_len, 0, half_len])
        self.line2 = self.build_GLline([half_len, all_len, half_len], [-1 * half_len, all_len, half_len])
        self.line3 = self.build_GLline([half_len, 0, -1 * half_len], [-1 * half_len, 0, -1 * half_len])
        self.line4 = self.build_GLline([half_len, all_len, -1 * half_len], [-1 * half_len, all_len, -1 * half_len])

        self.line5 = self.build_GLline([half_len, 0, half_len], [half_len, 0, -1 * half_len])
        self.line6 = self.build_GLline([half_len, 0, half_len], [half_len, all_len, half_len])
        self.line7 = self.build_GLline([half_len, all_len, half_len], [half_len, all_len, -1 * half_len])
        self.line8 = self.build_GLline([half_len, 0, -1 * half_len], [half_len, all_len, -1 * half_len])

        self.line9 = self.build_GLline([-1 * half_len, 0, half_len], [-1 * half_len, 0, -1 * half_len])
        self.line10 = self.build_GLline([-1 * half_len, 0, half_len], [-1 * half_len, all_len, half_len])
        self.line11 = self.build_GLline([-1 * half_len, all_len, half_len], [-1 * half_len, all_len, -1 * half_len])
        self.line12 = self.build_GLline([-1 * half_len, 0, -1 * half_len], [-1 * half_len, all_len, -1 * half_len])

        view_PD.addItem(self.line1)
        view_PD.addItem(self.line2)
        view_PD.addItem(self.line3)
        view_PD.addItem(self.line4)
        view_PD.addItem(self.line5)
        view_PD.addItem(self.line6)
        view_PD.addItem(self.line7)
        view_PD.addItem(self.line8)
        view_PD.addItem(self.line9)
        view_PD.addItem(self.line10)
        view_PD.addItem(self.line11)
        view_PD.addItem(self.line12)

    def plot(self):
        global img_rdi, img_rai, updateTime, view_text, count, angCurve, ang_cuv, img_cam, savefilename, view_rai, p13d, nice
        # ---------------------------------------------------
        self.app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        MainWindow.show()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        self.radio_group = ui.radio_btn_group
        self.static_rm = ui.sure_static
        self.image_label1 = ui.image_label1
        self.image_label2 = ui.image_label2
        # ----------------- realtime btn clicked connet -----------------
        self.start_dca_rtbtn = ui.dca1000_rtbtn
        self.send_cfg_rtbtn = ui.sendcfg_rtbtn
        self.record_rtbtn = ui.record_rtbtn
        self.stop_rtbtn = ui.stop_rtbtn
        self.save_rtbtn = ui.save_rtbtn
        self.exit_rtbtn = ui.exit_rtbtn
        self.restart_rtbtn = ui.restart_rtbtn
        self.restart_radar_rtbtn = ui.restart_radar_rtbtn
        self.set_camera_true_btn = ui.btn_frame_count
        self.camera_frame_count_lb = ui.edit_frame_count
        self.frame_count_lb = ui.label_frame_count1
        self.start_predict = ui.start_predict
        # self.stop_predict  = ui.stop_predict
        # ----------------- btn clicked connet -----------------
        self.start_dca_rtbtn.clicked.connect(self.ConnectDca1000)
        self.send_cfg_rtbtn.clicked.connect(self.openradar)
        self.record_rtbtn.clicked.connect(self.StartRecord)
        self.exit_rtbtn.clicked.connect(self.exit)
        self.save_rtbtn.clicked.connect(self.SaveData)
        self.restart_rtbtn.clicked.connect(self.restart)
        self.restart_radar_rtbtn.clicked.connect(self.restart_radar)
        self.set_camera_true_btn.clicked.connect(self.open_camera)
        self.radio_group.buttonClicked.connect(self.slot)
        self.start_predict.clicked.connect(self.predict_start)
        # -----------------------------------------------------
        self.view_xy = ui.graphicsView_xy
        self.xy_plane = pg.PlotDataItem(pen=pg.mkPen(width=1, color='r'), size=1)
        self.xy_plane_x = []
        self.xy_plane_y = []
        self.view_xy.addItem(self.xy_plane)

        self.view_cam = ui.graphicsView_cam
        self.cam_plane = pg.PlotDataItem(pen=pg.mkPen(width=1, color='b'), size=1)
        self.cam_plane_x = []
        self.cam_plane_y = []
        self.view_cam.addItem(self.cam_plane)

        self.view_rdi = ui.graphicsView.addViewBox()
        self.view_rai = ui.graphicsView_2.addViewBox()
        view_PD = ui.graphicsView_3
        # ---------------------------------------------------
        # lock the aspect ratio so pixels are always square
        self.view_rdi.setAspectLocked(True)
        self.view_rai.setAspectLocked(True)
        self.img_rdi = pg.ImageItem(border='w')
        self.img_rai = pg.ImageItem(border='w')
        self.img_rai_ele = pg.ImageItem(border='w')
        img_cam = pg.ImageItem(border='w')
        # -----------------
        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        view_PD.addItem(xgrid)
        view_PD.addItem(ygrid)
        view_PD.addItem(zgrid)
        xgrid.translate(0, 10, -10)
        ygrid.translate(0, 0, 0)
        zgrid.translate(0, 10, -10)
        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        p13d = gl.GLScatterPlotItem(pos=np.zeros([1, 3]), color=[50, 50, 50, 255])
        origin = gl.GLScatterPlotItem(pos=np.zeros([1, 3]), color=[255, 0, 0, 255])
        coord = gl.GLAxisItem(glOptions="opaque")
        coord.setSize(10, 10, 10)
        view_PD.addItem(p13d)
        view_PD.addItem(coord)
        view_PD.addItem(origin)
        view_PD.orbit(45, 6)
        view_PD.pan(1, 1, 1, relative=1)
        # self.lineup(view_PD)
        self.bounding_box(view_PD)
        # ang_cuv = pg.PlotDataItem(tmp_data, pen='r')
        # Colormap
        position = np.arange(64)
        position = position / 64
        position[0] = 0
        position = np.flip(position)
        colors = get_color()
        colors = np.flip(colors, axis=0)
        color_map = pg.ColorMap(position, colors)
        lookup_table = color_map.getLookupTable(0.0, 1.0, 256)
        self.img_rdi.setLookupTable(lookup_table)
        self.img_rai.setLookupTable(lookup_table)
        self.img_rai_ele.setLookupTable(lookup_table)
        self.view_rdi.addItem(self.img_rdi)
        self.view_rai.addItem(self.img_rai)
        self.view_rai.addItem(self.img_rai_ele)
        self.view_rdi.setRange(QtCore.QRectF(0, 0, 30, 70))
        self.view_rai.setRange(QtCore.QRectF(10, 0, 160, 80))
        updateTime = ptime.time()
        self.app.instance().exec_()

    def lineup(self, view_PD):
        ###---------------------------------------------
        self.hand = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=[0, 255, 0, 255], pxMode=True)
        view_PD.addItem(self.hand)
        self.indexfinger = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=[255, 0, 0, 255], pxMode=True)
        view_PD.addItem(self.indexfinger)
        self.thumb = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=[255, 0, 0, 255], pxMode=True)
        view_PD.addItem(self.thumb)
        origin = gl.GLScatterPlotItem(pos=np.array(
            [[0, 0.075, 0], [0, 0.075 * 2, 0], [0, 0.075 * 3, 0], [0, 0.075 * 4, 0], [0, 0.075 * 5, 0],
             [0, 0.075 * 6, 0]]), color=[255, 255, 255, 255])
        origin1 = gl.GLScatterPlotItem(pos=np.array(
            [[0.075 * -3, 0.3, 0], [0.075 * -2, 0.3, 0], [0.075 * -1, 0.3, 0], [0.075 * 1, 0.3, 0],
             [0.075 * 2, 0.3, 0], [0.075 * 3, 0.3, 0]]), color=[255, 255, 255, 255])
        origin2 = gl.GLScatterPlotItem(pos=np.array(
            [[0, 0.3, 0.075 * -3], [0, 0.3, 0.075 * -2], [0, 0.3, 0.075 * -1], [0, 0.3, 0.075 * 1],
             [0, 0.3, 0.075 * 2], [0, 0.3, 0.075 * 3]]), color=[255, 255, 255, 255])
        view_PD.addItem(origin)
        view_PD.addItem(origin1)
        view_PD.addItem(origin2)
        origin_P = gl.GLScatterPlotItem(pos=np.array(
            [[0, 0, 0]]), color=[255, 0, 0, 255])
        view_PD.addItem(origin_P)
        self.hand_line = gl.GLLinePlotItem(pos=np.array([[[0, 0, 0], [0, 0.075 * 10, 0]]]),
                                           color=[128, 255, 128, 255], antialias=False)
        self.hand_liney = gl.GLLinePlotItem(pos=np.array([[[0, 0, 0], [0, 0.075 * 10, 0]]]),
                                            color=[128, 255, 128, 255], antialias=False)
        self.hand_linex_2 = gl.GLLinePlotItem(
            pos=np.array([[[-0.075 * 8, 0.075 * 4, 0.075 * 2], [0.075 * 8, 0.075 * 4, 0.075 * 2]]]),
            color=[128, 255, 128, 255], antialias=False)
        self.hand_linex_1 = gl.GLLinePlotItem(
            pos=np.array([[[-0.075 * 8, 0.075 * 4, 0.075 * 1], [0.075 * 8, 0.075 * 4, 0.075 * 1]]]),
            color=[128, 255, 128, 255], antialias=False)
        self.hand_linex_d1 = gl.GLLinePlotItem(
            pos=np.array([[[-0.075 * 8, 0.075 * 4, 0.075 * -1], [0.075 * 8, 0.075 * 4, 0.075 * -1]]]),
            color=[128, 255, 128, 255], antialias=False)
        self.hand_linex_d2 = gl.GLLinePlotItem(
            pos=np.array([[[-0.075 * 8, 0.075 * 4, 0.075 * -2], [0.075 * 8, 0.075 * 4, 0.075 * -2]]]),
            color=[128, 255, 128, 255], antialias=False)

        self.hand_linex = gl.GLLinePlotItem(pos=np.array([[[-0.075 * 8, 0.075 * 4, 0], [0.075 * 8, 0.075 * 4, 0]]]),
                                            color=[128, 255, 128, 255], antialias=False)

        self.hand_linez = gl.GLLinePlotItem(pos=np.array([[[0, 0.075 * 4, -0.075 * 8], [0, 0.075 * 4, 0.075 * 8]]]),
                                            color=[0.5, 0.5, 0.9, 1], antialias=False)
        view_PD.addItem(self.hand_line)
        view_PD.addItem(self.hand_liney)
        view_PD.addItem(self.hand_linez)
        view_PD.addItem(self.hand_linex)


class TracjectPredict(QThread):
    preidct_xyz = pyqtSignal(np.ndarray)

    def __init__(self, model):
        super(TracjectPredict, self).__init__()
        self.model = model

    def predict(self, slding_voxel_dataIn):
        predict_out = self.model.predict(slding_voxel_dataIn)
        finalout = predict_out[:, -1, :]
        self.preidct_xyz.emit(finalout)


class DataPreprocess(QThread):
    pysig_sliding_voxel = pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super(DataPreprocess, self).__init__(*args, **kwargs)
        self.number = 0
        self.out_arr = np.zeros([3, 1, 32, 32, 32])

    def pointcloud2voxel(self, pd_dataIn):
        out_radar_p = []

        for i in range(len(pd_dataIn)):
            tmp_frame = pd_dataIn[i]
            arr = np.ndarray([1, 32, 32, 32])
            arr[:] = False

            point_count = 0
            tx = 0
            ty = 0
            tz = 0
            for c in range(tmp_frame.shape[0]):
                x = round(tmp_frame[c][0] / 0.009375 + 16)
                y = round(tmp_frame[c][1] / 0.009375)
                z = round(tmp_frame[c][2] / 0.009375 + 16)
                empty = False
                if x < 32 and y < 32 and z < 32 and x > 0 and y > 0 and z > 0:
                    # print("x:{} y:{} z:{}".format(x,y,z))
                    arr[0][x][y][z] = True
                    point_count += 1
                    tx += tmp_frame[c][0]
                    ty += tmp_frame[c][1]
                    tz += tmp_frame[c][2]
            out_radar_p.append(arr)
        return out_radar_p

    def voxel(self, inputdata, time_step, voxel_size):
        #   datainput shape --> (data_len, 1, 25, 25, 25)
        data_len = len(inputdata)
        sliding_len = data_len - (time_step - 1)
        out_arr = np.zeros([sliding_len, time_step, 1, voxel_size, voxel_size, voxel_size])

        for i in range(sliding_len):
            tmp = []
            for j in range(time_step):
                tmp.append(inputdata[i + j])
                out_arr[i, j] = tmp[j]
        # print(np.shape(out_arr))
        return out_arr

    def sliding_voxel_process(self, input_Queue):

        out_pd_arr = []
        for i in range(input_Queue.qsize()):
            if input_Queue.qsize() != 0:
                data = input_Queue.get()
                out_pd_arr.append(data)

        total_voxel = self.pointcloud2voxel(out_pd_arr)
        sliding_voxel = self.voxel(total_voxel, 3, 32)
        print(np.shape(sliding_voxel))
        self.pysig_sliding_voxel.emit(sliding_voxel)


if __name__ == '__main__':
    print('======Real Time Data Capture Tool======')
    count = 0
    realtime = Realtime_sys()
    plotIMAGE = threading.Thread(target=realtime.plot())
    plotIMAGE.start()
    print("Program Close")
    set_radar.StopRadar()
    sys.exit()
