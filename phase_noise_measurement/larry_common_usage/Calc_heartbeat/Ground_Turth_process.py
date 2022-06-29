import numpy as np
from larry_common_usage.Calc_heartbeat.IBI_process import Calc_groundtruth_HB

def ground_turth_process(PPG_dict, larry_cfg, data_typpe):
    '''
    data_typpe:  "ppg"/"ecg"/"radar"
    '''
    PPG_dict = dict(enumerate(PPG_dict.flatten()))[0]
    value_buf = PPG_dict["value"]
    time_buf = PPG_dict["time"]
    label_buf = PPG_dict["state_label"]
    HB_ppg_list = []
    window_size = larry_cfg.w_l * 4
    for i in range((len(value_buf) - window_size)):

        if (i % int(larry_cfg.shift_len)) == 0:
            tmp_ppg = np.array(value_buf[i:i + window_size])
            tmp_ppg_time = np.array(time_buf[i:i + window_size])
            hz = Calc_groundtruth_HB(tmp_ppg, tmp_ppg_time,data_typpe)
            HB_ppg_list.append(hz)

    return HB_ppg_list,label_buf
