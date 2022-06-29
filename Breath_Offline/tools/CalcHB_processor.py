import numpy as np
from larry_common_usage.DSP.band_pass_filter import band_pass
from  larry_common_usage.Calc_heartbeat.IBI_process import Calc_groundtruth_HB
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

class CalcHBProcessor():

    def __init__(self, cfg=None):
        self.widget_cfg = cfg

        self.function_list = {'0': self.STFT,
                              '1': self.IBI,
                              }
        self.plot_init =True
    def run_process(self, phase):
        self.filterd_phase = phase

        HB,spectral = self.function_list[str(np.where(self.widget_cfg["pw_HBCalc"])[0][0])]()
        return HB, spectral

    def STFT(self):
        half_fft_n = 512
        tmp_data = self.filterd_phase
        phase_spectrum  = np.fft.fft(tmp_data, n=int(half_fft_n * 2))
        phase_spectrum = np.abs(phase_spectrum[:half_fft_n])
        f_scale_index = np.array(np.linspace(0, half_fft_n - 1, half_fft_n) * 60 / half_fft_n * 10)
        if self.widget_cfg["vitalsign_mode"] == "breath":
            upper_bound = 50
            lower_bound = 6
        else:
            upper_bound = 120
            lower_bound = 55


        peak = np.array(find_peaks(phase_spectrum, distance=10), dtype=tuple)

        legal_peak_idx = np.where(np.logical_and(f_scale_index[peak[0]] >= lower_bound, \
                                                 f_scale_index[peak[0]] <= upper_bound))

        arr_value = phase_spectrum[peak[0][legal_peak_idx]]
        if len(arr_value) != 0:
            max_idx = np.argmax(arr_value)

            return f_scale_index[peak[0][legal_peak_idx]][max_idx], phase_spectrum
        else:
            return 0 , phase_spectrum

    def IBI(self):
        time_buff =np.linspace(0,len(self.filterd_phase)-1,len(self.filterd_phase))*0.05
        HB = Calc_groundtruth_HB(self.filterd_phase,time_buff,"radar")


        return HB , time_buff