import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import interpolate

def save_obj(obj, name ):
    with open('./out_result/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('./out_result/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def plot_all_figure_interplolate(input_fov_data):
    methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
               'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
               'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']
    fig, axs = plt.subplots(nrows=3, ncols=6, figsize=(9, 6),
                            subplot_kw={'xticks': [], 'yticks': []})
    for ax, interp_method in zip(axs.flat, methods):
        ax.imshow(input_fov_data, interpolation=interp_method, cmap=cm.jet)
        ax.set_title(str(interp_method))
    title = "method:", method, "channel:", channel
    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

def plot_Fov_single(input_fov_data, title):
    plt.figure()
    plt.imshow(input_fov_data, interpolation="bilinear", cmap=cm.jet)
    plt.title(str(title))
    plt.show()

def plot_Fov(input_fov_data, subplot_cc, plot_row_len ,plot_col_len ,row ,col , title):
    methods = ['bilinear']
    if subplot_cc == 0:
        fig, axs = plt.subplots(nrows=plot_row_len, ncols=plot_col_len, figsize=(9, 6),
                                subplot_kw={'xticks': [], 'yticks': []})

    ax = (row,col,subplot_cc)
    ax.imshow(input_fov_data, interpolation=methods, cmap=cm.jet)
    ax.set_title(str(title))
    plt.show()
    subplot_cc +=1
    return subplot_cc

#  ---- for chest data usage ----
angle_list = ["-60", "-50", "-40", "-30", "-20", "-10", "0", "+10", "+20", "+30", "+40", "+50", "+60"]
range_list = ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"]
subplot_cc = 0

for method in range(1,3):
    for channel in range(1,3):
        r = 0
        tmp_time1 = np.zeros([11, 13])
        snr_dic = load_obj("SNR_chest_DIC_ch"+str(channel))
        for rangeX in range_list:
            a = 0
            for angle in angle_list:

                name = "m" + str(method) + "_r" + rangeX + "_a" + angle + "_t" + str(1)
                tmp_time1[r,a] = snr_dic[name]
                a += 1
            r +=1
        if method == 1:
            title = "method: " + "spline" + ", channel:" + str(channel)
        elif method == 2:
            title = "method: " + "quadratic" + ", channel:" + str(channel)
        plot_Fov_single(tmp_time1, title)
        # plot_all_figure_interplolate(tmp_time1)
        # subplot_cc = plot_Fov(tmp_time1, subplot_cc, plot_row_len=2, plot_col_len=2, row=channel, col=method, title=name)