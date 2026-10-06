import urllib.request, re, time, html as ihtml, json
BASE="http://www.trainfrontview.net/"
COS={"phkd":"北海道私鉄","pthk":"東北私鉄","pknt":"関東私鉄","pkos":"甲信越私鉄",
"pcnt":"東海私鉄","pknk":"関西私鉄","psik":"四国私鉄","pkyu":"九州私鉄",
"fnkr":"ケーブルカー","slp":"スロープカー"}
def fetch(u):
    req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    raw=urllib.request.urlopen(req,timeout=30).read()
    for e in ("shift_jis","utf-8"):
        try: return raw.decode(e)
        except: pass
    return raw.decode("utf-8","ignore")
recs=json.load(open("private_records.json"))
have=len(recs)
for pfx,name in COS.items():
    n=1
    while True:
        u=f"{BASE}sozai-{pfx}{n}.htm"
        try: txt=fetch(u)
        except Exception: break
        blocks=re.split(r'<li>',txt,flags=re.I)[1:]
        added=0
        for b in blocks:
            imgs=re.findall(r'<img\s+src="([fp]/[^"]+\.png)"',b,re.I)
            if not imgs: continue
            brs=re.split(r'<br\s*/?>',b,flags=re.I)
            jp=ihtml.unescape(re.sub(r'<[^>]+>','',brs[1]).strip()) if len(brs)>=2 else ""
            en=ihtml.unescape(re.sub(r'<[^>]+>','',brs[2]).strip()) if len(brs)>=3 else ""
            recs.append({"company":name,"pfx":pfx,"imgs":imgs,"jp":jp,"en":en})
            added+=1
        nxt=[int(x) for x in re.findall(rf'sozai-{pfx}(\d+)\.htm',txt) if int(x)>n]
        if not nxt: break
        n=min(nxt); time.sleep(0.2)
    print(f"{name}: +{added} groups (page1)")
json.dump(recs,open("private_records.json","w"),ensure_ascii=False,indent=1)
print(f"\n总私铁组: {len(recs)} (新增 {len(recs)-have})")
