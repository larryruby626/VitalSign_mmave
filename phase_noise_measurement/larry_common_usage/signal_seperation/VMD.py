#%% Simple example: generate signal with 3 components + noise
import numpy as np
import matplotlib.pyplot as plt
from vmdpy import VMD
from scipy.signal import find_peaks

def VMD_process(f):
    alpha = 3000       # moderate bandwidth constraint
    tau = 0.            # noise-tolerance (no strict fidelity enforcement)
    K = 6            # 3 modes
    DC = 0             # no DC part imposed
    init = 1           # initialize omegas uniformly
    tol = 1e-7
    u, u_hat, omega = VMD(f, alpha, tau, K, DC, init, tol)
    # fftspectral = np.fft.fft(u[2].T, n=1024)
    # fftspectral = np.abs(fftspectral[:512])
    # fftsepctral = fftspectral[:512]
    return u[2].T


if __name__ == "__main__":

    # f = np.load("D:\\pythonProject\\larry_test\\CWT_Data\\on_32_64_0_20_HR.npy", allow_pickle=True)
    # f = np.load("D:\\pythonProject\\larry_test\\CWT_Data\\phase_HB_data_4.npy", allow_pickle=True)
    # f = np.load("D:\\pythonProject\\larry_test\\CWT_Data\\maxpeak_1_ch1.npy", allow_pickle=True)
    f = np.load("G:\\我的雲端硬碟\\開酷\\FoV_experiment\\dataset1101109\\Phase_Buff\\Automatic_peak\\sic255\\HR_20cm_time1.npy", allow_pickle=True)

    # f = f[200:300]
    #. some sample parameters for VMD
    alpha = 3000       # moderate bandwidth constraint
    tau = 0.1           # noise-tolerance (no strict fidelity enforcement)
    K = 5
    DC = 0             # no DC part imposed
    init = 1           # initialize omegas uniformly
    tol = 1e-7


    #. Run VMD
    u, u_hat, omega = VMD(f, alpha, tau, K, DC, init, tol)


    out_len = u.shape[0]

    #. Visualize decomposed modes
    plt.figure()
    plt.subplot(out_len+1,1,1)
    plt.plot(f)
    plt.title('Original signal')
    plt.xlabel('time (s)')

    for i in range(out_len):
        plt.subplot(out_len+1, 1, i+2)
        plt.plot(u[i].T)
        plt.title('Decomposed modes')
        plt.xlabel('time (s)')

    plt.legend(['Mode %d'%m_i for m_i in range(u.shape[0])])
    # plt.tight_layout()
    plt.figure()

    for i in range(out_len):
        plt.subplot(out_len, 1, i+1)
        fftspectral = np.fft.fft(u[i].T, n=1024)
        fftspectral = np.abs(fftspectral[:512])

        # fftspectral = fftspectral[:512]*np.conjugate(fftspectral[:512])
        # fftspectral = 10*np.log10(fftspectral)

        peak = find_peaks(fftspectral)
        maxidx = np.argmax(fftspectral)
        print(maxidx*60/51.2)

        plt.scatter(peak[0], fftspectral[peak[0]],c='r')

        plt.plot(fftspectral)
        # plt.xlim([0,200])
        plt.title('Decomposed FFT')
        plt.xlabel('time (s)')
    # plt.tight_layout()
    plt.pause(10000)

