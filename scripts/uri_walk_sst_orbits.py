"""Walk only SST_Orbits/ first; cap at depth 2, sample 2 children per level."""
import re, urllib.request as ur
BASE = "https://sst-aqua.gso.uri.edu/opendap/"
LINK_DIR  = re.compile(r'href="([^"\s]+)/contents\.html')
LINK_FILE = re.compile(r'<td align="left">\s*<a href="([^"]+?\.[a-zA-Z0-9_]+)\.html"', re.S)
def listing(path):
    try:
        html = ur.urlopen(BASE + path + "contents.html", timeout=20).read().decode()
    except Exception as e:
        return None, None, str(e)
    subs  = [s for s in sorted(set(LINK_DIR.findall(html))) if not s.startswith(("mailto:","http","%40eaDir"))]
    files = sorted(set(LINK_FILE.findall(html)))
    return subs, files, None
def walk(path, depth=0, max_depth=2, sample=2, show_files=3):
    subs, files, err = listing(path)
    if err: print("  "*depth + f"[ERR {path}: {err}]"); return
    print("  "*depth + f"{path or '/'}  ({len(subs)} dirs, {len(files)} files)")
    for f in files[:show_files]: print("  "*(depth+1) + f"file: {f}")
    if len(files) > show_files: print("  "*(depth+1) + f"... +{len(files)-show_files} more files")
    if depth >= max_depth: 
        if subs: print("  "*(depth+1) + f"[+{len(subs)} unexpanded]")
        return
    pick = subs if depth==0 else subs[:sample]
    for s in pick: walk(path+s+"/", depth+1, max_depth, sample, show_files)
    if depth>0 and len(subs)>len(pick):
        print("  "*(depth+1) + f"... +{len(subs)-len(pick)} more dirs at this level")
walk("SST_Orbits/", max_depth=2, sample=2)
