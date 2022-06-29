import sys
import numpy as np
import random
import matplotlib.pyplot as plt
from tools.p3interpolation import P3InterpolateDer
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy import signal

def plot_N_frame(ch1data, sure_plot,out_type):
    for i in range(32):
        ch1data[i,:] = ch1data[i,:] * (np.blackman((64)))
    rawdata = ch1data.copy()
    ch1data = np.fft.fft(ch1data, n=256)
    # ch1data = ch1data * 0.04841
    ch1data = ch1data * np.conjugate(ch1data)
    ch1data = np.real(ch1data[:,:int(ch1data.shape[1]/2)])

    if out_type == "linear":
        sum_chirp =(np.average(ch1data[1:,:],axis=0))
    elif out_type == "dBscale":
        plt.ylim([30,80])
        sum_chirp = 10 * np.log10((np.average(ch1data[1:, :], axis=0)))
    elif out_type == "psd":
        sum_chirp = (np.average(ch1data[1:, :int(ch1data.shape[1]/2)], axis=0))
        # f,Pxx_den = signal.welch(np.average(rawdata[1:, :], axis=0)*0.04841,fs= 6.25e3, nperseg=256)
        # vol_ch1 = 0.04841* rawdata
        vol_ch1 = rawdata
        fft_ch1 = np.fft.fft(vol_ch1*0.04841, n=256)/32
        power_ch1 = fft_ch1*np.conjugate(fft_ch1)
        ch1data = np.real(np.average(power_ch1[:, :int(ch1data.shape[1]/2)],axis=0))
        log_ch1 = 10*np.log10(ch1data)

        if sure_plot == False:
            plt.plot(log_ch1)
            # plt.ylim([0, 130])
            plt.xlabel('frequency [Hz]')
            plt.ylabel('PSD [V**2/Hz]')
            plt.show()
            plt.pause(0.05)
            plt.cla()

    if sure_plot == True:
        plt.plot(sum_chirp)
        plt.draw()
        plt.pause(0.05)
        plt.cla()

    return sum_chirp


def plot_data(data):
    plt.plot(data)
    plt.draw()
    plt.pause(0.05)
#


if __name__ == "__main__":

    # file_path = "./Fov_chest/"  #   KKT usage path
    file_path = "./dataset_7G_SIC_ON/"  #   KKT usage path
    # file_path = "./dataset_7G_SIC_Freeze/"  #   KKT usage path
    """
    out_type : linear / dBscale
    """
    noise_floor_arry = np.zeros([9, len(list(range(0, 128)))])
    sure_plot = True
    sure_plot_final_result = False
    sure_save = False
    sure_save_vetor = False
    vector_list = []
    out_type ="linear"
    # out_type ="dBscale"

    for time in range(1,9):
        # file_name = "background_time" + str(time) + ".npy"
        file_name = "noise_sample_time" + str(time) + ".npy"
        radar_data = np.load(file_path + file_name, allow_pickle=True)
        tmp_data = radar_data[:]
        ch1data = tmp_data[:,:4096]
        ch2data = tmp_data[:,4096:]
        ch1data = np.reshape(ch1data,[-1,32,128])
        ch2data = np.reshape(ch2data,[-1,32,128])
        ch1data = ch1data[:, :, :64]
        ch2data = ch2data[:, :, :64]
        for i in range(1000):
            if i == 0:
                sum_chirp = plot_N_frame(ch1data[i], sure_plot, out_type)
            else:
                sum_chirp += plot_N_frame(ch1data[i], sure_plot, out_type)
            vector_list.append(sum_chirp)

        sum_frame_chirp = sum_chirp/1000

        if sure_save_vetor:
            np.save("./noise_floor_vector_time"+ str(time)+".npy",vector_list)
            vector_list = []

        counter = 0
        for x in range(0,128):
            noise_floor_arry[0, counter] = x
            noise_floor_arry[time, counter] = np.average(sum_frame_chirp[x-2:x+2])
            if (x+2) > 127:
                noise_floor_arry[time, counter] = np.average(sum_frame_chirp[x - 2:127])
            if (x-2) < 0:
                noise_floor_arry[time, counter] = np.average(sum_frame_chirp[0:x+2])
            counter += 1

    sumof_noise_floor_arry = np.zeros([2, 128])
    sumof_noise_floor_arry[0, :] = noise_floor_arry[0,:]
    sumof_noise_floor_arry[1, :] = np.average(noise_floor_arry[1:], axis=0)


    if sure_plot_final_result:
        plt.figure()
        plt.title("Noise floor")
        plt.xlabel("fft range bin")
        plt.ylabel("power(dB)")
        for i in range(8):
            plt.plot(noise_floor_arry[0,:],noise_floor_arry[i+1,:], c="blue", linewidth=1.0)
        plt.plot(noise_floor_arry[0, :], sumof_noise_floor_arry[1,:], c="red", linewidth=3.0)
        # plt.ylim([20,100])

    if sure_save:
        if out_type == "linear":
            np.save("./sumof_noise_floor_linear_sicON.npy", sumof_noise_floor_arry)
        elif out_type == "dBscale":
            np.save("./sumof_noise_floor_freeze.npy", sumof_noise_floor_arry)

print(out_type, "noise floor processed finished")
sys.exit()