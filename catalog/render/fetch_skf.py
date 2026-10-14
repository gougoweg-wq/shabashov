# usage: SKF token in file given by SKF_TOKEN_FILE; args: name=uid ...
import json, os, sys, urllib.request, zipfile, io
tok = open(os.environ["SKF_TOKEN_FILE"]).read().strip()
credits = json.load(open("credits.json")) if os.path.exists("credits.json") else {}
for arg in sys.argv[1:]:
    name, uid = arg.split("=")
    meta = json.load(urllib.request.urlopen(f"https://api.sketchfab.com/v3/models/{uid}"))
    req = urllib.request.Request(f"https://api.sketchfab.com/v3/models/{uid}/download", headers={"Authorization": f"Token {tok}"})
    d = json.load(urllib.request.urlopen(req))
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(d["gltf"]["url"]).read()))
    dest = f"assets/skf_{name}"; z.extractall(dest)
    credits[name] = {"title": meta["name"], "author": meta["user"]["displayName"] or meta["user"]["username"],
                     "license": meta["license"]["label"], "url": meta["viewerUrl"]}
    print("ok", name, meta["license"]["slug"])
json.dump(credits, open("credits.json", "w"), ensure_ascii=False, indent=1)
