import json, re, os

recs = json.load(open("records.json"))
man = json.load(open("jr_icons/_manifest.json"))
# map orig_src -> local file
src2file = {m["orig_src"]: m["file"] for m in man}

COMPANY_DIR = {"t":"00_shinkansen","h":"01_hokkaido","e":"02_east","c":"03_tokai",
 "w":"04_west","s":"05_shikoku","k":"06_kyushu","f":"07_freight"}

# ---- classification ----
WORK_KW = re.compile(r'検測|除雪|機関|貨物|事業|測定|Working|Measurement|Measureing|Test|Inspection|Inspect|Train car|chiki|キヤ|トラ|ホッパ|コンテナ|タンク|車掌|入換|入替|研修|訓練|レール輸送|保守|碎石|燃料電池|ハイブリッド|DMV|災害')

def is_work(r):
    t = r["jp"]+" "+r["en"]
    return bool(WORK_KW.search(t))

def is_retired(r):
    return r["jp"].startswith("*") or r["en"].startswith("*") or "過去" in r["jp"]

# tokkyu 愛称 keywords (non-shinkansen named expresses)
TOKKYU = [
 "ライラック","カムイ","とかち","おおぞら","北斗","宗谷","サロベツ","オホーツク","大雪","はこだてライナー","フラノ","ノロッコ","流氷","スーパー","お召",
 "あずさ","かいじ","ひたち","ときわ","成田","サフィール","踊り子","草津","四万","日光","きぬがわ","いなほ","しらゆき","つがる","カシオペア","富士回遊","四季島","びゅう","さきがけ","はつかり","あかぎ","水上","伊豆","なごみ","お座敷","リゾート","快速",
 "ひだ","南紀","みえ","しなの","ふじかわ","あさぎり","ワイドビュー",
 "くろしお","やくも","サンダーバード","しらさぎ","こうのとり","はるか","はまかぜ","サンライズ","スーパーはくと","きのさき","まいづる","真如","まほろば","いにしへ","はなあかり","サンダー","東海道道中","TW","瑞風","ウエストエクスプレス","銀河","花嫁","ベルもんた","あめつち","○○のはなし","遊人","○○のはなし",
 "しおかぜ","いしづち","剣山","むろと","マリンライナー","南風","しまんと","宇和海","足摺","アンパンマン","モノレール","とろっこ","トロッコ","伊予灘","千年","夜明け","しまん",
 "ソニック","かもめ","みどり","ハウステンボス","ゆふ","きりしま","にちりん","かんぱち","ふたつ星","36ぷらす3","ななつ星","或る列車","いさぶろう","しんぺい","SL人吉","指宿","たまて箱","A列車","海幸山幸","九州横断","ひのくに","シーボルト","あそぼーい","海幸","やませみ","かわせみ","海幸山幸","ふたつ","4047",
]
def is_tokkyu(r):
    if r["pfx"]=="t": return False
    t = r["jp"]
    # line-named groups are not tokkyu
    if re.search(r'[一-龥]*線', t) and not any(k in t for k in ["特急","ライナー","快速"]):
        # has explicit 線 as main label -> likely line group, unless it also names an express
        pass
    for k in TOKKYU:
        if k in t:
            # exclude if pure line name like 常磐線
            return True
    return False

def is_line(r):
    t = r["jp"]
    if r["pfx"] in ("t","f"): return False
    # contains 線 but not as part of express name
    m = re.findall(r'[一-龥・/／]*線', t)
    return len(m)>0

# bucket
buckets = {"shinkansen":[],"tokkyu":[],"lines":[],"work":[],"other":[]}
for r in recs:
    retired = is_retired(r)
    if is_work(r):
        buckets["work"].append((r,retired)); continue
    if r["pfx"]=="t":
        buckets["shinkansen"].append((r,retired)); continue
    if is_tokkyu(r) and not re.search(r'線$|線[/／・]', r["jp"]):
        buckets["tokkyu"].append((r,retired)); continue
    if is_line(r):
        buckets["lines"].append((r,retired)); continue
    buckets["other"].append((r,retired))

for k,v in buckets.items():
    print(f"== {k}: {len(v)} 组 ==")
