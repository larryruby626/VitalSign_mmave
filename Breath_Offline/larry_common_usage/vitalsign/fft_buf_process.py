import numpy as np


def fft_buf_process(fft_buf, tmp_fft, cfg):
    window_len = cfg.w_l
    # fft_buf = np.array(fft_buf)
    # tmp_fft = np.array(tmp_fft)
    if fft_buf.shape[0] == 0:

        fft_buf = np.expand_dims(tmp_fft, axis=0)

    elif fft_buf.shape[0] < window_len:
        # print(fft_buf.shape,np.expand_dims(tmp_fft, axis=0).shape)
        fft_buf = np.vstack((fft_buf,np.expand_dims(tmp_fft, axis=0)))
    else:
        cfg.buf_state = True
        fft_buf = fft_buf[1:, :]
        fft_buf = np.vstack((fft_buf, np.expand_dims(tmp_fft, axis=0)))
    return fft_buf, cfg