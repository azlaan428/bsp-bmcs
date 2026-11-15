import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy.signal import butter, sosfiltfilt, medfilt

d = np.load("data/clean/b001_500hz.npz")
fs = int(d["fs"])
ecg = d["I"]

def butter_bp(x, lo=0.5, hi=40, order=4):
    sos = butter(order, [lo, hi], btype="band", fs=fs, output="sos")
    return sosfiltfilt(sos, x)

def median_baseline(x):
    base = medfilt(x, 101)     # 0.2 s window
    base = medfilt(base, 301)  # 0.6 s window
    return x - base

def wavelet_denoise(x, wavelet="sym8", level=9):
    coeffs = pywt.wavedec(x, wavelet, level=level)
    coeffs[0] = np.zeros_like(coeffs[0])  # drop baseline below about 0.5 Hz
    sigma = np.median(np.abs(coeffs[-1])) / 0.6745
    thr = sigma * np.sqrt(2 * np.log(len(x)))
    coeffs[1:] = [pywt.threshold(c, thr, mode="soft") for c in coeffs[1:]]
    return pywt.waverec(coeffs, wavelet)[: len(x)]

if __name__ == "__main__":
    y1 = butter_bp(ecg)
    y2 = median_baseline(ecg)
    y3 = wavelet_denoise(ecg)
    t = np.arange(len(ecg)) / fs
    s = slice(0, 10 * fs)
    plt.plot(t[s], y1[s], label="butterworth")
    plt.plot(t[s], y2[s], label="median baseline")
    plt.plot(t[s], y3[s], label="wavelet")
    plt.xlabel("seconds")
    plt.legend()
    plt.show()