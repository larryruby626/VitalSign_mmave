import numpy as np

def reshape_rawdata(rawdata):
    ch1data = rawdata[:4096]
    ch2data = rawdata[4096:]
    ch1data = np.reshape(ch1data, [32, 128])
    ch2data = np.reshape(ch2data, [32, 128])
    dataInCh1 = ch1data[:, :64]  # cut the down chirp
    dataInCh2 = ch2data[:, :64]  # cut the down chirp

    return dataInCh1, dataInCh2

def reshape_rawdata_forlist(list_data):
    """
    :param list: list=> [frames , 1D-rawdata]
    :return:
    """
    frame_number = len(list_data)
    buffer = np.zeros([frame_number, 32, 64])   # [frame]

    for f_n in range(frame_number):
        tmp_data = list_data[f_n]
        after_reshape = reshape_rawdata(tmp_data)
        buffer[f_n:, 32,64] = after_reshape
    return buffer


