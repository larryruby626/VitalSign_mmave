import numpy as np
from TI_paper_method.config import build_config
from larry_common_usage.Calc_heartbeat.Ground_Turth_process import ground_turth_process
from larry_common_usage.RawData_process.RawData2Rangefft import  build_fft_buffer_data
if __name__ == "__main__":
    buf, cfg = build_config()

    # path = "C:\\Fov_test\\"
    # name = "lie"
    # ecg_raw = np.load(path + name + "_ecg_dict.npy", allow_pickle=True)
    # HB_ppg_list,label_buf = ground_turth_process(ecg_raw,cfg,"ecg")
    # np.save(path+name+"_HB_buf.npy",HB_ppg_list)

    # path = "D:\\kkt_dataset\\lie_dataset\\"
    path = "C:\\data_set\\lie_dataset\\"

    stop_breath = False
    B_speed = ["slow", "fast"]
    # B_amp = ["light", "heavy"]
    # B_speed = ["fast"]
    B_amp = ["heavy"]
    B_person=["1"]
    for b_s in B_speed:
        for b_a in B_amp:
            for b_p in B_person:
                for time in range(2):
                    name = "seat_"+str(b_s)+"_"+str(b_a)+"_p"+str(b_p)\
                           +"_t"+str(time+1)
                    if stop_breath:
                        name = "lie_stop_p"+str(b_p)+"_t"+str(time+1)   #   for stopbreath
                    print("-----process {}-------".format(name))
                    ecg_raw = np.load(path +"raw\\"+ name + "_ecg_dict.npy", allow_pickle=True)

                    HB_ppg_list,label_buf = ground_turth_process(ecg_raw,cfg,"ecg")
                    build_fft_buffer_data(path, name)

                    np.save(path+"hb_gt\\"+name+"_HB_buf.npy",HB_ppg_list)

                    if stop_breath:
                        np.save(path+"hb_gt\\"+name+"_lb_buf.npy",label_buf)

