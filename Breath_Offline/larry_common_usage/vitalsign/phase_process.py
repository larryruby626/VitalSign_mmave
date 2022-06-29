import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


def fft2phase(fft_buf, cfg):
    if cfg.buf_state:
        phase = fft_buf[:, int(cfg.cur_idx)]
        phase = np.angle(phase)
        phase = np.unwrap(phase, axis=0)
        # phase = kkt_unwrap(phase)
        if False:
            plt.cla()
            plt.plot(phase)
            plt.pause(0.1)
            plt.draw()
        return phase, cfg
    else:
        return None, cfg


def phase2phasediff(phase):
    phase_diff = phase[:-1] - phase[1:]
    return phase_diff


# ---------------- Phase Map ---------------------------
def fft2phase_phasemap(fft_buf):
    phase_buf = np.zeros([fft_buf.shape[0], fft_buf.shape[1]])

    for r in range(fft_buf.shape[1]):
        phase = fft_buf[:, r]
        phase = np.angle(phase)
        phase = np.unwrap(phase, axis=0)
        phase = phase - np.average(phase)
        phase_buf[:, r] = phase
    return phase_buf


def Calc_target_inphase_map(phase_map):
    argmax_list = np.argmax(phase_map, axis=1)
    # print("phasemap:   {}".format(np.median(argmax_list)))
    return np.median(argmax_list)
# -------------------------------------------------------

def noise_removal(phase_diff):
    noise_list = np.where(abs(phase_diff) > 1)

    if len(noise_list[0]) != 0:
        for idx in noise_list[0]:
            if idx != 0 and idx != (len(phase_diff) - 1):
                p_l = [idx - 1, phase_diff[idx - 1]]
                p_u = [idx + 1, phase_diff[idx + 1]]
                out = (p_l[1] + p_u[1]) / 2  # 最簡單內插
                phase_diff[idx] = out

    return phase_diff


def window_RBM_detect(phase_dif):
    peak, pro = find_peaks(abs(phase_dif), height=0.6)
    plt.scatter(peak, phase_dif[peak], c='r')
    for idx in peak:
        phase_dif[idx - 20:idx + 60] = 0
    return phase_dif
