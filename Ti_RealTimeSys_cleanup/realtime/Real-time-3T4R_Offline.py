from offline_process_3t4r_for_correct import DataProcessor_offline
from scipy.signal import savgol_filter
from tkinter import filedialog
import tkinter as tk
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication
import pyqtgraph.opengl as gl
from tensorflow.keras.models import load_model
import numpy as np
import threading
import sys
import read_binfile
import time
from camera_offine import CamCapture
# -----------------------------------------------
from app_layout_2t4r_offline import Ui_MainWindow

class Realtime_sys():
    def __init__(self):
        self.pd_save_status = 0
        self.pd_save = []
        self.rdi = []
        self.rai = []
        self.btn_status = False
        self.run_state  = False
        self.sure_next = True
        self.sure_image = True
        # self.sure_image = False
        # self.sure_select = True
        self.sure_select = False
        self.frame_count = 0
        self.fps_count = 0
        self.rai_mode = 0
        self.data_proecsss = DataProcessor_offline()
        # self.path = 'C:/Users/user/Desktop/thmouse_training_data/'
        # self.path = 'C:/Users/user/Desktop/thmouse_training_data/circle/time3/'
        # self.path = 'C:/Users/user/Desktop/thmouse_training_data/circle/time2/'
        self.path = 'C:/Users/user/Desktop/thumouse_dataset_index_Enhance/'
        # self.load_gt()
        #   ----- Qthread ------
        self.preprocesser = DataPreprocess()
        self.preprocesser.sliding_voxel.connect(self.printobj)
        self.TracjectPredict =  TracjectPredict()
        self.TracjectPredict.preidct_xyz.connect(self.slot_tracject)

    def smooth(self, data):
        window = 9
        order = 3
        y_sf = savgol_filter(data, window, order)
        return y_sf

    def slot_tracject(self, out_xyz):
        # print(out_xyz.shape)
        # print(out_xyz)
        self.xy_plane_x.append(out_xyz[0])
        self.xy_plane_y.append(out_xyz[1])
        if len(self.xy_plane_x) > 20:
            self.xy_plane_x = self.xy_plane_x[1:]
            self.xy_plane_y = self.xy_plane_y[1:]

        # self.xy_plane.setData(self.xy_plane_x, self.xy_plane_y)
        self.xy_plane.setData(self.smooth(self.xy_plane_x), self.smooth(self.xy_plane_y))

    def printobj(self, data):
        data = np.reshape(data,[1,3,1,32,32,32])
        self.TracjectPredict.predict(data)

    def start(self):
        self.run_state = True
        self.frame_count
        self.stop_btn.setText("stop")
        if self.sure_image:
            self.th_cam1 = CamCapture(self.file_path_cam1)
            self.th_cam2 = CamCapture(self.file_path_cam2)
        self.update_figure()

    def stop(self):
        if self.run_state:
            self.stop_btn.setText("Continues")
        else:
            self.stop_btn.setText("stop")
        self.run_state = not(self.run_state)
        self.sure_next = True
        self.update_figure()

    def RDI_update(self):
        rd = self.RDI
        # img_rdi.setImage(np.rot90(rd, -1))
        if self.Sure_staic_RM == False:
        # ------no static remove------
        #     img_rdi.setImage(np.rot90(rd, -1), levels=[150, 250])
            img_rdi.setImage(np.rot90(rd, -1))
        # ------ static remove------
        else:
            img_rdi.setImage(np.rot90(rd, -1))

            # img_rdi.setImage(np.rot90(rd, -1), levels=[40, 150])

    def RAI_update(self):
        global count, view_rai, p13d
        a = self.RAI
        e = self.RAI_ele
        if self.Sure_staic_RM == False:
            # ------no static remove------
            # img_rai.setImage(np.fliplr((a)).T,levels=[20e4, 50.0e4])
            img_rai.setImage(np.fliplr((a)).T,)
            # self.img_rai_ele.setImage(np.fliplr((e)).T,levels=[2FG0e4, 50.0e4])
            self.img_rai_ele.setImage(np.fliplr((e)).T)

        else:
            # ------ static remove------
            img_rai.setImage(np.fliplr((a)).T, levels=[0.5e4, 2.0e4])
            # self.img_rai_ele.setImage(np.fliplr((e)).T,levels=[0.5e4, 50.0e4])
            self.img_rai_ele.setImage(np.fliplr((e)).T)

    def PD_update(self):
        global count, view_rai, p13d,nice,ax
        # --------------- plot 3d ---------------
        pos = self.PD
        pos = np.transpose(pos,[1,0])
        p13d.setData(pos=pos[:,:3],color= [1,0.35,0.02,1],pxMode= True)
        self.preprocesser.sliding_voxel_process(pos)

    def update_figure(self):
        global count,view_rai,p13d
        self.Sure_staic_RM = self.static_rm.isChecked()
        if self.frame_count == self.frame_total_len:
            self.run_state = False
            # print(len(self.pd_save))
            # print(self.pd_save)
            np.save(self.path+"pd_data.npy",self.pd_save)
            self.app.instance().exec_()

        if self.run_state:
            self.RDI ,self.RAI,self.RAI_ele,self.PD = self.data_proecsss.run_proecss(self.rawData[self.frame_count],\
                                                            self.rai_mode,self.Sure_staic_RM,self.chirp)
            # self.RDI_update()
            # self.RAI_update()
            self.PD_update()
            # self.set_plotdata()
            self.updatecam()
            self.pd_save.append(self.PD.T)
            time.sleep(0.05)
            if self.sure_next:
                self.frame_count +=1
                QtCore.QTimer.singleShot(1, self.update_figure)
                QApplication.processEvents()
            self.fps_count += 1
            # print(self.frame_count)

    def updatecam(self):
        if self.sure_image:
            # print(self.th_cam1.get_frame())
            self.image_label1.setPixmap((self.th_cam1.get_frame()))
            self.image_label2.setPixmap((self.th_cam2.get_frame()))

    def pre_frame(self):
        if self.frame_count >0:
            self.frame_count -=1
            self.sure_next = False
            self.run_state=True
            self.update_figure()

    def next_frame(self):
        if self.frame_count<=self.frame_total_len:
            self.frame_count += 1
            self.sure_next = False
            self.run_state = True
            self.update_figure()

    def SelectFolder(self):
        root = tk.Tk()
        root.withdraw()
        # self.file_path = filedialog.askopenfilename(parent=root, initialdir='D:\\Matt_yen_data\\NAS\\data\\bin file_processed\\new data(low powered)\\3t4r')
        # self.file_path = filedialog.askopenfilename(parent=root, initialdir='D:/kaiku_report/2021-0418for_posheng/')
        if self.sure_select == True:
            self.file_path = filedialog.askopenfilename(parent=root, initialdir=self.path)
            self.browse_text.setText(self.file_path)
        else:
            self.file_path = self.path + 'raw.npy'
            # self.file_path = self.path
            self.browse_text.setText(self.file_path)

        return self.file_path
    def SelectFolder_cam1(self):
        root = tk.Tk()
        root.withdraw()
        # self.file_path = filedialog.askopenfilename(parent=root, initialdir='D:\\Matt_yen_data\\NAS\\data\\bin file_processed\\new data(low powered)\\3t4r')
        if self.sure_select == True:
            self.file_path_cam1 = filedialog.askopenfilename(parent=root, initialdir=self.path)
            self.browse_text_cam1.setText(self.file_path_cam1)
        else:
            self.file_path_cam1 = self.path + 'vedio1.mp4'
            self.browse_text_cam1.setText(self.file_path_cam1)

        return self.file_path_cam1

    def SelectFolder_cam2(self):
        root = tk.Tk()
        root.withdraw()
        # self.file_path = filedialog.askopenfilename(parent=root, initialdir='D:\\Matt_yen_data\\NAS\\data\\bin file_processed\\new data(low powered)\\3t4r')
        if self.sure_select == True:
            self.file_path_cam2 = filedialog.askopenfilename(parent=root, initialdir=self.path)
            self.browse_text_cam2.setText(self.file_path_cam2)
        else:
            self.file_path_cam2 = self.path + 'vedio2.mp4'
            self.browse_text_cam2.setText(self.file_path_cam2)
        return self.file_path_cam2


    def enable_btns(self,state):
        self.pre_btn.setEnabled(state)
        self.next_btn.setEnabled(state)
        self.start_btn.setEnabled(state)
        self.stop_btn.setEnabled(state)

    def slot(self, object):
        print("Key was pressed, id is:", self.radio_group.id(object))
        '''
        raimode /0/1/2:
                0 -> FFT-RAI
                1 -> beamformaing RAI 
                3 -> static clutter removal
        '''
        self.rai_mode = self.radio_group.id(object)

        if self.rai_mode ==1:
            self.view_rai.setRange(QtCore.QRectF(10, 0, 170, 80))
        else:
            self.view_rai.setRange(QtCore.QRectF(-5, 0, 100, 60))

    def load_file(self):
        load_mode = 1
        if load_mode == 0 :
            self.rawData =read_binfile.read_bin_file(self.file_path,[64,64,32,3,4],mode=0,header=False,packet_num=4322)
            self.rawData = np.transpose(self.rawData,[0,1,3,2])
            self.chirp = 32
            self.frame_total_len = len(self.rawData)

        elif load_mode == 1:
            data  =np.load(self.file_path,allow_pickle=True)
            data = np.reshape(data, [-1, 4])
            data = data[:, 0:2:] + 1j * data[:, 2::]
            self.rawData = np.reshape(data,[-1,48,4,64])
            print(len(self.rawData))
            self.frame_total_len = len(self.rawData)
            self.chirp = 16

        self.enable_btns(True)

    def load_gt(self):
        self.hand_pd_1 = np.load(self.path + "/cam_hp.npy", allow_pickle=True)
        print("self.hand_pd_1 len is {}".format(self.hand_pd_1.shape))
        self.hand_pd_2 = np.load(self.path + "/cam_hp1.npy", allow_pickle=True)
        print("self.hand_pd_2 len is {}".format(self.hand_pd_2.shape))

    def GetGroundTruth(self,x1, y1, x2, y2):
        scale_x1 = 55 / 640 * 0.009375  # cm / pixel * (0.015 point/cm)
        scale_y1 = 43 / 480 * 0.009375
        scale_x2 = 45 / 640 * 0.009375
        scale_y2 = 29 / 480 * 0.009375

        if (y1 != None).all() == True:
            y1 = y1.astype(np.double)
            y1 = np.round((y1 * scale_y1), 3)
            y1 -= ((480 * scale_y1) / 2)

        x2 = np.where(x2 is not None, x2, np.double(320))
        x2 = x2.astype(np.double)
        x2 = (x2 * scale_x2)
        x2 -= ((640 * scale_x2) / 2)
        x2 = np.round(x2, 3)

        y2 = np.where(y2 is not None, y2, np.double(480))
        y2 = y2.astype(np.double)
        y2 = (y2 * scale_y2)
        y2 -= ((480 * scale_y2) / 2)
        y2 = np.round(y2, 3)

        return x2 * -1,  y1*-1 +0.009375*10 ,y2 *-1 ,

    def lineup_GT(self,view_PD):
        self.point_cloud_widget= view_PD
        self.traces = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=[0, 0, 255, 255], pxMode=True)
        self.hand = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=[0, 255, 0, 255], pxMode=True)
        self.hand_line = gl.GLLinePlotItem(pos=np.array([[[0, 0, 0], [2.5, 3.2, 1.5]], [[0, 0, 0], [1, 3.5, 4]]]),
                                           color=[128, 255, 128, 255], antialias=False)
        self.indexfinger = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=[0.35, 0.62, 0.35, 255], pxMode=True)
        self.thumb = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=[255, 0, 0, 255], pxMode=True)
        self.point_cloud_widget.addItem(self.traces)
        # self.point_cloud_widget.addItem(self.hand)
        self.point_cloud_widget.addItem(self.hand_line)
        self.point_cloud_widget.addItem(self.indexfinger)
        self.point_cloud_widget.addItem(self.thumb)

    def set_plotdata(self):
            h = self.frame_count
            data = self.GetGroundTruth(self.hand_pd_1[h * 2, :], self.hand_pd_1[h * 2 + 1, :],
                                       self.hand_pd_2[h * 2, :], self.hand_pd_2[h * 2 + 1, :])
            # data = np.array(data)
            # data = data[:, :3]
            # data = data.reshape([-1, 3])
            # self.traces.setData(pos=data, color=[0, 0, 255, 255], pxMode=True)
            hand = np.array(data)
            # print("hand_shape: {}".format(hand.shape))
            hand = hand.transpose([1, 0])


            self.hand.setData(pos=hand, color=[0, 255, 0, 255], pxMode=True)

            line = np.array(
                [[hand[0, :], hand[1, :]], [hand[1, :], hand[2, :]], [hand[2, :], hand[3, :]], [hand[3, :], hand[4, :]],
                 [hand[0, :], hand[5, :]],
                 [hand[5, :], hand[6, :]], [hand[6, :], hand[7, :]], [hand[7, :], hand[8, :]], [hand[5, :], hand[9, :]],
                 [hand[9, :], hand[10, :]],
                 [hand[10, :], hand[11, :]], [hand[11, :], hand[12, :]], [hand[9, :], hand[13, :]],
                 [hand[13, :], hand[14, :]], [hand[14, :], hand[15, :]],
                 [hand[15, :], hand[16, :]], [hand[13, :], hand[17, :]], [hand[17, :], hand[18, :]],
                 [hand[18, :], hand[19, :]], [hand[19, :], hand[20, :]],
                 [hand[0, :], hand[17, :]]])

            self.hand_line.setData(pos=line, color=[0.5, 0.7, 0.9, 255], antialias=False)

            self.indexfinger.setData(pos=hand[8, :], color=[0.88, 0.22, 0.35, 255], pxMode=True)
            self.thumb.setData(pos=hand[4, :], color=pg.glColor((255, 255, 0)), pxMode=True)

    def plot(self):
        global img_rdi, img_rai, updateTime, view_text, count, angCurve, ang_cuv, img_cam, savefilename,view_rai,p13d,nice
        # ---------------------------------------------------
        self.app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        MainWindow.show()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        self.browse_btn = ui.browse_btn
        self.browse_text = ui.textEdit
        self.browse_text_cam1 = ui.textEdit_cam1
        self.browse_text_cam2 = ui.textEdit_cam2
        self.load_btn = ui.load_btn
        self.start_btn = ui.start_btn
        self.stop_btn  =ui.stop_btn
        self.next_btn  =ui.next_btn
        self.pre_btn = ui.pre_btn
        self.radio_group =  ui.radio_btn_group
        self.static_rm = ui.sure_static
        self.cam1 = ui.label_cam1
        self.cam2 = ui.label_cam2
        self.cam1_btn =  ui.browse_cam1_btn
        self.cam2_btn =  ui.browse_cam2_btn
        self.image_label1 =ui.image_label1
        self.image_label2 =ui.image_label2
        # #----------------- btn clicked connet -----------------
        self.browse_btn.clicked.connect(self.SelectFolder)
        self.cam1_btn.clicked.connect(self.SelectFolder_cam1)
        self.cam2_btn.clicked.connect(self.SelectFolder_cam2)
        self.load_btn.clicked.connect(self.load_file)
        self.start_btn.clicked.connect(self.start)
        self.next_btn.clicked.connect(self.next_frame)
        self.pre_btn.clicked.connect(self.pre_frame)
        self.stop_btn.clicked.connect(self.stop)
        self.radio_group.buttonClicked.connect(self.slot)
        # # -----------------------------------------------------
        self.view_rdi = ui.graphicsView.addViewBox()
        self.view_rai = ui.graphicsView_2.addViewBox()
        self.view_xy = ui.graphicsView_xy

        view_PD = ui.graphicsView_3
        # ---------------------------------------------------
        # lock the aspect ratio so pixels are always square
        self.view_rdi.setAspectLocked(True)
        self.view_rai.setAspectLocked(True)
        self.xy_plane = pg.PlotDataItem(pen=pg.mkPen(width=1, color='r'), size=1)
        self.xy_plane_x = []
        self.xy_plane_y = []
        self.view_xy.addItem(self.xy_plane)
        img_rdi = pg.ImageItem(border='w')
        img_rai = pg.ImageItem(border='w')
        self.img_rai_ele = pg.ImageItem(border='w')

        img_cam = pg.ImageItem(border='w')
        #-----------------
        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        view_PD.addItem(xgrid)
        view_PD.addItem(ygrid)
        view_PD.addItem(zgrid)
        xgrid.translate(0,10,-10)
        ygrid.translate(0, 0, 0)
        zgrid.translate(0, 10, -10)
        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        p13d = gl.GLScatterPlotItem(pos = np.zeros([1,3]) ,color=[50, 50, 50, 255])
        origin = gl.GLScatterPlotItem(pos = np.zeros([1,3]),color=[255, 0, 0, 255])
        coord = gl.GLAxisItem(glOptions="opaque")
        coord.setSize(10, 10, 10)
        view_PD.addItem(p13d)
        view_PD.addItem(coord)
        view_PD.addItem(origin)

        # print(view_PD.cameraPosition())
        view_PD.orbit(45,6)
        view_PD.pan(1,1,1,relative=1)

        # self.lineup_grid(view_PD)
        self.lineup_GT(view_PD)
        # self.bounding_box(view_PD)
        self.enable_btns(False)
        # ang_cuv = pg.PlotDataItem(tmp_data, pen='r')
        # Colormap
        position = np.arange(64)
        position = position / 64
        position[0] = 0

        position = np.flip(position)
        colors = [[62, 38, 168, 255], [63, 42, 180, 255], [65, 46, 191, 255], [67, 50, 202, 255], [69, 55, 213, 255],
                  [70, 60, 222, 255], [71, 65, 229, 255], [70, 71, 233, 255], [70, 77, 236, 255], [69, 82, 240, 255],
                  [68, 88, 243, 255],
                  [68, 94, 247, 255], [67, 99, 250, 255], [66, 105, 254, 255], [62, 111, 254, 255], [56, 117, 254, 255],
                  [50, 123, 252, 255],
                  [47, 129, 250, 255], [46, 135, 246, 255], [45, 140, 243, 255], [43, 146, 238, 255], [39, 150, 235, 255],
                  [37, 155, 232, 255],
                  [35, 160, 229, 255], [31, 164, 225, 255], [28, 129, 222, 255], [24, 173, 219, 255], [17, 177, 214, 255],
                  [7, 181, 208, 255],
                  [1, 184, 202, 255], [2, 186, 195, 255], [11, 189, 188, 255], [24, 191, 182, 255], [36, 193, 174, 255],
                  [44, 195, 167, 255],
                  [49, 198, 159, 255], [55, 200, 151, 255], [63, 202, 142, 255], [74, 203, 132, 255], [88, 202, 121, 255],
                  [102, 202, 111, 255],
                  [116, 201, 100, 255], [130, 200, 89, 255], [144, 200, 78, 255], [157, 199, 68, 255], [171, 199, 57, 255],
                  [185, 196, 49, 255],
                  [197, 194, 42, 255], [209, 191, 39, 255], [220, 189, 41, 255], [230, 187, 45, 255], [239, 186, 53, 255],
                  [248, 186, 61, 255],
                  [254, 189, 60, 255], [252, 196, 57, 255], [251, 202, 53, 255], [249, 208, 50, 255], [248, 214, 46, 255],
                  [246, 220, 43, 255],
                  [245, 227, 39, 255], [246, 233, 35, 255], [246, 239, 31, 255], [247, 245, 27, 255], [249, 251, 20, 255]]
        colors = np.flip(colors, axis=0)
        color_map = pg.ColorMap(position, colors)
        lookup_table = color_map.getLookupTable(0.0, 1.0, 256)
        img_rdi.setLookupTable(lookup_table)
        img_rai.setLookupTable(lookup_table)
        self.img_rai_ele.setLookupTable(lookup_table)
        self.view_rdi.addItem(img_rdi)
        self.view_rai.addItem(img_rai)
        self.view_rai.addItem(self.img_rai_ele)
        self.view_rdi.setRange(QtCore.QRectF(0, 0, 30, 70))
        self.view_rai.setRange(QtCore.QRectF(10, 0, 160, 80))
        updateTime = ptime.time()
        if self.sure_select ==False:
            self.SelectFolder()
            self.SelectFolder_cam1()
            self.SelectFolder_cam2()
        self.app.instance().exec_()

    def lineup_grid(self,view_PD):
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
        self.hand_linex_2 = gl.GLLinePlotItem(pos=np.array([[[-0.075 * 8, 0.075 * 4, 0.075 * 2], [0.075 * 8, 0.075 * 4, 0.075 * 2]]]),
                                              color=[128, 255, 128, 255], antialias=False)
        self.hand_linex_1 = gl.GLLinePlotItem(pos=np.array([[[-0.075 * 8, 0.075 * 4, 0.075*1], [0.075 * 8, 0.075 * 4, 0.075*1]]]),
                                            color=[128, 255, 128, 255], antialias=False)
        self.hand_linex_d1 = gl.GLLinePlotItem(pos=np.array([[[-0.075 * 8, 0.075 * 4, 0.075 * -1], [0.075 * 8, 0.075 * 4, 0.075 * -1]]]),
                                            color=[128, 255, 128, 255], antialias=False)
        self.hand_linex_d2 = gl.GLLinePlotItem(pos=np.array([[[-0.075 * 8, 0.075 * 4, 0.075 * -2], [0.075 * 8, 0.075 * 4, 0.075 * -2]]]),
                                            color=[128, 255, 128, 255], antialias=False)

        self.hand_linex = gl.GLLinePlotItem(pos=np.array([[[-0.075 * 8, 0.075 * 4, 0], [0.075 * 8, 0.075 * 4, 0]]]),
                                            color=[128, 255, 128, 255], antialias=False)

        self.hand_linez = gl.GLLinePlotItem(pos=np.array([[[0, 0.075 * 4, -0.075 * 8], [0, 0.075 * 4, 0.075 * 8]]]),
                                            color=[0.5,0.5,0.9,1], antialias=False)
        view_PD.addItem(self.hand_line)
        view_PD.addItem(self.hand_liney)
        view_PD.addItem(self.hand_linez)
        view_PD.addItem(self.hand_linex)

    def build_GLline(self,p1,p2):
        x1 = p1[0];y1 = p1[1];z1 = p1[2]
        x2 = p2[0];y2 = p2[1];z2 = p2[2]
        return  gl.GLLinePlotItem(pos=np.array([[[x1, y1, z1], [x2, y2, z2]]]), color=[128, 255, 128, 255], antialias=False)

    def bounding_box(self,view_PD):
        '''
        :param view_PD:
        :return:
        '''
        # half_len = 0.1875
        # all_len = 0.1875*2
        all_len = 0.234375  # bounding box's width 25cm: 0.234375 = 25 * 0.009375(1cm/pyqtgraph-coord)
        half_len = all_len/2

        self.line1 = self.build_GLline([half_len,       0,    half_len], [-1*half_len,       0,    half_len])
        self.line2 = self.build_GLline([half_len, all_len,    half_len], [-1*half_len, all_len,    half_len])
        self.line3 = self.build_GLline([half_len,       0, -1*half_len], [-1*half_len,       0, -1*half_len])
        self.line4 = self.build_GLline([half_len, all_len, -1*half_len], [-1*half_len, all_len, -1*half_len])
        self.line5 = self.build_GLline([half_len,       0,    half_len], [half_len,       0, -1*half_len])
        self.line6 = self.build_GLline([half_len,       0,    half_len], [half_len, all_len,    half_len])
        self.line7 = self.build_GLline([half_len, all_len,    half_len], [half_len, all_len, -1*half_len])
        self.line8 = self.build_GLline([half_len,       0, -1*half_len], [half_len, all_len, -1*half_len])

        self.line9  = self.build_GLline([-1*half_len,       0,    half_len], [-1*half_len,       0, -1*half_len])
        self.line10 = self.build_GLline([-1*half_len,      0,    half_len], [-1*half_len, all_len,    half_len])
        self.line11 = self.build_GLline([-1*half_len, all_len,    half_len], [-1*half_len, all_len, -1*half_len])
        self.line12 = self.build_GLline([-1*half_len,      0, -1*half_len], [-1*half_len, all_len, -1*half_len])

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

        self.lineHleht_fov = self.build_GLline([0,0, 0], [17.32,10,0])
        self.lineHright_fov= self.build_GLline([0,0, 0], [-17.32,10,0])
        self.lineVup_fov= self.build_GLline([0,0, 0], [0,10,2.67949192431123])
        self.lineVdown_fov= self.build_GLline([0,0, 0],  [0,10,-2.67949192431123])

        view_PD.addItem(self.lineHleht_fov)
        view_PD.addItem(self.lineHright_fov)
        view_PD.addItem(self.lineVup_fov)
        view_PD.addItem(self.lineVdown_fov)

class TracjectPredict(QThread):
    preidct_xyz = pyqtSignal(np.ndarray)

    def __init__(self,*args, **kwargs):
        super(TracjectPredict, self).__init__(*args, **kwargs)
        path = "D:\\thumouse_new_dataset_32_32\\model\\voxel.h5"
        self.model = load_model(path)  # Load a HDF5 file


    def predict(self, slding_voxel_dataIn):
        predict_out = self.model.predict(slding_voxel_dataIn)
        finalout = predict_out[0,-1,:]
        # print(finalout)
        self.preidct_xyz.emit(finalout)


class DataPreprocess(QThread):
    sliding_voxel = pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super(DataPreprocess, self).__init__(*args, **kwargs)
        self.number = 0
        self.out_arr = np.zeros([3, 1,  32, 32, 32])

    def pointcloud2voxel(self, pd_dataIn):

        tmp_frame = pd_dataIn
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

            if x < 32 and y < 32 and z < 32 and x > 0 and y > 0 and z > 0:
                # print("x:{} y:{} z:{}".format(x,y,z))
                arr[0][x][y][z] = True
                point_count += 1
                tx += tmp_frame[c][0]
                ty += tmp_frame[c][1]
                tz += tmp_frame[c][2]

        return arr

    def sliding_voxel_process(self, inputdata):
        tmp_voxel=self.pointcloud2voxel(inputdata)
        if self.number<3:
            self.out_arr[self.number] = tmp_voxel
            self.number += 1
        else:
            self.out_arr[0:2] = self.out_arr[1:3]
            self.out_arr[2] = tmp_voxel
            self.sliding_voxel.emit(self.out_arr)



if __name__ == '__main__':
    print('======Real Time Data Capture Tool======')
    count = 0
    realtime = Realtime_sys()
    lock = threading.Lock()
    plotIMAGE = threading.Thread(target=realtime.plot())
    plotIMAGE.start()

    print("Program Close")
    sys.exit()
