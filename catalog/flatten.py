# -*- coding: utf-8 -*-
"""Maximum-compatibility PDF: every page becomes one JPEG; link annotations (clickable contents) are kept.
usage: python3 flatten.py in.pdf out.pdf [dpi] [quality]"""
import io, os, subprocess, sys, tempfile, glob
import pikepdf
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 120
q = int(sys.argv[4]) if len(sys.argv) > 4 else 80
tmp = tempfile.mkdtemp()
subprocess.run(["pdftoppm", "-r", str(dpi), "-jpeg", "-jpegopt", "quality=100", src, os.path.join(tmp, "p")], check=True,
               stderr=subprocess.DEVNULL)
files = sorted(glob.glob(os.path.join(tmp, "p-*.jpg")))
pdf = pikepdf.open(src)
out = pikepdf.new()
for pg, f in zip(pdf.pages, files):
    im = Image.open(f).convert("RGB")
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
    w, h = float(pg.mediabox[2]), float(pg.mediabox[3])
    xo = pikepdf.Stream(out, buf.getvalue(), Type=pikepdf.Name.XObject, Subtype=pikepdf.Name.Image, Width=im.width,
                        Height=im.height, ColorSpace=pikepdf.Name.DeviceRGB, BitsPerComponent=8, Filter=pikepdf.Name.DCTDecode)
    content = pikepdf.Stream(out, f"q {w} 0 0 {h} 0 0 cm /Im0 Do Q".encode())
    page = pikepdf.Dictionary(Type=pikepdf.Name.Page, MediaBox=[0, 0, w, h], Contents=content,
                              Resources=pikepdf.Dictionary(XObject=pikepdf.Dictionary(Im0=xo)))
    out.pages.append(pikepdf.Page(page))
# copy link annotations; internal links point to destination pages by index
idx = {p.objgen: i for i, p in enumerate(pdf.pages)}
for i, pg in enumerate(pdf.pages):
    annots = []
    for a in pg.get("/Annots", []):
        if a.get("/Subtype") != "/Link":
            continue
        na = pikepdf.Dictionary(Type=pikepdf.Name.Annot, Subtype=pikepdf.Name.Link, Rect=list(a.Rect), Border=[0, 0, 0])
        dest = a.get("/Dest")
        act = a.get("/A")
        if dest is None and act is not None and act.get("/S") == "/GoTo":
            dest = act.get("/D")
        if isinstance(dest, (pikepdf.String, pikepdf.Name)):  # named destination (Chromium: /Dests dict, "/p3")
            d = (pdf.Root.get("/Dests") or {}).get(str(dest) if str(dest).startswith("/") else "/" + str(dest))
            if d is None:
                try:
                    d = pikepdf.NameTree(pdf.Root.Names.Dests).get(str(dest))
                except Exception:
                    d = None
            dest = d.get("/D") if isinstance(d, pikepdf.Dictionary) else d
        if isinstance(dest, pikepdf.Array) and len(dest) and dest[0].objgen in idx:
            tgt = out.pages[idx[dest[0].objgen]].obj
            na.Dest = pikepdf.Array([tgt] + list(dest[1:]))
        elif act is not None and act.get("/S") == "/URI":
            na.A = pikepdf.Dictionary(S=pikepdf.Name.URI, URI=act.URI)
        else:
            continue
        annots.append(out.make_indirect(na))
    if annots:
        out.pages[i].obj.Annots = pikepdf.Array(annots)
out.docinfo["/Title"] = "UZHPL — Технический каталог"
out.save(dst, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.disable, min_version="1.4", linearize=True)
links = sum(len(p.obj.get("/Annots", [])) for p in out.pages)
print("saved", dst, os.path.getsize(dst) // 1024, "KB,", len(out.pages), "pages,", links, "links")
