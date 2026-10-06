import json, re

groups = json.load(open("all_groups.json"))
tm = json.load(open("/home/user/Doubao/chats/38445511791035394/japanrail/mini-japanrail-3d/data/tmaps.json"))
real = set()
for e in tm.values():
    for ln in e.get("lines", []):
        real.add(ln)

def core(s):
    """取线路名核心：去掉'本線/線'后缀和常见前缀"""
    s = s.strip()
    # 去掉 jr / 公司前缀
    s = re.sub(r'^(jr|東京メトロ|都営|大阪メトロ|札幌市営|横浜市営|神戸市営|福岡市|名古屋市|仙台市)', '', s)
    s = s.replace('線', '').replace('本', '')
    return s.strip('・/／ ')

def find_for(line):
    ln = core(line)
    if len(ln) < 1:
        return []
    cands = []
    for g in groups:
        if not g["files"]:
            continue
        t = (g["jp"] + " " + g["en"]).lower()
        gl = g["jp"].lower()
        if ln.lower() in t or ln.lower() in gl:
            cands.append(g)
    return cands

matched = {}
missing = []
for line in sorted(real):
    c = find_for(line)
    cur = [g for g in c if not g["jp"].startswith("*")]
    pick = cur[0] if cur else (c[0] if c else None)
    if pick:
        matched[line] = pick["files"][:2]
    else:
        missing.append(line)

print(f"真实线路:{len(real)}  匹配:{len(matched)}  缺:{len(missing)}")
print("\n还缺:")
for m in missing:
    print("  ", m)
json.dump(matched, open("line_icons_new.json", "w"), ensure_ascii=False, indent=1)
