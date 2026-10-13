import sys, glob
from PIL import Image
for f in glob.glob(sys.argv[1] + "/*.png"):
    im = Image.open(f).convert("RGBA")
    a = im.split()[3].point(lambda v: 255 if v > 8 else 0)
    bb = a.getbbox()
    if not bb: continue
    w, h = bb[2] - bb[0], bb[3] - bb[1]; p = int(max(w, h) * .06)
    im.crop((max(0, bb[0] - p), max(0, bb[1] - p), min(im.width, bb[2] + p), min(im.height, bb[3] + p))).save(f)
