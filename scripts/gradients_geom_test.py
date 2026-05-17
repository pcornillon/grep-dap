"""Determine the lat/lon orientation of gradients_by_period grids.

Strategy:
1. Read day_pixel_count and day_sum_SST from a representative month.
2. Compute per-cell mean SST where pixel_count > 0.
3. Locate the centroid of the cells with non-zero pixel_count and high
   mean SST -- expect tropics (lat ~ 0).
4. Locate cells with pixel_count == 0 -- mostly large landmasses; the
   pattern of land at, e.g., (lon~30E lat~10N -- Sudan; lon~120-150E
   lat~25S -- Australia; lon~80-90W lat~30-50N -- North America) lets
   us read off the convention used.
5. Compare January (winter NH) vs July (summer NH) to verify lat
   direction by checking which lat band the warmest zonal-mean SST
   sits in.
"""
import numpy as np
from pydap.client import open_url
import datetime as dt

BASE = "https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/"

def load(month_year):
    url = BASE + f"augmented_monthly_stats_{month_year}.nc"
    print(f"  opening {url}")
    ds = open_url(url, protocol="dap4")
    n   = np.asarray(ds["day_pixel_count"][:].data, dtype="f8")
    sst = np.asarray(ds["day_sum_SST"][:].data, dtype="f8")
    with np.errstate(invalid="ignore", divide="ignore"):
        mean_sst = np.where(n>0, sst/n, np.nan)
    return n, mean_sst   # shape (lon, lat) = (360, 180)

def show_grid_sample(arr, label):
    print(f"\n{label}:  shape={arr.shape}")
    print(f"  global min={np.nanmin(arr):.3f}, max={np.nanmax(arr):.3f}, "
          f"mean={np.nanmean(arr):.3f}")
    # Show a coarse 9x9 map by 40-deg blocks (lon stride 40, lat stride 20)
    print("  Coarse map (rows = lat blocks 0..179, cols = lon blocks 0..359):")
    # arr is (lon, lat); produce (lat-coarse, lon-coarse)
    lat_blocks = 9; lon_blocks = 12
    # crop to multiples
    L = arr.shape[1] // lat_blocks * lat_blocks   # 180 -> 180
    M = arr.shape[0] // lon_blocks * lon_blocks   # 360 -> 360
    a = arr[:M, :L]
    a = a.reshape(lon_blocks, M//lon_blocks, lat_blocks, L//lat_blocks)
    coarse = np.nanmean(a, axis=(1,3))            # (lon_blocks, lat_blocks)
    coarse = coarse.T                              # (lat_blocks, lon_blocks)
    # Print top to bottom
    for i_lat in range(lat_blocks):
        row = []
        for i_lon in range(lon_blocks):
            v = coarse[i_lat, i_lon]
            row.append("  .  " if np.isnan(v) else f"{v:5.1f}")
        print(f"    lat_block{i_lat:2d}: " + " ".join(row))

# January (NH winter) sample
print("="*70)
print("JANUARY 2020:")
n_jan, mean_jan = load("01_2020")
show_grid_sample(mean_jan, "Day-mean SST (Jan 2020)")

# July (NH summer)
print("="*70)
print("JULY 2020:")
n_jul, mean_jul = load("07_2020")
show_grid_sample(mean_jul, "Day-mean SST (Jul 2020)")

# Difference (Jul - Jan): in NH this should be POSITIVE; SH NEGATIVE
print("\nJUL - JAN difference (sign tells us which lat indices are NH):")
diff = mean_jul - mean_jan
show_grid_sample(diff, "SST(Jul) - SST(Jan)")

# Zonal mean of pixel_count vs lat
print("\nZonal valid-pixel-count vs lat-index (Jan):")
n_zonal = np.nanmean(n_jan, axis=0)  # along lon -> length 180
for i in range(0, 180, 20):
    print(f"  lat_idx {i:3d}..{i+19:3d}  mean N = {np.nanmean(n_zonal[i:i+20]):8.1f}")

# Now look at land via pixel-count == 0
print("\nFraction of zero-N cells per lat block (Jan):")
zero = (n_jan == 0).astype(float)
zonal_zero = zero.mean(axis=0)
for i in range(0, 180, 20):
    print(f"  lat_idx {i:3d}..{i+19:3d}  frac zero = {zonal_zero[i:i+20].mean():.3f}")

# Look at lon-index pattern of zero-N cells at a polar lat band
print("\nZero-N pattern at lat_idx 20-40 (one polar latitude band):")
print(" ", "".join("X" if x>0.5 else "." for x in zero[:, 20:40].mean(axis=1)))
print(" lon idx  ", " "*5, "0".rjust(0), " "*40, "90".rjust(0), " "*44, "180".rjust(0), " "*40, "270".rjust(0))

# A more direct test: find the warmest cell and report its (lon_idx, lat_idx).
# In Jul, warmest spot should be western Pacific warm pool (~145E, 5N) or Persian Gulf;
# in Jan, warmest tropics is similar but slightly shifted.
print("\nWarmest cell location (Jul 2020):")
loc = np.unravel_index(np.nanargmax(mean_jul), mean_jul.shape)
print(f"  lon_idx={loc[0]}, lat_idx={loc[1]}, value={mean_jul[loc]:.2f} C")
print("Warmest cell location (Jan 2020):")
loc = np.unravel_index(np.nanargmax(mean_jan), mean_jan.shape)
print(f"  lon_idx={loc[0]}, lat_idx={loc[1]}, value={mean_jan[loc]:.2f} C")
