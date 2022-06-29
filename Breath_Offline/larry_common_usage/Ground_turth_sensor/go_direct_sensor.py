import time
from larry_common_usage.Ground_turth_sensor.gdx import gdx
from PyQt5.QtCore import pyqtSignal,QThread

class GoDirectSensor(QThread):
    GoDirectSensor_V = pyqtSignal(list)

    def __init__(self, sensor_numb, samplerate, buffer_len=256):
        super(GoDirectSensor, self).__init__()
        self.sure_run = True
        self.sure_save =False
        self.buff = []
        self.save_v_buff = []
        self.set_buff_len = buffer_len
        self.sensor_numb = sensor_numb
        self.samplerate = samplerate
        self.gdx_init()
        self.frame_count = 0
        self.sure_count_time =False

    def gdx_init(self):
        self.gdxx = gdx()
        self.gdxx.open_usb()
        self.gdxx.select_sensors([self.sensor_numb])
        self.gdxx.start(self.samplerate)

    def clean(self):
        self.buff = []

    def run(self):
        if self.sure_count_time:
            self.time_start = time.time()

        while self.sure_run:

            measurements = self.gdxx.read()
            self.check_buffer_len()
            self.buff.append(measurements[0])
            self.GoDirectSensor_V.emit(self.buff)
            if self.sure_count_time:
                if self.frame_count>200 :
                    self.stoptime = time.time()
                    break
            self.frame_count +=1

        if self.sure_count_time:
            all_frame_time = time.time() - self.time_start
            print("collect time:{}, fps: {}".format(all_frame_time,200/all_frame_time))

    def save_trigger(self):
        self.sure_save = True

    def stop(self):
        self.sure_run = False

    def exit(self):
        self.device.stop()
        self.device.close()

    def check_buffer_len(self):
        if len(self.buff) == self.set_buff_len:
            self.buff = self.buff[1:]



if __name__ == '__main__':
    x = GoDirectSensor(sensor_numb=1, samplerate=20, buffer_len=20)
    x.run()
