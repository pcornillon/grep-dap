"""Locate a region of orbit 115220 (2024-01-01) with good thermal
contrast and lots of valid gradient pixels, then pull a sample
block of SST_In, regridded_sst, eastward_gradient,
northward_gradient, refined_mask, latitude, longitude.

The orbit travels from south to north and back; we sampled the
equator and the pole in earlier prompts. For this one we want a
mid-latitude ocean region where the gradient field is well populated.
The Mediterranean / North Atlantic at ~30-40 deg N is a good
candidate (orbit nadir traverse passes that area; see
scripts/uri_sample_equator.py for the orbit's nadir trajectory).
"""
import numpy as np
from pydap.client import open_url

URL = ("https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/2024/01/"
       "AQUA_MODIS_orbit_115220_20240101T011558_L2_SST-URI_24-2.nc4")

ds = open_url(URL, protocol="dap4")
# nadir_latitude/longitude tell us where the orbit is at each ny line.
nlat = np.asarray(ds["nadir_latitude"][:].data, dtype="f8")
nlon = np.asarray(ds["nadir_longitude"][:].data, dtype="f8")
print(f"orbit lines = {nlat.shape[0]}")
print(f"  nadir lat range:  [{nlat.min():.2f}, {nlat.max():.2f}]")
print(f"  nadir lon range:  [{nlon.min():.2f}, {nlon.max():.2f}]")

# Find nadir-lat = +35 N
mask = (nlat > 33) & (nlat < 37) & np.isfinite(nlon)
candidates = np.where(mask)[0]
print(f"Lines where nadir between 33 and 37 N: {candidates.size}")
# Among those, prefer lines where nadir lon is between -15 and 40 (Mediterranean / N Atlantic east)
for i in candidates[::500]:
    print(f"  i={i:6d}  nadir_lat={nlat[i]:6.2f}  nadir_lon={nlon[i]:7.2f}")
