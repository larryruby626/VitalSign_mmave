# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 14:21:13 2021

@author: ricky li
"""

import numpy as np


def vitalcfg():
    class cfg:
        Nchirp = 16
        Nsample = 128
        multibin = 0
        binNum = 0

        # const parameter declaration
        C = 3 * 10 ** 8
        fc = 60 * 10 ** 9
        lambdaa = C / fc
        framePeriod = 50 * 10 ** -3  # 50ms

    class fftcfg:
        # ---------------CFG------------------
        rangeFFTsize = 256
        range_apply_window = 0
        ChirpStart = 0
        ChirpEnd = 31
        # ChirpEnd = 7

    class cfarcfg:
        # kos = 0.55
        kos = 0.7
        logscale = 1
        guardLen = 2
        noiseWin = 4
        threshold1D = 0
        cfarmode = 4
        startIdx = 0
        endIdx = 63
        done = 0
        cnt = 0
        cnt_threshold = 10

    class bpfcfg:
        Fs = 1 / cfg.framePeriod
        N = 4  # order
        Fpass1 = 0.1  # Hz
        Fpass2 = 0.5  # Hz
        Apass = 0.5  # Passband Ripple (dB)
        zf = np.zeros((N), float)

    class hpfcfg:
        Fs = 1 / cfg.framePeriod
        N = 10  # order
        # N = 4  # order
        Fpass1 = 0.8  # Hz
        Fpass2 = 2  # Hz
        Apass = 0.5  # Passband Ripple (dB)
        zf = np.zeros((N), float)

    class larry_cfg:
        """
        :param sum_phase_type before --> sum before angle
                              after  --> sum after get angle
        :param filter_type    "kkt"
        """
        channel = 1
        f_b_num = 256  # frame buffer length
        # shift_len = [f_b_num/2]
        shift_len = [1]
        plot_fft_len = 500
        sure_plot_FFT = False
        sureplot_result = True
        sure_plot_phase_diff = False
        frame_enough = False
        sure_Multibin = True
        data_type = "kkt"
        # data_type = "ti"
        sum_phase_type = "after"
        filter_type = "ntut"

    class dpccfg:
        trigger = 0
        Nframe = 8
        fftsize = 1024
        framePeriod = cfg.framePeriod  # 50ms
        startFreq = 0.8  # Hz
        stopFreq = 2  # Hz
        targetIdx = 0
        filter_type = "ntut"
        # filter_type = "kkt"
        N = 10  # order
        zf = np.zeros((N), float)
        targetphase = np.zeros([larry_cfg.f_b_num])
        done = 0
        havedoneonce = 0
        rangebin = 0

    return fftcfg, dpccfg, cfarcfg, bpfcfg, hpfcfg, larry_cfg
