
import scipy.signal as sg
import numpy as np

def filter_adjust(filter_type):
    if filter_type == "kkt":
        b_filt_heart = np.array([0.108511395077895, 0, -0.217022790155790, 0, 0.108511395077895])
        a_filt_heart = np.array(
            [1.0000, -2.584280647174934, 2.747640809348158, -1.528758738815148, 0.399623026053622])
    elif filter_type == "ntut":
        PRIOR_HZ_HEART = (0.8, 2)
        b_filt_heart, a_filt_heart = sg.butter(5, [PRIOR_HZ_HEART[0] / 20 * 2, PRIOR_HZ_HEART[1] / 20 * 2],
                                               btype='bandpass')
    elif filter_type == "highpass":
        b_filt_heart, a_filt_heart = sg.butter(5, 0.8 / 20 * 2, btype='high')

    return b_filt_heart, a_filt_heart