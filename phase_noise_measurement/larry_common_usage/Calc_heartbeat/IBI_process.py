"""
@author: shiba-shiba-inu-maru-maru
"""
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from larry_common_usage.DSP.butter_filter import filter_adjust\


def plot_check_gt_window(value_buff,peak_idx,peak_arr):
    plt.plot(value_buff)
    plt.scatter(peak_idx,peak_arr)
    plt.show()

def Calc_groundtruth_HB(value_buff, time_buff, sensor_type):
    if sensor_type == "ppg":
        peak = np.array(find_peaks(value_buff, height=np.average(value_buff)+5, distance=60))
    elif sensor_type =="ecg":
        b_filt_heart,a_filt_heart =filter_adjust("highpass")
        value_buff = (signal.filtfilt(b_filt_heart, a_filt_heart, value_buff))
        peak = np.array(find_peaks(value_buff, height=75, distance=15))
    elif sensor_type == "radar":
        peak = np.array(find_peaks(value_buff, distance=10))

    peak_arr = value_buff[peak[0]]
    peak_idx = peak[0]
    arr_len = len(peak_arr)
    IBI_arr = np.array([])
    higher_bound = 1.0909  # Sec of the 55Hz/1min
    lower_bound = 0.5  # Sec of the 85Hz/1min

    if arr_len != 1:
        for i in range(arr_len - 1):

            tmp_IBI = abs(time_buff[int(peak_idx[i])] - time_buff[int(peak_idx[i + 1])])

            if tmp_IBI > lower_bound and tmp_IBI < higher_bound:
                IBI_arr = np.append(IBI_arr, tmp_IBI)

        return np.average(60 * (1 / IBI_arr))
    else:
        print("NO IBI !!!")


def plot_data2(data1, data2):
    plt.ylim([40, 100])
    plt.plot(data1)
    plt.plot(data2)
    plt.show()

if __name__ == "__main__":
    path = "G:\\我的雲端硬碟\\開酷\\FoV_experiment\\dataset1101109\\"
    # SIC_type = ["sicF", "sic64", "sic255"]
    # range_arr = ["20", "40", "60"]
    # Filetype = ["time1", 'time2', "time3", "stop"]
    SIC_type = ["sic255"]
    range_arr = ["40"]
    Filetype = ["time3"]

    for s_t in SIC_type:
        for r_a in range_arr:
            for f_t in Filetype:
                tmp_path = path + str(s_t) + "\\"
                tmpfile_name = str(s_t) + "_" + str(r_a) + "cm_" + str(f_t)

                value_buf = np.load(tmp_path + tmpfile_name + "_ppg_v.npy", allow_pickle=True)
                time_buf = np.load(tmp_path + tmpfile_name + "_ppg_t.npy", allow_pickle=True)

                window_len = 600
                ppg_windowlen = window_len * 4
                HB_list = []
                HB_ppg_list = []

                for i in range((len(value_buf) - ppg_windowlen)):
                    # if (i % 1 * 4) == 0:
                    tmp_ppg = np.array(value_buf[i:i + ppg_windowlen])
                    tmp_ppg_time = np.array(time_buf[i:i + ppg_windowlen])
                    end_idx = i + window_len
                    hz = Calc_groundtruth_HB(tmp_ppg, tmp_ppg_time)
                    # plot_data(tmp_ppg)
                    HB_ppg_list.append(hz)

                down_sample_hblist = HB_ppg_list[::4]
                averge = np.average(down_sample_hblist)
                reference = np.zeros(len(down_sample_hblist))
                reference[:] = averge
                plot_data2(down_sample_hblist, reference)
