import json, os, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
BASE="http://www.trainfrontview.net/"
recs=json.load(open("private_records.json"))
PCMP={"tob":"08_tobu","kese":"09_keisei","tkm":"10_metro","keio":"11_keio","seb":"12_seibu",
"odq":"13_odakyu","toq":"14_tokyu","khk":"15_keikyu","sote":"16_sotetsu","mei":"17_meitetsu",
"kin":"18_kintetsu","khan":"19_keihan","osak":"20_osakametro","hnq":"21_hankyu","hnsn":"22_hanshin",
"nan":"23_nankai","nisi":"24_nishitetsu","phks":"25_hokuriku","pcgk":"26_sanyosanin"}
def san(s):
    s=s.lower(); s=re.sub(r'[^a-z0-9]+','-',s).strip('-'); s=re.sub(r'-{2,}','-',s); return s or "untitled"
plan=[]; seen={}
for r in recs:
    d=os.path.join("jr_icons",PCMP[r["pfx"]]); os.makedirs(d,exist_ok=True)
    base=san(r["en"]) or san(r["jp"])
    for im in r["imgs"]:
        stem=san(os.path.splitext(os.path.basename(im))[0])
        fn=f"{base}__{stem}.png"
        if fn in seen: fn=f"{base}__{stem}-{seen[fn]}.png"
        seen[fn]=seen.get(fn,0)+1
        plan.append((BASE+im, os.path.join(d,fn)))
print("to dl:",len(plan))
def one(j):
    u,o=j
    if os.path.exists(o) and os.path.getsize(o)>100: return "skip"
    for a in range(3):
        try:
            req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
            data=urllib.request.urlopen(req,timeout=30).read()
            if len(data)<100 or data[:4]!=b'\x89PNG': raise ValueError("png")
            open(o,"wb").write(data); return "ok"
        except Exception as e:
            if a==2: return f"fail {u} {e}"
            time.sleep(1.5)
fails=[]; oks=0; sk=0
with ThreadPoolExecutor(max_workers=8) as ex:
    for res in ex.map(one,plan):
        if res=="ok":oks+=1
        elif res=="skip":sk+=1
        else:fails.append(res)
print("ok",oks,"skip",sk,"fail",len(fails))
for f in fails[:10]: print(f)
