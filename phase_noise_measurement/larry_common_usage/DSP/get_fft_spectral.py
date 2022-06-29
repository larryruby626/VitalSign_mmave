import numpy as np


def spectral_energy(input, fft_point=1024):
    out = np.fft.fft(input, n=fft_point)
    out = out[:int(fft_point/2)]
    out = out * np.conjugate(out)
    out = 10 * np.log10(out)
    return out

def spectral_abs(input, fft_point=1024, window = False):
    if window: input = input * np.hanning(len(input))
    out = np.fft.fft(input, n=fft_point)
    out = out[:int(fft_point/2)]
    out = abs(out)
    return out

