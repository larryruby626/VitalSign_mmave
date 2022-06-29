from Cleanup_version.process.config import *
from Cleanup_version.process.fft_process_byframe import *
from Cleanup_version.tools.Reshape_KKT_RawData import reshape_rawdata


# path = "D:\\kkt_dataset\\0119\\"
# name = "p2_50cm"
# raw_data = np.load(path + name + ".npy", allow_pickle=True)

def build_fft_buffer_data(path, name):

    raw_data = np.load(path+ "raw\\" + name + ".npy", allow_pickle=True)
    fftcfg, dpccfg, cfarcfg, bpfcfg, hpfcfg, larry_cfg = vitalcfg()
    for i in range(len(raw_data)):
        dataInCh1, dataInCh2 = reshape_rawdata(raw_data[i])
        sigfft1 = fft_process_byframe(dataInCh1, fftcfg, larry_cfg)

        sigfft = np.expand_dims(sigfft1, axis=1)
        # out_arr[i, :] = sigfft[:, 0]
        if i == 0:
            out_arr = np.copy(sigfft[:, 0])
        else:
            out_arr = np.vstack((out_arr, sigfft[:, 0]))

    np.save(path +"range_fft_buf\\"+ name + "_rangefft.npy", out_arr)


if __name__ == "__main__":
    # path = "D:\\kkt_dataset\\0119\\"
    # rawdata = np.load(path + "p2_stop_100cm" + ".npy", allow_pickle=True)
    # build_fft_buffer_data(path, "p2_stop_100cm", rawdata)
    # person = ["1", "2", "3"]
    # cm = ["50", "100", "150", "200"]
    # for cm_numb in cm:
    #     for p_numb in person:
            # filename = "p" + p_numb + "_" + cm_numb + "cm"
            # print("---------- {} ------------".format(filename))
            # rawdata = np.load(path + filename + ".npy", allow_pickle=True)
            # build_fft_buffer_data(path, filename, rawdata)

    # path = "D:\\kkt_dataset\\lie_dataset\\raw\\"
    path = "C:\\data_set\\lie_dataset\\"
    # B_speed = ["slow", "fast"]
    # B_amp = ["light", "heavy"]
    B_speed = ["fast"]
    B_amp = ["heavy"]
    B_person=["1"]
    for b_s in B_speed:
        for b_a in B_amp:
            for b_p in B_person:
                for time in range(4):
                    # name = "lie_"+str(b_s)+"_"+str(b_a)+"_p"+str(b_p)\
                    #        +"_t"+str(time+1)
                    name = "lie_stop_p"+str(b_p)+"_t"+str(time+1)
                    print("-----process {}-------".format(name))
                    build_fft_buffer_data(path, name)
