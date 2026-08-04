"""Autocorrelation of the stored gradient field as a function of lag.

For a gradient computed with operator support L, the gradient field
is correlated over scales <= L (because adjacent pixel pairs share
input pixels). The decorrelation length is therefore approximately
the operator support.
"""
import numpy as np, pickle
block = pickle.load(open("/tmp/grad_block2.pkl","rb"))
eg = block["eastward_gradient"]
ng = block["northward_gradient"]
mag = np.hypot(eg, ng)

# Restrict to central swath where pixels are near 1 km
J_LO, J_HI = 400, 1000
mag_c = mag[:, J_LO:J_HI].copy()

# Replace NaN with the mean of the field, just for autocorr; mask later
v = mag_c.copy()
mean_v = np.nanmean(v)
v_filled = np.where(np.isfinite(v), v - mean_v, 0)

# 1-D autocorrelation along across-track (j) axis: average over rows
def autocorr_1d(arr, axis, max_lag):
    """arr: 2-D filled, mean-removed. Returns lag-correlation along axis."""
    n = arr.shape[axis]
    out = []
    var = float(np.nanvar(arr.flatten()))  # global variance
    if axis == 0:
        for L in range(0, max_lag+1):
            if L == 0:
                num = np.nansum(arr * arr)
                cnt = arr.size
            else:
                num = np.nansum(arr[:-L,:] * arr[L:,:])
                cnt = arr[:-L,:].size
            out.append(num / cnt / var)
    else:
        for L in range(0, max_lag+1):
            if L == 0:
                num = np.nansum(arr * arr); cnt = arr.size
            else:
                num = np.nansum(arr[:,:-L] * arr[:,L:])
                cnt = arr[:,:-L].size
            out.append(num / cnt / var)
    return out

# Approx pixel spacing in km
dx = 1.35  # across-track
dy = 1.13  # along-track

print("Autocorrelation of |gradient| along across-track direction (lag pixels):")
ac_x = autocorr_1d(v_filled, axis=1, max_lag=20)
for L,a in enumerate(ac_x):
    print(f"  lag={L:2d}   distance={L*dx:5.2f} km   AC={a:+.3f}")

print("\nAutocorrelation along along-track direction (lag pixels):")
ac_y = autocorr_1d(v_filled, axis=0, max_lag=20)
for L,a in enumerate(ac_y):
    print(f"  lag={L:2d}   distance={L*dy:5.2f} km   AC={a:+.3f}")

# Same analysis on raw SST_In gradient (1-pixel centered diff) for reference
sst_in = block["SST_In"]
gx_raw = (sst_in[:,2:] - sst_in[:,:-2])/(2*dx)
ggi = np.where(np.isfinite(gx_raw), gx_raw - np.nanmean(gx_raw), 0)
print("\nFor reference: autocorrelation of 1-pixel-diff SST_In x-gradient:")
ac_raw = autocorr_1d(ggi, axis=1, max_lag=12)
for L,a in enumerate(ac_raw):
    print(f"  lag={L:2d}   distance={L*dx:5.2f} km   AC={a:+.3f}")
