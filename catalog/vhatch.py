# -*- coding: utf-8 -*-
"""Replace SVG <pattern> hatch fills with real vector hatching.

Chromium's PDF backend rasterises every <pattern> fill into a full-size bitmap, which blurs the
section drawings and bloats the PDF. Every hatch in the catalogue is a <rect>, so each one is
rewritten as: base-colour rect + hatch path clipped to the rect + outline. Hatches stay aligned
to the user-space grid exactly as the original patterns (patternUnits="userSpaceOnUse").
"""
import math
import re

MG, INS_D = "#8A8F96", "#B8963F"

# name: (base fill, stroke, stroke width)
STYLE = {"hCon": ("#ECECEA", MG, 1.0), "hBrick": ("#ECECEA", MG, 0.8),
         "hIns": ("#F6EED6", INS_D, 0.9), "hInsV": ("#F6EED6", INS_D, 0.9)}


def _f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _hatch(name, x, y, w, h):
    x0, y0, x1, y1 = x, y, x + w, y + h
    d = []
    if name == "hCon":  # 45° lines x + y = 12k
        for k in range(math.floor((x0 + y0) / 12) - 1, math.ceil((x1 + y1) / 12) + 2):
            c = 12 * k
            d.append(f"M{_f(x0 - 2)} {_f(c - x0 + 2)}L{_f(x1 + 2)} {_f(c - x1 - 2)}")
    elif name == "hBrick":  # rows of 6, joints every 12 alternating
        for j in range(math.floor(y0 / 6), math.ceil(y1 / 6) + 1):
            d.append(f"M{_f(x0)} {_f(6 * j)}H{_f(x1)}")
        for j in range(math.floor(y0 / 12), math.ceil(y1 / 12) + 1):
            for i in range(math.floor(x0 / 24), math.ceil(x1 / 24) + 1):
                bx, by = 24 * i, 12 * j
                d.append(f"M{bx + 6} {by}V{by + 6}M{bx + 18} {by + 6}V{by + 12}")
    elif name == "hIns":  # horizontal zigzag rows, tile 16 x 14
        for j in range(math.floor(y0 / 14), math.ceil(y1 / 14) + 1):
            by = 14 * j
            i0, i1 = math.floor(x0 / 16), math.ceil(x1 / 16)
            pts = []
            for i in range(i0, i1 + 1):
                bx = 16 * i
                pts += [(bx, by + 7), (bx + 4, by + 1), (bx + 8, by + 13), (bx + 12, by + 1)]
            pts.append((16 * (i1 + 1), by + 7))
            d.append("M" + "L".join(f"{_f(a)} {_f(b)}" for a, b in pts))
    elif name == "hInsV":  # vertical zigzag columns, tile 14 x 16
        for i in range(math.floor(x0 / 14), math.ceil(x1 / 14) + 1):
            bx = 14 * i
            j0, j1 = math.floor(y0 / 16), math.ceil(y1 / 16)
            pts = []
            for j in range(j0, j1 + 1):
                by = 16 * j
                pts += [(bx + 7, by), (bx + 1, by + 4), (bx + 13, by + 8), (bx + 1, by + 12)]
            pts.append((bx + 7, 16 * (j1 + 1)))
            d.append("M" + "L".join(f"{_f(a)} {_f(b)}" for a, b in pts))
    return "".join(d)


_RECT = re.compile(r'<rect\b([^>]*?)fill="url\(#(hCon|hBrick|hIns|hInsV)\)"([^>]*?)/?>')


def _attr(s, k):
    m = re.search(rf'\b{k}="([^"]*)"', s)
    return m.group(1) if m else None


def vectorize(html):
    n = [0]

    def sub(m):
        attrs = m.group(1) + m.group(3)
        name = m.group(2)
        try:
            x, y = float(_attr(attrs, "x") or 0), float(_attr(attrs, "y") or 0)
            w, h = float(_attr(attrs, "width")), float(_attr(attrs, "height"))
        except (TypeError, ValueError):
            return m.group(0)
        if w <= 0 or h <= 0:
            return m.group(0)
        base, col, sw = STYLE[name]
        n[0] += 1
        cid = f"vh{n[0]}"
        geo = f'x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}"'
        other = re.sub(r'\b(x|y|width|height)="[^"]*"', "", attrs).strip()
        outline = re.sub(r'\bfill="[^"]*"', "", other).strip()
        return (f'<rect {geo} fill="{base}" stroke="none"/>'
                f'<clipPath id="{cid}"><rect {geo}/></clipPath>'
                f'<path clip-path="url(#{cid})" d="{_hatch(name, x, y, w, h)}" fill="none" stroke="{col}" stroke-width="{sw}"/>'
                f'<rect {geo} fill="none" {outline}/>')

    return _RECT.sub(sub, html)
