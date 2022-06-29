import matplotlib.pyplot as plt
import numpy as np
import pywt
from scipy.signal import find_peaks

iter_freqs = [
    {"name": '0-30Hz' , "fmin":0, "fmax":30},
    {"name": '30-60Hz' , "fmin":30, "fmax":60},
    {"name": '40-120Hz' , "fmin":60, "fmax":100},
    # {"name": '40-120Hz' , "fmin":40, "fmax":120}
]


def TimeFrequencyWP(data, fs=625, wavelet='db3', maxlevel=7, sure_plot=False):

    # 小波包變換這裏的採樣頻率爲250，如果maxlevel太小部分波段分析不到
    wp = pywt.WaveletPacket(data=data, wavelet=wavelet, mode='smooth', maxlevel=maxlevel)
    # 頻譜由低到高的對應關係，這裏需要注意小波變換的頻帶排列默認並不是順序排列，所以這裏需要使用’freq‘排序。
    freqTree = [node.path for node in wp.get_level(maxlevel, 'freq')]
    # 計算maxlevel最小頻段的帶寬
    freqBand = fs/(2**maxlevel)
    #######################根據實際情況計算頻譜對應關係，這裏要注意係數的順序
    if sure_plot ==True:
        # 繪圖顯示
        fig, axes = plt.subplots(len(iter_freqs)+1, 1, figsize=(10, 7), sharex=True, sharey=False)
        # 繪製原始數據
        axes[0].plot(data)
        axes[0].set_title('原始數據')

    for iter in range(len(iter_freqs)):
        # 構造空的小波包
        # new_wp = pywt.WaveletPacket(data=None, wavelet=wavelet, mode='symmetric', maxlevel=maxlevel)
        new_wp = pywt.WaveletPacket(data=None, wavelet=wavelet, mode='smooth', maxlevel=maxlevel)
        for i in range(len(freqTree)):
            # 第i個頻段的最小頻率
            bandMin = i * freqBand
            # 第i個頻段的最大頻率
            bandMax = bandMin + freqBand
            # 判斷第i個頻段是否在要分析的範圍內
            if (iter_freqs[iter]['fmin']<=bandMin and iter_freqs[iter]['fmax']>= bandMax):
                # 給新構造的小波包參數賦值
                new_wp[freqTree[i]] = wp[freqTree[i]].data
        # 繪製對應頻率的數據

        if sure_plot == True:
        #
            axes[iter+1].plot(new_wp.reconstruct(update=True))
        #     # 設置圖名
            axes[iter+1].set_title(iter_freqs[iter]['name'])
        else:
            new_wp.reconstruct(update=True)

    return new_wp


if __name__ == '__main__':
    wavelet = pywt.Wavelet('db1')

    # ALL_heart_beat = np.load("D:\\pythonProject\\larry_test\\CWT_Data\\phase_HB_data_3.npy", allow_pickle=True)
    # ALL_heart_beat = np.load("D:\\pythonProject\\larry_test\\CWT_Data\\on_32_128_0_20_HR.npy", allow_pickle=True)
    # ALL_heart_beat = np.load("D:\\pythonProject\\larry_test\\CWT_Data\\maxpeak_4_ch1.npy", allow_pickle=True)
    ALL_heart_beat = np.load("G:\\我的雲端硬碟\\開酷\\FoV_experiment\\dataset1101109\\Phase_Buff\\Automatic_peak\\sicF\\BR_20cm_time1.npy", allow_pickle=True)

    clean_heart_beat = np.load("D:\\pythonProject\\larry_test\\CWT_Data\\hold_cleanwt.npy", allow_pickle=True)
    idx = 600
    ww_start = 0+idx
    ww_end = 300+idx

    # TimeFrequencyWP(ALL_heart_beat[ww_start:ww_end], 1200, wavelet='db4', maxlevel=8)
    # TimeFrequencyWP(ALL_heart_beat[1247:1370], 1200, wavelet='db4', maxlevel=8)
    x =TimeFrequencyWP(ALL_heart_beat, sure_plot=True).data

    new = abs(np.fft.fft(x,n=1024)[:512])
    peak =np.array(find_peaks(new, height=25))
    print(peak)
    plt.figure()
    plt.plot(new)
    plt.scatter(peak[0], new[peak[0]],c="r")
    plt.show()
