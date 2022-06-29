import numpy as np


def build_config():

    class buf:
        fft_buf = np.array([])
        fft_buf_c = 0
        stop_B_c = 0
        T_buffer = []
        psd_buffer = []
        std_buffer =np.zeros([1, 128])
        obj_loc_buffer = []
        range_buffer = []
        range_dif_buffer = []
        obj_state = "init"
        T_buf_shifter_num = 10
        T_buf_c = 0
        out_breath_rate_buffer = []
        delay_fiter_last = 0

    class cfg:
        """
        w_l: window length
        f_p: fft point
        """
        # w_l = 3600
        # w_l = 800
        w_l = 300
        f_p = 128
        shift_len = 1
        buf_state = False
        cur_idx = 0

    return buf, cfg
