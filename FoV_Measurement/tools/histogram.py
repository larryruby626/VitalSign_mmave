import numpy as np
import pandas as pd  # for DataFrames
import matplotlib.pyplot as plt

fs = 625 * 10**3
fftp = 256
no_period = 7

sin_fre = fs*no_period /(fftp)
print(sin_fre)

start_time = 0
end_time = 1/fs*256
sample_rate = fs
time = np.arange(start_time, end_time, 1/sample_rate)


frequency = sin_fre
amplitude = 2**15
theta = 0
# sinewave = (amplitude * np.sin(2 * np.pi * frequency * time + theta))
sinewave = np.floor(amplitude * np.sin(2 * np.pi * frequency * time + theta))
affter_fft = np.fft.fft(sinewave, n=256)
powerfft = affter_fft*np.conjugate(affter_fft)
log_fft = np.where(powerfft > 0.0000000001, 10*np.log10(powerfft),0)
voltage1adc = 0.0484

log_fft_dbmv = np.where(powerfft > 0.0000000001, 10*np.log10(powerfft*voltage1adc),0)
# log_fft = 10 * np.log10(affter_fft*np.conjugate(affter_fft))
plt.figure()
plt.plot(time,log_fft_dbmv)
plt.plot(time,log_fft,c="green")
plt.show()

print(20*np.log10(32768) + 20*np.log10(256/2))

