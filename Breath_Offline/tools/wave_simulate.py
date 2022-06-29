import matplotlib.pyplot as plt
import numpy as np


def wave_sumlate_process(window_len, RR, HB, fft_point=1024):
    w_len = window_len/20
    R_hz = RR
    H_hz = HB
    fft_n = fft_point
    t = np.linspace(0, w_len, int(w_len * 20), endpoint=False)  # 定義時間陣列
    AMP = 2
    x = AMP * np.cos(2 * np.pi * R_hz * t)
    harmornic_num = 15

    for i in range(harmornic_num):
        tmp_wave = AMP * (0.8 ** (i + 1)) * np.cos(2 * np.pi * R_hz * (i + 1) * t)  # 產生弦波

        if i < 3:
            tmp_wave = AMP * (1/(i+1)) * np.cos(2 * np.pi * R_hz * (i + 1) * t)  # 產生弦波
        elif i < 6:
            tmp_wave = AMP * (1/(i+1)) * np.cos(2 * np.pi * R_hz * (i + 1) * t)  # 產生弦波
        elif i < 9:
            tmp_wave = AMP * (1/(i+1)) * np.cos(2 * np.pi * R_hz * (i + 1) * t)  # 產生弦波

        x = x + tmp_wave

    # sencond order IMD
    sencond_1 = R_hz + H_hz
    sencond_2 = R_hz - H_hz
    # x = x + AMP / 4 * np.cos(2 * np.pi * sencond_1 * t)  # 產生弦波
    # x = x + AMP / 4 * np.cos(2 * np.pi * sencond_2 * t)  # 產生弦波
    # Third order IMD
    # Third = 2 * R_hz + H_hz
    # Third1 = 2 * R_hz - H_hz
    # Third2 = 2 * H_hz + R_hz
    # Third3 = 2 * H_hz - R_hz
    # x = x + AMP / 5 * np.cos(2 * np.pi * Third * t)  # 產生弦波
    # x = x + AMP / 5 * np.cos(2 * np.pi * Third1 * t)  # 產生弦波
    # x = x + AMP / 5 * np.cos(2 * np.pi * Third2 * t)  # 產生弦波
    # x = x + AMP / 5 * np.cos(2 * np.pi * Third3 * t)  # 產生弦波

    y = AMP / 4 * np.cos(2 * np.pi * H_hz * t)  # 產生弦波
    y1 = AMP / 4 * np.cos(2 * np.pi * H_hz * 2 * t)  # 產生弦波
    out = x + y + y1
    return out


if __name__ == "__main__":
    fft_n = 1024
    out = wave_sumlate_process(1024, 0.16, 1.566, fft_point=1024)

    plt.plot(out)  # 繪圖
    plt.xlabel('Frame nubmer(20FPS)')
    plt.ylabel('Amplitude')
    plt.figure()
    # out = out * np.hanning(len(out))
    x_axis = np.linspace(0, int(fft_n / 2), int(fft_n / 2)) / fft_n * 2 * 10
    plt.plot(x_axis, abs(np.fft.fft(out, n=fft_n))[:int(fft_n / 2)])
    plt.show()
