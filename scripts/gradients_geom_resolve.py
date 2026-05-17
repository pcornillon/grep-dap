"""Resolve gradients_by_period lat/lon conventions by checking known
geographic features (continents, ocean centers) against day_pixel_count.
"""
import numpy as np
from pydap.client import open_url

URL = ("https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/"
       "augmented_monthly_stats_01_2020.nc")
ds = open_url(URL, protocol="dap4")
n = np.asarray(ds["day_pixel_count"][:].data, dtype="f8")
print("Shape (lon, lat):", n.shape)
print("N>0 cells total:", int((n>0).sum()), "out of", n.size)

# Helper: given a candidate lat_origin and lon_origin (0 or -180),
# look at whether known-land cells are zero and known-ocean cells are positive.
LAND_POINTS = [
    ("Sahara",         20.0,  25.0),  # E, N
    ("Australia interior", 135.0, -25.0),
    ("Amazon basin", -60.0,  -5.0),
    ("Central US",   -100.0, 40.0),
    ("Greenland",    -42.0,  72.0),
    ("Tibet",         85.0,  32.0),
]
OCEAN_POINTS = [
    ("Pacific center",   -150.0,  0.0),
    ("Atlantic center",  -30.0,   0.0),
    ("Indian Ocean",      80.0, -20.0),
    ("North Pacific",   -160.0,  35.0),
    ("Persian Gulf",      52.0,  27.0),
    ("Warm Pool",        150.0,   5.0),
]

# Two lon conventions to try:
#  CONV-A: lon_idx 0 = -179.5  (cell-centered, -180..+180)
#  CONV-B: lon_idx 0 =    0.5  (cell-centered, 0..360)
# Two lat conventions to try:
#  LAT-S2N: lat_idx 0 = -89.5
#  LAT-N2S: lat_idx 0 = +89.5

def lonidx(lon, conv):
    if conv == "A":  # -180..180
        return int(round(lon + 179.5))
    else:            # 0..360
        v = lon if lon >= 0 else lon + 360
        return int(round(v - 0.5))

def latidx(lat, conv):
    if conv == "S2N":
        return int(round(lat + 89.5))
    else:
        return int(round(89.5 - lat))

for lon_conv in ("A","B"):
    for lat_conv in ("S2N","N2S"):
        print(f"\n--- lon_conv={lon_conv}, lat_conv={lat_conv} ---")
        score_land = 0; score_ocean = 0
        for name, lon, lat in LAND_POINTS:
            li = lonidx(lon, lon_conv) % 360
            la = latidx(lat, lat_conv)
            la = max(0, min(179, la))
            v = n[li, la]
            ok = "LAND_OK" if v == 0 else "LAND_FAIL"
            if v == 0: score_land += 1
            print(f"  {name:22s} lon={lon:+6.1f}, lat={lat:+5.1f} -> (li={li:3d},la={la:3d})  N={int(v):6d}  {ok}")
        for name, lon, lat in OCEAN_POINTS:
            li = lonidx(lon, lon_conv) % 360
            la = latidx(lat, lat_conv)
            la = max(0, min(179, la))
            v = n[li, la]
            ok = "OCEAN_OK" if v > 0 else "OCEAN_FAIL"
            if v > 0: score_ocean += 1
            print(f"  {name:22s} lon={lon:+6.1f}, lat={lat:+5.1f} -> (li={li:3d},la={la:3d})  N={int(v):6d}  {ok}")
        print(f"  >>> land matches {score_land}/{len(LAND_POINTS)};  ocean matches {score_ocean}/{len(OCEAN_POINTS)}")
