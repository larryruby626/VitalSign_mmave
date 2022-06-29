import numpy as np

def return_file_name(range, time, type):
    if type == 1:
        file_name = str(range) + str(time + 1)
    elif type == 2:
        file_name = "dongle_" + str(range) + "cm_time" + str(time + 1)
    elif type == 3:
        file_name = "PoB_" + str(range) + "cm_time" + str(time + 1)

    return file_name

def get_var(data):
    var_v = np.var(data)
    var_total = var_v ** 0.5
    return var_total

if __name__ == "__main__":
    path = "D:\\kkt_dataset\\SIC_phase_noise_110_11_22\\"
    dataset_type = ["case3", "dongle", "PoB"]
    data_set = dataset_type[0]
    save_path = path
    sure_save = True

    if data_set == 'case3':
        range_arr = ["seat_stable", "seat_type", "walk_out"]
        file_numb = 1
    elif data_set == 'dongle':
        range_arr = ["20", "40", "60"]
        file_numb = 2
    elif data_set == 'PoB':
        range_arr = ["20", "40", "60"]
        file_numb = 3


    ch1 = []
    ch3 = []
    for r_a in range_arr:

        for f_t in range(5):
            tmpfile_name = return_file_name(r_a, f_t, file_numb)

            tmp_ch1_phase =np.load(path + data_set + "\\phase_buffer\\P_ch1_" + tmpfile_name + ".npy",allow_pickle=True)
            tmp_ch3_phase= np.load(path + data_set + "\\phase_buffer\\P_ch3_" + tmpfile_name + ".npy",allow_pickle=True)
            var_ch1 = get_var(tmp_ch1_phase)
            var_ch3 = get_var(tmp_ch3_phase)
            # print("file {} ch1_var:{}, ch3_var:{}".format(tmpfile_name,var_ch1,var_ch3))
            ch1.append(var_ch1)
            ch3.append(var_ch3)
    if data_set == "case3":

        ch1_dic=  {"seat_stable":ch1[0:5],"seat_type":ch1[5:10],"walk_out":ch1[10:]}
        ch3_dic=  {"seat_stable":ch3[0:5],"seat_type":ch3[5:10],"walk_out":ch3[10:]}
    else:
        ch1_dic=  {"20":ch1[0:5],"40":ch1[5:10],"60":ch1[10:]}
        ch3_dic=  {"20":ch3[0:5],"40":ch3[5:10],"60":ch3[10:]}
    if sure_save:

        np.save(".\\phase_noise_dic\\"+data_set+"_ch1_dic.npy",ch1_dic)
        np.save(".\\phase_noise_dic\\"+data_set+"_ch3_dic.npy",ch3_dic)




