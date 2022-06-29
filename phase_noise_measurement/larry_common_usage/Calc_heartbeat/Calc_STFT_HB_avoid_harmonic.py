

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def plot_data(data,scatter,idx):
    plt.plot(data)
    plt.xlim([0, 120])
    plt.ylim([0, 50])
    plt.scatter(idx, scatter)
    plt.draw()
    plt.pause(0.01)
    plt.show()
    plt.cla()

def calc_BPM(phase_buf,IBI_BPM,RR,RRinter):
    tmp_data = phase_buf
    x = np.linspace(1, 14, 15)


    phase_spectrum = np.fft.fft(tmp_data, n=2048)



    # phase_spectrum = phase_spectrum[:512] * np.conjugate(phase_spectrum[:512])
    # phase_spectrum = np.real(phase_spectrum)
    # phase_spectrum = 10*np.log10(phase_spectrum)
    fft_spectral = np.abs(phase_spectrum[:512])


    f_scale_index = np.array(np.linspace(0, 511, 512) * 60 / 51.2)
    # plt.plot(phase_buf)
    # plt.show()
    # return calc_peak(phase_spectrum, f_scale_index), phase_spectrum, phase_buf




    upper_bound = 120
    lower_bound = 55    # threshold = 17  # TIME4 & 9: 17 ORTHER: 20
    # lower_bound = 60    # threshold = 17  # TIME4 & 9: 17 ORTHER: 20
    # peak = np.array(find_peaks(fft_spectral, height=5, distance=10), dtype=tuple)
    # peak = np.array(find_peaks(fft_spectral,height=150), dtype=tuple)
    peak = np.array(find_peaks(fft_spectral,np.max(fft_spectral)-10), dtype=tuple)
    print(peak)
    if len(peak[0])>=3:
        plt.cla()
        plt.plot(fft_spectral)
        print(peak[0])
        print(peak[0] % RR)
        print(peak[0] % RRinter)
        plt.show()

        print("ss")
    legal_peak_idx = np.where(np.logical_and(f_scale_index[peak[0]] >= lower_bound, \
                                             f_scale_index[peak[0]] <= upper_bound))

    arr_value = fft_spectral[peak[0][legal_peak_idx]]

    # min_idx = np.argmin(abs(f_scale_index[peak[0][legal_peak_idx]]-IBI))
    # return f_scale_index[peak[0][legal_peak_idx]][min_idx]

    # print(f_scale_index[peak[0][legal_peak_idx]])
    # print(min_idx,IBI)
    # print(abs(peak[0][legal_peak_idx]-IBI))
    # possible_idx = np.where(abs(f_scale_index[peak[0][legal_peak_idx]] - IBI) < 10)
    # target_index = possible_idx[0][np.argmax(fft_spectral[peak[0][legal_peak_idx]][possible_idx[0]])]

    if len(arr_value) != 0:
        max_idx = np.argmax(arr_value)

    return (f_scale_index[peak[0][legal_peak_idx]][max_idx],peak[0][legal_peak_idx][max_idx]), phase_spectrum, phase_buf
