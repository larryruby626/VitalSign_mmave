import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
import scipy.signal as sg


def find_3dB(log_scale_data, idx):
    kkt_max = (np.argmax(log_scale_data))
    kkt = interp1d(log_scale_data[:kkt_max], idx[:kkt_max], kind="linear")
    kkt_2 = interp1d(log_scale_data[kkt_max:], idx[kkt_max:], kind="linear")
    return kkt([-3]), kkt_2([-3])


PRIOR_HZ_HEART = (0.8, 2)
PRIOR_HZ_BREATH = (0.1, 0.5)
PRIOR_RANGE_BIN = (10, 30)
VITAL_SIGN_BUFFER_NUMS = 20


b_KKT = np.array([0.108511395077895, 0, -0.217022790155790, 0, 0.108511395077895])
a_KKT = np.array([1.0000, -2.584280647174934, 2.747640809348158, -1.528758738815148, 0.399623026053622])
b_NTUT = np.array([0.005170966050632, 0, -0.010341932101263, 0, 0.005170966050632])
a_NTUT = np.array([1.0000, -3.804951951129208, 5.447016344482779, -3.478323653690533, 0.836281526065139])
b_filt_heart, a_filt_heart = sg.butter(3, [PRIOR_HZ_HEART[0]/20*2, PRIOR_HZ_HEART[1]/20*2], btype='bandpass')
print(b_filt_heart)
print(a_filt_heart)
b_NTUT = b_filt_heart
a_NTUT = a_filt_heart

w_KKT, h_KTT = signal.freqz(b_KKT, a_KKT)
w_NTUT, h_NTUT = signal.freqz(b_NTUT, a_NTUT)
w_NTUT_1, h_NTUT_1 = signal.freqz(b_NTUT, a_NTUT)
db_kkt = 20 * np.log10(abs(h_KTT))
db_NTUT = 20 * np.log10(abs(h_NTUT))

fig, ax1 = plt.subplots()
plt.subplot(121)
start_band, stop_band = find_3dB(db_kkt, w_KKT)
plt.vlines(start_band, -60, 5, linestyles="dotted", colors='r')
plt.vlines(stop_band, -60, 5, linestyles="dotted", colors='r')
plt.title('Bandpass filter frequency response - KKT')
plt.plot(w_KKT, 20 * np.log10(abs(h_KTT)), 'b')
plt.ylabel('Amplitude [dB]', color='b')
plt.xlabel('Frequency [rad/sample]')
plt.text(2, 1, "start_freqz:{}".format(start_band))
plt.text(2, -4, "stop_freqz:{}".format(stop_band))
# ax2 = ax1.twinx()   共X軸不同Y軸
plt.grid()
plt.ylim([-60, 5])

plt.subplot(122)
start_band, stop_band = find_3dB(db_NTUT, w_NTUT)
plt.title('Bandpass filter frequency response - NTUT')
plt.vlines(start_band, -60, 5, linestyles="dotted", colors='r')
plt.vlines(stop_band, -60, 5, linestyles="dotted", colors='r')
plt.text(2, 1, "start_freqz:{}".format(start_band))
plt.text(2, -4, "stop_freqz:{}".format(stop_band))
plt.plot(w_NTUT, 20 * np.log10(abs(h_NTUT)), 'b')
plt.ylabel('Amplitude [dB]', color='b')
plt.xlabel('Frequency [rad/sample]')
plt.ylim([-60, 5])

plt.grid()
plt.show()
