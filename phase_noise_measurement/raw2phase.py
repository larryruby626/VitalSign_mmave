import matplotlib.pyplot as plt
import numpy as np

from larry_common_usage.DSP.fft_average_chirp2oneframe import fft_chirp2frame
from larry_common_usage.RawData_process.Reshape_KKT_RawData import reshape_rawdata


def return_file_name(range, time, type):
    if type == 1:
        file_name = str(range) + str(time + 1)
    elif type == 2:
        file_name = "dongle_" + str(range) + "cm_time" + str(time + 1)
    elif type == 3:
        file_name = "PoB_" + str(range) + "cm_time" + str(time + 1)

    return file_name


def append_fft_data(fft_all, tmp_avg_fft):
    if fft_all.shape[0] == 0:
        fft_all = tmp_avg_fft
        fft_all = np.expand_dims(fft_all, axis=0)
    else:
        fft_all = np.vstack((fft_all, tmp_avg_fft))
    return fft_all


def raw2phase(raw_data):
    fft_all_ch1 = np.array([])
    fft_all_ch3 = np.array([])
    for i in range(len(rawdata)):
        dataInCh1, dataInCh3 = reshape_rawdata(rawdata[i])

        tmp_avg_fft_ch1 = fft_chirp2frame(dataInCh1)
        tmp_avg_fft_ch3 = fft_chirp2frame(dataInCh3)

        fft_all_ch1 = append_fft_data(fft_all_ch1, tmp_avg_fft_ch1)
        fft_all_ch3 = append_fft_data(fft_all_ch3, tmp_avg_fft_ch3)

    sum_fft_ch1 = np.sum(fft_all_ch1, axis=0)
    sum_fft_ch3 = np.sum(fft_all_ch3, axis=0)
    corner_reflector_idx_ch1 = np.argmax(sum_fft_ch1[20:]) + 20
    corner_reflector_idx_ch3 = np.argmax(sum_fft_ch3[20:]) + 20
    corner_reflector_phase_ch1 = np.unwrap(np.angle(fft_all_ch1[:, corner_reflector_idx_ch1]))
    corner_reflector_phase_ch3 = np.unwrap(np.angle(fft_all_ch3[:, corner_reflector_idx_ch3]))

    return corner_reflector_phase_ch1, corner_reflector_phase_ch3


if __name__ == "__main__":
    """
    path: PLZ fill it with the dataset's path on your computer
    data_set: PLZ change the nubmer x data_type[x] to switching dataset 
        
    """
    path = "D:\\kkt_dataset\\SIC_phase_noise_110_11_22\\"
    dataset_type = ["case3", "dongle", "PoB"]
    data_set = dataset_type[0]
    save_path = path
    sure_save = True

    if data_set == 'case3':
        range_arr = ["seat_stable", "seat_type", "walk_out"]
        file_numb = 1
    elif data_set == 'dongle':
        range_arr = ["20", "40", "60"]
        file_numb = 2
    elif data_set == 'PoB':
        range_arr = ["20", "40", "60"]
        file_numb = 3

    for r_a in range_arr:
        for f_t in range(5):
            plt.figure()
            tmpfile_name = return_file_name(r_a, f_t, file_numb)
            print("process: ", tmpfile_name)
            rawdata = np.load(path + data_set + "\\" + tmpfile_name + ".npy", allow_pickle=True)
            ch1_phase, ch3_phase = raw2phase(rawdata)

            if sure_save == True:
                np.save(path + data_set + "\\phase_buffer\\P_ch3_" + tmpfile_name + ".npy", ch3_phase)
                np.save(path + data_set + "\\phase_buffer\\P_ch1_" + tmpfile_name + ".npy", ch1_phase)
