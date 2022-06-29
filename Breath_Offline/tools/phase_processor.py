import numpy as np
from larry_common_usage.signal_seperation.VMD import VMD_process
from larry_common_usage.signal_seperation.cwt_process import TimeFrequencyWP
from larry_common_usage.DSP.band_pass_filter import band_pass
from larry_common_usage.DSP.get_fft_spectral import spectral_abs
import matplotlib.pyplot as plt
class PhaseProcessor():
    def __init__(self, cfg=None):
        self.widget_cfg = cfg
        self.function_list = {'0': self.normal_method,
                              '1': self.phasediff_method,
                              '2': self.cwt_method,
                              '3': self.vmd_method,
                              '4': self.phase_coherence_method,
                              }

        self.init = True

    def run_process(self, fft_framebuf, target_idx):
        """
        select and run the function which you had choose
        """
        self.fft_frame_buf = fft_framebuf
        self.target_idx = target_idx
        return  self.function_list[str(np.where(self.widget_cfg["pw_phaseprocess"])[0][0])]()


    def vital_sign_mode_process(self,phase):

        if self.widget_cfg["vitalsign_mode"] == "breath":
            phase = band_pass(0.1, 0.8, phase, 20)
        else:
            phase = band_pass(0.8, 2, phase, 20)

        return phase


    def normal_method(self):
        phase = self.fft_frame_buf[:, int(self.target_idx)]
        phase = np.angle(phase)
        phase = np.unwrap(phase, axis=0)
        return self.vital_sign_mode_process(phase)

    def phasediff_method(self):
        phase = self.fft_frame_buf[:, int(self.target_idx)]
        phase = np.angle(phase)
        phase = np.unwrap(phase, axis=0)
        phase_diff = phase[:-1] - phase[1:]

        return self.vital_sign_mode_process(phase_diff)

    def cwt_method(self):
        phase = self.normal_method()
        cwt_phase = TimeFrequencyWP(phase).data
        return cwt_phase

    def vmd_method(self):
        phase = self.normal_method()
        vmd_phase = VMD_process(phase)
        return vmd_phase

    def phase_coherence_method(self):
        around_bin_num = 3
        counter_nub = 0
        aroundphase = np.zeros([self.fft_frame_buf.shape[0], 7])
        # filter is for the unwrap phase cause the DC offset
        phase = band_pass(0.1,3,np.unwrap(np.angle(self.fft_frame_buf[:, int(self.target_idx - around_bin_num)])),20)
        aroundphase[:, 0] = phase

        for idx in range(int(self.target_idx - (around_bin_num-1)), int(self.target_idx + around_bin_num), 1):
            phase = band_pass(0.1, 3,  np.unwrap(np.angle(self.fft_frame_buf[:,idx])), 20)
            aroundphase[:, counter_nub] =phase
            counter_nub += 1

        out_aroundphase = np.average(aroundphase,axis=1)

        return  self.vital_sign_mode_process(out_aroundphase)

    def raw_phase_process(self,fft_buf,targetidx):

        phase = fft_buf[:, int(targetidx)]
        phase = np.angle(phase)
        phase = np.unwrap(phase, axis=0)
        phase = band_pass(0.1, 5, phase, 20)


        return phase

    def calc_RR(self,fft_buf,targetidx):

        phase = fft_buf[:, int(targetidx)]
        phase = np.angle(phase)
        phase = np.unwrap(phase, axis=0)
        phase = band_pass(0.1, 0.5, phase, 20)

        RR = np.argmax(spectral_abs(phase))
        return RR


