import json, os, re, csv

records = json.load(open("records.json"))
COMPANY_DIR = {"t":"00_shinkansen","h":"01_hokkaido","e":"02_east","c":"03_tokai",
 "w":"04_west","s":"05_shikoku","k":"06_kyushu","f":"07_freight"}
COMPANY_JP = {"t":"JR新幹線","h":"JR北海道","e":"JR東日本","c":"JR東海",
 "w":"JR西日本","s":"JR四国","k":"JR九州","f":"JR貨物"}

def san(s):
    s = s.lower(); s = re.sub(r'[^a-z0-9]+','-', s).strip('-'); s = re.sub(r'-{2,}','-', s)
    return s or "untitled"

rows=[]; seen={}
for r in records:
    d = COMPANY_DIR[r["pfx"]]
    base = san(r["en"]) or san(r["jp"])
    for im in r["imgs"]:
        stem = os.path.splitext(os.path.basename(im))[0]
        stem_s = san(stem)
        fn = f"{base}__{stem_s}.png"
        key=fn
        if fn in seen: fn = f"{base}__{stem_s}-{seen[fn]}.png"
        seen[key]=seen.get(key,0)+1
        rows.append({
            "company": COMPANY_JP[r["pfx"]],
            "jp_name": r["jp"],
            "en_name": r["en"],
            "orig_src": "f/"+os.path.basename(im),
            "file": f"jr_icons/{d}/{fn}"
        })

with open("jr_icons/_manifest.csv","w",newline="",encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["company","jp_name","en_name","orig_src","file"])
    w.writeheader(); w.writerows(rows)
print("manifest rows:", len(rows))
# also json for programmatic use
json.dump(rows, open("jr_icons/_manifest.json","w"), ensure_ascii=False, indent=1)
