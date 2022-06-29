import sys
import numpy as np
import random
import matplotlib.pyplot as plt
from tools.p3interpolation import P3InterpolateDer
from scipy.interpolate import InterpolatedUnivariateSpline, interp1d
from scipy import signal


def plot_N_frame(ch1data, sure_plot, linear_noise):
    for i in range(32):
        ch1data[i, :] = ch1data[i, :] * (np.blackman((64)))
    ch1data = np.fft.fft(ch1data, n=256)
    # plt.plot(ch1data[1,:], color='blue')
    ch1data = ch1data * np.conjugate(ch1data)
    ch1data = np.real(ch1data[:, :int(ch1data.shape[1] / 2)])

    ch1data_signal = ch1data - linear_noise[1, :]
    ch1data_signal = np.average(ch1data_signal[1:, :], axis=0)
    sum_chirp = 10 * np.log10(ch1data_signal)
    # valueX = np.array(np.arange(1, 129)) * 0.534
    valueX = np.array(np.arange(1, 129)) * 0.5

    if sure_plot == True:
        plt.plot(valueX, 10 * np.log10(np.average(ch1data[1:, :], axis=0)), color='green', label="Signal + Noise")
        # plt.plot(valueX, sum_chirp,color='red')
        plt.plot(valueX, 10 * np.log10(linear_noise[1, :]),color='blue', label="Noise Floor")
        plt.draw()
        plt.legend()
        # plt.pause(0.001)
    #
    return sum_chirp
    # plt.cla()


def plot_data(data):
    plt.plot(data)
    plt.draw()
    plt.pause(0.05)


def reshape_radar_data(radar_data):

    tmp_data = radar_data
    ch1data = tmp_data[:4096]
    ch2data = tmp_data[4096:]
    # plot_data(ch1data)  # rawdata
    ch1data = np.reshape(ch1data, [32, 128])
    ch2data = np.reshape(ch2data, [32, 128])
    ch1data = ch1data[:, :64]
    ch2data = ch2data[:, :64]
    return ch1data, ch2data


if __name__ == "__main__":
    """
    file_path : add your dataset folder path
    save_path :　path to save the target bin Signal dB dataset
    channel   : 1/2 channel1 data and channel2 data
    """
    # path = './dataset_7G_SIC_Freeze/'
    path = './dataset_7G_SIC_ON/'
    # path = './Fov_chest/'
    file_path = path  # KKT usage path
    save_path = path + "/processed_data/"

    #  ---- for corner reflector usage ----
    # angele_list = ["-30", "-20", "-10", "0", "+10", "+20", "+30"] # SIC_freeze
    angele_list = ["-40", "-30", "-20", "-10", "0", "+10", "+20", "+30", "+40"]  # SICON
    range_list = ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"]
    # range_list = [ "20", "25", "30", "35", "40", "45", "50", "55", "60"]

    #  ---- for chest data usage ----
    # angele_list = ["-60", "-50", "-40", "-30", "-20", "-10", "0", "+10", "+20", "+30", "+40", "+50", "+60"]
    # range_list = ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"]

    #  ---- for single usage ----
    # range_list = ["60"]
    # angele_list = ["+30"]


    channel = 2
    # sure_plot = True
    sure_plot = False
    sure_save = True
    # sure_save = False

    if sure_plot:
        plt.figure()
    #   ---- load the linear noise for caculate real signal ----
    # linear_noise = np.load("sumof_noise_floor_linear_freeze.npy")
    linear_noise = np.load("./noise_floor/sumof_noise_floor_linear_sicON.npy")
    for time in range(1,2):
        for angle in angele_list:
            for r in range_list:
                file_name = "range" + r + "_angle" + angle + "_time_" + str(time) + ".npy"
                print("start {} cacluate".format(file_name ))
                radar_data = np.load(file_path + file_name, allow_pickle=True)
                rangex = int(r)
                snr_method1 = []
                snr_method2 = []
                for frame_num in range(1000):
                    ch1data, ch2data = reshape_radar_data(radar_data[frame_num])

                    if channel ==1:
                        sum_chirp = plot_N_frame(ch1data, sure_plot, linear_noise)
                    elif channel ==2:
                        sum_chirp = plot_N_frame(ch2data, sure_plot, linear_noise)

                    peaK_arr, dicttt = signal.find_peaks(sum_chirp, height=50, threshold=None, distance=30, prominence=None,
                                                         width=None, wlen=None,
                                                         rel_height=0.5, plateau_size=None)
                    if len(peaK_arr)!= 0 :
                        usable_peaK_arr = []
                        usable_dicttt =[]
                        #  ---  check is the peak in legal range ---
                        cc = 0
                        for obj in peaK_arr:
                            if ((rangex*2)-obj)<20:
                                usable_peaK_arr.append(obj)
                                usable_dicttt.append(dicttt["peak_heights"][cc])
                            cc+=1
                        if len(usable_dicttt) != 0:
                            #  ---  find the max peak in usable array ---
                            tmp_index = np.argmax(usable_dicttt, axis=None, out=None)
                            current_peak_index = usable_peaK_arr[tmp_index]
                            """
                            --------------- method 1 spline---------------
                            """
                            x_axis = []
                            for i in range(128):
                                x_axis.append(i)
                            wnum = 5  #spline window number
                            if current_peak_index-wnum>5:
                                x_axis = x_axis[current_peak_index-wnum:current_peak_index+wnum]
                                f = InterpolatedUnivariateSpline(x_axis, sum_chirp[current_peak_index-wnum:current_peak_index+wnum], k=4)
                                cr_pts = f.derivative().roots()
                                cr_pts = np.append(cr_pts, (x_axis[0], x_axis[-1]))  # also check the endpoints of the interval
                                cr_vals = f(cr_pts)
                                min_index = np.argmin(cr_vals)
                                max_index = np.argmax(cr_vals)

                            """
                            --------------- method 2 quadratic ---------------
                            """
                            p = [x for x in range(current_peak_index - 1, current_peak_index + 2)]

                            p_l = [p[0], sum_chirp[p[0]]]
                            p_c = [p[1], sum_chirp[p[1]]]
                            p_u = [p[2], sum_chirp[p[2]]]
                            max_x_th2, max_y_th2, x, y = P3InterpolateDer(p_l, p_c, p_u)
                            # print("method1: ", np.round(max_x_th2), )
                            # print("method1: ",cr_pts[max_index], cr_vals[max_index] )
                            # print("method2: ",np.round(max_x_th2),max_y_th2)
                            if np.isnan(cr_vals[max_index]):
                                print("FUCK!!!!The value is Nan!!!!!!")
                            else:
                                snr_method1.append([cr_pts[max_index], cr_vals[max_index]])

                            snr_method2.append([np.round(max_x_th2),max_y_th2])

                            if sure_plot == True:
                                # plt.scatter(peaK_arr, sum_chirp[peaK_arr], c="blue",s=20)
                                # plt.scatter(cr_pts[max_index], cr_vals[max_index], c="red")
                                # plt.scatter(max_x_th2, max_y_th2, c="green")
                                plt.title(file_name)
                                plt.xlabel("range(cm)")
                                plt.ylabel("power(dB)")
                                plt.ylim([45,110])
                                plt.draw()
                                plt.pause(0.001)
                                plt.cla()
                                # plt.pause(200) # freeze the plot

                if sure_save == True:
                    if channel ==1 :
                        np.save(save_path + "channel1\\m1_"+file_name, snr_method1)
                        np.save(save_path + "channel1\\m2_"+file_name, snr_method2)
                    elif channel == 2 :
                        np.save(save_path + "channel2\\m1_" + file_name, snr_method1)
                        np.save(save_path + "channel2\\m2_" + file_name, snr_method2)

    print("process end")
    sys.exit()
