import numpy as np

path = "C:\\Fov_test\\新增資料夾\\"
name = "lie_slow_light_p1_t3_ecg_dict"
PPG_dict = np.load(path+name+".npy",allow_pickle=True)
PPG_dict = dict(enumerate(PPG_dict.flatten()))[0]
value_buf = PPG_dict["value"]
time_buf = PPG_dict["time"]
print(time_buf[-1]-time_buf[0])
# name1 = "lie_slow_light_p1_t1_ecg_dict"
# PPG_dict2 = np.load(path+name1+".npy",allow_pickle=True)
# PPG_dict2 = dict(enumerate(PPG_dict2.flatten()))[0]
# value_buf2 = PPG_dict2["value"]
# time_buf2 = PPG_dict2["time"]

#
# len1= len(value_buf)
# len2 = len(value_buf2)
# len_dif = len1-len2
#
# out_time = (time_buf[-len_dif:])
# out_V    = (value_buf[-len_dif:])
# state_buff = []
# ecg_dict = {"value": out_V, "time": out_time, "state_label": state_buff}
# np.save(path+name+".npy",ecg_dict)
#
#


