import json, re, os
from collections import OrderedDict

recs = json.load(open("records.json"))
man = {m["orig_src"]: m for m in json.load(open("jr_icons/_manifest.json"))}
COMPANY = {"t":"JR新幹線","h":"JR北海道","e":"JR東日本","c":"JR東海","w":"JR西日本","s":"JR四国","k":"JR九州","f":"JR貨物"}

def local_files(r):
    out=[]
    for im in r["imgs"]:
        key = "f/"+im.split("/")[-1]
        if key in man: out.append(man[key]["file"].replace("jr_icons/",""))
    return out

def extract_series(r):
    """pull series tokens like E5, H5, 223, 287 from english label"""
    txt = r["en"]
    # E### / N700 / 313 etc
    ser = set(re.findall(r'\b[EHJKPRS]\d{2,3}[A-Z]?\b', txt))
    ser |= set(re.findall(r'\b\d{3}[A-Z]?(?:-\d+)?\b', txt))
    return sorted(ser)

def retired(r):
    return r["jp"].startswith("*") or r["en"].startswith("*")

# ---- classify each group into one bucket ----
def bucket(r):
    jp, en = r["jp"], r["en"]
    if r["pfx"]=="t": return "shinkansen"
    if r["pfx"]=="f": return "freight"
    # work / special
    if re.search(r'検測|除雪|機関|貨物|事業|測定|Working|Measurement|Measureing|Inspection|Test|chiki|キヤ|トラ|ホッパ|コンテナ|タンク|車掌|入換|入替|研修|訓練|レール輸送|保守|碎石|燃料電池|DMV|お召|ロイヤル|Royal|イベント|SL |蒸気|C11|D51|DD51|DE10|展示|博物館|museum|博物', jp+en):
        return "work"
    return None

# Build grouped entries. Key = normalized Japanese label.
shinkansen, tokkyu, lines = OrderedDict(), OrderedDict(), OrderedDict()

def add(d, key, r):
    if key not in d:
        d[key] = {"company":COMPANY[r["pfx"]], "jp":key, "series":[], "images":[], "retired_all":True, "current_images":[]}
    e = d[key]
    if not retired(r): e["retired_all"]=False
    for f in local_files(r):
        if f not in e["images"]: e["images"].append(f)
        if not retired(r) and f not in e["current_images"]: e["current_images"].append(f)
    for s in extract_series(r):
        if s not in e["series"]: e["series"].append(s)

for r in recs:
    b = bucket(r)
    jp = r["jp"].strip()
    if b=="shinkansen":
        # key = the love name; use jp but clean * prefix
        key = jp.lstrip("*★ ").strip() or r["en"]
        add(shinkansen, key, r)
    elif b in ("work","freight"):
        continue
    else:
        # tokkyu vs line
        # line if label primarily names 線
        line_m = re.findall(r'[一-龥・/／]*線', jp)
        has_tokyu_word = re.search(r'特急|ライナー|快速|エアポート', jp)
        if line_m and not (has_tokyu_word and not re.search(r'線$', jp)):
            key = jp.lstrip("*★ ").strip()
            add(lines, key, r)
        else:
            key = jp.lstrip("*★ ").strip() or r["en"]
            add(tokkyu, key, r)

out = {"shinkansen":shinkansen,"tokkyu":tokkyu,"lines":lines}
json.dump(out, open("jr_icon_map.json","w"), ensure_ascii=False, indent=1)
print(f"shinkansen: {len(shinkansen)} keys, tokkyu: {len(tokkyu)} keys, lines: {len(lines)} keys")
print("\n--- shinkansen keys ---")
for k,v in shinkansen.items(): print(f"  {k:24s} series={v['series']} imgs={len(v['images'])} retired={v['retired_all']}")
