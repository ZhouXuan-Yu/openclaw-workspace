import sys, io
p = r"C:\Users\ZhouXuan\navi-ai\ZhouXuan_\uploads\新录音 49.txt"
raw = open(p, "rb").read()
for enc in ("utf-8", "gbk", "utf-16"):
    try:
        txt = raw.decode(enc)
        print("ENCODING OK:", enc, "len:", len(txt))
        break
    except Exception as e:
        print("fail", enc, e)
lines = txt.splitlines()
print("LINES:", len(lines))
print("======FIRST 40======")
for l in lines[:40]:
    print(l)
print("======LAST 15======")
for l in lines[-15:]:
    print(l)
