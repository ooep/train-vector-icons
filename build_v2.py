import json, re
from collections import OrderedDict

recs = json.load(open("records.json"))
man = json.load(open("jr_icons/_manifest.json"))
mkey = {m["orig_src"]: m for m in man}
COMPANY = {"t":"JR新幹線","h":"JR北海道","e":"JR東日本","c":"JR東海","w":"JR西日本","s":"JR四国","k":"JR九州","f":"JR貨物"}

def local_files(r):
    out=[]
    for im in r["imgs"]:
        k = "f/"+im.split("/")[-1]
        if k in mkey: out.append(mkey[k]["file"].replace("jr_icons/",""))
    return out

def series_of(r):
    txt = r["en"]
    # E5/E6/E8/E231/N700S/700/800/223/225/323...
    s = set(re.findall(r'\b[EHNKDSPR]\d{2,4}[A-Z]?\b', txt))
    s |= set(re.findall(r'\b\d{3,4}[A-Z]?(?:-\d+)?\b', txt))
    # also from jp like 739, 323
    s |= set(re.findall(r'\b\d{3}\b', r["jp"]))
    return sorted(x for x in s if not x.startswith("20") or len(x)<=3 or True)

def retired(r):
    return r["jp"].startswith("*") or r["en"].startswith("*")

def classify(r):
    jp, en = r["jp"].strip(), r["en"]
    if r["pfx"]=="t": return "shinkansen"
    if r["pfx"]=="f": return "skip"
    # work / special vehicles
    if re.search(r'検測|除雪|機関|貨物|事業|測定|Working|Measurement|Measureing|Inspection|Test|chiki|キヤ|トラ|ホッパ|コンテナ|タンク|車掌|入換|入替|研修|訓練|レール輸送|保守|碎石|燃料電池|DMV|お召|ロイヤル|Royal|SL |蒸気|C11|D51|DD51|DE10|展示|博物館|museum|VVVF|試験|Future train|Future|Future', jp+en):
        return "skip"
    # area group?
    is_area = bool(re.search(r'地区|エリア|Area|area', jp+en))
    # line group?
    line_names = re.findall(r'[一-龥・/／]*線', jp)
    is_line = bool(line_names) and not re.search(r'特急|ライナー', jp)
    if is_line or (is_area and not re.search(r'特急|ライナー|快速', jp)):
        return "lines"
    return "tokkyu"

buckets = OrderedDict([("shinkansen",OrderedDict()),("tokkyu",OrderedDict()),("lines",OrderedDict())])

def add(bucket, key, r):
    key = key.lstrip("*★ ").strip()
    if not key: key = r["en"].lstrip("*")
    if key not in buckets[bucket]:
        buckets[bucket][key] = {"company":COMPANY[r["pfx"]],"jp":key,"series":[],"current_images":[],"retired_images":[],"all_retired":True}
    e = buckets[bucket][key]
    for f in local_files(r):
        if retired(r):
            if f not in e["retired_images"]: e["retired_images"].append(f)
        else:
            e["all_retired"]=False
            if f not in e["current_images"]: e["current_images"].append(f)
    for s in series_of(r):
        if s not in e["series"]: e["series"].append(s)

for r in recs:
    b = classify(r)
    if b=="skip": continue
    add(b, r["jp"] if b!="shinkansen" else r["jp"], r)

# stats
for k,v in buckets.items():
    cur = sum(1 for e in v.values() if not e["all_retired"])
    print(f"{k}: {len(v)} keys ({cur} current, {len(v)-cur} retired-only)")

json.dump(buckets, open("jr_icon_map_v2.json","w"), ensure_ascii=False, indent=1)

# CSV flat
import csv
with open("jr_icon_map_v2.csv","w",newline="",encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["bucket","company","name","series","current_images","retired_images","all_retired"])
    for bk,d in buckets.items():
        for k,e in d.items():
            w.writerow([bk,e["company"],k," ".join(e["series"]),
                        ";".join(e["current_images"]),";".join(e["retired_images"]),e["all_retired"]])
print("\nCSV rows:", sum(len(d) for d in buckets.values()))
