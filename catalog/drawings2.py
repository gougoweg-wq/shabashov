# -*- coding: utf-8 -*-
"""v2 drawings: callout overlays, 1220x3050 panel layouts, formats, interior joints, glue prep."""
import json
import os
from lib import svg, rect, ln, label, pl, poly2, OR, GR, DG, MG, LG, XL, HPL, INS_D

HERE = os.path.dirname(os.path.abspath(__file__))


def callout_fig(img, keys, W=1200, H=1460, dx=46, dy=-40, crop=None):
    """3D image + numbered badges at projected anchor points (img/v2/<img>.json)."""
    pts = json.load(open(os.path.join(HERE, "img", "v2", img + ".json")))
    vb = crop or (0, 0, W, H)
    s = f'<image href="img/v2/{img}.png" x="0" y="0" width="{W}" height="{H}"/>'
    for i, k in enumerate(keys):
        if k not in pts:
            continue
        x, y = pts[k]
        tx, ty = x + dx, y + dy
        s += (f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ty}" stroke="{GR}" stroke-width="1.6"/>'
              f'<circle cx="{x}" cy="{y}" r="4.5" fill="{GR}"/>'
              f'<circle cx="{tx}" cy="{ty}" r="19" fill="{OR}" stroke="#fff" stroke-width="3"/>'
              f'<text x="{tx}" y="{ty + 6.5}" text-anchor="middle" font-size="18" font-weight="700" fill="#fff" font-family="Inter">{i + 1}</text>')
    return (f'<svg viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" width="100%" xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink">{s}</svg>')


def legend(items, cols=2):
    return (f'<div class="lst" style="grid-template-columns:repeat({cols},1fr)">' + "".join(
        f'<div class="li"><span class="badge">{i + 1}</span><div><h4>{a}</h4>{f"<p>{b}</p>" if b else ""}</div></div>'
        for i, (a, b) in enumerate(items)) + '</div>')


# ---------------------------------------------------------------- 1220 x 3050 panel layouts
def panel_layout(sys="rivet", W=460, H=1000, label_dims=True):
    """Panel 1220x3050 to scale with profiles (dashed) and fastener scheme."""
    k = (H - 80) / 3050.0
    pw, ph = 1220 * k, 3050 * k
    x0, y0 = (W - pw) / 2 + 20, 40
    s = rect(x0, y0, pw, ph, "#ECEAE6", GR, 1.4)
    cols = [30, 610, 1190]
    for c in cols:
        x = x0 + c * k
        s += ln(x, y0 - 18, x, y0 + ph + 18, MG, 1.2, 'stroke-dasharray="8 6"')
    rows = [120 + i * 560 for i in range(6)]
    if sys in ("rivet", "screw"):
        fx, fy = 610, rows[2]
        for c in cols:
            for r in rows:
                x, y = x0 + c * k, y0 + r * k
                if (c, r) == (fx, fy):
                    s += f'<circle cx="{x}" cy="{y}" r="9" fill="{OR}"/><circle cx="{x}" cy="{y}" r="3" fill="#fff"/>'
                else:
                    s += f'<circle cx="{x}" cy="{y}" r="8" fill="#fff" stroke="{GR}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="2.6" fill="{GR}"/>'
        cx, cy = x0 + fx * k, y0 + fy * k
        for dx_, dy_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s += (f'<line x1="{cx + dx_ * 16}" y1="{cy + dy_ * 16}" x2="{cx + dx_ * 52}" y2="{cy + dy_ * 52}" stroke="{OR}" stroke-width="2.4" '
                  f'marker-end="url(#aOr)"/>')
    if sys == "glue":
        for c in cols:
            x = x0 + c * k
            s += rect(x - 9, y0 + 8, 18, ph - 16, "url(#hIns)", OR, 1.2, 'opacity=".9"')
    if sys == "hidden":
        for r in (300, 1300, 2300, 2950):
            y = y0 + r * k
            s += ln(x0 - 14, y, x0 + pw + 14, y, MG, 1.2, 'stroke-dasharray="8 6"')
            for c in (200, 1020):
                s += rect(x0 + c * k - 14, y - 6, 28, 12, "#fff", GR, 1.6)
    if label_dims:
        s += label(x0 + pw / 2, y0 + ph + 34, "1220 мм", 15, "middle", 600, GR)
        s += (f'<text x="{x0 - 18}" y="{y0 + ph / 2}" font-size="15" font-weight="600" fill="{GR}" text-anchor="middle" '
              f'font-family="Inter" transform="rotate(-90 {x0 - 18} {y0 + ph / 2})">3050 мм</text>')
    return svg(W, H, s)


def formats_svg(W=912, H=430):
    fm = [("915 × 2135", 915, 2135, "1,95 м²"), ("1220 × 2800", 1220, 2800, "3,42 м²"),
          ("1220 × 3050", 1220, 3050, "3,72 м²"), ("1830 × 4270", 1830, 4270, "7,81 м²")]
    k = 330 / 4270.0
    s = ""
    x = 20
    for i, (n, w, h, a) in enumerate(fm):
        rw, rh = w * k, h * k
        y = 360 - rh
        hl = i == 2
        s += rect(x, y, rw, rh, "#FFF4EC" if hl else XL, OR if hl else GR, 2 if hl else 1.2)
        s += label(x, 392, n, 17, "start", 700, GR) + label(x, 414, a, 13, "start", 500, MG)
        if hl:
            s += label(x + rw / 2, y + rh / 2 + 5, "★", 16, "middle", 700, OR)
        x += rw + 120
    return svg(W, H, s)


# ---------------------------------------------------------------- interior joints & corners (2D)
def _hpl(x, y, w, h):
    return rect(x, y, w, h, HPL, "#000", .8)


def ijoint(kind, W=440, H=300):
    s = rect(0, 0, W, H, "#fff", LG, 1)
    t = 13
    base = rect(30, 170, 380, 26, "url(#hBrick)", MG, .8) + rect(30, 160, 380, 10, "#e8e2d4", MG, .6)
    names = {"tongue": "ШПУНТ / ПАЗ", "gasket": "РЕЗИНОВЫЙ УПЛОТНИТЕЛЬ", "hprof": "ДЕКОРАТИВНЫЙ ПРОФИЛЬ",
             "open": "ОТКРЫТЫЙ ШОВ", "miter": "УГОЛ 45° (УСОВКА)", "corner": "УГЛОВОЙ ПРОФИЛЬ",
             "shadow": "ТЕНЕВОЙ ШОВ", "edge": "ТОРЕЦ / КРОМКА"}
    if kind == "tongue":
        s += base + _hpl(30, 147, 190, t) + _hpl(226, 147, 184, t)
        s += rect(220, 151, 14, 5, HPL, "#000", .6) + rect(220, 147, 6, 13, "#fff", "none", 0)
        s += rect(212, 151, 14, 5, "#fff", "#000", .6)
    elif kind == "gasket":
        s += base + _hpl(30, 147, 184, t) + _hpl(226, 147, 184, t) + rect(214, 145, 12, 17, "#3a3b3d", "#000", .6)
    elif kind == "hprof":
        s += base + _hpl(30, 147, 180, t) + _hpl(230, 147, 180, t)
        s += pl([(202, 143), (238, 143)], "#9aa0a7", 4) + pl([(202, 162), (238, 162)], "#9aa0a7", 4) + ln(220, 143, 220, 162, "#9aa0a7", 4)
    elif kind == "open":
        s += base + _hpl(30, 147, 184, t) + _hpl(226, 147, 184, t) + rect(200, 160, 40, 2, "#3a3b3d", "none", 0)
    elif kind == "miter":
        s += rect(60, 70, 26, 200, "url(#hBrick)", MG, .8) + rect(86, 244, 300, 26, "url(#hBrick)", MG, .8)
        s += poly2([(86, 70), (99, 70), (99, 231), (86, 244)], HPL, "#000", .8)
        s += poly2([(86, 244), (99, 231), (386, 231), (386, 244)], HPL, "#000", .8)
        s += ln(86, 244, 99, 231, OR, 2)
    elif kind == "corner":
        s += rect(60, 70, 26, 200, "url(#hBrick)", MG, .8) + rect(86, 244, 300, 26, "url(#hBrick)", MG, .8)
        s += _hpl(86, 70, 13, 156) + _hpl(117, 231, 269, 13) + pl([(86, 228), (86, 244), (115, 244)], "#9aa0a7", 4)
    elif kind == "shadow":
        s += base + _hpl(30, 147, 180, t) + _hpl(230, 147, 180, t) + rect(210, 147, 20, 13, "#2a2b2d", "none", 0)
    elif kind == "edge":
        s += base + _hpl(30, 147, 300, t) + f'<path d="M330 147 q8 0 8 6.5 q0 6.5 -8 6.5" fill="{HPL}" stroke="{OR}" stroke-width="2"/>'
    s += label(W / 2, 40, names[kind], 13, "middle", 700, GR, 1.5)
    return svg(W, H, s)


def glue_prep(W=912, H=520):
    """Panel back: profile position lines and bonding zones (sand + primer)."""
    k = 440 / 3050.0
    pw, ph = 1220 * k, 3050 * k
    x0, y0 = 70, 40
    s = rect(x0, y0, pw, ph, "#F1EEE9", GR, 1.4) + label(x0 + pw / 2, y0 + ph + 30, "ТЫЛЬНАЯ СТОРОНА HPL", 12, "middle", 700, MG, 1.5)
    for c in (30, 610, 1190):
        x = x0 + c * k
        s += rect(x - 7, y0 + 4, 14, ph - 8, "#FFD9C2", OR, 1)
        s += ln(x, y0 - 12, x, y0 + ph + 12, OR, 1, 'stroke-dasharray="5 4"')
    tx = x0 + pw + 60
    items = [("1", "Разметка положения панели", "по раскладке фасада"), ("2", "Разметка линий профилей", "на тыльной стороне"),
             ("3", "Шлифование зон контакта", "абразив по системе"), ("4", "Очистка", "безворсовая салфетка, очиститель"),
             ("5", "Праймер / активатор", "только в зонах контакта"), ("6", "Выдержка", "время — по инструкции")]
    for i, (n, a, b) in enumerate(items):
        y = y0 + 22 + i * 74
        s += (f'<circle cx="{tx + 14}" cy="{y}" r="14" fill="{OR}"/><text x="{tx + 14}" y="{y + 5}" text-anchor="middle" font-size="14" '
              f'font-weight="700" fill="#fff" font-family="Inter">{n}</text>')
        s += label(tx + 40, y + 2, a, 17, "start", 600, GR) + label(tx + 40, y + 24, b, 14, "start", 400, MG)
    return svg(W, H, s)


def rivet_sec(fixed=True, W=430, H=420):
    """Enlarged section: rivet Ø5 in Ø10 panel hole; fixed point with sleeve, sliding point with free play."""
    s = rect(0, 0, W, H, XL, "none", 0)
    k = 11
    px, pt = 150, 8 * k            # panel x, thickness
    fx, ft = px + pt + 1.2 * k, 2 * k
    cy = 220
    s += rect(px, 60, pt, 320, HPL, "#000", 1)
    s += rect(px + pt, 60, 1.2 * k, 320, "#1a1a1a", "none", 0)                      # EPDM
    s += rect(fx, 60, ft, 320, "#cfd3d8", GR, 1)                                    # profile
    s += rect(px, cy - 5 * k, pt, 10 * k, XL, "none", 0)                            # panel hole Ø10
    if fixed:
        s += rect(px, cy - 5 * k, pt * .75, 10 * k, OR, GR, .8)                       # sleeve Ø10 x 6
    s += rect(px + pt, cy - 2.6 * k, 1.2 * k, 5.2 * k, XL, "none", 0)
    s += rect(fx, cy - 2.55 * k, ft, 5.1 * k, XL, "none", 0)                        # UK hole Ø5.1
    gap = 0 if fixed else 6
    hx = px - gap
    s += f'<path d="M{hx} {cy - 8 * k} Q{hx - 3 * k} {cy} {hx} {cy + 8 * k} Z" fill="#8a8f96" stroke="{GR}"/>'
    s += rect(hx, cy - 2.5 * k, fx + ft - hx + 6, 5 * k, "#c3c8ce", GR, .8)
    s += f'<path d="M{fx + ft + 6} {cy - 3.6 * k} q{2.2 * k} {3.6 * k} 0 {7.2 * k}" fill="#c3c8ce" stroke="{GR}"/>'
    s += label(W / 2, 34, "ФИКСИРОВАННАЯ ТОЧКА" if fixed else "СКОЛЬЗЯЩАЯ ТОЧКА", 15, "middle", 700, OR if fixed else GR, 1.5)
    if fixed:
        s += label(W / 2, 404, "Гильза фикс. точки Ø10 × 6, отв. 5,1", 13, "middle", 500, DG)
    else:
        s += f'<line x1="{px + pt / 2}" y1="{cy - 5 * k - 18}" x2="{px + pt / 2}" y2="{cy - 3 * k}" stroke="{OR}" stroke-width="2.4" marker-end="url(#aOr)"/>'
        s += f'<line x1="{px + pt / 2}" y1="{cy + 5 * k + 18}" x2="{px + pt / 2}" y2="{cy + 3 * k}" stroke="{OR}" stroke-width="2.4" marker-end="url(#aOr)"/>'
        s += label(W / 2, 404, "Зазор под головкой — наконечник G3", 13, "middle", 500, DG)
    for (y, t) in ((96, "HPL"), (132, "EPDM"), (168, "Профиль")):
        s += label(330, y, t, 13, "start", 600, GR)
    s += ln(px + pt / 2, 96 - 4, 326, 92, GR, .8) + ln(px + pt + 6, 132 - 4, 326, 128, GR, .8) + ln(fx + ft / 2, 168 - 4, 326, 164, GR, .8)
    return svg(W, H, s)
