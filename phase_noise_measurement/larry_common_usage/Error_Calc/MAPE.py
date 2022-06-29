import numpy as np
def mape(y_true, y_pred):
    '''
    引數:
    y_true -- 測試集目標真實值
    y_pred -- 測試集目標預測值
    返回:
    mape -- MAPE 評價指標
    '''
    return np.round(np.mean(np.abs((y_true - y_pred) / y_true)) * 100,2)