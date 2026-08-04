"""COARDS audit for the SST_Orbits sample file.

Reads /tmp/sst_inv.json (produced by sst_orbits_dmr_inventory.py) and
classifies each variable's COARDS completeness, listing missing
attributes and proposed best-guess values. Also lists CF/ACDD-style
recommendations not strictly required by COARDS.

COARDS criteria applied per variable:
  - units            (UDUNITS-compliant string)
  - long_name        (recommended; treated as required by this audit)
  - _FillValue       (if any data can be missing -- treated as required
                      for all but scalars)
  - scale_factor/add_offset (required together when raw dtype is packed
                      integer with a non-trivial scale)
  - For 'time' variables: units must be of form '<unit> since <REF>'
  - For latitude:  units must be one of {degrees_north, degree_north,
                   degree_N, degrees_N, degreeN, degreesN}
  - For longitude: units must be one of the corresponding east set

Coordinate-axis classification (lat/lon/time) is by standard_name
*or* by units pattern *or* by a name match.
"""
import json
import re
from collections import OrderedDict

UDUNITS_BAD_OK_MAP = {
    "C":   "degree_Celsius",   # not UDUNITS; suggest replacement
    "C/km": "degree_Celsius km-1",
    "seconds": None,  # depends -- for time variables needs reference
}

LAT_UNITS_OK = {"degrees_north","degree_north","degree_N","degrees_N","degreeN","degreesN"}
LON_UNITS_OK = {"degrees_east","degree_east","degree_E","degrees_E","degreeE","degreesE"}

def first(vs): return vs[0] if vs else None

def is_lat(name, attrs):
    sn = first(attrs.get("standard_name",(None,[]))[1]) if "standard_name" in attrs else None
    un = first(attrs.get("units",(None,[]))[1]) if "units" in attrs else None
    return (sn == "latitude") or (un in LAT_UNITS_OK) or (name.lower().endswith("latitude"))

def is_lon(name, attrs):
    sn = first(attrs.get("standard_name",(None,[]))[1]) if "standard_name" in attrs else None
    un = first(attrs.get("units",(None,[]))[1]) if "units" in attrs else None
    return (sn == "longitude") or (un in LON_UNITS_OK) or (name.lower().endswith("longitude"))

def is_time(name, attrs):
    sn = first(attrs.get("standard_name",(None,[]))[1]) if "standard_name" in attrs else None
    ln = first(attrs.get("long_name",(None,[]))[1]) if "long_name" in attrs else None
    if sn == "time": return True
    if name.lower() in ("time","datetime","date_time"): return True
    # Heuristic: a time-of-event variable has long_name like "... since YYYY-..."
    if ln and "since" in ln.lower() and any(d in ln for d in ("19","20")):
        return True
    if sn and ("start_time" in sn or "end_time" in sn):
        return True
    return False

def is_string_var(typ):
    return typ in ("String","URL","Char")

def attr_value(attrs, key):
    if key not in attrs: return None
    return first(attrs[key][1])

def audit_var(v):
    """Return dict with status, missing_coards (list of dicts), notes."""
    name = v["name"]; typ = v["type"]; dims = v["dims"]
    a = v["attrs"]
    units = attr_value(a, "units")
    long_name = attr_value(a, "long_name")
    fill = attr_value(a, "_FillValue") or attr_value(a, "missing_value")
    scale = attr_value(a, "scale_factor")
    offset = attr_value(a, "add_offset")
    missing = []
    # ------ units check ------
    if is_string_var(typ):
        pass  # strings don't need units
    elif units is None:
        # Suggest based on variable role
        if "count" in name.lower() or "index" in name.lower() or "_pixel_count" in name.lower():
            guess = "1"
        elif "mask" in name.lower() or "qual" in name.lower() or "quality" in name.lower():
            guess = "1"
        else:
            guess = "1"
        missing.append({"attr":"units","reason":"absent",
                        "guess": guess})
    else:
        # Validate units when present
        if is_lat(name,a) and units not in LAT_UNITS_OK:
            missing.append({"attr":"units","reason":f"'{units}' is not a COARDS latitude unit",
                            "guess":"degrees_north"})
        elif is_lon(name,a) and units not in LON_UNITS_OK:
            missing.append({"attr":"units","reason":f"'{units}' is not a COARDS longitude unit",
                            "guess":"degrees_east"})
        elif is_time(name,a) and "since" not in units:
            # Time variable -- units must include a reference
            guess = "seconds since 1970-01-01 00:00:00 UTC"
            missing.append({"attr":"units","reason":f"time variable but units '{units}' has no reference",
                            "guess":guess})
        elif units in ("C",) :
            missing.append({"attr":"units","reason":"'C' is not UDUNITS (would be coulomb)",
                            "guess":"degree_Celsius"})
        elif units in ("C/km",):
            missing.append({"attr":"units","reason":"'C/km' uses non-UDUNITS 'C' and '/'",
                            "guess":"degree_Celsius km-1"})
        # Mismatched units for wind speed labelled mm
        if name in ("L2eqa_AMSR_E_wind_speed",) and units == "mm":
            missing.append({"attr":"units","reason":"wind speed labelled 'mm' (almost certainly wrong)",
                            "guess":"m s-1"})
        # Mismatched units for pixel-count labelled C
        if name in ("L2eqa_MODIS_num_SST",) and units == "C":
            missing.append({"attr":"units","reason":"pixel count labelled 'C' (wrong; it's a count)",
                            "guess":"1"})
    # ------ long_name ------
    if long_name is None and not is_string_var(typ):
        # propose from name itself
        missing.append({"attr":"long_name","reason":"absent","guess":name.replace("_"," ")})
    # ------ _FillValue ------
    if fill is None and not is_string_var(typ) and len(dims) > 0:
        # scalars and strings excluded
        if typ.startswith("Float"):
            missing.append({"attr":"_FillValue","reason":"absent","guess":"NaN"})
        elif typ in ("Int8","UInt8","Byte"):
            missing.append({"attr":"_FillValue","reason":"absent","guess":"-1"})
        elif typ.startswith("Int") or typ.startswith("UInt"):
            missing.append({"attr":"_FillValue","reason":"absent",
                            "guess":"type-specific (e.g. -32767 for Int16)"})
    # ------ scale/offset coherence ------
    # If add_offset given, scale_factor must also be given (and vice versa);
    # if neither given but dtype is packed and we know it should be packed,
    # flag. We only flag pairs.
    if (scale is None) != (offset is None):
        missing.append({"attr":"scale_factor/add_offset",
                        "reason":"one present, the other absent",
                        "guess":"both should be set together"})

    status = "Complete" if not missing else "Incomplete"
    return {"name":name, "type":typ, "dims":dims, "status":status,
            "missing_coards":missing, "units":units, "long_name":long_name,
            "fill":fill, "scale":scale, "offset":offset,
            "standard_name": attr_value(a,"standard_name"),
            "valid_min": attr_value(a,"valid_min"),
            "valid_max": attr_value(a,"valid_max")}

def recommend_extra(v):
    """Recommendations beyond COARDS."""
    name = v["name"]; typ = v["type"]; dims = v["dims"]; a = v["attrs"]
    recs = []
    n = name.lower()
    # 2D data variables that aren't themselves coordinates: recommend
    # coordinates and ancillary_variables.
    is_data2d = (len(dims) == 2 and not is_string_var(typ) and
                 not is_lat(name,a) and not is_lon(name,a))
    if is_data2d:
        if "SST" in name or "sst" in name:
            recs.append(("coordinates","\"latitude longitude DateTime\""))
            recs.append(("ancillary_variables","\"qual_sst refined_mask\""))
            recs.append(("cell_methods","\"area: point\""))
            recs.append(("source","\"MODIS Aqua L2 SST, NASA OceanColor (oceandata.sci.gsfc.nasa.gov)\""))
        elif "gradient" in n:
            recs.append(("coordinates","\"latitude longitude DateTime\""))
            recs.append(("ancillary_variables","\"refined_mask qual_sst\""))
            recs.append(("cell_methods",
                "\"ny: derivative nx: derivative (interval: 1 pixel)\""))
            recs.append(("comment",
                "\"East / North components of in-pixel SST gradient computed from regridded_sst.\""))
        elif "mask" in n or "qual" in n:
            recs.append(("flag_values","\"0 1\" (mask) or \"0 1 2 3 4\" (qual)"))
            recs.append(("flag_meanings","\"good bad\" / \"best good questionable bad notprocessed\""))
            recs.append(("comment","\"Replace malformed 'flag_masks=0' with proper flag_values.\""))
    # time variables
    if is_time(name,a):
        recs.append(("calendar","\"gregorian\""))
        recs.append(("axis","\"T\""))
    # latitude variables
    if is_lat(name,a):
        recs.append(("axis","\"Y\""))
    if is_lon(name,a):
        recs.append(("axis","\"X\""))
    # AMSR-E variables: instrument provenance and the AMSR-E retirement caveat
    if "AMSR" in name:
        recs.append(("source","\"AMSR-E aboard NASA Aqua (data only available 2002-06 to 2011-10)\""))
        recs.append(("comment","\"In 2024-era orbit files this field is 1x1 placeholder (AMSR-E retired 2011-10).\""))
    # File-name / orbit-number variables would benefit from provenance attrs
    if "granule" in n or "filenames" in n:
        recs.append(("comment","\"Source granule filenames from oceandata.sci.gsfc.nasa.gov\""))
    return recs

inv = json.load(open("/tmp/sst_inv.json"))
audit = {"global_attributes_by_group": {}, "variables": []}
for g in inv["groups"]:
    audit["global_attributes_by_group"][g["path"]] = g["global_attributes"]
    for v in g["variables"]:
        a = audit_var(v)
        a["group"] = g["path"]
        a["fqn"]   = (g["path"].rstrip("/") + "/" + v["name"]) if g["path"]!="/" else "/"+v["name"]
        a["recommendations"] = recommend_extra(v)
        audit["variables"].append(a)

# Summary
total = len(audit["variables"])
complete = sum(1 for v in audit["variables"] if v["status"]=="Complete")
print(f"Total variables: {total}")
print(f"COARDS Complete : {complete}")
print(f"COARDS Incomplete: {total-complete}")
print()
print("Variables by group:")
for g in inv["groups"]:
    cnt = sum(1 for v in audit["variables"] if v["group"]==g["path"])
    com = sum(1 for v in audit["variables"] if v["group"]==g["path"] and v["status"]=="Complete")
    print(f"  {g['path']:30s} {com:2d}/{cnt:2d} complete")

import json as _j
with open("/tmp/sst_audit.json","w") as fh:
    _j.dump(audit, fh, indent=2)
print("\nWrote /tmp/sst_audit.json")
