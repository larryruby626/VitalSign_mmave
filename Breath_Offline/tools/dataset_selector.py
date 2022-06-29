import numpy as np

from larry_common_usage.RawData_process.ECG2HBbuf import ecg2hb_process,ppg2hb_process
from larry_common_usage.RawData_process.RawData2Rangefft import build_fft_buffer_data


class cfg:
    """
    w_l: window length
    f_p: fft point
    """
    w_l = 300
    f_p = 128
    shift_len = 1


class AICAdjustDataset:
    def __init__(self):
        self.path = "D:/kkt_dataset/AIC_Adjust_dataset/"
        self.TIA = ["7", "9", "11"]
        self.HP = ["1", "2"]
        self.time = ["1", "2", "3"]
        self.cfg = cfg()

    def load_singe_processed_data(self, tia_n=0, hp_n=0, time_n=0):
        tmpname = "40cm_TIA" + self.TIA[tia_n] + "_HP" + self.HP[hp_n] + "_time" + self.time[time_n]
        frame_buf = np.load(self.path + "range_fft_buf\\" + tmpname + "_rangefft.npy", allow_pickle=True)
        HB_GT = np.load(self.path + "hb_gt\\" + tmpname + "_HB_buf.npy", allow_pickle=True)
        return frame_buf, HB_GT

    def load_singe_raw_data(self, tia_n=0, hp_n=0, time_n=0):
        tmpname = "40cm_TIA" + self.TIA[tia_n] + "_HP" + self.HP[hp_n] + "_time" + self.time[time_n]
        frame_buf = np.load(self.path + "range_fft_buf\\" + tmpname + "_rangefft.npy", allow_pickle=True)
        HB_GT = np.load(self.path + "hb_gt\\" + tmpname + "_HB_buf.npy", allow_pickle=True)
        return frame_buf, HB_GT

    def loop_data(self):

        for tia in self.TIA:
            for hp in self.HP:
                for t in self.time:
                    tmpname = "40cm_TIA" + tia + "_HP" + hp + "_time" + t
                    ecg_raw = np.load(self.path + tmpname + "_ppg_v.npy", allow_pickle=True)
                    ppg2hb_process(name=tmpname,
                                   path=self.path,
                                   ecg_raw=ecg_raw,
                                   cfg=self.cfg)
                    # build_fft_buffer_data(self.path, tmpname)


class SICAdjustDataset:
    def __init__(self):

        self.path = "D:\\kkt_dataset\\SIC_Adjust_dataset\\"
        self.data_type = ["sic64", "sic255", "sicF"]
        self.range = ["20", "40", "60"]
        self.time = ["time1", "time2", "time3", "stop"]
        self.cfg = cfg()

    def load_singe_processed_data(self, datatype_n=0, range_n=0, t_n=0):
        path = self.path + self.data_type[datatype_n] + "/"
        tmpname = self.data_type[datatype_n] + "_" + self.range[range_n] + "cm_" + self.time[t_n]
        frame_buf = np.load(path + "range_fft_buf\\" + tmpname + "_rangefft.npy", allow_pickle=True)
        HB_GT = np.load(path + "hb_gt\\" + tmpname + "_HB_buf.npy", allow_pickle=True)
        return frame_buf, HB_GT

    def load_singe_raw_data(self, datatype_n=0, range_n=0, t_n=0):
        self.path = self.path + self.data_type[datatype_n] + "/"
        tmpname = self.data_type[datatype_n] + "_" + self.range[range_n] + "cm_" + self.time[t_n]
        frame_buf = np.load(self.path + "range_fft_buf\\" + tmpname + "_rangefft.npy", allow_pickle=True)
        HB_GT = np.load(self.path + "hb_gt\\" + tmpname + "_HB_buf.npy", allow_pickle=True)
        return frame_buf, HB_GT

    def loop_data(self):

        for d_t in self.data_type:
            path = self.path + d_t + "\\"
            print(path)
            for r in self.range:
                for t in self.time:
                    tmpname = d_t + "_" + r + "cm_" + t
                    print("process ------- {} ------".format(tmpname))
                    #----- combine the time and value to one data file
                    # ecg_raw = np.load(path + tmpname + "_ppg_v.npy", allow_pickle=True)
                    # ecg_t  = np.load(path + tmpname + "_ppg_t.npy", allow_pickle=True)
                    # lb = np.zeros(len(ecg_raw))
                    # dic = {"value":ecg_raw,"time":ecg_t,"state_label":lb}
                    # np.save(path+tmpname+"_ppg_combine.npy",dic)
                    ecg_raw = np.load(path + tmpname + "_ppg_combine.npy", allow_pickle=True)
                    # build_fft_buffer_data(path, tmpname)
                    ppg2hb_process(name=tmpname,
                                   path=path,
                                   ecg_raw=ecg_raw,
                                   cfg=self.cfg)


class SeatDataset:
    def __init__(self):
        self.path = "D:/kkt_dataset/seat_dataset/"
        self.range = ["50", "100", "150", "200"]
        self.person = ["1", "2", "3"]
        self.cfg = cfg()

    def load_singe_processed_data(self, person_n=0, range_n=0):
        tmpname = "p" + self.person[person_n] + "_" + self.range[range_n] + "cm"
        frame_buf = np.load(self.path + "range_fft_buf\\" + tmpname + "_rangefft.npy", allow_pickle=True)
        HB_GT = np.load(self.path + "hb_gt\\" + tmpname + "_HB_buf.npy", allow_pickle=True)
        return frame_buf, HB_GT

    def load_singe_raw_data(self, person_n=0, range_n=0):
        tmpname = "p" + self.person[person_n] + "_" + range_n + "cm"
        frame_buf = np.load(self.path + "raw_data\\" + tmpname + ".npy", allow_pickle=True)
        HB_GT = np.load(self.path + "raw_data\\" + tmpname + "_ecg_dict.npy", allow_pickle=True)
        return frame_buf, HB_GT

    def loop_data(self):

        for person in self.person:
            for range_n in self.range:
                tmpname = "p" + person + "_" + range_n + "cm"
                ecg_raw = np.load(self.path + tmpname + "_ecg_dict.npy", allow_pickle=True)
                ecg2hb_process(name=tmpname,
                               path=self.path,
                               ecg_raw=ecg_raw,
                               cfg=self.cfg)
                build_fft_buffer_data(self.path, tmpname)


class LiesDataset:
    """
    This dataset is using for compare the different combine of breathing type in a lie pose
    which is the stable's condition
    """

    def __init__(self):
        self.path = "D:/kkt_dataset/lie_dataset/"
        self.breath_type = ["slow_light", "slow_heavy", "fast_light", "stop"]
        self.time = ["1", "2", "3"]
        self.cfg = cfg()

    def load_singe_processed_data(self, breath_type_n=0, time_n=0):
        tmpname = "lie_"+self.breath_type[breath_type_n]+"_p1_t"+ self.time[time_n]
        frame_buf = np.load(self.path + "range_fft_buf\\" + tmpname + "_rangefft.npy", allow_pickle=True)
        HB_GT = np.load(self.path + "hb_gt\\" + tmpname + "_HB_buf.npy", allow_pickle=True)
        return frame_buf, HB_GT

    def load_singe_raw_data(self, breath_type_n=0, time_n=0):
        tmpname = "lie_"+self.breath_type[breath_type_n]+"_p1_t"+ self.time[time_n]

        frame_buf = np.load(self.path + "raw_data\\" + tmpname + ".npy", allow_pickle=True)
        HB_GT = np.load(self.path + "raw_data\\" + tmpname + "_ecg_dict.npy", allow_pickle=True)
        return frame_buf, HB_GT

    def loop_data(self):

        for person in self.person:
            for range_n in self.range:
                tmpname = "p" + person + "_" + range_n + "cm"
                ecg_raw = np.load(self.path + tmpname + "_ecg_dict.npy", allow_pickle=True)
                ecg2hb_process(name=tmpname,
                               path=self.path,
                               ecg_raw=ecg_raw,
                               cfg=self.cfg)
                build_fft_buffer_data(self.path, tmpname)


if __name__ == "__main__":
    x = SICAdjustDataset()
    x.loop_data()

