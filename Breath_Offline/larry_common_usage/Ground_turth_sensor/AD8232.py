import numpy as np
import warnings
import threading
import serial.tools.list_ports
from PyQt5.QtCore import pyqtSignal,QThread
import time


class AD8232(QThread):
    AD8232_V= pyqtSignal(np.ndarray,np.ndarray)

    def __init__(self ,buffer_len=256):
        super(AD8232, self).__init__()
        self.sure_run = True
        self.sure_start = False
        self.sure_save =False
        self.value_buff = []
        self.time_buff = []
        self.save_v_buff = []
        self.save_t_buff = []
        self.set_buff_len = buffer_len
        self.AD8232_init()
        self.frame_count = 0
        self.sure_count_time =False
        self.start_count = False
    def AD8232_init(self):
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Arduino' in p.description  # may need tweaking to match new arduinos
        ]
        if not arduino_ports:
            raise IOError("No Arduino found")
        if len(arduino_ports) > 1:
            warnings.warn('Multiple Arduinos found - using the first')
        print("Connect comport:{}".format(arduino_ports[0]))
        self.ser = serial.Serial(arduino_ports[0], 9600, timeout=0.5)

    def clean(self):
        self.value_buff = []
        self.time_buff = []
        self.save_v_buff = []
        self.save_t_buff = []

    def run(self):
        if self.sure_count_time:
            self.time_start = time.time()

        while self.sure_run:
            str_input = (self.ser.readline()).decode("utf-8").split()
            if len(str_input) == 2:
                tmp_value = str_input[0]
                tmp_time = float(str_input[1]) / 1000
                # print("amplitude: ", tmp_value, " time(s):", tmp_time)
                self.check_buffer_len()
                self.value_buff = np.append(self.value_buff, int(tmp_value))
                self.time_buff = np.append(self.time_buff, tmp_time)
                print(tmp_time)
                if self.sure_save:
                    self.save_v_buff = np.append(self.save_v_buff, tmp_value)
                    self.save_t_buff = np.append(self.save_t_buff, int(tmp_time))
                self.AD8232_V.emit(self.value_buff,self.time_buff)
                if float(tmp_time)<0.1:
                    self.start_count = True

                if self.start_count:
                    self.frame_count +=1
                    if float(tmp_time) >= 60:
                        break


        if self.sure_count_time:
            print("collect time:{}, fps: {}".format(60,self.frame_count/60))

    def save_trigger(self):
        self.sure_save = True

    def save_data(self, path):
        np.save(path + "value.npy", self.save_v_buff)
        np.save(path + "time.npy", self.save_t_buff)
        self.sure_save = False
        self.clean()

    def stop(self):
        self.sure_run = False

    def exit(self):
        self.ser.close()

    def check_buffer_len(self):
        if len(self.value_buff) >= self.set_buff_len:
            self.value_buff = self.value_buff[1:]
            self.time_buff = self.time_buff[1:]


if __name__ == '__main__':
    x = AD8232(sensor_numb=1, samplerate=20, buffer_len=20)
    x.run()
