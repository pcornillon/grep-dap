"""Pull the Pacific block (i=11417..11617, full swath j=0..1354)."""
import numpy as np
from pydap.client import open_url
import pickle

URL = ("https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/2024/01/"
       "AQUA_MODIS_orbit_115220_20240101T011558_L2_SST-URI_24-2.nc4")
I0, I1 = 11417, 11617
J0, J1 = 0, 1354
ds = open_url(URL, protocol="dap4")

def get(name):
    v = ds[name]
    raw = np.asarray(v[I0:I1, J0:J1].data, dtype="f8")
    fill = v.attributes.get("_FillValue", None)
    vmin = v.attributes.get("valid_min", None)
    vmax = v.attributes.get("valid_max", None)
    sc   = v.attributes.get("scale_factor", None)
    of   = v.attributes.get("add_offset",  None)
    bad  = np.zeros_like(raw, dtype=bool)
    if fill is not None: bad |= (raw == float(fill))
    if vmin is not None: bad |= (raw < float(vmin))
    if vmax is not None: bad |= (raw > float(vmax))
    if sc is not None:   raw = raw * float(sc)
    if of is not None:   raw = raw + float(of)
    raw = np.where(bad, np.nan, raw)
    return raw

names = ["SST_In","regridded_sst","eastward_gradient","northward_gradient",
         "refined_mask","qual_sst","latitude","longitude"]
block = {n: get(n) for n in names}
with open("/tmp/grad_block2.pkl","wb") as fh:
    pickle.dump(block, fh)
print(f"Block: {I1-I0} lines x {J1-J0} pixels  (total {(I1-I0)*(J1-J0)} pixels)")
for k,v in block.items():
    a = v[np.isfinite(v)]
    if a.size==0: print(f"  {k:20s} ALL NaN"); continue
    print(f"  {k:20s} valid={a.size:7d}/{v.size:7d}  "
          f"range=[{a.min():9.4f},{a.max():9.4f}]  mean={a.mean():8.4f}  std={a.std():8.4f}")
print()
print(f"  lat span: [{block['latitude'].min():.2f}, {block['latitude'].max():.2f}]")
print(f"  lon span: [{block['longitude'].min():.2f}, {block['longitude'].max():.2f}]")
