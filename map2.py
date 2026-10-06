import json, re

groups = json.load(open("all_groups.json"))
# 不挑现役退役，全部有图的都能用
allg = [g for g in groups if g["files"]]

tm = json.load(open("/home/user/Doubao/chats/38445511791035394/japanrail/mini-japanrail-3d/data/tmaps.json"))
real = set()
for e in tm.values():
    for ln in e.get("lines", []):
        real.add(ln)

done = json.load(open("line_icons_new.json"))
missing = sorted(real - set(done.keys()))

def core_variants(line):
    """生成线路名的多种归一化形式"""
    s = line
    out = set()
    # 去 N号線 前缀
    s2 = re.sub(r'^\d+号線', '', s)
    out.add(s2)
    out.add(s2.replace('線',''))
    out.add(s2.replace('本線',''))
    # 去 jr 前缀
    s3 = re.sub(r'^(jr|JR)', '', s2)
    out.add(s3)
    out.add(s3.replace('線',''))
    # 去常见公司前缀
    for pre in ["東京メトロ","都営","大阪メトロ","札幌市営","横浜市営","神戸市営","福岡市","名古屋市",
                "仙台市","広島電鉄","広電","長崎電気軌道","鹿児島市電","熊本市電","函館市電",
                "富山地方鉄道","富山軌道","伊予鉄道","札幌市営地下鉄","横浜市営地下鉄",
                "神戸市営地下鉄","福岡市地下鉄","千葉都市","多摩都市","沖縄都市","大阪モノレール",
                "東京モノレール","北九州モノレール","国際文化公園都市","東京臨海新交通",
                "広島新交通","東部丘陵","地下鉄","市営","電鉄","電気軌道","鉄道","軌道","本線","支線","支線"]:
        v = s3.replace(pre, '')
        out.add(v)
        out.add(v.replace('線',''))
    return [v for v in out if len(v) >= 2]

def find(line):
    cands = []
    vs = core_variants(line)
    for g in allg:
        jp = g["jp"]
        en = g["en"].lower()
        sc = 0
        for v in vs:
            vl = v.lower()
            if len(vl) < 2: continue
            if vl in jp.lower(): sc += 10
            if vl in en: sc += 6
        # 双向：group jp 的核心词出现在 line 里
        gjp = jp.replace('線','').replace('*','').strip()
        # group 标签里可能有多个线路名用 / 分隔
        for part in re.split(r'[/／]', gjp):
            part = part.strip().replace('線','')
            if len(part) >= 2 and part.lower() in line.lower():
                sc += 8
        if sc > 0:
            cands.append((sc, g))
    cands.sort(key=lambda x: -x[0])
    return cands[0] if cands else None

result = dict(done)
still = []
for line in missing:
    r = find(line)
    if r and r[0] >= 8:
        result[line] = r[1]["files"][:2]
    else:
        still.append((line, r[1]["jp"] if r else "?", r[0] if r else 0))

json.dump(result, open("line_icons_new.json", "w"), ensure_ascii=False, indent=1)
print(f"现在覆盖: {len(result)}/{len(real)}, 还缺: {len(still)}")
print("\n=== 仍缺 ===")
for line, near, sc in still:
    print(f"  {line:28s} sc={sc} 最近={near}")
