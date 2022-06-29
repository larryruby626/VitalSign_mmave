import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt

def mse(y_true,y_pred):
    rms = mean_squared_error(y_true, y_pred)
    return rms

def rmse(y_true,y_pred):
    rms = sqrt(mean_squared_error(y_true, y_pred))
    return rms

def mape(y_true, y_pred):
    '''
    引數:
    y_true -- 測試集目標真實值
    y_pred -- 測試集目標預測值
    返回:
    mape -- MAPE 評價指標
    '''
    return np.round(np.mean(np.abs((y_true - y_pred) / y_true)) * 100,2)