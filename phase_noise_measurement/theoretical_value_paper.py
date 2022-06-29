import numpy as np
import matplotlib.pyplot as plt
import sympy
from larry_common_usage.xlsx_writer import XlsxWriter

def inverse_log(v):
    v = v / 10
    out = 10 ** v
    return out

def get_theoretical():
    phase_N_arr = []
    x_label = np.array(range(15, 60, 1))
    print(x_label)
    for i in range(15, 60, 1):
        x = 1 / (np.sqrt(2 * inverse_log(i)))
        phase_N_arr.append(x)
    return  phase_N_arr

def get_phase_noise(arr):
    phase_N_arr = []
    for i in arr:
        x = 1 / (np.sqrt(2 * inverse_log(i)))
        phase_N_arr.append(x)
    return phase_N_arr


def theoretical_plot():
    ch1 = [50.29, 46.43, 42.96, 34.71, 35.33, 32.52, 31.75, 30.50, 28.72, 27.50, 25.92]
    ch3 = [47.34, 42.58, 40.16, 32.90, 31.70, 30.27, 29.30, 27.78, 26.10, 25.71, 23.27]
    x_label = np.array(range(15, 60, 1))
    xx = get_theoretical()
    r_x_label = x_label[::-1]
    r_xx = xx[::-1]
    plt.gca().invert_xaxis()
    plt.plot(r_x_label,r_xx)
    plt.xlabel("SNR(dB) Post Range-FFT")
    plt.ylabel("Phase- RMS(radians)")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    theoretical_plot()