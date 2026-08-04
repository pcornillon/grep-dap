"""Compare gradient MAGNITUDES (rotation-invariant) of stored vs
centered-diff for various operator scales. Independent of orbit
heading. Also a 1-D cross-section visualization.
"""
import numpy as np, pickle

block = pickle.load(open("/tmp/grad_block2.pkl","rb"))
sst_in = block["SST_In"]
sst_re = block["regridded_sst"]
e_grad = block["eastward_gradient"]
n_grad = block["northward_gradient"]
lat    = block["latitude"]
lon    = block["longitude"]

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1 = np.radians(lat1); p2 = np.radians(lat2)
    dp = np.radians(lat2-lat1); dl = np.radians(lon2-lon1)
    a = np.sin(dp/2)**2 + np.cos(p1)*np.cos(p2)*np.sin(dl/2)**2
    return 2*R*np.arcsin(np.sqrt(a))

dx = haversine_km(lat[:, 1:-1], lon[:, 1:-1], lat[:, 2:], lon[:, 2:])
dy = haversine_km(lat[1:-1, :], lon[1:-1, :], lat[2:, :], lon[2:, :])
print(f"Pixel spacing  dx_median={np.nanmedian(dx):.3f} km  "
      f"dy_median={np.nanmedian(dy):.3f} km")

stored_mag = np.hypot(e_grad, n_grad)

J_LO, J_HI = 400, 1000
I_LO, I_HI = 10, 190  # keep room for the largest h

def cand_mag(src, h):
    """Magnitude of centered-diff gradient computed at scale h pixels in
    both directions."""
    gxc = (src[:, 2*h:] - src[:, :-2*h]) / (2*h*np.nanmedian(dx))
    gyc = (src[2*h:, :] - src[:-2*h, :]) / (2*h*np.nanmedian(dy))
    # Align: gxc has columns 0..nx-2h-1 (representing original col h..nx-h-1)
    # gyc has rows  0..ny-2h-1 (representing original row h..ny-h-1)
    # Combine over (i_h .. ny-h-1, j_h .. nx-h-1)
    g = np.hypot(gxc[h:-h, :], gyc[:, h:-h])
    return g

print()
print("="*80)
print("GRADIENT MAGNITUDE: stored vs centered-diff (rotation-invariant)")
print("="*80)
for src_name in ("SST_In","regridded_sst"):
    src = block[src_name]
    print(f"\n  source = {src_name}")
    for h in (1, 2, 3, 4, 5, 6, 7, 8, 10):
        cm = cand_mag(src, h)
        # Stored magnitude window: skip h pixels on each side
        sm = stored_mag[h:-h, h:-h]
        # Restrict to central j range to avoid swath-edge pixel growth
        sm = sm[:, max(0,J_LO-h):min(sm.shape[1], J_HI-h)]
        cm = cm[:, max(0,J_LO-h):min(cm.shape[1], J_HI-h)]
        mask = np.isfinite(sm) & np.isfinite(cm)
        if mask.sum() < 1000:
            print(f"    h={h:2d} (support {2*h:3d} km)  too few valid")
            continue
        a = sm[mask]; b = cm[mask]
        r = np.corrcoef(a, b)[0,1]
        rms = float(np.sqrt(np.mean((a-b)**2)))
        bias = float(np.mean(b-a))
        ratio = float(np.mean(b)/np.mean(a))
        print(f"    h={h:2d}  support={2*h:3d} km   r={r:+.3f}  RMSE={rms:.4f}  "
              f"bias={bias:+.4f}  mean_ratio_cand/stored={ratio:.3f}  n={mask.sum()}")

# Also: compare mean magnitudes (no spatial registration needed)
print()
print("Spatially-averaged |gradient| comparisons:")
stored_mean = np.nanmean(stored_mag[I_LO:I_HI, J_LO:J_HI])
print(f"  stored                                   mean|g| = {stored_mean:.5f} C/km")
for src_name in ("SST_In","regridded_sst"):
    print(f"\n  source = {src_name}")
    for h in (1, 2, 3, 5, 7, 10):
        cm = cand_mag(block[src_name], h)
        m = np.nanmean(cm[I_LO-h:I_HI-h, J_LO-h:J_HI-h])
        print(f"    h={h:2d}  support={2*h:3d} km   mean|g| = {m:.5f}  "
              f"ratio_cand/stored = {m/stored_mean:.3f}")
