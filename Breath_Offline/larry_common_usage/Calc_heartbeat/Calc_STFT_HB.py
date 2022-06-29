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
    plt.cla()

def calc_BPM(phase_buf):
    tmp_data = phase_buf
    phase_spectrum = np.fft.fft(tmp_data, n=1024)
    phase_spectrum = phase_spectrum[:512] * np.conjugate(phase_spectrum[:512])
    phase_spectrum = np.real(phase_spectrum)
    phase_spectrum = 10*np.log10(phase_spectrum)
    # phase_spectrum = np.abs(phase_spectrum[:512])
    f_scale_index = np.array(np.linspace(0, 511, 512) * 60 / 51.2)

    return calc_peak(phase_spectrum, f_scale_index), phase_spectrum, phase_buf


def calc_peak(fft_spectral, f_scale_index):
    upper_bound = 120
    lower_bound = 55    # threshold = 17  # TIME4 & 9: 17 ORTHER: 20
    # peak = np.array(find_peaks(fft_spectral, height=threshold))
    # print(find_peaks(fft_spectral,height=5))
    # peak = np.array(find_peaks(fft_spectral, height=20, distance=10), dtype=tuple)
    peak = np.array(find_peaks(fft_spectral, height=5, distance=10), dtype=tuple)

    legal_peak_idx = np.where(np.logical_and(f_scale_index[peak[0]] >= lower_bound, \
                                             f_scale_index[peak[0]] <= upper_bound))

    arr_value = fft_spectral[peak[0][legal_peak_idx]]
    # print("arr_value:", arr_value)
    if len(arr_value) != 0:
        max_idx = np.argmax(arr_value)

        return f_scale_index[peak[0][legal_peak_idx]][max_idx]

