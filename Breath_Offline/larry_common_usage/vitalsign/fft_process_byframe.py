# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 15:37:25 2021

@author: ricky li
"""
import numpy as np
import matplotlib.pyplot as plt



def fft_process_byframe(dataIn, fftcfg, larry_cfg):
    rangeFFTsize = fftcfg.rangeFFTsize
    range_apply_window = fftcfg.range_apply_window
    ChirpStart = fftcfg.ChirpStart
    ChirpEnd = fftcfg.ChirpEnd
    # print(ChirpEnd-ChirpStart+1)
    sigfftall = np.array
    [Nadc, Nchirp] = np.shape(dataIn)

    sigfftall =  np.zeros([ChirpEnd-ChirpStart, int(rangeFFTsize/2)],dtype=np.complex_)
    first_pass = False
    for i in range(ChirpStart, ChirpEnd + 1):
        # sig = dataIn[i, :] * np.blackman(64)
        sig = dataIn[i, :] * np.hanning(64)
        # sig = dataIn[i, :] * 1
        sigfft = np.fft.fft(sig, n=fftcfg.rangeFFTsize)

        if i == 0:
            pass
        else:
            if not first_pass:
                if larry_cfg.data_type == "ti":
                    # plt.plot(10*np.log10((sigfft[:]*np.conjugate(sigfft[:]))))
                    sigfftall[i-1,:] = sigfft[int(sigfft.shape[0] / 2):]   # ti

                    # plt.show()

                else:
                    sigfftall[i-1,:] = sigfft[:int(sigfft.shape[0] / 2)]   # kkt

                first_pass = True
            else:
                if larry_cfg.data_type == "ti":
                    sigfftall[i-1,:] = sigfft[int(sigfft.shape[0] / 2):]   # ti

                else:
                    sigfftall[i-1,:] = sigfft[:int(sigfft.shape[0] / 2)]   # kkt

    sigfftall = np.sum(sigfftall, axis=0)
    if larry_cfg.data_type == "ti":
        return sigfftall[::-1]
    else:
        return sigfftall[:]
