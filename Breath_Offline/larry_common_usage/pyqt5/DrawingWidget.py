import numpy as np
import pyqtgraph as pg
# from pyqtgraph.PlotWidget import setTitle
from PyQt5.QtWidgets import QApplication


##=====================================================================================
class DrawingWidget(pg.LayoutWidget):
    __PlotWidget = None

    # def __init__(self, title, xlabel_length, x_lb_name, y_lb_name):
    def __init__(self, title="Plot_Widget"):
        pg.LayoutWidget.__init__(self)

        self.drawingTitle = title
        self.setupUI()

    def setupUI(self):
        self.__PlotWidget = pg.PlotWidget(title=self.drawingTitle)
        self.addWidget(self.__PlotWidget)

    # -------------- add as new obj -----------------------
    def add_line_obj(self, c="w"):
        plot = pg.PlotDataItem()
        setting_pen = pg.mkPen(color=c)
        plot.setPen(pen=setting_pen)
        self.__PlotWidget.addItem(plot)
        return plot

    def setData_with_color(self,OBJ, Data, c="w"):
        """
        b, g, r, c, m, y, k, w
        """
        setting_pen = pg.mkPen(color=c)
        print(Data)
        OBJ.setData(Data, pen=setting_pen)

    def line_obj_SetData(self, OBJ, Value, Index=None):
        Value = np.array(Value)
        if Index is not None:
            try:
                OBJ.setData(Index, Value)
            except:
                pass
                # print("Input format error!!!")
                # print("index shape is :{}", Index.shape)
                # print("Value shape is :{}", Value.shape)
        else:
            try:
                OBJ.setData(Value)
            except:
                pass
                # print("Input format error!!!")
                # print("Value shape is :{}", Value.shape)

    def add_scatter_obj(self, c="r"):
        scatters = pg.ScatterPlotItem(brush=c)
        self.__PlotWidget.addItem(scatters)
        return scatters

    def scatter_obj_SetData(self, OBJ, Index, Value):
        OBJ.clear()
        point = [{"pos": [Index, Value], "data": 1}]
        OBJ.addPoints(point)

    def clear_obj_widget(self, OBJ):
        OBJ.clear()
    # -------------- add as new obj -----------------------
    def add_bar_plot(self):
        self.bar_plot = pg.BarGraphItem(x=[], height=[], width=0.6)
        self.__PlotWidget.addItem(self.bar_plot)

    def update_bar_plot(self, value):
        x_idx = np.arange(len(value))
        self.bar_plot.setOpts(x=x_idx, height=value, width=0.6)

    def add_text_items(self, HZ, Peak, x):
        text = pg.TextItem(
            html='<div style="text-align: center"><span style="color: #FF0; font-size: 12pt;">Hz:</span><span style="color: #FFF;font-size: 12pt;">' + HZ + '</span><br><span style="color: #FF0; font-size: 12pt;">peakval:</span><span style="color: #FFF;font-size: 12pt;">' + Peak + '</div>',
            anchor=(-0.3, 0.5), angle=0, border='w', fill=(0, 0, 255, 100))
        self.__PlotWidget.addItem(text)
        text.setPos(0, x.max() + 100)

    def plot_scatter(self, value, index):
        self.scatters.clear()
        # print(index,value)
        dick = [{"pos": [index, value], "data": 1}]
        self.scatters.addPoints(dick)

    def setYRange(self, min, max):
        self.__PlotWidget.setYRange(min, max)

    def setXRange(self, min, max):
        self.__PlotWidget.setXRange(min, max)

    def setlb(self, xlabel, ylabel):
        self.__PlotWidget.setLabel('bottom', xlabel)  # x-label
        self.__PlotWidget.setLabel('left', ylabel)

    def settitle(self, title_txt):
        self.__PlotWidget.setTitle(title=title_txt)

    def forloop_add_plot(self, data):
        self.__PlotWidget.clear()
        for i in range(data.shape[1]):
            tmp = pg.PlotDataItem()
            tmp.setData(data[:, i])
            self.__PlotWidget.addItem(tmp)




if __name__ == '__main__':
    import sys

    app = QApplication([])
    x = DrawingWidget("ssss")
    x.show()
    sys.exit(app.exec_())
