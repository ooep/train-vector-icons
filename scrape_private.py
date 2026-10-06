import urllib.request, re, time, html as ihtml, os, json
BASE="http://www.trainfrontview.net/"
COS={"tob":"東武","kese":"京成","tkm":"東京メトロ","keio":"京王","seb":"西武","odq":"小田急",
"toq":"東急","khk":"京急","sote":"相鉄","mei":"名鉄","kin":"近鉄","khan":"京阪","osak":"大阪メトロ",
"hnq":"阪急","hnsn":"阪神","nan":"南海","nisi":"西鉄","phks":"北陸","pcgk":"山陽山陰"}
def fetch(u):
    req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    raw=urllib.request.urlopen(req,timeout=30).read()
    for e in ("shift_jis","utf-8"):
        try: return raw.decode(e)
        except: pass
    return raw.decode("utf-8","ignore")

records=[]
for pfx,name in COS.items():
    n=1
    while True:
        u=f"{BASE}sozai-{pfx}{n}.htm"
        try: txt=fetch(u)
        except Exception: break
        blocks=re.split(r'<li>',txt,flags=re.I)[1:]
        for b in blocks:
            imgs=re.findall(r'<img\s+src="([fp]/[^"]+\.png)"',b,re.I)
            if not imgs: continue
            brs=re.split(r'<br\s*/?>',b,flags=re.I)
            jp=ihtml.unescape(re.sub(r'<[^>]+>','',brs[1]).strip()) if len(brs)>=2 else ""
            en=ihtml.unescape(re.sub(r'<[^>]+>','',brs[2]).strip()) if len(brs)>=3 else ""
            records.append({"company":name,"pfx":pfx,"imgs":imgs,"jp":jp,"en":en})
        # next page?
        nxt=[int(x) for x in re.findall(rf'sozai-{pfx}(\d+)\.htm',txt) if int(x)>n]
        if not nxt: break
        n=min(nxt); time.sleep(0.2)
    print(f"{name}: total groups so far {len(records)}")
json.dump(records,open("private_records.json","w"),ensure_ascii=False,indent=1)
print("private groups:",len(records),"images:",sum(len(r['imgs']) for r in records))
