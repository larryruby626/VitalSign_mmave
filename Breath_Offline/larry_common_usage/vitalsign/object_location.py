import numpy as np
import matplotlib.pyplot as plt
from larry_common_usage.DSP.delay_filter import delay_filter_src

def range_diff_counter(range_diff_buffer,threshold = 5):
    count = 0
    for v in range_diff_buffer:
        if v > threshold:
            count += 1
    return True if count>5 else False

def Oject_detect(max_value,psd_thr=5000,buf_cfg=None):
    counter = buf_cfg.fft_buf_c
    if buf_cfg is not None:
        # print(max_value,psd_thr)
        if max_value < psd_thr:
            counter +=1
        else:
            counter = 0

        if counter>10:
            buf_cfg.obj_state = "Empty"
        else:
            buf_cfg.obj_state = "Objected"


    buf_cfg.fft_buf_c = counter
    return buf_cfg


def Oject_Location(frame_buf, show_searchbin_plot=False, buf_cfg=None):

    FFT_std_buf = buf_cfg.std_buffer
    range_buf = buf_cfg.range_buffer
    range_buf_diff = buf_cfg.range_dif_buffer
    Last_frame = buf_cfg.delay_fiter_last
    motion_state = True
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
        tmp_idx = np.argmax(tmp_range)
        tmp_idx_v = np.max(tmp_range)
        buf_cfg = Oject_detect(tmp_idx_v,buf_cfg=buf_cfg)
        if len(range_buf) == 0 :
            range_buf.append(tmp_idx)
        elif len(range_buf) >=1 and len(range_buf)<=10:
            range_buf.append(tmp_idx)
            range_buf_diff.append(abs(tmp_idx - range_buf[-2]))
        else:
            range_buf.append(tmp_idx)
            range_buf_diff = range_buf_diff[1:]
            range_buf = range_buf[1:]
            range_buf_diff.append(abs(tmp_idx - range_buf[-2]))
            # raw_fft = abs(np.average(FFT_std_buf, axis=0))
            # raw_fft,Last_frame = delay_filter_src(raw_fft,Last_frame,0.5)



    buf_cfg.delay_fiter_last = Last_frame
    buf_cfg.std_buffer = FFT_std_buf
    buf_cfg.range_buffer = range_buf
    buf_cfg.range_dif_buffer = range_buf_diff
    if  tmp_range is not None:
        return tmp_range , np.sum(FFT_std_buf, axis=0)
    else:
        return  0 , np.sum(FFT_std_buf, axis=0)