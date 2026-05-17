"""Test sign conventions and inter-variable consistency of gradient
variables in gradients_by_period.

Questions:
  Q1. Are eastward_gradient and northward_gradient signed?
       (sum should range over both signs)
  Q2. Is magnitude_gradient strictly non-negative (it should be)?
  Q3. Does sum_magnitude_gradient >= |sum_eastward_gradient|+|sum_northward_gradient|?
       Or are eastward / northward / magnitude unrelated decompositions?
  Q4. Same questions for grad_{as,at,mag}_per_km vs grad_{e,n,mag}.
  Q5. Is grad_mag_per_km approximately sqrt(grad_as_per_km^2 + grad_at_per_km^2)
       cell by cell? (probably not at the cell aggregate level)
  Q6. Are *_pixel_count, *_as_pixel_count, *_at_pixel_count distinct?
"""
import numpy as np
from pydap.client import open_url

URL = ("https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/"
       "augmented_monthly_stats_07_2020.nc")
ds = open_url(URL, protocol="dap4")

def rd(name):
    return np.asarray(ds[name][:].data, dtype="f8")

vars_to_get = [
    "day_pixel_count","day_as_pixel_count","day_at_pixel_count",
    "day_sum_SST","day_sum_SST_squared",
    "day_sum_eastward_gradient","day_sum_eastward_gradient_squared",
    "day_sum_northward_gradient","day_sum_northward_gradient_squared",
    "day_sum_magnitude_gradient","day_sum_magnitude_gradient_squared",
    "day_sum_grad_as_per_km","day_sum_grad_as_per_km_squared",
    "day_sum_grad_at_per_km","day_sum_grad_at_per_km_squared",
    "day_sum_grad_mag_per_km","day_sum_grad_mag_per_km_squared",
]
data = {n: rd(n) for n in vars_to_get}

def s(arr, lab):
    a = arr[np.isfinite(arr)]
    if a.size == 0:
        return f"{lab:46s} empty"
    return (f"{lab:46s} n={a.size:6d}  min={a.min():12.4f}  max={a.max():12.4f}  "
            f"mean={a.mean():10.4f}  std={a.std():10.4f}")

print("="*100)
print("Q1/Q2: ranges of gradient sums (signed vs unsigned)")
print("="*100)
for v in [
    "day_sum_eastward_gradient",
    "day_sum_northward_gradient",
    "day_sum_magnitude_gradient",
    "day_sum_grad_as_per_km",
    "day_sum_grad_at_per_km",
    "day_sum_grad_mag_per_km",
]:
    print(s(data[v], v))

print()
print("Squared sums (must be >= 0):")
for v in [
    "day_sum_eastward_gradient_squared",
    "day_sum_northward_gradient_squared",
    "day_sum_magnitude_gradient_squared",
    "day_sum_grad_as_per_km_squared",
    "day_sum_grad_at_per_km_squared",
    "day_sum_grad_mag_per_km_squared",
]:
    print(s(data[v], v))

print()
print("="*100)
print("Q3: does sum_magnitude correlate with sqrt(sum_east**2 + sum_north**2)?")
print("    (it shouldn't if it's the sum of per-pixel magnitudes)")
print("="*100)
e = data["day_sum_eastward_gradient"]; n = data["day_sum_northward_gradient"]
m = data["day_sum_magnitude_gradient"]
hyp = np.sqrt(e*e + n*n)
mask = np.isfinite(m) & np.isfinite(hyp) & (m > 0)
ratio = m[mask] / np.where(hyp[mask]>0, hyp[mask], np.nan)
print(s(ratio, "ratio  sum_magnitude / sqrt(sum_e**2 + sum_n**2)"))
print("  If ~1.0 everywhere: sum_magnitude is magnitude of vector sum (rare)")
print("  If >>1.0:           sum_magnitude is sum of per-pixel magnitudes (expected)")

print()
print("="*100)
print("Q4-5: pixel counts compared")
print("="*100)
N   = data["day_pixel_count"]
NAS = data["day_as_pixel_count"]
NAT = data["day_at_pixel_count"]
print(s(N,  "day_pixel_count"))
print(s(NAS,"day_as_pixel_count"))
print(s(NAT,"day_at_pixel_count"))
print()
mask = (N>0)
print("N_as / N_pix where N_pix > 0:")
print(s((NAS[mask] / N[mask]), "ratio  as_count / pixel_count"))
print("N_at / N_pix where N_pix > 0:")
print(s((NAT[mask] / N[mask]), "ratio  at_count / pixel_count"))
print("Are NAS == NAT in every cell?")
diff = np.where(np.isfinite(NAS) & np.isfinite(NAT), NAS-NAT, np.nan)
print(s(diff, "(as_count - at_count)"))

print()
print("="*100)
print("Q6: per-cell mean components (mean(sum)/N, after divide)")
print("="*100)
def perc(name, count_name):
    sv = data[name]; nv = data[count_name]
    ok = np.isfinite(sv) & np.isfinite(nv) & (nv>0)
    m = sv[ok]/nv[ok]
    print(s(m, f"per-cell mean  {name}/{count_name}"))

perc("day_sum_eastward_gradient","day_pixel_count")
perc("day_sum_northward_gradient","day_pixel_count")
perc("day_sum_magnitude_gradient","day_pixel_count")
perc("day_sum_grad_as_per_km",   "day_as_pixel_count")
perc("day_sum_grad_at_per_km",   "day_at_pixel_count")
perc("day_sum_grad_mag_per_km",  "day_as_pixel_count")

# Note: choice of count for grad_mag is a guess; try both
print()
print("Same per-cell mean using day_at_pixel_count as divisor for grad_mag and grad_as/at:")
perc("day_sum_grad_as_per_km",   "day_at_pixel_count")
perc("day_sum_grad_at_per_km",   "day_at_pixel_count")
perc("day_sum_grad_mag_per_km",  "day_at_pixel_count")
