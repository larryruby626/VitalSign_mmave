import socket
import time
import threading
import numpy as np
from PyQt5.QtCore import QThread, QMutex


def send_cmd(code):
    # command code list
    CODE_1 = (0x01).to_bytes(2, byteorder='little', signed=False)
    CODE_2 = (0x02).to_bytes(2, byteorder='little', signed=False)
    CODE_3 = (0x03).to_bytes(2, byteorder='little', signed=False)
    CODE_4 = (0x04).to_bytes(2, byteorder='little', signed=False)
    CODE_5 = (0x05).to_bytes(2, byteorder='little', signed=False)
    CODE_6 = (0x06).to_bytes(2, byteorder='little', signed=False)
    CODE_7 = (0x07).to_bytes(2, byteorder='little', signed=False)
    CODE_8 = (0x08).to_bytes(2, byteorder='little', signed=False)
    CODE_9 = (0x09).to_bytes(2, byteorder='little', signed=False)
    CODE_A = (0x0A).to_bytes(2, byteorder='little', signed=False)
    CODE_B = (0x0B).to_bytes(2, byteorder='little', signed=False)
    CODE_C = (0x0C).to_bytes(2, byteorder='little', signed=False)
    CODE_D = (0x0D).to_bytes(2, byteorder='little', signed=False)
    CODE_E = (0x0E).to_bytes(2, byteorder='little', signed=False)

    # packet header & footer
    header = (0xA55A).to_bytes(2, byteorder='little', signed=False)
    footer = (0xEEAA).to_bytes(2, byteorder='little', signed=False)

    # data size
    dataSize_0 = (0x00).to_bytes(2, byteorder='little', signed=False)
    dataSize_6 = (0x06).to_bytes(2, byteorder='little', signed=False)

    # data
    data_FPGA_config = (0x01020102031e).to_bytes(6, byteorder='big', signed=False)  # lvds 4
    # data_FPGA_config = (0x01020102011e).to_bytes(6, byteorder='big', signed=False)   # lvds 2
    data_packet_config = (0xc005350c0000).to_bytes(6, byteorder='big', signed=False)

    # connect to DCA1000
    connect_to_FPGA = header + CODE_9 + dataSize_0 + footer
    read_FPGA_version = header + CODE_E + dataSize_0 + footer
    config_FPGA = header + CODE_3 + dataSize_6 + data_FPGA_config + footer
    config_packet = header + CODE_B + dataSize_6 + data_packet_config + footer
    start_record = header + CODE_5 + dataSize_0 + footer
    stop_record = header + CODE_6 + dataSize_0 + footer

    if code == '9':
        re = connect_to_FPGA
    elif code == 'E':
        re = read_FPGA_version
    elif code == '3':
        re = config_FPGA
    elif code == 'B':
        re = config_packet
    elif code == '5':
        re = start_record
    elif code == '6':
        re = stop_record
    else:
        re = 'NULL'
    # print('send command:', re.hex())
    return re


def get_color():
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
    return colors


class ConnectDca(threading.Thread):

    def __init__(self):
        super(ConnectDca, self).__init__()
        print('Connect to DCA1000')
        print('=======================================')
        self.config_address = ('192.168.33.30', 4096)
        self.FPGA_address_cfg = ('192.168.33.180', 4096)
        self.cmd_order = ['9', 'E', '3', 'B', '5', '6']

    def run(self):
        sockConfig = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockConfig.bind(self.config_address)
        for k in range(5):
            # Send the command
            sockConfig.sendto(send_cmd(self.cmd_order[k]), self.FPGA_address_cfg)
            time.sleep(0.1)
            # Request data back on the config port
            msg, server = sockConfig.recvfrom(2048)
            # print('receive command:', msg.hex())

