import numpy as np
from scipy.signal import find_peaks


def signal_peak_process(signal, threshold,interval):
    vaule_list= np.array([])
    idx_list= np.array([])

    peak = find_peaks(signal, height=threshold,distance=interval)

    vaule_list = signal[peak[0]]
    idx_list = peak[0]

    return  vaule_list, idx_list