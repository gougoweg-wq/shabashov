# -*- coding: utf-8 -*-
"""Recompress large images in uzhpl-catalog.pdf to JPEG (keeps the file small enough for macOS Preview / messengers)."""
import io, sys, zlib
import pikepdf
from PIL import Image

src = sys.argv[1] if len(sys.argv) > 1 else "uzhpl-catalog.pdf"
dst = sys.argv[2] if len(sys.argv) > 2 else src
Q, MAXW = 76, 1400

pdf = pikepdf.open(src, allow_overwriting_input=True)
done = set()
imgs = [o for o in pdf.objects if isinstance(o, pikepdf.Stream) and o.get("/Subtype") == "/Image"]
smasks = {o.get("/SMask").objgen for o in imgs if o.get("/SMask") is not None}
for raw in imgs:
    if True:
        if raw.objgen in done or raw.objgen in smasks:
            continue
        done.add(raw.objgen)
        if len(raw.read_raw_bytes()) < 20000:
            continue
        try:
            pim = pikepdf.PdfImage(raw).as_pil_image()
        except Exception:
            continue
        smask = raw.get("/SMask")
        if smask is not None:  # flatten transparency on white
            try:
                a = pikepdf.PdfImage(smask).as_pil_image().convert("L").resize(pim.size)
                bgim = Image.new("RGB", pim.size, "white"); bgim.paste(pim.convert("RGB"), mask=a); pim = bgim
            except Exception:
                continue
        im = pim.convert("RGB")
        cols = im.getcolors(256)
        if cols is None and im.getcolors(6000) is not None:
            # rasterised SVG hatch patterns (Chromium flattens <pattern> fills): 16-colour palette is visually identical
            im = im.quantize(colors=12, method=Image.Quantize.MEDIANCUT).convert("RGB")
            cols = im.getcolors(256)
        if cols is not None:  # flat drawings / hatch patterns: lossless indexed + Flate stays crisp and small
            pal_im = im.quantize(colors=len(cols), method=Image.Quantize.FASTOCTREE) if len(cols) > 1 else im.convert("P")
            pal = pal_im.getpalette()[:3 * len(cols)] if len(cols) > 1 else list(cols[0][1])
            n = max(1, len(pal) // 3)
            raw.write(zlib.compress(pal_im.tobytes(), 9), filter=pikepdf.Name.FlateDecode)
            raw.ColorSpace = pikepdf.Array([pikepdf.Name.Indexed, pikepdf.Name.DeviceRGB, n - 1, pikepdf.String(bytes(pal))])
            raw.BitsPerComponent = 8
            for k in ("/SMask", "/DecodeParms", "/Mask"):
                if k in raw:
                    del raw[k]
            continue
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=Q, optimize=True, progressive=False)
        raw.write(buf.getvalue(), filter=pikepdf.Name.DCTDecode)
        raw.Width, raw.Height = im.width, im.height
        raw.ColorSpace = pikepdf.Name.DeviceRGB; raw.BitsPerComponent = 8
        for k in ("/SMask", "/DecodeParms", "/Mask"):
            if k in raw:
                del raw[k]
# de-duplicate identical image streams (same hatch raster / photo used on several pages)
import hashlib
canon, nrep = {}, 0
for o in [o for o in pdf.objects if isinstance(o, pikepdf.Stream) and o.get("/Subtype") == "/Image"]:
    h = hashlib.md5(o.read_raw_bytes() + repr(sorted((k, str(v)) for k, v in o.items())).encode()).hexdigest()
    canon.setdefault(h, o)
by_gen = {}
for h, o in canon.items():
    by_gen[h] = o
key = {}
for o in pdf.objects:
    if isinstance(o, pikepdf.Stream) and o.get("/Subtype") == "/Image":
        h = hashlib.md5(o.read_raw_bytes() + repr(sorted((k, str(v)) for k, v in o.items())).encode()).hexdigest()
        key[o.objgen] = h
for o in list(pdf.objects):
    if not isinstance(o, (pikepdf.Dictionary, pikepdf.Stream)):
        continue
    res = o.get("/Resources")
    if res is None or "/XObject" not in res:
        continue
    xo = res.XObject
    for k in list(xo.keys()):
        v = xo[k]
        if v.objgen in key:
            c = canon[key[v.objgen]]
            if c.objgen != v.objgen:
                xo[k] = c; nrep += 1
for page in pdf.pages:
    xo = page.get("/Resources", {}).get("/XObject") if page.get("/Resources") is not None else None
    if xo is None:
        continue
    for k in list(xo.keys()):
        v = xo[k]
        if v.objgen in key and canon[key[v.objgen]].objgen != v.objgen:
            xo[k] = canon[key[v.objgen]]; nrep += 1
print("dedup refs", nrep)
pdf.save(dst, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
print("saved", dst)
