"""Sample data from URI Hyrax to validate metadata inferences.

For the SST_Orbits sample: SST_In ranges, gradient ranges, lat/lon ranges.
For gradients_by_period: variable ranges, day_pixel_count, sum/N ratios.
"""
import numpy as np
from pydap.client import open_url

ORBIT_URL = ("https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/2024/01/"
             "AQUA_MODIS_orbit_115220_20240101T011558_L2_SST-URI_24-2.nc4")
GRAD_URL  = ("https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/"
             "augmented_monthly_stats_07_2020.nc")

def stats(arr, scale=1.0, offset=0.0, fill=None):
    a = np.asarray(arr, dtype="f8")
    if fill is not None:
        a = a[a != fill]
    a = a[~np.isnan(a)]
    if a.size == 0:
        return "empty"
    v = a * scale + offset
    return (f"n={a.size}, min={v.min():.4f}, max={v.max():.4f}, "
            f"mean={v.mean():.4f}, std={v.std():.4f}")

print("="*70)
print("ORBIT file (DAP4 protocol)")
ds = open_url(ORBIT_URL, protocol="dap4")
print(" keys:", list(ds.keys())[:25], "...")

# A 100-line × 100-px window from the middle of the orbit
i0, j0 = 20000, 600
print("\nSampling [i0,i0+100, j0,j0+100]:")
for v, scale in [("SST_In",0.005), ("eastward_gradient",0.0001),
                 ("northward_gradient",0.0001), ("latitude",1.0),
                 ("longitude",1.0)]:
    try:
        sub = ds[v][i0:i0+100, j0:j0+100].data
        fill_attr = ds[v].attributes.get("_FillValue", None)
        s = stats(sub, scale=scale, fill=fill_attr)
        print(f"  {v:24s} : {s}")
    except Exception as e:
        print(f"  {v}: ERROR {e}")

# 1D variables along orbit
for v in ("nadir_latitude","nadir_longitude","time_from_start_orbit"):
    try:
        sub = ds[v][i0:i0+100].data
        fill_attr = ds[v].attributes.get("_FillValue", None)
        print(f"  {v:24s} : {stats(sub, fill=fill_attr)}")
    except Exception as e:
        print(f"  {v}: ERROR {e}")

# DateTime is a scalar (Float64, no dims): use [...]
try:
    dt = float(ds["DateTime"][...].data)
    import datetime as _dt
    print(f"  DateTime              : {dt:.1f} s since 1970-01-01  ->  {_dt.datetime.utcfromtimestamp(dt).isoformat()} UTC")
except Exception as e:
    print(f"  DateTime: ERROR {e}")

print("\n" + "="*70)
print("GRADIENTS file (DAP4 protocol)")
gd = open_url(GRAD_URL, protocol="dap4")
print(" keys:", list(gd.keys()))
print(" shape (day_pixel_count):", gd["day_pixel_count"].shape)
# read entire 360x180 (small)
for v in ("day_pixel_count","night_pixel_count","day_sum_SST","night_sum_SST",
          "day_sum_magnitude_gradient","night_sum_magnitude_gradient",
          "day_sum_eastward_gradient","day_sum_northward_gradient"):
    sub = gd[v][:].data
    print(f"  {v:36s} {stats(sub)}")

# Per-cell means where pixel counts > 0
day_n = np.asarray(gd["day_pixel_count"][:].data, dtype="f8")
day_sst_sum = np.asarray(gd["day_sum_SST"][:].data, dtype="f8")
day_mag_sum = np.asarray(gd["day_sum_magnitude_gradient"][:].data, dtype="f8")
day_mag_n   = np.asarray(gd["day_as_pixel_count"][:].data, dtype="f8")
ok = day_n > 0
mean_sst = day_sst_sum[ok] / day_n[ok]
print(f"\n  Derived day-mean SST (sum_SST/day_pixel_count): "
      f"n={mean_sst.size}, min={mean_sst.min():.3f}, max={mean_sst.max():.3f}, "
      f"mean={mean_sst.mean():.3f}, std={mean_sst.std():.3f}")
ok2 = day_mag_n > 0
mean_mag = day_mag_sum[ok2] / day_mag_n[ok2]
print(f"  Derived day-mean gradient magnitude: n={mean_mag.size}, "
      f"min={mean_mag.min():.6f}, max={mean_mag.max():.4f}, "
      f"mean={mean_mag.mean():.5f}, std={mean_mag.std():.5f}")
