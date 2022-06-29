from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5 import QtGui
import sys
import pyqtgraph as pg
import numpy as np

class ColorMap:
    def __init__(self, position=None):
        colors = [[62, 38, 168, 255], [63, 42, 180, 255], [65, 46, 191, 255], [67, 50, 202, 255], [69, 55, 213, 255],
                  [70, 60, 222, 255], [71, 65, 229, 255], [70, 71, 233, 255], [70, 77, 236, 255], [69, 82, 240, 255],
                  [68, 88, 243, 255],
                  [68, 94, 247, 255], [67, 99, 250, 255], [66, 105, 254, 255], [62, 111, 254, 255], [56, 117, 254, 255],
                  [50, 123, 252, 255],
                  [47, 129, 250, 255], [46, 135, 246, 255], [45, 140, 243, 255], [43, 146, 238, 255],
                  [39, 150, 235, 255],
                  [37, 155, 232, 255],
                  [35, 160, 229, 255], [31, 164, 225, 255], [28, 129, 222, 255], [24, 173, 219, 255],
                  [17, 177, 214, 255],
                  [7, 181, 208, 255],
                  [1, 184, 202, 255], [2, 186, 195, 255], [11, 189, 188, 255], [24, 191, 182, 255], [36, 193, 174, 255],
                  [44, 195, 167, 255],
                  [49, 198, 159, 255], [55, 200, 151, 255], [63, 202, 142, 255], [74, 203, 132, 255],
                  [88, 202, 121, 255],
                  [102, 202, 111, 255],
                  [116, 201, 100, 255], [130, 200, 89, 255], [144, 200, 78, 255], [157, 199, 68, 255],
                  [171, 199, 57, 255],
                  [185, 196, 49, 255],
                  [197, 194, 42, 255], [209, 191, 39, 255], [220, 189, 41, 255], [230, 187, 45, 255],
                  [239, 186, 53, 255],
                  [248, 186, 61, 255],
                  [254, 189, 60, 255], [252, 196, 57, 255], [251, 202, 53, 255], [249, 208, 50, 255],
                  [248, 214, 46, 255],
                  [246, 220, 43, 255],
                  [245, 227, 39, 255], [246, 233, 35, 255], [246, 239, 31, 255], [247, 245, 27, 255],
                  [249, 251, 20, 255]]
        colors = np.flip(colors, axis=0)
        if position is None:
            position = np.arange(64)
            position = position / 64
            position[0] = 0
            position = np.flip(position)
        color_map = pg.ColorMap(position, colors)
        self.lookup_table = color_map.getLookupTable(0.0, 1.0, 256)


class CustomWidget(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)  # parent

        self.window = pg.GraphicsLayoutWidget()
        self.image = pg.ImageItem()
        self.view_box = pg.ViewBox()
        self.view_box.addItem(self.image)
        self.plot = pg.PlotItem(viewBox=self.view_box)
        self.window.addItem(self.plot)
        # self.addItem(plot)
        self.setCentralWidget(self.window)
        map_color = ColorMap()
        self.image.setLookupTable(map_color.lookup_table)

    def set_image_data(self, data):
        self.image.setImage(data)

class phase_map_widget(pg.GraphicsLayoutWidget):
    def __init__(self,title):
        super(phase_map_widget, self).__init__()
        self.image = pg.ImageItem()
        self.view_box = pg.ViewBox()
        self.view_box.addItem(self.image)
        self.plot = pg.PlotItem(viewBox=self.view_box,title=title)
        self.addItem(self.plot)
        map_color = ColorMap()
        self.image.setLookupTable(map_color.lookup_table)


    def set_image_data(self, data):
        self.image.setImage(data)

if __name__ == "__main__":
    app = QApplication([])
    w = CustomWidget()
    w.show()
    sys.exit(app.exec_())