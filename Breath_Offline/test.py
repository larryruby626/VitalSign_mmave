import numpy as np




class test():
    def __init__(self):
        self.widget_cfg = {
            "vitalsign_mode": "",
            "current_wiget": "",
            "Mode": "single",
            "single_file_path": "",
            "save_result_path": "",
            "save_type": [False, False, False],
            "multi_dataset": [False, False, False, False],
            "pw_targetidx": [True, False],
            "pw_phaseprocess": [],
            "pw_HBCalc": [],
            "vital_sign_window_len": 256,
            "vital_sign_shfit_len": 10

        }
        self.search_bin = {'0': "searchbin_",
                       '1': "maxpower_"}

        print(self.search_bin[str(np.where(self.widget_cfg["pw_targetidx"])[0][0])])

import matplotlib.pyplot as plt



xxx = np.load("C:\\Users\\user\\Downloads\\40cm_TIA7_HP1_time2_searchbin_normal_STFT.npy",allow_pickle=True)
dic = dict(enumerate(xxx.flatten()))[0]

cur_hb_list = dic["radar"]
ds_hb_gt = dic["gt"]
font = {'family': 'sans-serif',
        'color':  'Black',
        'weight': 'normal',
        'size': 16,
        }
p1, = plt.plot(cur_hb_list)
p2, = plt.plot(ds_hb_gt)
plt.ylim([50,120])
plt.legend([p1, p2], ["Radar estiate", "Ground truth"])
plt.text(2, 110, "RMSE : {}".format(np.round(dic["rmse"],2)), fontdict=font)
plt.text(2, 105, "MAPE : {} %".format(np.round(dic["mape"],2)), fontdict=font)
# plt.title()
plt.ylabel("BPM")
plt.savefig("C:\\Users\\user\\Downloads\\fig.jpg")
