"""Compare the stored eastward_gradient against centered differences of
various scales computed from SST_In and from regridded_sst.

The metric is the Pearson correlation and RMSE between the stored
gradient and the candidate gradient over pixels where BOTH are valid.

Approximation: at nadir lat ~20 N descending, across-track in this
swath is nearly east-west and along-track is nearly north-south, so
the swath x-axis (j) is approximately the eastward direction. We
use this to compare directly to eastward_gradient.

Pixel spacing dx: at the swath center, the MODIS pixel spacing is
~1 km; we use dx=1 km here. For each j-step we will also compute the
true ground distance from latitude/longitude to verify.
"""
import numpy as np, pickle

block = pickle.load(open("/tmp/grad_block2.pkl","rb"))
sst_in = block["SST_In"]
sst_re = block["regridded_sst"]
e_grad = block["eastward_gradient"]
n_grad = block["northward_gradient"]
lat    = block["latitude"]
lon    = block["longitude"]

# Compute actual across-track distance per pixel using haversine on (lat, lon).
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1 = np.radians(lat1); p2 = np.radians(lat2)
    dp = np.radians(lat2-lat1); dl = np.radians(lon2-lon1)
    a = np.sin(dp/2)**2 + np.cos(p1)*np.cos(p2)*np.sin(dl/2)**2
    return 2*R*np.arcsin(np.sqrt(a))

# Pixel spacing across-track (j) and along-track (i) at every interior pixel
dx = haversine_km(lat[:, 1:-1], lon[:, 1:-1], lat[:, 2:], lon[:, 2:])
dy = haversine_km(lat[1:-1, :], lon[1:-1, :], lat[2:, :], lon[2:, :])
print(f"Pixel spacing (km):")
print(f"  across-track (dx): median={np.nanmedian(dx):.3f}, "
      f"5%={np.nanpercentile(dx,5):.3f}, 95%={np.nanpercentile(dx,95):.3f}")
print(f"  along-track  (dy): median={np.nanmedian(dy):.3f}, "
      f"5%={np.nanpercentile(dy,5):.3f}, 95%={np.nanpercentile(dy,95):.3f}")

# Restrict comparison to the central j-range where pixels are near 1km
j_lo, j_hi = 400, 1000
def grad_centered_x(arr, h, dxs):
    """Centered finite difference at scale h pixels in j direction."""
    # arr: (ny, nx); returns (ny, nx-2h) sliced; align with j indices [h..nx-h-1]
    g = (arr[:, 2*h:] - arr[:, :-2*h])
    # spacing between j and j+2h is sum of consecutive dx's
    # dx defined for j=1..nx-2 (positions 1..nx-2 in original)
    # we want the distance between pixel j_left and j_right
    # distance = dx at j_left + dx at j_left+1 + ... + dx at j_right-1
    # for a window of 2h, that's h*median dx approximately
    # Simpler: just use median dx times 2h
    return g / (2 * h * np.nanmedian(dxs))

def grad_centered_y(arr, h, dys):
    g = (arr[2*h:, :] - arr[:-2*h, :])
    return g / (2 * h * np.nanmedian(dys))

def stats(stored, candidate, mask):
    a = stored[mask]; b = candidate[mask]
    keep = np.isfinite(a) & np.isfinite(b)
    if keep.sum() < 100:
        return None
    a = a[keep]; b = b[keep]
    r = np.corrcoef(a, b)[0,1]
    rms = float(np.sqrt(np.mean((a-b)**2)))
    bias = float(np.mean(b-a))
    return r, rms, bias, int(keep.sum())

print()
print("="*80)
print("EASTWARD GRADIENT: stored vs centered-diff of input at scale 2h km")
print("(2h is the distance between sampled pixels, i.e. the operator support)")
print("="*80)
for src_name in ("SST_In","regridded_sst"):
    src = block[src_name]
    print(f"\n  source = {src_name}")
    for h in (1, 2, 3, 4, 5, 7, 10):
        gx = grad_centered_x(src, h, dx)  # shape (ny, nx-2h)
        # Align with original j window: gx[:,k] corresponds to j = k + h
        # We compare in the central j window [j_lo..j_hi]
        stored = e_grad[:, j_lo:j_hi]
        cand   = gx[:, j_lo - h : j_hi - h]
        mask = np.isfinite(stored) & np.isfinite(cand)
        s = stats(stored, cand, mask)
        if s is None:
            print(f"    h={h:2d} (operator support {2*h:3d} km)   too few overlapping valid pixels")
            continue
        r, rms, bias, n = s
        print(f"    h={h:2d} (support {2*h:3d} km)   r={r:+.3f}  RMSE={rms:.5f}  "
              f"bias={bias:+.5f}  n={n}")

print()
print("="*80)
print("NORTHWARD GRADIENT: stored vs centered-diff in along-track direction")
print("="*80)
for src_name in ("SST_In","regridded_sst"):
    src = block[src_name]
    print(f"\n  source = {src_name}")
    for h in (1, 2, 3, 5, 7, 10):
        gy = grad_centered_y(src, h, dy)
        stored = n_grad[h:-h, j_lo:j_hi]
        cand   = gy[:, j_lo:j_hi]
        mask = np.isfinite(stored) & np.isfinite(cand)
        s = stats(stored, cand, mask)
        if s is None:
            print(f"    h={h:2d} (support {2*h:3d} km)   too few overlapping valid pixels")
            continue
        r, rms, bias, n = s
        print(f"    h={h:2d} (support {2*h:3d} km)   r={r:+.3f}  RMSE={rms:.5f}  "
              f"bias={bias:+.5f}  n={n}")
