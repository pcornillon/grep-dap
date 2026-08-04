"""Walk the orbit and find a 200-line region with many valid gradient
pixels in a contiguous block.
"""
import numpy as np
from pydap.client import open_url

URL = ("https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/2024/01/"
       "AQUA_MODIS_orbit_115220_20240101T011558_L2_SST-URI_24-2.nc4")
ds = open_url(URL, protocol="dap4")
v = ds["eastward_gradient"]
fill = float(v.attributes.get("_FillValue", -2147483647))
vmin = float(v.attributes.get("valid_min", -200000))
vmax = float(v.attributes.get("valid_max",  200000))

# Walk through the orbit in 1000-line chunks, count valid pixels.
ny = 40271
best = (0, -1)
results = []
for i0 in range(0, ny, 1000):
    i1 = min(i0+1000, ny)
    raw = np.asarray(v[i0:i1, :].data, dtype="f8")
    valid = (raw != fill) & (raw >= vmin) & (raw <= vmax)
    n = int(valid.sum())
    frac = n / raw.size
    results.append((i0,i1,n,frac))
    if n > best[0]:
        best = (n, i0)
results.sort(key=lambda r: -r[2])
print("Top 10 chunks by valid gradient pixels:")
for r in results[:10]:
    print(f"  i={r[0]:5d}-{r[1]:5d}  valid={r[2]:7d}  frac={r[3]:.3f}")
print(f"\nBest chunk start: i0={best[1]}")

# Now within the best 1000-line chunk, find the best 200x100 block
i0_best = best[1]
print(f"\nDetail in best chunk (i0={i0_best}, line by line valid count):")
raw = np.asarray(v[i0_best:i0_best+1000, :].data, dtype="f8")
valid_per_line = ((raw != fill) & (raw >= vmin) & (raw <= vmax)).sum(axis=1)
# Find 200-line windows with high counts
totals = np.convolve(valid_per_line, np.ones(200), mode="valid")
i_best200 = int(np.argmax(totals))
print(f"  best 200-line window: lines {i_best200}..{i_best200+200} from {i0_best}, "
      f"total valid = {int(totals[i_best200])}")
# What's the nadir loc?
nlat = np.asarray(ds["nadir_latitude"][i0_best+i_best200:i0_best+i_best200+200].data, dtype="f8")
nlon = np.asarray(ds["nadir_longitude"][i0_best+i_best200:i0_best+i_best200+200].data, dtype="f8")
print(f"  nadir lat range in this window: [{nlat.min():.2f}, {nlat.max():.2f}]")
print(f"  nadir lon range in this window: [{nlon.min():.2f}, {nlon.max():.2f}]")
