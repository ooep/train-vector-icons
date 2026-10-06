import urllib.request, re, time, html as ihtml, os, json

BASE = "http://www.trainfrontview.net/"
companies = {"t":"JR新幹線","h":"JR北海道","e":"JR東日本","c":"JR東海","w":"JR西日本","s":"JR四国","k":"JR九州","f":"JR貨物"}
pages = {"t":[1,2],"h":[1,2],"e":[1,2,3,4,5,6,7,8],"c":[1],"w":[1,2,3,4,5,6,7,8],"s":[1,2],"k":[1,2,3],"f":[1,2]}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=30).read()
    for enc in ("shift_jis","utf-8"):
        try: return raw.decode(enc)
        except: pass
    return raw.decode("utf-8","ignore")

records = []
for pfx, pgs in pages.items():
    cname = companies[pfx]
    for n in pgs:
        u = f"{BASE}sozai-{pfx}{n}.htm"
        txt = fetch(u)
        # split by <li>
        blocks = re.split(r'<li>', txt, flags=re.I)[1:]
        for b in blocks:
            imgs = re.findall(r'<img\s+src="(f/[^"]+\.png)"', b, flags=re.I)
            # labels: text after <br> ... <br> english
            # strip tags
            # find japanese label: first text after first <br>
            brs = re.split(r'<br\s*/?>', b, flags=re.I)
            jp = en = ""
            if len(brs) >= 2:
                jp = re.sub(r'<[^>]+>','', brs[1]).strip()
            if len(brs) >= 3:
                en = re.sub(r'<[^>]+>','', brs[2]).strip()
            jp = ihtml.unescape(jp); en = ihtml.unescape(en)
            if imgs:
                records.append({"company":cname,"pfx":pfx,"page":n,"imgs":imgs,"jp":jp,"en":en})
        time.sleep(0.3)

total_imgs = sum(len(r["imgs"]) for r in records)
print("vehicle groups:", len(records), "total images:", total_imgs)
json.dump(records, open("records.json","w"), ensure_ascii=False, indent=1)
# sample
for r in records[:6]:
    print(r["company"], "|", r["jp"], "|", r["en"], "|", len(r["imgs"]), "imgs:", r["imgs"][:3])
