import json
groups = json.load(open("all_groups.json"))
tk = json.load(open("/home/user/Doubao/chats/38445511791035394/japanrail/mini-japanrail-3d/data/tokkyu.json"))
all_names = sorted(set(tk["nm"].values()) | set(tk["nmI"].values()))

def find(*keys, co=None):
    out=[]
    for g in groups:
        t=(g["jp"]+" "+g["en"]).lower()
        if co and co.lower() not in g["co"].lower(): continue
        if all(k.lower() in t for k in keys): out.append(g)
    return out
def files(*gs):
    s=[]
    for g in gs:
        for f in g["files"]:
            if f not in s: s.append(f)
    return s

RULES = {
 # 新幹線
 "のぞみ": find("n700"), "ひかり": find("n700"), "こだま": find("n700"),
 "みずほ": find("800"), "さくら": find("800"), "つばめ": find("800"),
 "はやぶさ": find("hayabusa"), "こまち": find("komachi"), "やまびこ": find("yamabiko"),
 "なすの": find("yamabiko"), "とき": find("kagayaki"), "たにがわ": find("max"),
 "かがやき": find("kagayaki"), "はくたか": find("kagayaki"), "あさま": find("asama"),
 "つるぎ": find("kagayaki"), "はやて": find("hayabusa"), "かもめ": find("kamome"),
 "つばさ": find("tsubasa"),
 # JR北海道
 "カムイ": find("lilac","kamui"), "ライラック": find("lilac","kamui"),
 "スーパー北斗": find("hokuto"), "北斗": find("hokuto"), "とかち": find("tokachi"),
 "おおぞら": find("ozora","tokachi"), "オホーツク": find("tokachi","soya"),
 "宗谷": find("tokachi","soya"), "サロベツ": find("tokachi","soya"),
 "エアポート": find("lilac","kamui"),
 # JR东日本
 "あずさ": find("azusa","kaiji"), "かいじ": find("azusa","kaiji"),
 "ひたち": find("hitachi","tokiwa"), "ときわ": find("hitachi","tokiwa"),
 "成田エクスプレス": find("n'ex","boso"), "踊り子": find("odoriko"),
 "サフィール踊り子": find("odoriko"), "草津": find("kusatsu"), "四万": find("kusatsu"),
 "きぬがわ": find("日光","きぬがわ"), "いなほ": find("inaho"), "しらゆき": find("inaho"),
 "つがる": find("tsugaru"), "カシオペア": find("cassiopeia"), "富士回遊": find("fuji","excursion"),
 "はちおうじ": find("azusa","kaiji"), "さざなみ": find("boso"), "わかしお": find("boso"),
 "しおさい": find("boso"), "湘南": find("azusa","kaiji"), "あかぎ": find("kusatsu"),
 # JR东海
 "ひだ": find("hida","mie"), "南紀": find("hida","nanki"), "みえ": find("hida","mie"),
 "しなの": find("shinano"), "ふじかわ": find("fujikawa"), "伊那路": find("iida"),
 # JR西日本
 "サンダーバード": find("thunderbird"), "しらさぎ": find("shirasagi"),
 "くろしお": find("kuroshio"), "こうのとり": find("kounotori"), "はるか": find("haruka"),
 "やくも": find("yakumo"), "はまかぜ": find("sanin"),
 "スーパーはくと": find("はくと"), "きのさき": find("sanin"),
 "まいづる": find("sanin"), "たんご": find("sanin"), "はしだて": find("sanin"),
 "スーパーいなば": find("sanin"), "スーパーおき": find("sanin"),
 "スーパーまつかぜ": find("sanin"), "サンライズ出雲": find("sunrise"),
 "サンライズ瀬戸": find("sunrise"), "らくラクびわこ": find("thunderbird"),
 "らくラクはりま": find("thunderbird"),
 # JR四国
 "しおかぜ": find("shiokaze","ishizuchi"), "いしづち": find("shiokaze","ishizuchi"),
 "南風": find("shikoku","express"), "しまんと": find("shimanto"),
 "宇和海": find("shikoku","express"), "あしずり": find("shimanto"),
 "うずしお": find("shikoku","express"), "剣山": find("tsurugisan","muroto"),
 "むろと": find("tsurugisan","muroto"), "マリンライナー": find("marine"),
 # JR九州
 "ソニック": find("sonic"), "リレーかもめ": find("kamome","sonic"),
 "みどり": find("midori"), "ハウステンボス": find("huis"), "ゆふ": find("yufu"),
 "きりしま": find("kirishima"), "にちりん": find("kamome","sonic"),
 "にちりんシーガイア": find("kamome","sonic"), "ひゅうが": find("kamome","sonic"),
 "かささぎ": find("sonic"), "きらめき": find("sonic"), "九州横断特急": find("yufu"),
 "指宿のたまて箱": find("いぶたま"), "博多南": find("kamome","sonic"),
 "かんぱち・いちろく": find("kanpachi"), "ふたつ星4047": find("two stars"),
 "36ぷらす3": find("around","kyushu"), "ななつ星": find("seven"), "或る列車": find("aru"),
 # 私铁-小田急
 "はこね": find("ロマンスカー"), "さがみ": find("ロマンスカー"), "えのしま": find("ロマンスカー"),
 "モーニングウェイ": find("ロマンスカー"), "ホームウェイ": find("ロマンスカー"),
 "メトロはこね": find("ロマンスカー"), "メトロさがみ": find("ロマンスカー"),
 "メトロえのしま": find("ロマンスカー"), "メトロホームウェイ": find("ロマンスカー"),
 "メトロモーニングウェイ": find("ロマンスカー"), "ふじさん": find("ロマンスカー"),
 "小田急特急": find("ロマンスカー"),
 # 私铁-京急/京成
 "京急特急": find("快特"), "アクセス特急": find("skyliner"),
 "エアポート快特": find("快特"), "京成特急": find("skyliner"),
 "京成快速特急": find("skyliner"), "スカイライナー": find("skyliner"),
 # 私铁-东武
 "りょうもう": find("ryomo"), "けごん": find("kegon"), "リバティ会津": find("spacia"),
 "東武特急": find("spacia"), "川越特急": find("ryomo"),
 # 私铁-西武/京王/相铁/东急
 "ラビュー": find("raview"), "西武特急": find("raview"),
 "京王特急": find("keio","9000"), "京王ライナー": find("keio","9000"),
 "相鉄特急": find("sotetsu"), "東急特急": find("東横"),
 # 私铁-名铁/近铁/阪急/阪神/山阳/南海/京阪/西铁
 "ミュースカイ": find("ミュースカイ"), "名鉄特急": find("ミュースカイ"),
 "近鉄特急": find("shimakaze","hinotori"),
 "阪急特急": find("京都","神戸"), "阪神特急": find("hanshin"),
 "直通特急": find("sanyo"), "山陽電鉄特急": find("sanyo"),
 "ラピート": find("rapit"), "サザン": find("rapit"), "こうや": find("kouya"),
 "りんかん": find("kouya"), "泉北ライナー": find("semboku"),
 "京阪特急": find("keihan"), "西鉄特急": find("omuta"),
 # 其他
 "能登かがり火": find("hokuto"), "SLばんえつ物語": find("banetsu"),
 "長野電鉄特急": find("nagano"), "富山地方鉄道特急": find("toyama"),
 "一畑電車特急": find("ichibata"), "秩父鉄道特急": find("chichibu"),
}

out={}; missing=[]
for name in all_names:
    fl=files(*RULES.get(name,[]))
    if not fl: missing.append(name)
    out[name]=fl
json.dump(out,open("final_tokkyu_icons.json","w"),ensure_ascii=False,indent=1)
print(f"共{len(all_names)}爱称，有图{len(all_names)-len(missing)}，缺{len(missing)}")
print("缺:",missing)
