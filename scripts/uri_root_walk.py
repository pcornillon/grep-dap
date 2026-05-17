#!/usr/bin/env python
"""Walk the URI OPeNDAP Hyrax root catalog one level deep.

Prints the first ~10 entries of each top-level container so the caller
can identify representative datasets without dragging back every page.
"""
import re
import urllib.request as ur

BASE = "https://sst-aqua.gso.uri.edu/opendap/"
TIMEOUT = 30

# Parse the root once.
root_html = ur.urlopen(BASE, timeout=TIMEOUT).read().decode()
top_dirs = sorted(set(re.findall(r'href="([^"]+)/contents.html', root_html)))
print("ROOT contains:")
for d in top_dirs:
    print(" ", d + "/")

# For each top-level dir, list ~first 20 entries.
for d in top_dirs:
    if d.startswith("%40"):  # @eaDir is a Synology NAS artifact, ignore
        continue
    url = f"{BASE}{d}/contents.html"
    try:
        html = ur.urlopen(url, timeout=TIMEOUT).read().decode()
    except Exception as e:
        print(f"\n[{d}] FAILED: {e}")
        continue
    dirs = sorted(set(re.findall(r'href="([^"]+)/contents.html', html)))
    files = sorted(set(re.findall(r'href="([^"\/]+\.(?:nc|h5|hdf|nc4|h5|nc3))(?:\.html)?"', html)))
    # Generic file pattern: anything with a known DAP-served extension.
    files_any = sorted(set(re.findall(r'<td align="left">\s*<a href="([^"\/]+\.[a-zA-Z0-9]+)\.html"', html)))
    print(f"\n[{d}/] {len(dirs)} subdirs, {len(files_any)} file-like entries")
    for sd in dirs[:10]:
        print(f"   dir : {sd}/")
    for f in files_any[:6]:
        print(f"   file: {f}")
    if len(dirs) > 10:
        print(f"   ... + {len(dirs)-10} more dirs")
    if len(files_any) > 6:
        print(f"   ... + {len(files_any)-6} more files")
