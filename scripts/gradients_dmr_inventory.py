"""DMR inventory for a sample gradients_by_period file.

Confirm what's there: dimensions, variables, attrs (expecting nothing
beyond structure). Try several files across the period to make sure
the schema is constant.
"""
import re
import urllib.request as ur

BASE = "https://sst-aqua.gso.uri.edu/opendap/gradients_by_period/"
ATOMIC = ("Byte","Int8","UInt8","Int16","UInt16","Int32","UInt32",
          "Int64","UInt64","Float32","Float64","String","URL","Char")

def fetch_dmr(fname):
    url = BASE + fname + ".dmr.xml"
    text = ur.urlopen(url, timeout=30).read().decode()
    return text

def summarize(text):
    dims = re.findall(r'<Dimension\s+name="([^"]+)"\s+size="(\d+)"', text)
    vars_ = []
    for m in re.finditer(rf'<({"|".join(ATOMIC)})\s+name="([^"]+)"\s*(/>|>)', text):
        typ, name, ender = m.group(1), m.group(2), m.group(3)
        if ender == "/>":
            body = ""
        else:
            mclose = re.search(rf'</{typ}\s*>', text[m.end():])
            body = text[m.end():m.end()+mclose.start()] if mclose else ""
        ds = re.findall(r'<Dim\s+name="([^"]+)"\s*/>', body)
        attrs = re.findall(r'<Attribute\s+name="([^"]+)"\s+type="[^"]+">\s*<Value>([^<]*)</Value>', body)
        vars_.append((typ, name, ds, attrs))
    # global attributes
    # strip out variable bodies first
    masked = text
    for t in ATOMIC:
        masked = re.sub(rf'<{t}\s+name="[^"]+"\s*/>', '', masked)
        masked = re.sub(rf'<{t}\s+name="[^"]+"\s*>.*?</{t}>', '', masked, flags=re.S)
    glob = re.findall(r'<Attribute\s+name="([^"]+)"\s+type="[^"]+">\s*<Value>([^<]*)</Value>', masked)
    return dims, vars_, glob

# Check a few files across the period
for f in ("augmented_monthly_stats_01_2003.nc",
          "augmented_monthly_stats_07_2020.nc",
          "augmented_monthly_stats_12_2024.nc"):
    print(f"\n=== {f} ===")
    text = fetch_dmr(f)
    dims, vars_, glob = summarize(text)
    print(f"  Dimensions:  {dims}")
    print(f"  Global attrs ({len(glob)}): {glob}")
    nattrs = sum(len(a) for _,_,_,a in vars_)
    print(f"  Variables ({len(vars_)}); total attrs across all vars: {nattrs}")
    if vars_:
        # show variable type/name (suppress attrs if all empty)
        for typ, name, ds, attrs in vars_:
            print(f"    {typ:8s} {name:42s} dims={ds}  attrs={attrs}")
