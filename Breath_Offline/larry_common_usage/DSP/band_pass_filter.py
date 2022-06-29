import  numpy as np
import scipy.signal as sg
from scipy import interpolate

def band_pass(start_freqz, end_freqz, data, sample_fz):
    """
    :param start_freqz: startband frequency
    :param end_freqz:   endband frequency
    :param data:        needed filter data
    :param sample_fz:   data sample rate (fps)
    :return:
    """
    PRIOR_HZ = [start_freqz, end_freqz]
    halfBand_freqz= sample_fz/2
    b_filt, a_filt = sg.butter(1, [PRIOR_HZ[0] /halfBand_freqz,
                                   PRIOR_HZ[1] /halfBand_freqz], btype='bandpass')

    sig_out= sg.filtfilt(b_filt, a_filt, data)
    return  sig_out
