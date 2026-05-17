import numpy as np
from pydap.client import open_url
import datetime as dt

print("="*70)
print("usage_sst.md headline example")
print("="*70)
URL = ("https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/2024/01/"
       "AQUA_MODIS_orbit_115220_20240101T011558_L2_SST-URI_24-2.nc4")
ds = open_url(URL, protocol="dap4")
print(f"  number of top-level keys: {len(list(ds.keys()))}")

sst   = ds["SST_In"]
patch = sst[29200:29300, 600:700]
data  = np.asarray(patch.data, dtype="f8")
fill  = float(sst.attributes["_FillValue"])
scale = float(sst.attributes["scale_factor"])
data[data == fill] = np.nan
data *= scale
vmin = float(sst.attributes["valid_min"]) * scale
vmax = float(sst.attributes["valid_max"]) * scale
data[(data < vmin) | (data > vmax)] = np.nan
a = data[np.isfinite(data)]
print(f"  SST_In sample: n_valid={a.size}, range=[{a.min():.2f},{a.max():.2f}], mean={a.mean():.2f}")
ds_time = float(ds["DateTime"][...].data)
print(f"  DateTime -> {dt.datetime.utcfromtimestamp(ds_time).isoformat()} UTC")

print()
print("="*70)
print("usage_gradient_SST.md headline example")
print("="*70)
URL = ("https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/"
       "augmented_monthly_stats_07_2020.nc")
ds = open_url(URL, protocol="dap4")
N    = np.asarray(ds["day_pixel_count"][:].data,  dtype="f8")
S    = np.asarray(ds["day_sum_SST"][:].data,      dtype="f8")
SMG  = np.asarray(ds["day_sum_magnitude_gradient"][:].data, dtype="f8")
mean_sst = np.where((N > 0) & np.isfinite(S),   S / N,   np.nan)
mean_mag = np.where((N > 0) & np.isfinite(SMG), SMG / N, np.nan)
ms = mean_sst[np.isfinite(mean_sst)]
mm = mean_mag[np.isfinite(mean_mag)]
print(f"  per-cell day-mean SST       n={ms.size}, range=[{ms.min():.2f},{ms.max():.2f}], mean={ms.mean():.2f}")
print(f"  per-cell day-mean |grad|    n={mm.size}, range=[{mm.min():.4f},{mm.max():.4f}], mean={mm.mean():.4f}")

print()
print("="*70)
print("usage_gradient_SST.md §5.2 bounding-box example")
print("="*70)
lonidx = lambda lon: int(round(lon + 179.5))
latidx = lambda lat: int(round(lat + 89.5))
i_lon0, i_lon1 = lonidx(-100), lonidx(-50) + 1
i_lat0, i_lat1 = latidx( 20),  latidx( 50) + 1
print(f"  bbox indices: lon={i_lon0}:{i_lon1}  lat={i_lat0}:{i_lat1}")
N_box = np.asarray(ds["day_pixel_count"][i_lon0:i_lon1, i_lat0:i_lat1].data, dtype="f8")
S_box = np.asarray(ds["day_sum_SST"][i_lon0:i_lon1, i_lat0:i_lat1].data, dtype="f8")
mean_box = np.where(N_box > 0, S_box / N_box, np.nan)
mb = mean_box[np.isfinite(mean_box)]
print(f"  box shape: {mean_box.shape}, n_valid={mb.size}, mean SST = {mb.mean():.2f} °C")
