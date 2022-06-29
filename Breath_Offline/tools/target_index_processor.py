import numpy as np
from larry_common_usage.vitalsign.phase_process import *
from larry_common_usage.vitalsign.Filter_process import Phase_filter_proecss

class TargetIdxProcessor():

    def __init__(self, cfg=None):
        self.widget_cfg = cfg


    def run_process(self, fft_framebuf):
        """
        select and run the function which you had choose
        """
        self.fft_frame_buf = fft_framebuf
        self.function_list = {'0': self.phase_map_method,
                              '1': self.Max_power_method}
        targetidx = self.function_list[str(np.where(self.widget_cfg["pw_targetidx"])[0][0])]()

        return  targetidx

    def phase_map_method(self):
        phase = fft2phase_phasemap(self.fft_frame_buf)
        phase_RR, phase_HB, phase_both = Phase_filter_proecss(phase)
        # phase_RR = wgc_smoothing_forBR(phase_RR)
        fft = abs(np.fft.fft(phase_RR, n=1024, axis=0)[:512])
        phase_map = np.sum(fft, axis=0)
        phase_map = (phase_map - np.min(phase_map)) / np.max(phase_map)
        target_idx = Calc_target_inphase_map(abs(self.fft_frame_buf * phase_map))

        return target_idx, abs(self.fft_frame_buf * phase_map)

    def Max_power_method(self):
        frame_buf = self.fft_frame_buf
        FFT_std_buf = np.zeros([1, frame_buf.shape[1]])
        range_buf = []
        range_buf_diff = []
        for i in range((frame_buf.shape[0])):
            if len(FFT_std_buf) == 0:
                FFT_std_buf = frame_buf[0]
            elif len(FFT_std_buf) < 3:
                FFT_std_buf = np.vstack((FFT_std_buf, np.expand_dims(frame_buf[i], axis=0)))
            else:
                FFT_std_buf = FFT_std_buf[1:, :]
                FFT_std_buf = np.vstack((FFT_std_buf, np.expand_dims(frame_buf[i], axis=0)))
                tmp_range = np.std(FFT_std_buf, axis=0)
                tmp_idx = np.argmax(tmp_range)
                if len(range_buf) != 0:
                    range_buf_diff.append(abs(tmp_idx - range_buf[-1]))
                range_buf.append(tmp_idx)
        return np.median(range_buf),None

