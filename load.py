import os
import numpy as np
import wfdb
from scipy.signal import decimate

def load(name, fs_out=500):
    r = wfdb.rdrecord(f"data/raw/{name}")
    q = int(r.fs // fs_out)
    y = decimate(r.p_signal, q, axis=0, zero_phase=True)
    return dict(zip(r.sig_name, y.T)), fs_out

if __name__ == "__main__":
    os.makedirs("data/clean", exist_ok=True)
    for n in ["b001", "b002", "b003"]:
        sig, fs = load(n)
        np.savez(f"data/clean/{n}_500hz.npz", fs=fs, **sig)
        print(n, round(len(sig["I"]) / fs), "seconds at", fs, "Hz")