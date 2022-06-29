import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
# from pyqtgraph.PlotWidget import setTitle
from pyqtgraph.Qt import QtGui, QtCore


##=====================================================================================
class Drawing_vitalsign(pg.LayoutWidget):
    __Stemplot = None

    # def __init__(self, title, xlabel_length, x_lb_name, y_lb_name):
    def __init__(self, title):
        pg.LayoutWidget.__init__(self)

        self.drawingTitle = title
        self.setupUI()

    def setupUI(self):

        self.__Stemplot = pg.PlotWidget(title=self.drawingTitle)

        self.plot = pg.PlotDataItem()

        self.scatters = pg.ScatterPlotItem(brush='b')
        self.target_scatter = pg.ScatterPlotItem(brush='g', size=10)
        self.window_plot = pg.PlotDataItem()
        self.cur_window_plot = pg.PlotDataItem()
        self.ppg = pg.PlotDataItem()
        self.ppg_IBI = pg.PlotDataItem()
        self.ppg_IBI1 = pg.PlotDataItem()

        self.__Stemplot.addItem(self.plot)
        self.__Stemplot.addItem(self.window_plot)
        self.__Stemplot.addItem(self.cur_window_plot)
        self.__Stemplot.addItem(self.scatters)
        self.__Stemplot.addItem(self.target_scatter)
        self.__Stemplot.addItem(self.ppg)
        self.__Stemplot.addItem(self.ppg_IBI)
        self.__Stemplot.addItem(self.ppg_IBI1)
        setting_pen = pg.mkPen(color='g')
        self.ppg_IBI.setPen(setting_pen)

        setting_pen = pg.mkPen(color='w')
        self.plot.setPen(pen=setting_pen)
        self.addWidget(self.__Stemplot)

    def set_IBI_plot(self, inputdata, index):
        if index == 0:
            self.ppg_IBI.setData(inputdata)

        else:
            self.ppg_IBI.setData([], inputdata)

    def set_IBI_plot_with_x(self, inputdata, xlb):
        setting_pen = pg.mkPen(color='g')
        self.ppg_IBI.setPen(setting_pen)
        self.ppg_IBI.setData(xlb, inputdata)

    def add_bar_plot(self):
        self.bar_plot = pg.BarGraphItem(x=[], height=[], width=0.6)
        self.__Stemplot.addItem(self.bar_plot)

    def update_bar_plot(self, value):
        x_idx = np.arange(len(value))
        self.bar_plot.setOpts(x=x_idx, height=value, width=0.6)

    def add_text_items(self, HZ, Peak, x):
        text = pg.TextItem(
            html='<div style="text-align: center"><span style="color: #FF0; font-size: 12pt;">Hz:</span><span style="color: #FFF;font-size: 12pt;">' + HZ + '</span><br><span style="color: #FF0; font-size: 12pt;">peakval:</span><span style="color: #FFF;font-size: 12pt;">' + Peak + '</div>',
            anchor=(-0.3, 0.5), angle=0, border='w', fill=(0, 0, 255, 100))
        self.__Stemplot.addItem(text)
        text.setPos(0, x.max() + 100)

    def adjust_xlabel(self, xlabel_length):
        self.xlabel = np.linspace(1, xlabel_length, xlabel_length)

    def plot_scatter(self, value, index):
        self.scatters.clear()
        # print(index,value)
        dick = [{"pos": [index, value], "data": 1}]
        self.scatters.addPoints(dick)

    def plot_target_scatter(self, value, index):
        self.target_scatter.setData(index, value)

    def setYData(self, ydata):
        self.__Stemplot.setYData(ydata)

    def setYRange(self, min, max):
        self.__Stemplot.setYRange(min, max)

    def setXRange(self, min, max):
        self.__Stemplot.setXRange(min, max)

    def set_window_phase(self, start_idx, end_idx, data):
        self.xlabel = np.array(np.linspace(start_idx, end_idx, end_idx - start_idx))

        if len(data) >= len(self.xlabel):
            self.window_plot.setData(self.xlabel, data)
        else:
            self.window_plot.setData(data)
        self.window_plot.setPen("b")

    def set_current_window_phase(self, start_idx, end_idx, data):
        self.xlabel = np.array(np.linspace(start_idx, end_idx, end_idx - start_idx))

        if len(data) >= len(self.xlabel):
            self.cur_window_plot.setData(self.xlabel, data)
        else:
            self.cur_window_plot.setData(data)
        self.cur_window_plot.setPen("r")

    def setData(self, sigfftall):
        self.plot.setData(sigfftall[:] )

    def setphaseData(self, sigfftall, index):
        if index == 0:
            self.plot.setData(sigfftall)
        else:
            self.plot.setData([], sigfftall)

    def setppg(self, sigall,index):
        if index == 0:
            self.ppg.setData(sigall)
            self.ppg.setPen(pg.mkPen('r', width=1))
        else:
            self.ppg.setData([], sigall)
    def setppg_withxl(self, sigall, x_index):
        self.ppg.setData(x_index, sigall[:])
        self.ppg.setPen(pg.mkPen('r', width=1))

    def setppg_withxl1(self, sigall, x_index):
        self.ppg_IBI1.setData(x_index, sigall[:])
        # self.ppg.setData(sigall[:] )
        self.ppg_IBI1.setPen(pg.mkPen('y', width=1))

    def setphase_data(self, sigfftall, x_index):
        self.plot.setData(x_index, sigfftall[:])

    def setlb(self, xlabel, ylabel):
        self.__Stemplot.setLabel('bottom', xlabel)  # x-label
        self.__Stemplot.setLabel('left', ylabel)

    def settitle(self, title_txt):

        self.__Stemplot.setTitle(title=title_txt)

    def set_plot_pen(self):
        # self.plot.setPen(pg.mkPen('b', width=5))
        self.ppg.setPen(pg.mkPen('r', width=1))

    def forloop_add_plot(self, data):
        self.__Stemplot.clear()
        for i in range(data.shape[1]):
            tmp = pg.PlotDataItem()
            tmp.setData(data[:, i])
            self.__Stemplot.addItem(tmp)

    ##=============================  Unit Testing  ========================================


if __name__ == '__main__':
    from vitalcfg import *
    from scipy.signal import lfilter
    import numpy as np
    from fft_process_byframe import *
    from cfar_detection import *
    from whole_detect_process import *
    from multibinSum import *
    from unwrap_process import *
    from calcOsc import *
    from oscCheckFFT import *


    def data_update():
        global g_StempTemp, phase, count, data, qtimer, cfg, interference_canceller_cfg, fftcfg, ncsumcfg1, ncsumcfg2, dpccfg, \
            cfarcfg, unwrapcfg, bpfcfg, hpfcfg, oscDectcfg, oscDectcfg_heart, phase_buf

        if count > 1000:
            qtimer.stop()
            app.exec()
        rawdata = data[count]
        ch1data = rawdata[:4096]
        ch2data = rawdata[4096:]
        ch1data = np.reshape(ch1data, [32, 128])
        ch2data = np.reshape(ch2data, [32, 128])
        # cut the down chirp
        dataInCh1 = ch1data[:, :64]
        dataInCh2 = ch2data[:, :64]

        sigfftall = fft_process_byframe(dataInCh1, fftcfg)

        sigfftall = np.expand_dims(sigfftall, axis=1)
        g_StempTemp.adjust_xlabel(len(sigfftall[:, 0]))
        g_StempTemp.setData(sigfftall[:, 0])  ## setting pen=None disables line drawing

        sigfft1 = sigfftall
        sigfft2 = sigfftall
        # [tmp_v, tmp_idx, diffVal, cfarcfg_temp] = cfar_detection(10*np.log10(np.real(sigfft1*np.conjugate(sigfft1))), cfarcfg);
        [tmp_v, tmp_idx, diffVal, cfarcfg_temp] = cfar_detection(10 * np.log10(np.abs(sigfft1)), cfarcfg);

        g_StempTemp.plot_scatter(tmp_v, tmp_idx)

        [cfarcfg, ncsumcfg1, ncsumcfg2, dpccfg] = whole_detect_process(sigfft1, sigfft2, cfarcfg, ncsumcfg1, ncsumcfg2,
                                                                       dpccfg)

        if dpccfg.done == 1 and dpccfg.havedoneonce == 1:
            # print("go in")
            g_StempTemp.plot_target_scatter((10 * np.log10(np.abs(sigfft1)))[dpccfg.targetIdx], dpccfg.targetIdx)
            if not np.any(np.isin(range(dpccfg.targetIdx - 2, dpccfg.targetIdx + 3), tmp_idx)) == 1:
                cfarcfg.cnt = cfarcfg.cnt + 1
            else:
                cfarcfg.cnt = 0

            if cfarcfg.cnt == cfarcfg.cnt_threshold:
                cfarcfg.done = 0

            targetSig = multibinSum(sigfft1, dpccfg.targetIdx, cfg.multibin, cfg.binNum)
            targetPhase = np.angle(targetSig)
            targetPhaseAll, unwrapcfg = unwrap_process(targetPhase, unwrapcfg)

            phase_buf.append(targetPhaseAll[0])
            phase.adjust_xlabel(int(len(phase_buf)))

            print("s")
            phase.setData(phase_buf[:])
            # print(targetPhaseAll.shape)

            targetPhaseAllfilter, bpfcfg.zf = lfilter(
                np.array([0.005170966050632, 0, -0.010341932101263, 0, 0.005170966050632]),
                np.array([1.0000, -3.804951951129208, 5.447016344482779, -3.478323653690533, 0.836281526065139]),
                targetPhaseAll,
                zi=bpfcfg.zf)

            targetPhaseAllfilter_heart, hpfcfg.zf = lfilter(
                np.array([0.108511395077895, 0, -0.217022790155790, 0, 0.108511395077895]),
                np.array([1.0000, -2.584280647174934, 2.747640809348158, -1.528758738815148, 0.399623026053622]),
                targetPhaseAll,
                zi=hpfcfg.zf)

            delta_d = calcOsc(targetPhaseAllfilter, cfg.lambdaa)
            delta_d_heart = calcOsc(targetPhaseAllfilter_heart, cfg.lambdaa)

            oscDectcfg = oscCheckFFT(delta_d, oscDectcfg)

        count += 1


    (cfg, interference_canceller_cfg, fftcfg, ncsumcfg1, ncsumcfg2, dpccfg,
     cfarcfg, unwrapcfg, bpfcfg, hpfcfg, oscDectcfg, oscDectcfg_heart) = vitalcfg()

    # filename = "C:\\Fov_test\\range10_angle+10_time_1.npy"
    filename = "C:\\Fov_test\\breath_test.npy"
    data = np.load(filename, allow_pickle=True)
    phase_buf = []
    g_StempTemp = None
    count = 0
    app = QtGui.QApplication([])
    app.setAttribute(QtCore.Qt.AA_Use96Dpi)

    win = QtGui.QMainWindow()
    number = 32

    g_StempTemp = Drawing_vitalsign('test', number)
    g_StempTemp.setYRange(10, 60)

    phase = Drawing_vitalsign('test', number)

    layout = QVBoxLayout()
    layout.addWidget(g_StempTemp)
    layout.addWidget(phase)

    widget = QWidget()
    widget.setLayout(layout)

    win.setCentralWidget(widget)
    win.show()
    win.setWindowTitle('Unit test')

    qtimer = QtCore.QTimer()
    qtimer.timeout.connect(data_update)
    # qtimer.setInterval(500)
    qtimer.start(50)

    app.exec()
    qtimer.stop()
