import json, re

groups = json.load(open("all_groups.json"))
# 只保留有图的、现役的（不以*开头），*号是退役/旧涂装
live = [g for g in groups if g["files"] and not g["jp"].startswith("*")]
retired = [g for g in groups if g["files"] and g["jp"].startswith("*")]

tm = json.load(open("/home/user/Doubao/chats/38445511791035394/japanrail/mini-japanrail-3d/data/tmaps.json"))
real = set()
for e in tm.values():
    for ln in e.get("lines", []):
        real.add(ln)

# 已有映射
done = json.load(open("line_icons_new.json"))
missing = sorted(real - set(done.keys()))
print(f"待映射: {len(missing)}")

def tokens(line):
    """从线路名提取可匹配的核心词"""
    s = line
    # 去掉"N号線"前缀（如 1号線東山線 → 東山線）
    s = re.sub(r'^\d+号線', '', s)
    # 去掉 jr / 公司前缀
    s = re.sub(r'^(jr|JR)', '', s)
    # 去掉常见公司前缀（保留后面的线路名）
    for pre in ["東京メトロ","都営","大阪メトロ","札幌市営","横浜市営","神戸市営","福岡市","名古屋市",
                "仙台市","広島電鉄","広電","長崎電気軌道","鹿児島市電","熊本市電","函館市電",
                "富山地方鉄道","富山軌道","伊予鉄道","熊本市電","札幌市営地下鉄","横浜市営地下鉄",
                "神戸市営地下鉄","福岡市地下鉄","名古屋市","京都","東京","大阪","横浜","神戸","札幌",
                "名古屋","仙台","広島","北九州","千葉都市","多摩都市","沖縄都市","大阪モノレール",
                "東京モノレール","北九州モノレール","国際文化公園都市","東京臨海新交通","日暮里・舎人",
                "広島新交通","東部丘陵","ゆりかもめ","りんかい","ニュートラム","ポートアイランド",
                "六甲アイランド","南港ポートタウン","西神延伸","西神","北神","ポートアイランド",
                "地下鉄","市営","私鉄","電鉄","電気軌道","鉄道","線","本","支線","支線"]:
        s = s.replace(pre, "")
    s = s.strip("・/／ 　")
    return s

def score(line, g):
    """给 line 和 group g 打分"""
    jp = g["jp"]
    en = g["en"].lower()
    lt = line.lower()
    jl = jp.lower()
    sc = 0
    # 核心词匹配
    core = tokens(line).lower()
    if len(core) >= 2:
        if core in jl: sc += 10
        if core in en: sc += 8
    # 直接子串
    for w in [line, line.replace("線",""), line.replace("本線","")]:
        if len(w) >= 2 and w.lower() in jl: sc += 6
        if len(w) >= 2 and w.lower() in en: sc += 4
    # 命中公司上下文
    co = g["co"]
    if "北海道" in line and "北海道" in co: sc += 2
    if "東北" in line and "東北" in co: sc += 2
    return sc

result = dict(done)
unmapped = []
for line in missing:
    best, bestsc = None, 0
    for g in live:
        sc = score(line, g)
        if sc > bestsc:
            bestsc, best = sc, g
    if best and bestsc >= 6:
        result[line] = best["files"][:2]
    else:
        # 退役图兜底
        for g in retired:
            sc = score(line, g)
            if sc > bestsc:
                bestsc, best = sc, g
        if best and bestsc >= 6:
            result[line] = best["files"][:2]
        else:
            unmapped.append((line, tokens(line), best["jp"] if best else "", bestsc))

json.dump(result, open("line_icons_new.json", "w"), ensure_ascii=False, indent=1)
print(f"\n自动对上: {len(result)-len(done)}, 还没对上: {len(unmapped)}")
print("\n=== 没对上的（需要手工） ===")
for line, core, near, sc in unmapped:
    print(f"  {line:30s}  core=[{core}]  最近=[{near}] sc={sc}")
