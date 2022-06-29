import numpy as np
import matplotlib.pyplot as plt
import sympy
from larry_common_usage.xlsx_writer import XlsxWriter

def inverse_log(v):
    v = v / 10
    out = 10 ** v
    return out

def get_theoretical():
    phase_N_arr = []
    x_label = np.array(range(15, 60, 1))
    print(x_label)
    for i in range(15, 60, 1):
        x = 1 / (np.sqrt(2 * inverse_log(i)))
        phase_N_arr.append(x)

def get_phase_noise(arr):
    phase_N_arr = []
    for i in arr:
        x = 1 / (np.sqrt(2 * inverse_log(i)))
        phase_N_arr.append(x)
    return phase_N_arr

##----------------計算由FOV結果取得的noise---------------

ch1 = [50.29, 46.43, 42.96, 34.71, 35.33, 32.52, 31.75, 30.50, 28.72, 27.50, 25.92]
ch3 = [47.34, 42.58, 40.16, 32.90, 31.70, 30.27, 29.30, 27.78, 26.10, 25.71, 23.27]
x_label = np.array(range(10, 61, 5))
channel1_phasenoise = get_phase_noise(ch1)
channel3_phasenoise = get_phase_noise(ch3)
##------------------------------------------------------

ch3_noise_arr = np.load("../phase_noise_dic/dongle_ch1_dic.npy", allow_pickle=True)
noise_arr = np.load("../phase_noise_dic/dongle_ch3_dic.npy", allow_pickle=True)
xl_path = "..\\phase_noise_dic\\dongle_total.xlsx"

xl = XlsxWriter(xl_path)
xl.addline(["time", "1", "2", "3", "4", "5"])
ch3_noise_dict = dict(enumerate(ch3_noise_arr.flatten()))[0]
noise_dict = dict(enumerate(noise_arr.flatten()))[0]
list_20 = np.array(noise_dict["20"])
list_40 = np.array(noise_dict["40"])
list_60 = np.array(noise_dict["60"])
ch3_list_20 = np.array(ch3_noise_dict["20"])
ch3_list_40 = np.array(ch3_noise_dict["40"])
ch3_list_60 = np.array(ch3_noise_dict["60"])
x_label_20 = list(np.array(np.ones(5)*20))
x_label_40 = np.array(np.ones(5)*40)
x_label_60 = np.array(np.ones(5)*60)
p1, = plt.plot(x_label,channel1_phasenoise)
p2, = plt.plot(x_label,channel3_phasenoise)
x_label_20 = [x-0.5 for x in x_label_20]
x_label_40 = [x-0.5 for x in x_label_40]
x_label_60 = [x-0.5 for x in x_label_60]
p3 = plt.scatter(x_label_20,list_20,s=20,alpha=0.5,c='b')
p4 = plt.scatter(x_label_40,list_40,s=20,alpha=0.5,c='b')
p5 = plt.scatter(x_label_60,list_60,s=20,alpha=0.5,c='b')
x_label_20 = [x+1 for x in x_label_20]
x_label_40 = [x+1 for x in x_label_40]
x_label_60 = [x+1 for x in x_label_60]
p6 = plt.scatter(x_label_20,ch3_list_20,s=20,alpha=0.5,c='orange')
p7 = plt.scatter(x_label_40,ch3_list_40,s=20,alpha=0.5,c='orange')
p8 = plt.scatter(x_label_60,ch3_list_60,s=20,alpha=0.5,c='orange')
xl.addline(list_20)
xl.addline(list_40)
xl.addline(list_60)
xl.addline(ch3_list_20)
xl.addline(ch3_list_40)
xl.addline(ch3_list_60)
xl.save()
plt.ylabel("phase(radians)")
plt.xlabel("cm(radar to conner reflector)")
plt.legend([p1,p2,p3,p6], ["channel1 by FOV SNR", "channel3 by FOV SNR",'channel1 measure','channel3 measure'])
plt.title("Phase Noise to distance by FoV experiment SNR(theoretical)")
plt.show()
