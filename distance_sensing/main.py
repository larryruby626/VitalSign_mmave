import numpy as np
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

def print_single(data):
    plt.figure()
    plt.plot(data)
    plt.show()

def build_config():

    class buf:
        std_buffer =np.zeros([1, 128])
        range_buffer = []
        range_dif_buffer = []
        delay_filter_buff = []
        delay_fiter_last = []

    return buf

def print_loop_update(data,data2=None):

    plt.subplot(211) if data2 is not None else plt.subplot(111)
    plt.cla()

    p1,= plt.plot(data)
    plt.legend([p1],["FFT result"])
    plt.draw()
    if data2 is not None:
        plt.subplot(212)
        p2, = plt.plot(data2,c='r')
        plt.legend([p2], ["STD-FFT Result"])
    plt.draw()
    plt.pause(0.1)
    plt.cla()

def fft_chirp2frame(dataIn, fftsize=256, data_type="kkt",chirp_num=32):
    """
    :param dataIn: raw frame data ipput
    :param fftsize: the fft size you wanna do
    :param data_type: kkt / ti
    :return
    """
    rangeFFTsize = fftsize
    ChirpStart = 0
    ChirpEnd = chirp_num-1
    sigfftall = np.array
    [Nadc, Nchirp] = np.shape(dataIn)
    first_pass = False
    sigfftall =  np.zeros([ChirpEnd-ChirpStart, int(rangeFFTsize/2)],dtype=np.complex_)

    for i in range(ChirpStart, ChirpEnd + 1):
        # sig = dataIn[i, :] * np.blackman(64)
        sig = dataIn[i, :] * np.hanning(64)
        sigfft = np.fft.fft(sig, n=fftsize)
        if i == 0:
            pass
        else:
            if not first_pass:
                if data_type == "ti":
                    sigfftall[i-1,:]  = sigfft[int(sigfft.shape[0] / 2):]  # ti

                else:
                    sigfftall[i-1,:]  = sigfft[:int(sigfft.shape[0] / 2)]  # kkt

                first_pass = True
            else:
                if data_type == "ti":
                    sigfftall[i-1,:]  = sigfft[int(sigfft.shape[0] / 2):]  # ti

                else:
                    sigfftall[i-1,:]  = sigfft[:int(sigfft.shape[0] / 2)]  # kkt
    sigfftall = np.sum(sigfftall, axis=0)

    if data_type == "ti":
        return sigfftall[::-1]
    else:
        return sigfftall[:]


def delay_filter_src(X, a_weight, buf_cfg=None):
    """
    :param X: new frame input
    :param pre_Y: last src_weight
    :param a_weight: the weight to mulitply pre_y
    :return: 1). after src process data
             2). the current src_weight to feed next frame
    """
    pre_Y = buf_cfg.delay_fiter_last
    Y = (1 - a_weight) * X + a_weight * pre_Y
    buf_cfg.delay_fiter_last = Y

    return buf_cfg


def Oject_Location(frame_buf, show_searchbin_plot=False, buf_cfg=None):

    FFT_std_buf = buf_cfg.std_buffer
    range_buf = buf_cfg.range_buffer
    range_buf_diff = buf_cfg.range_dif_buffer
    tmp_range = None

    if len(FFT_std_buf) == 1:
        FFT_std_buf = frame_buf
        FFT_std_buf = np.vstack((FFT_std_buf, np.expand_dims(frame_buf, axis=0)))
    elif len(FFT_std_buf) < 3:
        print(FFT_std_buf.shape)
        FFT_std_buf = np.vstack((FFT_std_buf, np.expand_dims(frame_buf, axis=0)))
    else:

        FFT_std_buf = FFT_std_buf[1:, :]
        FFT_std_buf = np.vstack((FFT_std_buf, np.expand_dims(frame_buf, axis=0)))
        tmp_range = np.std(FFT_std_buf, axis=0)

    buf_cfg.std_buffer = FFT_std_buf
    buf_cfg.range_buffer = range_buf
    buf_cfg.range_dif_buffer = range_buf_diff

    if  tmp_range is not None:
        return tmp_range , np.sum(FFT_std_buf, axis=0)
    else:
        return  [] , np.sum(FFT_std_buf, axis=0)


def reshape_rawdata(rawdata):
    ch1data = rawdata[:4096]
    ch2data = rawdata[4096:]
    ch1data = np.reshape(ch1data, [32, 128])
    ch2data = np.reshape(ch2data, [32, 128])
    dataInCh1 = ch1data[:, :64]  # cut the down chirp
    dataInCh2 = ch2data[:, :64]  # cut the down chirp

    return dataInCh1, dataInCh2
if __name__ == '__main__':
    """
    Description:
        Data is collecting the AIC openloop(SIC OFF),and the people
        stay seeting in the different range(50/100/150/200cm) and keep breath.
        
    oneline_rawdata=> 8192:  2(ch) * 128(ADC sample up&down) * 32(chirps)
        
    """

    raw = np.load("p2_50cm.npy",allow_pickle= True)
    # raw = np.load("p2_100cm.npy",allow_pickle= True)
    buf_cfg =build_config()
    print("raw data's shape is : {} (frame, oneline_rawdata)".format(raw.shape))

    for f_idx in range(raw.shape[1]):
         dataInCh1, dataInCh2 = reshape_rawdata(raw[f_idx,:])
         fft_Ch1= fft_chirp2frame(dataInCh1)
         fft_std, rawfft  = Oject_Location(fft_Ch1, show_searchbin_plot=True, buf_cfg=buf_cfg)
         if len(fft_std) >1 :
            print_loop_update(data=abs(rawfft), data2=abs(fft_std))

            # if len(buf_cfg.delay_fiter_last)==0:
            #     buf_cfg.delay_fiter_last

