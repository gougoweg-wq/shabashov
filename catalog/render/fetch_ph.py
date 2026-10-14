import json, os, sys, urllib.request
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "uzhpl-catalog/1.0"})).read()
for name in sys.argv[1:]:
    d = json.loads(get(f"https://api.polyhaven.com/files/{name}"))
    if "gltf" in d:
        g = d["gltf"]["1k"]["gltf"]; base = f"assets/{name}"
        os.makedirs(base, exist_ok=True)
        open(f"{base}/{name}.gltf", "wb").write(get(g["url"]))
        for rel, v in g.get("include", {}).items():
            p = f"{base}/{rel}"; os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(get(v["url"]))
    elif "hdri" in d:
        os.makedirs("assets/hdri", exist_ok=True)
        open(f"assets/hdri/{name}.hdr", "wb").write(get(d["hdri"]["1k"]["hdr"]["url"]))
    else:  # texture
        os.makedirs(f"assets/tex/{name}", exist_ok=True)
        for m in ("Diffuse", "nor_gl", "Rough", "arm"):
            if m in d and "1k" in d[m]:
                f = d[m]["1k"]["jpg"]; open(f"assets/tex/{name}/{m}.jpg", "wb").write(get(f["url"]))
    print("ok", name)
