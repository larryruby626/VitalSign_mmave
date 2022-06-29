from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


def notch_filter(fs, f0, Q, data):
    '''
    fs :  Sample frequency (Hz)
    f0 : Frequency to be removed from signal (Hz)
    Q :  Quality factor
    '''
    b, a = signal.iirnotch(f0, Q, fs)
    filted_signal = signal.filtfilt(b, a, data)
    return filted_signal


# Design notch filter
def plot_frequency_respones(fs, f0, Q):
    '''
       fs :  Sample frequency (Hz)
       f0 : Frequency to be removed from signal (Hz)
       Q :  Quality factor
       '''
    b, a = signal.iirnotch(f0, Q, fs)
    freq, h = signal.freqz(b, a, fs=fs)
    # Plot
    fig, ax = plt.subplots(2, 1, figsize=(8, 6))
    ax[0].plot(freq, 20 * np.log10(abs(h)), color='blue')
    ax[0].set_title("Frequency Response")
    ax[0].set_ylabel("Amplitude (dB)", color='blue')
    ax[0].set_xlim([0, 10])
    ax[0].set_ylim([-25, 10])
    ax[0].grid()
    ax[1].plot(freq, np.unwrap(np.angle(h)) * 180 / np.pi, color='green')
    ax[1].set_ylabel("Angle (degrees)", color='green')
    ax[1].set_xlabel("Frequency (Hz)")
    ax[1].set_xlim([0, 10])
    ax[1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
    ax[1].set_ylim([-90, 90])
    ax[1].grid()
    plt.show()


if __name__ == "__main__":
    plot_frequency_respones(10, 0.02, 30)
