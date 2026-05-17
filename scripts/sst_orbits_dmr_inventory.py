"""Comprehensive DMR inventory of an SST_Orbits sample file.

Parses the DAP4 DMR XML and emits, for every variable (root + every
group), the variable's type, fully qualified name, dimensions, and
every attribute present (name -> value). The output is structured
enough to feed downstream COARDS scoring.
"""
import json
import re
import urllib.request as ur
from collections import OrderedDict

URL = ("https://sst-aqua.gso.uri.edu/opendap/SST_Orbits/2024/01/"
       "AQUA_MODIS_orbit_115220_20240101T011558_L2_SST-URI_24-2.nc4.dmr.xml")

# Standard DAP4 numeric/string atomic types.
ATOMIC = ("Byte", "Int8", "UInt8", "Int16", "UInt16", "Int32", "UInt32",
          "Int64", "UInt64", "Float32", "Float64", "String", "URL", "Char")
ATOMIC_RE = "|".join(ATOMIC)

# DMR XML namespace prefix is the default xmlns; strip it by ignoring.
def strip_ns(text):
    return re.sub(r'\sxmlns(:\w+)?="[^"]+"', "", text)

text = ur.urlopen(URL, timeout=30).read().decode()
text = strip_ns(text)

def parse_attributes(block):
    """Pull <Attribute name="X" type="T"><Value>v</Value>...</Attribute> entries.
    Only top-level attribute children of `block` (not nested inside
    inner variables). Returns OrderedDict name -> list of values."""
    attrs = OrderedDict()
    # depth-aware pass: walk through, skipping anything between < and matching </
    i = 0
    n = len(block)
    while True:
        m = re.search(r'<Attribute\s+name="([^"]+)"\s+type="([^"]+)"\s*>',
                      block[i:])
        if not m: break
        a_start = i + m.start()
        # find matching </Attribute>
        m_end = re.search(r'</Attribute\s*>', block[a_start:])
        if not m_end: break
        a_body = block[a_start + m.end()-m.start():a_start + m_end.start()]
        # only accept this attribute if it is at the "top level" of `block`:
        # check no unmatched <Group / <variable / <Attribute exists in block[:a_start]
        # without its closing tag. Simpler: require the Attribute is a direct
        # child by counting open vs close of (Group|Attribute|<ATOMIC ... >)
        # tags before a_start.
        prefix = block[:a_start]
        opens  = len(re.findall(r'<(?:Group|Attribute|'+ATOMIC_RE+r')\b[^>/]*>', prefix))
        closes = len(re.findall(r'</(?:Group|Attribute|'+ATOMIC_RE+r')>', prefix))
        if opens == closes:
            name = m.group(1); typ = m.group(2)
            vals = re.findall(r'<Value>([^<]*)</Value>', a_body)
            attrs[name] = (typ, vals)
        i = a_start + m_end.end()
    return attrs

def parse_variables_in_block(block, group_path):
    """Find atomic-type variables that are direct children of `block`,
    excluding those that live inside any inner <Group> ... </Group>."""
    # Mask out group bodies so we don't see vars inside subgroups.
    masked = mask_subgroups(block)
    out = []
    for m in re.finditer(
        rf'<({ATOMIC_RE})\s+name="([^"]+)"(\s*/>|\s*>)', masked):
        typ = m.group(1); name = m.group(2); ender = m.group(3)
        start = m.start()
        if ender.strip() == "/>":
            body = ""
            end = m.end()
        else:
            # match its closing tag respecting nesting; for DAP4 atomic
            # variables they don't nest other atomic vars, so a plain
            # regex find is safe.
            mclose = re.search(rf'</{typ}\s*>', masked[m.end():])
            if not mclose: continue
            body = masked[m.end():m.end()+mclose.start()]
            end  = m.end()+mclose.end()
        dims = re.findall(r'<Dim\s+name="([^"]+)"\s*/>', body)
        attrs = parse_attributes(body)
        out.append({
            "type":   typ,
            "fqn":    group_path + "/" + name if group_path else "/" + name,
            "name":   name,
            "dims":   dims,
            "attrs":  {k: (t, vs) for k,(t,vs) in attrs.items()},
        })
    return out

def mask_subgroups(block):
    """Replace every <Group ...>...</Group> body (recursively) with spaces
    so regexes against `block` only see the current level."""
    out = list(block)
    pos = 0
    while True:
        m = re.search(r'<Group\s+name="[^"]+"\s*>', "".join(out[pos:]))
        if not m: break
        s = pos + m.start()
        depth = 1
        i = pos + m.end()
        while i < len(out) and depth > 0:
            mm = re.search(r'<(/?)Group\b[^>]*>', "".join(out[i:]))
            if not mm: break
            if mm.group(1) == "":
                depth += 1
            else:
                depth -= 1
            i += mm.end()
        # blank out s..i but leave the original tags intact at the start/end
        # so atomic-var search isn't confused; simplest: blank out body
        # between the start tag end and the matching close tag start.
        # For our purposes, blank out the entire region s..i.
        for k in range(s, i):
            out[k] = " "
        pos = i
    return "".join(out)

def parse_dimensions(block):
    return re.findall(r'<Dimension\s+name="([^"]+)"\s+size="(\d+)"', block)

def walk_groups(block, group_path=""):
    """Recursively yield (group_path, body_block) for each group; root included."""
    yield (group_path, block)
    # find direct subgroups
    pos = 0
    while True:
        m = re.search(r'<Group\s+name="([^"]+)"\s*>', block[pos:])
        if not m: break
        gs = pos + m.start()
        gn = m.group(1)
        # find matching close
        depth = 1
        i = pos + m.end()
        while i < len(block) and depth > 0:
            mm = re.search(r'<(/?)Group\b[^>]*>', block[i:])
            if not mm: break
            if mm.group(1) == "": depth += 1
            else:                 depth -= 1
            i += mm.end()
        body = block[pos + m.end(): i - len('</Group>')]
        yield from walk_groups(body, group_path + "/" + gn)
        pos = i

# Drop the outer <Dataset ...> wrapper to operate on its inner content.
mds = re.search(r'<Dataset[^>]*>(.*)</Dataset>', text, re.S)
inner = mds.group(1) if mds else text

result = {
    "url": URL,
    "groups": [],
}
for gpath, gbody in walk_groups(inner, ""):
    dims = parse_dimensions(mask_subgroups(gbody))
    vars_ = parse_variables_in_block(gbody, gpath)
    g_attrs = OrderedDict()
    # group-level attributes are Attribute elements that are direct children
    # of the group/root block; reuse parse_attributes on a copy where the
    # variable bodies are blanked out (so we don't pick up var attrs).
    masked = mask_subgroups(gbody)
    for typ in ATOMIC:
        masked = re.sub(rf'<{typ}\s+name="[^"]+"\s*/>', "", masked)
        masked = re.sub(rf'<{typ}\s+name="[^"]+"\s*>.*?</{typ}>', "",
                        masked, flags=re.S)
    g_attrs = parse_attributes(masked)
    result["groups"].append({
        "path":  gpath or "/",
        "dimensions": dims,
        "global_attributes": {k: (t, vs) for k,(t,vs) in g_attrs.items()},
        "variables": vars_,
    })

import sys
print(json.dumps(result, indent=2))
