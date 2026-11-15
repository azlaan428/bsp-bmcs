import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt, find_peaks
from ecg_filters import butter_bp

def pan_tompkins(x, fs):
    sos = butter(2, [5, 15], btype="band", fs=fs, output="sos")
    f = sosfiltfilt(sos, x)
    sq = np.gradient(f) ** 2
    w = int(0.15 * fs)
    mwi = np.convolve(sq, np.ones(w) / w, mode="same")
    height = 0.35 * np.percentile(mwi, 99.5)
    peaks, _ = find_peaks(mwi, height=height, distance=int(0.25 * fs))
    clean = butter_bp(x)
    out = []
    for p in peaks:
        lo, hi = max(0, p - int(0.1 * fs)), min(len(x), p + int(0.1 * fs))
        out.append(lo + int(np.argmax(clean[lo:hi])))
    return np.unique(out)

if __name__ == "__main__":
    d = np.load("data/clean/b001_500hz.npz")
    fs = int(d["fs"])
    ecg = d["I"]
    r = pan_tompkins(ecg, fs)
    print("beats:", len(r), " mean heart rate:", round(60 / np.mean(np.diff(r) / fs), 1), "bpm")
    clean = butter_bp(ecg)
    t = np.arange(len(ecg)) / fs
    s = slice(0, 10 * fs)
    plt.plot(t[s], clean[s])
    rr = r[r < 10 * fs]
    plt.plot(rr / fs, clean[rr], "rv")
    plt.xlabel("seconds")
    plt.show()