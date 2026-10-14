# -*- coding: utf-8 -*-
"""v4 exploded assemblies: the clean v2 axonometry + the full layer stack, with tidy side callouts."""
from lib import *

PAD = ("#4b4d52", "#2f3135", "#64676d")      # paronite thermal pad (front, side, top)
EPDM = ("#141517", "#0b0b0c", "#2b2c2f")


def exploded2(system="rivet"):
    """Returns (svg_body, points) in a 936 x 980 box. points: key -> (x, y) screen anchor."""
    A = Axo(585, 120, 0.80)
    g = ""
    vh = 640
    sx0, sy0 = A.p(-80, vh + 30, 420); sx1, sy1 = A.p(430, vh + 30, -40)
    g += (f'<ellipse cx="{(sx0 + sx1) / 2:.0f}" cy="{(sy0 + sy1) / 2 + 20:.0f}" rx="{abs(sx1 - sx0) / 2:.0f}" ry="40" '
          f'fill="#000" opacity=".12" filter="url(#fSh)"/>')
    g += a_wall(A, 0, 430, 0, vh, -40, 0)
    cols = [70, 300]
    rows = [(60, True), (330, False), (560, False)]
    P = 6  # pad thickness
    for cu in cols:
        for (rv, fixed) in rows:
            g += A.box(cu - 5, cu + 31, rv - 5, rv + 51, 0, P, *PAD, .6)
            g += a_bracket(A, cu, rv, P, 150, sliding=not fixed)
    E = 120
    g_ins = a_ins(A, -40, 230, 0, vh, 0, 100)
    # dowels on the insulation (visible right of the membrane)
    dow = [(196, 150), (196, 470)]
    for (u, v) in dow:
        g_ins += A.box(u - 1.5, u + 1.5, v - 1.5, v + 1.5, 60, 100, "#cfd3d8", "#9aa1a9", "#e8eaec", .4)
        x, y = A.p(u, v, 100)
        g_ins += (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="9" ry="8" fill="#f1f2f3" stroke="#7c828a" stroke-width=".9"/>'
                  f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="#7c828a"/>')
    mem_d = 100 + E * .8
    g_mem = a_mem(A, -80, 160, 0, vh, mem_d, mem_d + 3)
    for (u, v) in [(40, 150), (40, 470)]:
        x, y = A.p(u, v, mem_d + 3)
        g_mem += (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="9" ry="8" fill="#f1f2f3" stroke="#7c828a" stroke-width=".9"/>'
                  f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="#7c828a"/>')
    g += g_ins + g_mem
    pd0 = 150 + E * 1.7
    d_web = pd0 - 60
    pf = d_web + 40
    uL, uT = cols[1] + 22, cols[0] + 22
    g += a_lprofile(A, uL, -20, vh + 10, d_web)
    g += a_tprofile(A, uT, -20, vh + 10, d_web)
    # profile -> bracket rivets on the profile web, at every bracket row
    for cu in (uL, uT):
        for (rv, _) in rows:
            g += A.dot(cu + 3, rv + 16, d_web + 12, 2.6, "#d8dbdf") + A.dot(cu + 3, rv + 32, d_web + 12, 2.6, "#d8dbdf")
    # EPDM strips on the profile face
    if system in ("rivet", "screw", "vent"):
        g += A.box(uL - 17, uL - 3, -20, vh + 10, pf, pf + 2, *EPDM, .4)
        g += A.box(uT - 16, uT + 19, -20, vh + 10, pf, pf + 2, *EPDM, .4)
    if system == "glue":
        # primer zones (on L and T flanges), EPDM in the joint zone of the T, tape + adhesive bead
        g += A.box(uL - 20, uL + 1, -20, vh + 10, pf, pf + 1, "#e9e3d2", "#c9c2ae", "#f4efe2", .3)
        g += A.box(uT - 38, uT + 41, -20, vh + 10, pf, pf + 1, "#e9e3d2", "#c9c2ae", "#f4efe2", .3)
        g += A.box(uT - 4, uT + 7, -20, vh + 10, pf + 1, pf + 3, *EPDM, .4)
        for cu, (a0, a1, b0, b1) in ((uL, (-18, -12, -8, 0)), (uT, (-34, -26, -20, -11))):
            g += A.box(cu + a0, cu + a1, 20, vh - 10, pf + 1, pf + 5, "#202124", "#111", "#333", .5)
            g += A.box(cu + b0, cu + b1, 20, vh - 10, pf + 1, pf + 8, OR, "#b84d10", "#f59a62", .5)
        for cu, (a0, a1, b0, b1) in ((uT, (26, 34, 14, 23)),):
            g += A.box(cu + a0, cu + a1, 20, vh - 10, pf + 1, pf + 5, "#202124", "#111", "#333", .5)
            g += A.box(cu + b0, cu + b1, 20, vh - 10, pf + 1, pf + 8, OR, "#b84d10", "#f59a62", .5)
    if system == "hidden":
        for rv in (100, 420):
            g += A.box(-40, 420, rv, rv + 14, pf, pf + 6, "url(#gSteel)", STEEL_D, STEEL_L, .6)
    pd = pf + E * 1.6
    riv = []
    if system in ("rivet", "screw", "vent"):
        for cu in (uT - 22, uT + 22, uL - 10):
            for vv in (60, 230, 400, 560):
                riv.append((cu, vv))
    cut = 300
    up = [r for r in riv if r[0] < 190 and r[1] < cut]
    lo = [r for r in riv if r[0] < 190 and r[1] > cut + 12]
    panel = a_panel(A, -60, 190, -10, cut, pd, 9, [] if system == "screw" else up)
    panel2 = a_panel(A, -60, 190, cut + 12, vh + 10, pd, 9, [] if system == "screw" else lo)
    if system == "hidden":  # klammers exploded between the rails and the panel
        for vv in (92, 412):
            for u0 in (10, 130):
                g += A.box(u0, u0 + 36, vv, vv + 30, pf + 58, pf + 66, "#B5BBC2", STEEL_D, STEEL_L, .6)
                g += A.box(u0, u0 + 36, vv + 22, vv + 30, pf + 40, pf + 58, "#C9CED4", STEEL_D, STEEL_L, .6)
    g += panel2 + panel
    if system == "screw":
        for (u, v) in up + lo:
            x, y = A.p(u, v, pd + 9)
            g += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#9aa0a7" stroke="#4d5157" stroke-width=".9"/>'
                  f'<path d="M{x - 2.6:.1f} {y:.1f}h5.2M{x:.1f} {y - 2.6:.1f}v5.2" stroke="#3a3d42" stroke-width="1.1"/>')
    gd = (pf + pd) / 2
    for uu in (40, 200):
        x0, y0 = A.p(uu, vh + 30, gd); x1, y1 = A.p(uu, -60, gd)
        g += air([(x0, y0), (x1, y1)], 2.4, "10 7")
    pts = {"wall": (420, 470, 0), "anchor": (cols[1] + 11, 60 + 23, P + 4), "bracket": (cols[1] + 26, 330 + 30, 110),
           "pad": (cols[1] + 31, 560 + 50, 3), "ins": (-30, 40, 100), "dowel": (196, 470, 100),
           "mem": (150, 380, mem_d + 3), "lprof": (uL + 2, 200, d_web + 25), "prof_rivet": (uL + 3, 560 + 32, d_web + 12),
           "tprof": (uT + 2, vh - 20, d_web + 25), "epdm": (uL - 10, 20, pf + 2), "primer": (uL - 10, 20, pf + 1),
           "tape": (uT - 30, 520, pf + 5), "bead": (uL - 4, 420, pf + 8), "rail": (400, 107, pf + 6),
           "clip": (148, 107, pf + 66), "panel": (60, 200, pd + 9), "panel2": (60, 470, pd + 9),
           "fastener": (uT - 22, 400, pd + 9), "gap": (120, -40, gd)}
    if system == "glue":
        pts["epdm"] = (uT + 1, 60, pf + 3)
        pts["primer"] = (uL - 10, 20, pf + 1)
    return g, {k: A.p(*v) for k, v in pts.items()}


def callout_svg(system, keys, W=936, H=980, crop=(190, 70, 746, 830)):
    """Exploded drawing with numbered badges on short leaders pointing away from the drawing centre."""
    import math
    g, P = exploded2(system)
    cx, cy = 600, 470
    placed, out = [], ""
    for n, k in enumerate(keys, 1):
        if k not in P:
            continue
        x, y = P[k]
        vx, vy = x - cx, y - cy
        L = math.hypot(vx, vy) or 1
        vx, vy = vx / L, vy / L
        r = 58
        while True:
            bx, by = x + vx * r, y + vy * r
            bx, by = min(max(bx, 24), W - 24), min(max(by, 24), H - 24)
            if all(math.hypot(bx - px, by - py) > 38 for px, py in placed) or r > 260:
                break
            r += 14
        placed.append((bx, by))
        out += (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{GR}" stroke-width="1"/>'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{GR}"/>' + num(round(bx, 1), round(by, 1), n, 16))
    from lib import DEFS
    x, y, w, h = crop
    return (f'<svg viewBox="{x} {y} {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg">{DEFS}{g + out}</svg>')


# ------------------------------------------------------------------ panel 1220 x 3050 schemes (v2 style, bold)
def panel_scheme(sys="rivet", W=440, H=1010):
    """Dark 1220 x 3050 panel to scale with profile lines and the fastening scheme of a system."""
    k = min((H - 110) / 3050.0, (W - 80) / 1220.0)
    pw, ph = 1220 * k, 3050 * k
    x0, y0 = W - pw - 12, 40
    X = lambda mm: x0 + mm * k
    Y = lambda mm: y0 + mm * k
    s = (f'<defs><linearGradient id="gPan" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3d42"/>'
         f'<stop offset="1" stop-color="#1d1f22"/></linearGradient></defs>')
    s += f'<rect x="{x0 + 8}" y="{y0 + 10}" width="{pw}" height="{ph}" fill="#000" opacity=".12"/>'
    s += f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="url(#gPan)" stroke="#000" stroke-width="1.2"/>'
    cols = [30, 610, 1190]
    if sys in ("rivet", "screw", "glue"):
        for c in cols:
            s += ln(X(c), y0 - 22, X(c), y0 + ph + 22, MG, 1.2, 'stroke-dasharray="12 5 2 5"')
    if sys in ("rivet", "screw"):
        rows = [120 + i * 560 for i in range(6)]
        fx, fy = X(610), Y(rows[2])
        for c in cols:
            for r in rows:
                x, y = X(c), Y(r)
                if (c, r) == (610, rows[2]):
                    s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{OR}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#fff"/>'
                else:
                    s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="none" stroke="#fff" stroke-width="2"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#fff"/>'
        for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            L = 70 if dy else 46
            s += arrow(fx + dx * 22, fy + dy * 22, fx + dx * (22 + L), fy + dy * (22 + L), OR, 2.6)
    if sys == "glue":
        for c in cols:
            a = X(c) - 13
            s += f'<rect x="{a:.1f}" y="{y0 + 12}" width="26" height="{ph - 24:.1f}" fill="#e9e3d2" opacity=".9"/>'
            s += f'<rect x="{a + 3:.1f}" y="{y0 + 22}" width="7" height="{ph - 44:.1f}" fill="#0e0f10"/>'
            s += f'<rect x="{a + 14:.1f}" y="{y0 + 22}" width="9" height="{ph - 44:.1f}" fill="{OR}"/>'
    if sys == "hidden":
        for r in (300, 1300, 2300, 2950):
            y = Y(r)
            s += ln(x0 - 22, y, x0 + pw + 22, y, MG, 1.2, 'stroke-dasharray="12 5 2 5"')
            for c in (150, 1070):
                x = X(c)
                s += f'<rect x="{x - 16:.1f}" y="{y - 9:.1f}" width="32" height="18" rx="2" fill="#C9CED4" stroke="#fff" stroke-width="1.4"/>'
        fx, fy = X(150), Y(300)
        s += f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="6" fill="{OR}"/>'
    # dimensions
    s += ln(x0, y0 + ph + 34, x0 + pw, y0 + ph + 34, GR, 1) + ln(x0, y0 + ph + 26, x0, y0 + ph + 42, GR, 1) + ln(x0 + pw, y0 + ph + 26, x0 + pw, y0 + ph + 42, GR, 1)
    s += label(x0 + pw / 2, y0 + ph + 60, "1220", 17, "middle", 700)
    s += ln(x0 - 34, y0, x0 - 34, y0 + ph, GR, 1) + ln(x0 - 42, y0, x0 - 26, y0, GR, 1) + ln(x0 - 42, y0 + ph, x0 - 26, y0 + ph, GR, 1)
    s += f'<text x="{x0 - 44}" y="{y0 + ph / 2}" font-size="17" font-weight="700" fill="{GR}" font-family="Inter" text-anchor="middle" transform="rotate(-90 {x0 - 44} {y0 + ph / 2})">3050</text>'
    return svg(W, H, s)
