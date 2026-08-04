"""Sample an equatorial slice of the same orbit to confirm SST realism."""
import numpy as np
from pydap.client import open_url
URL = ("https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/2024/01/"
       "AQUA_MODIS_orbit_115220_20240101T011558_L2_SST-URI_24-2.nc4")
ds = open_url(URL, protocol="dap4")
# Look at orbit nadir_lat to find equator crossing
nlat = np.asarray(ds["nadir_latitude"][:].data, dtype="f8")
print(f"nadir_latitude: shape={nlat.shape}, min={nlat.min():.2f}, max={nlat.max():.2f}")
# index where nadir_lat is closest to 0
idx = np.argmin(np.abs(nlat))
print(f"  equator crossing near i={idx}  nadir_lat={nlat[idx]:.3f}")
i0 = max(0, idx-50); j0 = 600
def stats(a, scale=1.0, fill=None):
    a = np.asarray(a, dtype="f8")
    if fill is not None: a = a[a != fill]
    a = a[np.isfinite(a)]
    if a.size == 0: return "empty"
    a = a*scale
    return f"n={a.size}, range=[{a.min():.4f}, {a.max():.4f}], mean={a.mean():.4f}, std={a.std():.4f}"
for v, sc in [("SST_In",0.005), ("eastward_gradient",0.0001), ("northward_gradient",0.0001),
              ("latitude",0.001), ("longitude",0.001), ("regridded_sst",0.005)]:
    sub = ds[v][i0:i0+100, j0:j0+100].data
    fill = ds[v].attributes.get("_FillValue", None)
    print(f"  {v:24s} {stats(sub, scale=sc, fill=fill)}")
