# usage_gradient_SST.md — URI Monthly SST and SST-Gradient Statistics

A working guide for an AI agent (or any client program) that needs to
access and use the monthly SST and SST-gradient statistics product
served by the University of Rhode Island Graduate School of
Oceanography. **The files themselves carry zero semantic metadata; everything
in §3–§5 below has been inferred from the variable names, the
companion `SST_Orbits/` branch, and direct data probes.** Treat the
inferred values accordingly.

---

## 1. What this dataset is

- **Producer:** P. Cornillon, URI / GSO, "SST Fronts" project
  (`http://www.sstfronts.org`). Inferred from the sibling branch
  `SST_Orbits/`, which is fully attributed and is the upstream of
  this product.
- **Source data:** the URI L2 MODIS-Aqua SST orbit files in
  `SST_Orbits/` (which themselves derive from NASA OceanColor L2
  granules).
- **Product type:** monthly accumulations on a global 1° × 1° grid of
  per-pixel SST and SST-gradient statistics, broken out by day-side
  (Aqua ascending node, ~13:30 LST) and night-side (Aqua descending
  node, ~01:30 LST).
- **Bookkeeping:** every quantity is stored as a *sum* (Σ) and a
  *sum-of-squares* (Σ²) along with a *pixel count* (N) so that the
  monthly cell mean and variance can be recovered as
  `mean = Σ/N`, `var = Σ²/N − (Σ/N)²`.
- **Temporal coverage:** 270 monthly files, `01_2003` through
  `12_2024`.
- **Spatial scale of the underlying gradient:** the per-pixel
  gradients that get summed into these cells were computed at the L2
  swath level using a differentiation operator with effective support
  of **~5 km** (4–6 km from three independent estimates; see §6 for
  details). The 1° cell is therefore a *bin*, not the spatial
  resolution of the underlying measurement.

## 2. Server endpoint

OPeNDAP Hyrax. DAP4 preferred.

```
Base:    https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/
Catalog: https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/contents.html
```

Filename pattern (flat directory, 270 files):
```
augmented_monthly_stats_MM_YYYY.nc
```
- `MM` = `01`–`12`
- `YYYY` = `2003`–`2024`

## 3. File schema (verified by DMR)

Two dimensions and 34 `Float64` variables, all of shape `(lon, lat)`
where `lon = 360` and `lat = 180`. The schema is identical across
all 270 files.

**There are no coordinate variables.** There are no `units`, no
`long_name`, no `_FillValue`, no `standard_name`, and no global
attributes. The mapping below is inferred.

### 3.1 Implicit coordinate grid (inferred and verified)

Cell-centered global 1° × 1° grid:
```
lat[k] = -89.5 + k     for k = 0..179      (south → north)
lon[k] = -179.5 + k    for k = 0..359      (cell-centered, -180..+180)
```
Verified by classifying six known-land points (Sahara, Australia
interior, Amazon basin, Central US, Greenland, Tibet) and six
known-ocean points (Pacific/Atlantic centers, Indian Ocean, North
Pacific, Persian Gulf, Western Pacific warm pool) against
`day_pixel_count`. Only this convention gets all 12 right.

### 3.2 The 34 variables (inferred semantics)

All variables are `Float64`, shape `(lon, lat) = (360, 180)`,
fill value `NaN`.

**Pixel counts (6):** dimensionless, `units="1"`.
| Variable                   | Meaning                                                    |
| -------------------------- | ---------------------------------------------------------- |
| `day_pixel_count`          | Number of valid daytime SST pixels in cell over month      |
| `night_pixel_count`        | Same, night-time                                           |
| `day_as_pixel_count`       | Number of pixels with valid along-scan gradient (daytime)  |
| `night_as_pixel_count`     | Same, night-time                                           |
| `day_at_pixel_count`       | Number of pixels with valid along-track gradient (daytime) |
| `night_at_pixel_count`     | Same, night-time                                           |

**SST sums (4):** `units = "degree_Celsius"` (for the squared
sums, `units = "degree_Celsius2"`).
| Variable                  | Meaning                                                  |
| ------------------------- | -------------------------------------------------------- |
| `day_sum_SST`             | Σ T over valid daytime SST pixels in the cell            |
| `day_sum_SST_squared`     | Σ T² over the same pixels                                |
| `night_sum_SST`           | Σ T at night                                             |
| `night_sum_SST_squared`   | Σ T² at night                                            |

**Geographic gradient sums (8):** `units = "degree_Celsius km-1"`
(squared: `degree_Celsius2 km-2`). Signed.
| Variable                                | Meaning                                |
| --------------------------------------- | -------------------------------------- |
| `day_sum_eastward_gradient`             | Σ ∂T/∂east  over valid day pixels      |
| `day_sum_eastward_gradient_squared`     | Σ (∂T/∂east)²                          |
| `day_sum_northward_gradient`            | Σ ∂T/∂north                            |
| `day_sum_northward_gradient_squared`    | Σ (∂T/∂north)²                         |
| `night_sum_eastward_gradient` & sq      | Same, night-time                       |
| `night_sum_northward_gradient` & sq     | Same, night-time                       |

**Geographic gradient magnitudes (4):** `units =
"degree_Celsius km-1"`. Non-negative.
| Variable                                | Meaning                                |
| --------------------------------------- | -------------------------------------- |
| `day_sum_magnitude_gradient`            | Σ |∇T| (per-pixel magnitudes)          |
| `day_sum_magnitude_gradient_squared`    | Σ |∇T|²                                |
| `night_sum_magnitude_gradient` & sq     | Same, night-time                       |

**Swath-relative gradient sums (8):** `units = "degree_Celsius km-1"`.
Signed. (`as` = along-scan, across-track in swath coordinates;
`at` = along-track.)
| Variable                                | Meaning                                |
| --------------------------------------- | -------------------------------------- |
| `day_sum_grad_as_per_km` & sq           | Σ along-scan ∂T/∂s                     |
| `day_sum_grad_at_per_km` & sq           | Σ along-track ∂T/∂t                    |
| `night_sum_grad_as_per_km` & sq         | Same, night                            |
| `night_sum_grad_at_per_km` & sq         | Same, night                            |

**Swath-relative gradient magnitudes (4):** `units =
"degree_Celsius km-1"`.
| Variable                                | Meaning                                |
| --------------------------------------- | -------------------------------------- |
| `day_sum_grad_mag_per_km` & sq          | Σ |∇T| in swath frame, day             |
| `night_sum_grad_mag_per_km` & sq        | Same, night                            |

### 3.3 Divisor to convert each sum to a per-cell mean

Pair every `*_sum_*` with the right count. **This is the most likely
thing to get wrong.**

| Sum                                      | Divisor                |
| ---------------------------------------- | ---------------------- |
| `*_sum_SST`, `*_sum_SST_squared`         | `*_pixel_count`        |
| `*_sum_eastward_gradient` ± sq           | `*_pixel_count`        |
| `*_sum_northward_gradient` ± sq          | `*_pixel_count`        |
| `*_sum_magnitude_gradient` ± sq          | `*_pixel_count`        |
| `*_sum_grad_as_per_km` ± sq              | `*_as_pixel_count`     |
| `*_sum_grad_at_per_km` ± sq              | `*_at_pixel_count`     |
| `*_sum_grad_mag_per_km` ± sq             | `*_at_pixel_count` *   |

\* Verified empirically by comparing per-cell averages: dividing
`day_sum_grad_mag_per_km` by `day_at_pixel_count` produces
0.044 °C/km, matching `day_sum_magnitude_gradient` /
`day_pixel_count` = 0.046 °C/km, whereas dividing by
`day_as_pixel_count` gives 0.022 (clearly wrong).

## 4. Access pattern (Python / pydap)

```python
from pydap.client import open_url
import numpy as np

URL = ("https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/"
       "augmented_monthly_stats_07_2020.nc")
ds = open_url(URL, protocol="dap4")

# 360 x 180 grid is small; read the whole field in one shot
N    = np.asarray(ds["day_pixel_count"][:].data,  dtype="f8")  # (lon, lat)
S    = np.asarray(ds["day_sum_SST"][:].data,      dtype="f8")
SMG  = np.asarray(ds["day_sum_magnitude_gradient"][:].data, dtype="f8")

# Per-cell day-mean SST (mask cells with zero or NaN N)
mean_sst = np.where((N > 0) & np.isfinite(S), S / N, np.nan)

# Per-cell day-mean gradient magnitude (uses the same N divisor)
mean_mag = np.where((N > 0) & np.isfinite(SMG), SMG / N, np.nan)
```

For a multi-month time series, iterate over filenames:
```python
def url(yyyy, mm):
    return ("https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/"
            f"augmented_monthly_stats_{mm:02d}_{yyyy:04d}.nc")
```

## 5. Recipes

### 5.1 Recover variance per cell

```python
N    = np.asarray(ds["day_pixel_count"][:].data, dtype="f8")
S    = np.asarray(ds["day_sum_SST"][:].data,     dtype="f8")
SS   = np.asarray(ds["day_sum_SST_squared"][:].data, dtype="f8")
ok   = (N > 1) & np.isfinite(S) & np.isfinite(SS)
mean = np.where(ok, S/N,         np.nan)
var  = np.where(ok, SS/N - mean**2, np.nan)
std  = np.sqrt(np.maximum(var, 0))
```

### 5.2 Bounding-box subset

The grid is regular, so bbox subsetting is just index arithmetic:
```python
def lonidx(lon_deg):  # cell-centered, -180..180
    return int(round(lon_deg + 179.5))
def latidx(lat_deg):  # south to north
    return int(round(lat_deg + 89.5))

i_lon0, i_lon1 = lonidx(-100), lonidx(-50) + 1   # Atlantic 100W..50W
i_lat0, i_lat1 = latidx( 20),  latidx( 50) + 1   # 20N..50N

# Pull only the bbox to minimize bytes on the wire (DAP4 hyperslab)
N_box = np.asarray(
    ds["day_pixel_count"][i_lon0:i_lon1, i_lat0:i_lat1].data, dtype="f8")
S_box = np.asarray(
    ds["day_sum_SST"][i_lon0:i_lon1, i_lat0:i_lat1].data, dtype="f8")
mean_box = np.where(N_box > 0, S_box / N_box, np.nan)
```

### 5.3 Aggregate across years for one month (climatology)

```python
import numpy as np, calendar
from pydap.client import open_url

def open_month(yyyy, mm):
    return open_url(
        "https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/"
        f"augmented_monthly_stats_{mm:02d}_{yyyy:04d}.nc",
        protocol="dap4")

MM = 7  # July climatology
N_total = np.zeros((360,180), dtype="f8")
S_total = np.zeros_like(N_total)
for yyyy in range(2003, 2025):
    ds = open_month(yyyy, MM)
    N = np.asarray(ds["day_pixel_count"][:].data, dtype="f8")
    S = np.asarray(ds["day_sum_SST"][:].data,    dtype="f8")
    keep = np.isfinite(S) & np.isfinite(N)
    N_total += np.where(keep, N, 0)
    S_total += np.where(keep, S, 0)

clim_mean_sst = np.where(N_total > 0, S_total / N_total, np.nan)
```

## 6. Provenance, pitfalls, and what is *not* inferrable

### 6.1 Provenance (inferred, not declared in the file)

- **Day/night split:** Aqua ascending vs. descending nodes (~13:30 vs.
  ~01:30 local solar time). Inferred from the standard MODIS-Aqua
  convention; the file does not declare it.
- **`as`/`at`:** along-scan (across-track) / along-track in swath
  coordinates. Inferred from the naming grammar and from the
  observation that the std-deviations of the swath-relative
  components match those of `eastward`/`northward` to within ~10%.
- **Upstream gradient algorithm:** centered finite difference with
  half-width 2–3 pixels (full operator support 4–6 km, equivalently
  ~5 km on the L2 swath) applied to the masked SST field
  `regridded_sst` of `SST_Orbits/`. Verified by three independent
  estimates (pixel-count ratios, magnitude-RMSE matching,
  autocorrelation length). The exact functional form of the operator
  (centered diff vs. Sobel vs. local LSQ of similar support) cannot
  be distinguished from the public-side data.

### 6.2 Pitfalls

1. **No metadata in the file.** No `units`, no fill, no globals.
   The values in §3 are inferences; treat them as the working
   semantics, not declared truth.

2. **Use the right divisor.** The three pixel-count flavours are
   distinct (typical means: `pixel_count=10030`, `as=8110`,
   `at=4090`); see §3.3.

3. **NaN propagation.** Some cells with `pixel_count > 0` have NaN
   in `sum_SST` (an undeclared fill semantic). Always mask before
   dividing.

4. **Lat / lon are not stored.** Only the dimensions `lat` and `lon`
   exist; you have to construct cell-center coordinates yourself
   (§3.1).

5. **No time inside the file.** The single month is encoded only in
   the filename. There is no `time` variable. For a time series,
   parse `MM` and `YYYY` from the filename and either store
   alongside or synthesize a CF-style time coordinate.

6. **`sum_magnitude_gradient` is the sum of per-pixel magnitudes,
   not the magnitude of the vector sum.** Verified: the ratio of
   `sum_magnitude_gradient` to `√(sum_eastward² + sum_northward²)`
   averages ~12 per cell. Use the per-cell mean
   `sum_magnitude_gradient / pixel_count` if you want the average
   per-pixel |∇T|.

7. **1° cells are bins, not measurement resolution.** The underlying
   gradient values were computed at ~5 km on the L2 swath. Do not
   advertise this product as "1° SST gradient" — advertise it as
   "L2 ~5 km SST gradients aggregated into 1° monthly bins".

### 6.3 What I won't guess

- `date_created` / `history` of any particular file: I have no
  evidence to assign them.
- The exact functional form of the upstream gradient operator
  (centered diff vs. Sobel vs. local LSQ): only the effective
  support is inferable.
- Whether a `gradients_by_period_5day/` sibling directory (which
  returns HTTP 403) follows the same schema with a 5-day period;
  likely but not verified.
- Quality-control thresholds that may have been applied at the
  aggregation step.

## 7. Provenance contacts

- Project home: `http://www.sstfronts.org`
- Contact: `pcornillon@gso.uri.edu`
- Companion dataset: `SST_Orbits/` — per-orbit L2 files with full
  CF-1.5 metadata; see `usage_sst.md`.
