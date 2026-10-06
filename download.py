import json, os, re, time, hashlib, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "http://www.trainfrontview.net/"
records = json.load(open("records.json"))

COMPANY_DIR = {
 "t":"00_shinkansen","h":"01_hokkaido","e":"02_east","c":"03_tokai",
 "w":"04_west","s":"05_shikoku","k":"06_kyushu","f":"07_freight"
}
OUT = "jr_icons"
os.makedirs(OUT, exist_ok=True)

def san(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+','-', s).strip('-')
    s = re.sub(r'-{2,}','-', s)
    return s or "untitled"

# build download plan: (url, out_path)
plan = []
manifest = []
seen_names = {}
for r in records:
    d = os.path.join(OUT, COMPANY_DIR[r["pfx"]])
    os.makedirs(d, exist_ok=True)
    base = san(r["en"]) or san(r["jp"])
    for im in r["imgs"]:
        stem = os.path.splitext(os.path.basename(im))[0]
        stem_s = san(stem)
        fn = f"{base}__{stem_s}.png"
        # dedupe
        key = fn
        if fn in seen_names:
            fn = f"{base}__{stem_s}-{seen_names[fn]}.png"
        seen_names[key] = seen_names.get(key,0)+1
        out = os.path.join(d, fn)
        plan.append((BASE+im, out, im, r))

print("to download:", len(plan))

def one(job):
    url, out, orig, r = job
    if os.path.exists(out) and os.path.getsize(out) > 100:
        return ("skip", out)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read()
            if len(data) < 100 or data[:4] != b'\x89PNG':
                raise ValueError("not png: %d bytes %r" % (len(data), data[:8]))
            open(out,"wb").write(data)
            return ("ok", out)
        except Exception as e:
            if attempt == 2: return ("fail", f"{url} :: {e}")
            time.sleep(1.5*(attempt+1))

fails=[]; oks=0; skips=0
with ThreadPoolExecutor(max_workers=8) as ex:
    for res in ex.map(one, plan):
        if res[0]=="ok": oks+=1
        elif res[0]=="skip": skips+=1
        else: fails.append(res[1])

print("downloaded:", oks, "skipped:", skips, "failed:", len(fails))
for f in fails[:20]: print("FAIL", f)
json.dump(fails, open("fails.json","w"))
