#!/usr/bin/env python
"""Walk the publicly accessible directories on the URI Hyrax server.

After probing, only SST_Orbits/ and gradients_by_period/ return 200; the
others return Hyrax 403 (filesystem perms). For each public branch we
recursively list, capping at a reasonable depth and per-page count.
"""
import re
import urllib.request as ur

BASE = "https://sst-aqua.gso.uri.edu/opendap/"
TIMEOUT = 30

LINK_DIR  = re.compile(r'href="([^"\s]+)/contents\.html')
# matches the <td align="left"><a href="FILE.html"> ... wrappers
LINK_FILE = re.compile(r'<td align="left">\s*<a href="([^"]+?\.[a-zA-Z0-9_]+)\.html"', re.S)

def get(url):
    try:
        return ur.urlopen(url, timeout=TIMEOUT).read().decode()
    except Exception as e:
        return f"<<ERR: {e}>>"

def listing(path):
    """Return (subdirs, files) for a Hyrax contents.html page."""
    html = get(BASE + path + "contents.html")
    if html.startswith("<<ERR"):
        return None, None
    subs = sorted(set(LINK_DIR.findall(html)))
    # filter out external/mailto and self
    subs = [s for s in subs if not s.startswith(("mailto:", "http", "%40eaDir"))]
    files = sorted(set(LINK_FILE.findall(html)))
    return subs, files

def walk(path, depth=0, max_depth=3, show_files=4):
    subs, files = listing(path)
    if subs is None:
        print("  " * depth + f"[ERR] {path}")
        return
    print("  " * depth + f"{path or '/'}  ({len(subs)} dirs, {len(files)} files)")
    for f in files[:show_files]:
        print("  " * (depth + 1) + f"file: {f}")
    if len(files) > show_files:
        print("  " * (depth + 1) + f"... +{len(files)-show_files} more files")
    if depth >= max_depth:
        if subs:
            print("  " * (depth + 1) + f"[stop at max_depth; {len(subs)} subdirs not expanded]")
        return
    # Walk only a sample of subdirectories at deeper levels.
    sample = subs if depth == 0 else subs[:3]
    for s in sample:
        walk(path + s + "/", depth + 1, max_depth, show_files)
    if depth > 0 and len(subs) > len(sample):
        print("  " * (depth + 1) + f"... +{len(subs)-len(sample)} more dirs at this level")

for branch in ("SST_Orbits/", "gradients_by_period/"):
    print("=" * 70)
    walk(branch, max_depth=2, show_files=3)
