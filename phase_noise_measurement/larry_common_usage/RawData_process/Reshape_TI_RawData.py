import numpy as np
import matplotlib.pyplot as plt


def reshape_rawdata(data):
    print(data.shape)
    data = np.reshape(data, [-1, 4])
    data = data[:, 0:2:] + 1j * data[:, 2::]
    print(data.shape)
    rawData = np.reshape(data, [-1, 32, 4, 64])
    returndata = rawData[0,:,0,:]
    return returndata


def plotdata(arr):
    plt.cla()
    # plt.xlim([0, 30])
    plt.plot(arr)
    plt.pause(0.01)


if __name__ == "__main__":
    RAWDATA = np.load("C:\\python_proj\\thmouse_training_data\\up\\time0\\raw.npy", allow_pickle=True)
    data_arr = reshape_rawdata(RAWDATA)
    phase_arr = []
    idx = 200
    for i in range((data_arr.shape[0])):
        tmp = (data_arr[i, 1, 1, :])
        tmp = tmp * np.hanning(len(tmp))
        fft = np.fft.fft(tmp, n=256)
        phase_arr.append(np.angle(fft[idx]))
        fft = fft * np.conjugate(fft)
        fft = np.real(fft)
        logfft = 10 * np.log10(fft)
        logfft = np.flip(logfft)
        # plotdata(logfft)

    unwrapped = np.unwrap(phase_arr)
    rm_dc = (unwrapped-np.mean(unwrapped))
    vare = np.var(rm_dc)

    plotdata((unwrapped-np.mean(unwrapped)))
    final = np.zeros([len(rm_dc)])
    final[:] = vare**0.5
    plt.plot(final)

