import urllib.request, re, time

BASE = "http://www.trainfrontview.net/"
companies = {"t":"新幹線","h":"JR北海道","e":"JR東日本","c":"JR東海","w":"JR西日本","s":"JR四国","k":"JR九州","f":"JR貨物"}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=30).read()
    for enc in ("shift_jis","utf-8"):
        try: return raw.decode(enc)
        except: pass
    return raw.decode("utf-8","ignore")

pages = {}
for pfx, name in companies.items():
    # discover pagination
    found = []
    n = 1
    while True:
        u = f"{BASE}sozai-{pfx}{n}.htm"
        try:
            html = fetch(u)
        except Exception as ex:
            break
        found.append(n)
        # look for next page link
        m = re.findall(rf'sozai-{pfx}(\d+)\.htm', html)
        nxt = [int(x) for x in m if int(x) > n]
        if not nxt: break
        n = min(nxt)
        time.sleep(0.3)
    pages[pfx] = (name, found)
    print(pfx, name, "pages:", found)
