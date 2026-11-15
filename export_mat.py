import os
import numpy as np
from scipy.io import savemat

os.makedirs("data/mat", exist_ok=True)
for n in ["b001", "b002", "b003"]:
    d = np.load(f"data/clean/{n}_500hz.npz")
    savemat(f"data/mat/{n}.mat",
            {"fs": int(d["fs"]), "I": d["I"], "II": d["II"], "RESP": d["RESP"], "SCG": d["SCG"]})
    print(n, "saved")