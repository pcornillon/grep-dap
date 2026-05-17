# usage_sst.md — URI L2 MODIS Aqua SST Orbits

A working guide for an AI agent (or any client program) that needs to
access and use the per-orbit MODIS-Aqua SST product served by the
University of Rhode Island Graduate School of Oceanography. Everything
below is verified against the live server.

---

## 1. What this dataset is

- **Producer:** P. Cornillon, URI / GSO, "SST Fronts" project
  (`http://www.sstfronts.org`).
- **Source data:** NASA OceanColor L2 MODIS Aqua granules
  (`oceandata.sci.gsfc.nasa.gov`), reprocessed and bundled by orbit by
  URI (URI version tag in the filename, currently `24-2`).
- **Product type:** per-orbit L2 swath, plus a co-located L2-equal-area
  resampling that brings AMSR-E microwave fields onto the same grid
  (when AMSR-E was operational, 2002-06 to 2011-10).
- **Temporal coverage:** 2002–2024 (year/month organization;
  ~14 orbits/day × ~365 d × 23 yr ≈ 1.2 × 10⁵ orbit files).
- **Compliance claim:** `Conventions=CF-1.5`. In practice it is mostly
  CF-compliant; a few specific gaps are noted in §6.

## 2. Server endpoint

OPeNDAP Hyrax. DAP4 is preferred (single `.dmr.xml` per dataset).

```
Base:    https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/
Catalog: https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/{YYYY}/{MM}/contents.html
```

Filename pattern:
```
AQUA_MODIS_orbit_{NNNNNN}_{YYYYMMDD}T{hhmmss}_L2_SST-URI_24-2.nc4
```
- `NNNNNN` is the absolute Aqua orbit number.
- `{YYYYMMDD}T{hhmmss}` is the orbit start time UTC.

The trailing `_24-2.nc4` is a URI-internal version tag and may change
in future re-processings.

## 3. Access pattern (Python / pydap)

```python
from pydap.client import open_url

URL = ("https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/2024/01/"
       "AQUA_MODIS_orbit_115220_20240101T011558_L2_SST-URI_24-2.nc4")
ds = open_url(URL, protocol="dap4")            # DAP4 preferred
list(ds.keys())                                # 20 root-level + 2 groups
ds.tree()                                      # full hierarchy view
```

To sub-set a 100 × 100 pixel window near the equator (where SST is
reliably populated):
```python
import numpy as np
sst   = ds["SST_In"]
patch = sst[29200:29300, 600:700]               # triggers a single DAP4 GET
data  = np.asarray(patch.data, dtype="f8")      # numpy ndarray, raw
fill  = float(sst.attributes["_FillValue"])     # = -32767 (Int16)
scale = float(sst.attributes["scale_factor"])   # = 0.005
data[data == fill] = np.nan
data *= scale                                    # now in degree Celsius
# Optional: also mask values outside valid_min..valid_max
vmin = float(sst.attributes["valid_min"]) * scale
vmax = float(sst.attributes["valid_max"]) * scale
data[(data < vmin) | (data > vmax)] = np.nan
```

> **Tip:** Many index ranges of an orbit are over land, sea ice, or
> heavy cloud and will return all-NaN after masking. To pick a
> window of guaranteed open ocean, first pull
> `nadir_latitude` (length `ny`, cheap) and locate an index where
> the satellite is over a tropical or sub-tropical ocean basin
> (e.g.\ where `nadir_latitude` is between $-30^\circ$ and $+30^\circ$).

For high-volume work, enable caching:
```python
from pydap.net import create_session
session = create_session(use_cache=True)
ds = open_url(URL, protocol="dap4", session=session)
```

## 4. File contents (the part most users care about)

Three groups: root (the swath itself), `/Regrid_to_L2eqa/` (a
companion grid with co-located AMSR-E), and `/contributing_granules/`
(provenance). Two dimensions matter for normal use:
- `ny` = number of along-track lines per orbit (~40 000)
- `nx` = 1354 across-track pixels (MODIS 1 km swath)

### 4.1 SST and gradients (root group)

| Variable                  | dtype  | shape   | units      | meaning                                                        |
| ------------------------- | ------ | ------- | ---------- | -------------------------------------------------------------- |
| `SST_In`                  | Int16  | (ny,nx) | °C         | raw L2 SST (scale 0.005, fill −32767, valid [−3, 45] °C)       |
| `regridded_sst`           | Int16  | (ny,nx) | °C         | masked SST used for the gradient computation (same packing)    |
| `eastward_gradient`       | Int32  | (ny,nx) | °C / km    | east component of ∇T (scale 1e-4, fill −2147483647)            |
| `northward_gradient`      | Int32  | (ny,nx) | °C / km    | north component of ∇T (scale 1e-4)                             |
| `refined_mask`            | Int8   | (ny,nx) | flag       | 1 where the original L2 gradient was flagged as too high       |
| `qual_sst`                | Int8   | (ny,nx) | flag       | 0=BEST, 1=GOOD, 2=QUESTIONABLE, 3=BAD, 4=NOTPROCESSED          |

### 4.2 Pixel geolocation (root group)

| Variable                | dtype  | shape   | units         | meaning                                                  |
| ----------------------- | ------ | ------- | ------------- | -------------------------------------------------------- |
| `latitude`              | Int32  | (ny,nx) | degrees_north | scale 1e-3 (raw values × 0.001 give degrees)            |
| `longitude`             | Int32  | (ny,nx) | degrees_east  | scale 1e-3; range valid_min/max = ±720°                  |
| `regridded_latitude`    | Int32  | (ny,nx) | degrees_north | corresponding to `regridded_sst`                         |
| `regridded_longitude`   | Int32  | (ny,nx) | degrees_east  |                                                          |
| `nadir_latitude`        | Float32| (ny,)   | degrees_north | sub-spacecraft latitude per scan line                    |
| `nadir_longitude`       | Float32| (ny,)   | degrees_east  | sub-spacecraft longitude per scan line                   |
| `left_/right_swath_edge_trackline_{latitude,longitude}` | Float32 | (ny,) | degrees | swath edges |

### 4.3 Time (root group)

| Variable                | dtype   | shape | units               | meaning                            |
| ----------------------- | ------- | ----- | ------------------- | ---------------------------------- |
| `DateTime`              | Float64 | scalar| seconds (see note)  | orbit start, seconds since 1970-01-01 UTC |
| `time_from_start_orbit` | Float32 | (ny,) | seconds             | elapsed seconds since `DateTime`   |
| `region_start`, `region_end` | Int32 | (i=5,) | (index)         | 5 along-orbit subregions           |

### 4.4 Co-located AMSR-E (group `/Regrid_to_L2eqa/`)

- `L2eqa_MODIS_{SST,std_SST,num_SST}` — MODIS resampled to L2eqa grid
  with sub-cell statistics.
- `L2eqa_AMSR_E_{SST,wind_speed,water_vapor,cloud_liquid_water}` —
  AMSR-E fields resampled to L2eqa grid.
- `AMSR_E_{SST,lat,lon,wind_speed,water_vapor,cloud_liquid_water}` —
  AMSR-E on its native footprint.
- `MODIS_SST_on_AMSR_E_grid`, `convolved_MODIS_on_AMSR_E_grid` —
  MODIS resampled, then convolved with the AMSR-E antenna pattern.

In all 2024-era files these AMSR-E fields are 1×1 placeholders
(AMSR-E retired October 2011); see §6.

### 4.5 Provenance (group `/contributing_granules/`)

`filenames`, `start_time`, `end_time`, `granule_start_index`,
`granule_end_index`, `orbit_start_index`, `orbit_end_index` — the
list of NASA OceanColor L2 granules stitched together to form the
orbit, with byte-range indices.

## 5. Recipes

### 5.1 Plot a 200-line window of SST at the equator

```python
import numpy as np, matplotlib.pyplot as plt
from pydap.client import open_url

URL = ("https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/2024/01/"
       "AQUA_MODIS_orbit_115220_20240101T011558_L2_SST-URI_24-2.nc4")
ds = open_url(URL, protocol="dap4")

# find the equator crossing
nlat = np.asarray(ds["nadir_latitude"][:].data, dtype="f8")
i_eq = int(np.argmin(np.abs(nlat)))

# pull SST_In around it
sst_var = ds["SST_In"]
sst     = sst_var[i_eq-100:i_eq+100, :]
fill  = float(sst_var.attributes["_FillValue"])
scale = float(sst_var.attributes["scale_factor"])
data  = np.asarray(sst.data, dtype="f8")
data[data == fill] = np.nan
data *= scale

plt.imshow(data, cmap="viridis"); plt.colorbar(label="SST (°C)"); plt.show()
```

### 5.2 Bounding-box subset by latitude/longitude

OPeNDAP subsetting is by array index, not by lat/lon. For a lat/lon
box you have two practical options:

1. **Bracketing approach.** Pull `nadir_latitude` and
   `nadir_longitude` (cheap; both are length `ny`), find the index
   range whose nadir is inside your box, then pull `SST_In` over that
   index range and mask client-side by per-pixel `latitude`/`longitude`.

2. **Hyrax `geogrid()` function.** Hyrax exposes a server-side
   `geogrid` function for geographic bbox subsets, but the exact
   invocation differs across deployments. Try the bracketing approach
   first; it always works.

### 5.3 Get the orbit's start time

```python
import datetime as dt
ds_time = float(ds["DateTime"][...].data)      # seconds since 1970-01-01
print(dt.datetime.utcfromtimestamp(ds_time).isoformat(), "UTC")
```

## 6. Pitfalls to know about

1. **`units="C"` is not UDUNITS.** UDUNITS treats `C` as coulomb. A
   strict CF reader will reject it. Treat the value as
   `degree_Celsius`. Same for `units="C/km"` → `degree_Celsius km-1`.

2. **`DateTime` units lack a reference.** The declared `units="seconds"`
   has no epoch; the epoch is buried in the `long_name` string. Use
   `seconds since 1970-01-01 00:00:00 UTC` when converting.

3. **`latitude`/`longitude` are Int32 with `scale_factor=0.001`.**
   The DMR does declare the scale, but it is easy to miss. Sample raw
   values are ~70000–80000 near the pole.

4. **`flag_masks=0` on `refined_mask` and `qual_sst` is malformed.**
   The intent is enumerated flags; use `flag_values` semantics
   (`0..1` for `refined_mask`, `0..4` for `qual_sst`).

5. **AMSR-E retirement (Oct 2011).** Files after that date carry
   1×1 placeholders in the `/Regrid_to_L2eqa/AMSR_E_*` and
   `L2eqa_AMSR_E_*` variables. Trust nothing in those slots for any
   orbit after 2011-10.

6. **Mismatched units on co-located AMSR-E.**
   `L2eqa_AMSR_E_wind_speed` declares `units="mm"`; based on packing
   it is clearly `m s-1` (the sibling `AMSR_E_wind_speed` is correctly
   labelled `m s-1`).
   `L2eqa_MODIS_num_SST` declares `units="C"`; it is a pixel count
   (`units="1"`).

7. **Cross-product validation.** For any cell in
   `/Regrid_to_L2eqa/`, `L2eqa_MODIS_num_SST > 0` is the validity test;
   never trust the value alone.

## 7. Where to look next

- Sibling branch `gradients_by_period/` holds monthly aggregates of
  the per-pixel gradients defined here. See `usage_gradient_SST.md`.
- Other top-level directories on the same server (`MUR/`,
  `JAXA_Orbits/`, `RSS_Orbits/`, `matchups*/`, `timeSeries*/`,
  `iQuamBuoy/`) exist but return HTTP 403; contact the data manager
  if needed.
- Project home: `http://www.sstfronts.org`.
- Contact: pcornillon@gso.uri.edu.
