import numpy as np


def delay_filter_src(X, pre_Y, a_weight):
    """
    :param X: new frame input
    :param pre_Y: last src_weight
    :param a_weight: the weight to mulitply pre_y
    :return: 1). after src process data
             2). the current src_weight to feed next frame
    """
    #
    # axis = 0
    # reordering = np.arange(len(X.shape))
    # reordering[0] = axis
    # reordering[axis] = 0
    # tmp_mean = X.transpose(reordering).mean(0)
    #
    # Y = (1 - a_weight) * tmp_mean + a_weight * pre_Y
    #
    # output_val = X - Y
    #
    # return output_val.transpose(reordering), Y

    Y = (1 - a_weight) * X + a_weight * pre_Y
    output_val = X - Y
    return output_val, Y