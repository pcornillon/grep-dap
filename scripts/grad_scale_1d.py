"""1-D analysis: pick rows where stored eastward_gradient has a strong
peak, look at how wide the gradient peak is.

A delta-function input would give a peak whose width is the operator
support. For a centered-diff at scale h, the peak width is 2h.
"""
import numpy as np, pickle
block = pickle.load(open("/tmp/grad_block2.pkl","rb"))
sst_in = block["SST_In"]
sst_re = block["regridded_sst"]
eg = block["eastward_gradient"]
ng = block["northward_gradient"]
mag = np.hypot(eg, ng)

# Find rows with the strongest single-pixel gradient (likely a front)
peak_per_row = np.nanmax(mag[:, 200:1150], axis=1)
top = np.argsort(peak_per_row)[::-1][:6]
print("Top 6 rows by peak |gradient|:")
for i in top:
    j_peak = 200 + np.nanargmax(mag[i, 200:1150])
    print(f"  i={i:3d}  j_peak={j_peak:4d}  |g|={mag[i,j_peak]:.3f}  "
          f"SST_In neighborhood = {sst_in[i, max(0,j_peak-5):j_peak+6]}")

# For the top row, plot a 50-pixel window of SST_In, regridded_sst, and gradients
i_pick = int(top[0])
j_peak = 200 + int(np.nanargmax(mag[i_pick, 200:1150]))
print(f"\nDeep-dive: row i={i_pick}, peak at j={j_peak}")
j_lo, j_hi = max(0, j_peak-30), min(1354, j_peak+30)
print(f"  window j=[{j_lo},{j_hi}]")
print(f"  {'j':>4s} {'SST_In':>10s} {'reg_sst':>10s} {'e_grad':>10s} {'n_grad':>10s} {'|g|':>10s}")
for j in range(j_lo, j_hi):
    print(f"  {j:4d} {sst_in[i_pick,j]:10.4f} {sst_re[i_pick,j]:10.4f} "
          f"{eg[i_pick,j]:10.4f} {ng[i_pick,j]:10.4f} {mag[i_pick,j]:10.4f}")

# Compute centered diffs at h=1,2,3,5 of regridded_sst on this row
print()
print("My centered-diff candidates (cell pixel spacing ~1.35 km across-track):")
dx_med = 1.35
for h in (1,2,3,5,7):
    row = sst_re[i_pick]
    grad_h = (row[2*h:] - row[:-2*h]) / (2*h*dx_med)
    j_center = j_peak  # check stored vs my grad at and near the peak
    if j_center - h < 0 or j_center + h >= len(row): continue
    my_g = grad_h[j_center - h]
    stored_g = eg[i_pick, j_center]
    print(f"  h={h:2d}, op_support={2*h:2d}km   my_grad@peak={my_g:+.4f}, "
          f"stored@peak={stored_g:+.4f}")

# Average gradient peak width: count how many adjacent j have |g| > 0.5 * peak
print()
print("Peak width analysis (how broad is the stored gradient peak?):")
for k, i in enumerate(top[:5]):
    if not np.isfinite(mag[i]).any(): continue
    j_peak = 200 + np.nanargmax(mag[i, 200:1150])
    peak = mag[i, j_peak]
    # walk left from j_peak until |g| < peak/2
    left = j_peak
    while left > 0 and np.isfinite(mag[i,left-1]) and mag[i,left-1] >= peak*0.5:
        left -= 1
    right = j_peak
    while right < 1353 and np.isfinite(mag[i,right+1]) and mag[i,right+1] >= peak*0.5:
        right += 1
    half_width_pixels = right - left
    half_width_km = half_width_pixels * dx_med
    print(f"  row i={i:3d}  peak={peak:.3f}  HWHM_pixels={half_width_pixels}  "
          f"HWHM_km={half_width_km:.1f}")
