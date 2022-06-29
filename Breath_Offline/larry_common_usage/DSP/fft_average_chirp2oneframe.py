import  numpy as np


def fft_chirp2frame(dataIn, fftsize=256, data_type="kkt",chirp_num=32):
    """
    :param dataIn: raw frame data ipput
    :param fftsize: the fft size you wanna do
    :param data_type: kkt / ti
    :return:
    """
    rangeFFTsize = fftsize
    ChirpStart = 0
    ChirpEnd = chirp_num-1
    sigfftall = np.array
    [Nadc, Nchirp] = np.shape(dataIn)
    first_pass = False

    for i in range(ChirpStart, ChirpEnd + 1):
        # sig = dataIn[i, :] * np.blackman(64)
        sig = dataIn[i, :] * np.hanning(64)
        # sig = dataIn[i, :] * 1
        sigfft = np.fft.fft(sig, n=fftsize)
        if i == 0:
            pass
        else:
            if not first_pass:
                if data_type == "ti":
                    sigfftall = sigfft[int(sigfft.shape[0] / 2):]  # ti

                else:
                    sigfftall = sigfft[:int(sigfft.shape[0] / 2)]  # kkt

                first_pass = True
            else:
                if data_type == "ti":
                    sigfftall = sigfft[int(sigfft.shape[0] / 2):]  # ti

                else:
                    sigfftall = sigfft[:int(sigfft.shape[0] / 2)]  # kkt

    if data_type == "ti":
        return sigfftall[::-1]
    else:
        return sigfftall[:]