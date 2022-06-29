import numpy as np
from larry_common_usage.Calc_heartbeat.Ground_Turth_process import ground_turth_process

def ecg2hb_process(name,path,ecg_raw, cfg,save_stop_lb=False):
    print("-----process {}-------".format(name))
    HB_ppg_list, label_buf = ground_turth_process(ecg_raw, cfg, "ecg")
    np.save(path + "hb_gt\\" + name + "_HB_buf.npy", HB_ppg_list)
    if save_stop_lb :
        np.save(path + "hb_gt\\" + name + "_lb_buf.npy", label_buf)

def ppg2hb_process(name,path,ecg_raw, cfg,save_stop_lb=False):
    print("-----process {}-------".format(name))
    HB_ppg_list, label_buf = ground_turth_process(ecg_raw, cfg, "ppg")
    # print(HB_ppg_list)
    np.save(path + "hb_gt\\" + name + "_HB_buf.npy", HB_ppg_list)
    if save_stop_lb :
        np.save(path + "hb_gt\\" + name + "_lb_buf.npy", label_buf)




