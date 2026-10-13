# -*- coding: utf-8 -*-
"""Technical illustrations: exploded assemblies, components, buildings."""
from lib import *


# =========================================================== exploded assemblies
def exploded(system="rivet", W=936, H=980, numbers=True, compact=False):
    """Exploded axonometric of a ventilated facade. Layers inside -> outside.
    system: rivet | glue | hidden | screw | vent"""
    A = Axo(585, 120, 0.80)
    g = ""
    vh = 640          # visible height
    sx0, sy0 = A.p(-80, vh + 30, 420); sx1, sy1 = A.p(430, vh + 30, -40)
    g += (f'<ellipse cx="{(sx0+sx1)/2:.0f}" cy="{(sy0+sy1)/2 + 20:.0f}" rx="{abs(sx1-sx0)/2:.0f}" ry="40" '
          f'fill="#000" opacity=".14" filter="url(#fSh)"/>')
    # 1 wall
    g += a_wall(A, 0, 430, 0, vh, -40, 0)
    # anchors drilled holes shading
    # 2 brackets (fixed upper / sliding lower) in two columns
    cols = [70, 300]
    rows = [(60, True), (330, False), (560, False)]
    for cu in cols:
        for (rv, fixed) in rows:
            g += a_bracket(A, cu, rv, 0, 150, sliding=not fixed)
    # 3 insulation (exploded to sit around brackets) — draw cut away on right so brackets show
    E = 120   # explode step
    ins_d0 = 0
    g_ins = a_ins(A, -40, 230, 0, vh, ins_d0 + E * .0, ins_d0 + 100)
    # 4 membrane
    g_mem = a_mem(A, -80, 160, 0, vh, 100 + E * .8, 100 + E * .8 + 3)
    g += g_ins + g_mem
    # 5/6 profiles
    prof = ""
    pd0 = 150 + E * 1.7
    if system in ("rivet", "glue", "screw", "vent"):
        prof += a_lprofile(A, cols[1] + 22, -20, vh + 10, pd0 - 60)
        prof += a_tprofile(A, cols[0] + 22, -20, vh + 10, pd0 - 60)
    else:  # hidden: vertical profiles + horizontal hanging rails
        prof += a_lprofile(A, cols[1] + 22, -20, vh + 10, pd0 - 60)
        prof += a_tprofile(A, cols[0] + 22, -20, vh + 10, pd0 - 60)
    g += prof
    # glue extras: tape + bead on profiles
    pf = pd0 - 60 + 40  # profile face d
    if system == "glue":
        for cu in (cols[0] + 22, cols[1] + 22):
            g += A.box(cu - 30, cu - 22, 20, vh - 10, pf, pf + 4, "#202124", "#111", "#333", .5)
            g += A.box(cu - 12, cu - 2, 20, vh - 10, pf, pf + 6, OR, "#b84d10", "#f59a62", .5)
    if system == "hidden":
        for rv in (100, 420):
            g += A.box(-40, 420, rv, rv + 14, pf, pf + 6, "url(#gSteel)", STEEL_D, STEEL_L, .6)
    # 8 panel(s) exploded forward
    pd = pf + E * 1.6
    riv = []
    if system in ("rivet", "screw"):
        for cu in cols:
            for vv in (60, 230, 400, 560):
                riv.append((cu + 22 - 60 + 60, vv))
    lower_cut = 300
    panel = a_panel(A, -60, 190, -10, lower_cut, pd, 9, [r for r in riv if r[0] < 190 and r[1] < lower_cut])
    panel2 = a_panel(A, -60, 190, lower_cut + 12, vh + 10, pd, 9, [r for r in riv if r[0] < 190 and r[1] > lower_cut + 12])
    if system == "hidden":
        # clips on rear of panel
        for (vv) in (90, 410):
            g += A.box(30, 70, vv, vv + 26, pd - 14, pd, "#B5BBC2", STEEL_D, STEEL_L, .6)
            g += A.box(120, 160, vv, vv + 26, pd - 14, pd, "#B5BBC2", STEEL_D, STEEL_L, .6)
    g += panel2 + panel
    # screw: washers ring
    # airflow arrows in the gap (vent): between membrane and panel
    gd = (pf + pd) / 2
    ax0, ay0 = A.p(40, vh + 30, gd)
    ax1, ay1 = A.p(40, -60, gd)
    g += air([(ax0, ay0), (ax1, ay1)], 2.6, "10 7")
    bx0, by0 = A.p(200, vh + 30, gd)
    bx1, by1 = A.p(200, -60, gd)
    g += air([(bx0, by0), (bx1, by1)], 2.6, "10 7")
    mem_d = 100 + E * .8
    pts = {"wall": (420, 600, 0), "bracket": (cols[1] + 26, 330 + 23, 100),
           "anchor": (cols[1] + 11, 60 + 23, 4), "ins": (-20, 470, 100), "mem": (60, 250, mem_d + 3),
           "lprof": (cols[1] + 22, 40, pd0 - 60 + 20), "tprof": (cols[0] + 22, vh - 10, pf),
           "panel": (40, 120, pd + 9), "panel2": (40, 470, pd + 9), "rivet": (82, 230, pd + 9),
           "gap": (120, -40, gd), "clip": (50, 100, pd - 7), "rail": (380, 107, pf + 6),
           "glue": (cols[1] + 15, 200, pf + 6), "tape": (cols[1] - 4, 420, pf + 4)}
    return A, g, pts


EXPL_POINTS = {
    # name: (u,v,d) anchor points for callouts
    "wall": (420, 520, -10),
    "bracket": (300 + 26, 330 + 23, 60),
    "anchor": (300 + 11, 60 + 23, 4),
    "ins": (0, 420, 100),
    "mem": (100, 300, 151),
    "lprof": (322, 120, 140),
    "tprof": (92, 640, 145),
    "panel": (60, 150, 290),
    "panel2": (60, 500, 290),
    "rivet": (82, 230, 299),
    "gap": (150, -20, 205),
}


def exploded_figure(system, items, W=936, H=900, side="right"):
    """items: list of (key, label) in legend order -> numbered callouts."""
    A, g, EXPL_POINTS = exploded(system)
    # place numbers next to anchor points
    out = g
    for i, (key, _) in enumerate(items):
        u, v, d = EXPL_POINTS[key]
        x, y = A.p(u, v, d)
        out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="{GR}"/>'
        out += num(x + 0, y - 0 + 0, i + 1, 16) if False else ""
        out += (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + 26:.0f}" y2="{y - 26:.0f}" stroke="{GR}" stroke-width="1"/>'
                + num(x + 38, y - 38, i + 1, 16))
    return svg(W, H, out)


# =========================================================== buildings
def building(W=936, H=1100, dark=False, variant=0, warm=True):
    """Architectural elevation-perspective of a building with HPL rainscreen grid."""
    g = rect(0, 0, W, H, "url(#gSkyDark)" if dark else "url(#gSky)", "none", 0)
    # ground
    gy = H * .86
    g += rect(0, gy, W, H - gy, "#2a2b2d" if dark else "#cfccc6", "none", 0)
    # main volume in 2-point-ish perspective: left facade (dark HPL), right facade (orange-brown HPL)
    vx = W * (.58 if variant == 0 else .42)  # corner x
    top = H * .10
    Lx = W * .02
    Rx = W * 1.02
    lt, lb = top + 90, gy - 20     # far left top/bottom
    rt, rb = top + 60, gy - 10
    # left face polygon
    g += poly2([(Lx, lt), (vx, top), (vx, gy + 6), (Lx, lb)], "url(#pHpl)", "none", 0)
    g += poly2([(vx, top), (Rx, rt), (Rx, rb), (vx, gy + 6)], "#8a4a2a" if variant == 0 else "#3a3c40", "none", 0)
    # panel grid: left face
    rows = 11
    for i in range(1, rows):
        t = i / rows
        y1 = lt + (lb - lt) * t
        y2 = top + (gy + 6 - top) * t
        g += ln(Lx, y1, vx, y2, "#121315", 1.6)
        y3 = rt + (rb - rt) * t
        g += ln(vx, y2, Rx, y3, "#3a1f12" if variant == 0 else "#1b1c1f", 1.6)
    cols = 9
    for j in range(1, cols):
        s = j / cols
        x = Lx + (vx - Lx) * (s ** 1.25)
        g += ln(x, lt + (top - lt) * (s ** 1.25), x, lb + (gy + 6 - lb) * (s ** 1.25), "#121315", 1.6)
    for j in range(1, 6):
        s = j / 6
        x = vx + (Rx - vx) * (s ** .85)
        g += ln(x, top + (rt - top) * s ** .85, x, gy + 6 + (rb - gy - 6) * s ** .85,
                "#3a1f12" if variant == 0 else "#1b1c1f", 1.6)
    # windows ribbon on left face
    for k in range(4):
        t0 = .22 + k * .19
        t1 = t0 + .07
        for (a, b) in ((.08, .30), (.40, .62), (.72, .93)):
            pts = []
            for (s, t) in ((a, t0), (b, t0), (b, t1), (a, t1)):
                xs = Lx + (vx - Lx) * (s ** 1.25)
                yt = lt + (top - lt) * (s ** 1.25)
                yb = lb + (gy + 6 - lb) * (s ** 1.25)
                pts.append((xs, yt + (yb - yt) * t))
            g += poly2(pts, "url(#gGlassWarm)" if warm and k % 2 == 0 and dark else "url(#gGlass)", "#0e0f10", 1.5)
    # rivets dots subtle on right face
    for i in range(1, 11):
        for j in range(1, 12):
            s = j / 12
            t = i / 11
            x = vx + (Rx - vx) * (s ** .85)
            yt = top + (rt - top) * s ** .85
            yb = gy + 6 + (rb - gy - 6) * s ** .85
            y = yt + (yb - yt) * (t - .045)
            g += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.6" fill="#c9a189" opacity=".55"/>'
    # corner highlight & shade
    g += ln(vx, top, vx, gy + 6, "#d7d7d7" if not dark else "#777", 1.4)
    g += poly2([(vx, top), (Rx, rt), (Rx, rb), (vx, gy + 6)], "url(#gShade)", "none", 0)
    # parapet line
    g += pl([(Lx, lt - 10), (vx, top - 12), (Rx, rt - 10)], "#e6e6e6" if not dark else "#9a9a9a", 3)
    # ground line & trees silhouettes
    g += rect(0, gy + 6, W, 6, "#bdb9b2" if not dark else "#1f2022", "none", 0)
    return svg(W, H, g, extra='preserveAspectRatio="xMidYMid slice" style="display:block;height:100%"')


from building3d import building  # noqa: E402,F811


def hpl_closeup(W=500, H=500):
    """Close-up of HPL panel joint + rivet heads + corner, in axonometry."""
    A = Axo(250, 70, 1.6, U=(0.75, 0.32), D=(-0.6, 0.34))
    g = rect(0, 0, W, H, "#3a3d42", "none", 0)
    g += a_panel(A, -60, 140, 0, 160, 0, 10, [(20, 30), (110, 30), (20, 130), (110, 130)])
    g += a_panel(A, -60, 140, 168, 330, 0, 10, [(20, 198), (110, 198), (20, 300), (110, 300)])
    return svg(W, H, g, extra='preserveAspectRatio="xMidYMid slice" style="display:block;height:100%"')


# =========================================================== component drawings (isolated)
def comp(kind, W=240, H=170):
    A = Axo(W * .5, H * .2, 1.0)
    g = ""
    if kind == "panel":
        A = Axo(W * .55, 18, 1.0)
        g += a_panel(A, -60, 80, 0, 120, 0, 9)
    elif kind == "panel_groove":
        A = Axo(W * .55, 18, 1.0)
        g += a_panel(A, -60, 80, 0, 120, 0, 10)
        a, b = A.p(80, 30, 4), A.p(80, 100, 4)
        g += f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{OR}" stroke-width="3"/>'
    elif kind == "membrane":
        cx, cy = W * .42, H * .5
        g += rect(cx - 70, cy - 36, 140, 72, "url(#pMem)", "#2c2f33", 1)
        g += f'<ellipse cx="{cx + 70}" cy="{cy}" rx="16" ry="36" fill="#5b6067" stroke="#2c2f33"/>'
        g += f'<ellipse cx="{cx + 70}" cy="{cy}" rx="6" ry="13" fill="#2b2d31"/>'
        g += poly2([(cx - 70, cy + 36), (cx - 110, cy + 60), (cx + 30, cy + 60), (cx + 70, cy + 36)], "#555a61", "#2c2f33", 1)
    elif kind == "insulation":
        A = Axo(W * .55, 30, 1.0)
        g += a_ins(A, -40, 80, 0, 90, 0, 50)
    elif kind == "lprofile":
        A = Axo(W * .5, 10, 1.0, U=(0.8, 0.3), D=(-0.62, 0.36))
        g += a_lprofile(A, 30, 0, 130, 0, 46, 3, 30)
    elif kind == "tprofile":
        A = Axo(W * .5, 10, 1.0)
        g += a_tprofile(A, 30, 0, 130, 0, 46, 3, 36)
    elif kind == "vprofile":
        A = Axo(W * .5, 10, 1.0)
        g += a_tprofile(A, 30, 0, 130, 0, 46, 3, 30)
        g += A.box(60, 66, 0, 130, 40, 52, "url(#gSteelV)", STEEL_D, STEEL_L, .6)
    elif kind in ("bracket_fixed", "bracket_sliding"):
        A = Axo(W * .52, 30, 1.6)
        g += a_bracket(A, 0, 0, 0, 70, sliding=(kind == "bracket_sliding"), h=56, w=30)
    elif kind == "anchor":
        x, y = 30, H * .5
        g += rect(x, y - 13, 12, 26, "#9aa0a7", GR, 1)
        g += rect(x + 12, y - 9, 16, 18, "#b5bac0", GR, .8)
        g += rect(x + 28, y - 7, 140, 14, "url(#gSteel)", GR, .8)
        g += rect(x + 120, y - 10, 50, 20, "#c2c7cd", GR, .8)
        for i in range(x + 34, x + 118, 7):
            g += ln(i, y - 7, i + 4, y + 7, "#7d838a", .8)
    elif kind == "dowel":
        x, y = 30, H * .5
        g += f'<ellipse cx="{x + 6}" cy="{y}" rx="7" ry="24" fill="#c9ccd0" stroke="{GR}"/>'
        g += rect(x + 8, y - 8, 140, 16, "#d6d8db", GR, .8)
        for i in range(x + 20, x + 140, 12):
            g += ln(i, y - 8, i, y + 8, MG, .8)
    elif kind == "rivet":
        x, y = 40, H * .5
        g += f'<path d="M{x} {y - 22} Q{x + 14} {y} {x} {y + 22} Z" fill="url(#gSteel)" stroke="{GR}"/>'
        g += rect(x + 2, y - 8, 66, 16, "url(#gSteel)", GR, .8)
        g += rect(x + 68, y - 2.5, 90, 5, "#9aa0a7", GR, .6)
        g += f'<circle cx="{x + 160}" cy="{y}" r="4.5" fill="#9aa0a7" stroke="{GR}" stroke-width=".6"/>'
    elif kind == "screw":
        x, y = 40, H * .5
        g += f'<ellipse cx="{x + 2}" cy="{y}" rx="6" ry="26" fill="{HPL}" stroke="#000"/>'
        g += rect(x + 6, y - 22, 6, 44, "#b8bdc3", GR, .8)
        g += rect(x + 12, y - 7, 120, 14, "url(#gSteel)", GR, .8)
        for i in range(x + 16, x + 128, 8):
            g += ln(i, y - 7, i + 5, y + 7, "#7d838a", .8)
        g += poly2([(x + 132, y - 7), (x + 150, y), (x + 132, y + 7)], "#c2c7cd", GR, .8)
    elif kind == "gasket":
        A = Axo(W * .5, 40, 1.2)
        g += A.box(-30, 70, 0, 60, 0, 8, "#26282b", "#111", "#3a3d41", .7)
        for vv in (18, 42):
            a, b = A.p(0, vv, 8), A.p(40, vv, 8)
            g += f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#f2f3f5" stroke-width="7" stroke-linecap="round"/>'
    elif kind == "tape":
        cx, cy = W * .5, H * .52
        g += f'<ellipse cx="{cx}" cy="{cy + 14}" rx="66" ry="34" fill="#111"/>'
        g += rect(cx - 66, cy - 14, 132, 28, "#1b1c1e", "none", 0)
        g += f'<ellipse cx="{cx}" cy="{cy - 14}" rx="66" ry="34" fill="#2a2c2f" stroke="#000"/>'
        g += f'<ellipse cx="{cx}" cy="{cy - 14}" rx="34" ry="17" fill="#e8e9eb" stroke="#999"/>'
        g += f'<path d="M{cx + 52} {cy - 34} l40 -6 l2 10 l-38 8z" fill="{OR}"/>'
    elif kind == "epdm":
        cx, cy = W * .5, H * .52
        g += f'<ellipse cx="{cx}" cy="{cy + 16}" rx="70" ry="36" fill="#0f1011"/>'
        g += rect(cx - 70, cy - 16, 140, 32, "#1a1b1d", "none", 0)
        g += f'<ellipse cx="{cx}" cy="{cy - 16}" rx="70" ry="36" fill="#26282b" stroke="#000"/>'
        g += f'<ellipse cx="{cx}" cy="{cy - 16}" rx="40" ry="20" fill="#fff" stroke="#999"/>'
    elif kind == "cartridge":
        x, y = 22, H * .5
        g += rect(x, y - 20, 160, 40, "url(#gSteelV)", GR, 1, 'rx="6"')
        g += rect(x + 30, y - 20, 70, 40, "#fff", GR, .8)
        g += label(x + 65, y + 5, "ПУ КЛЕЙ", 11, "middle", 700, GR)
        g += poly2([(x + 160, y - 9), (x + 205, y - 3), (x + 205, y + 3), (x + 160, y + 9)], "#e4e6e8", GR, .8)
    elif kind in ("primer", "activator"):
        cx, cy = W * .5, H * .55
        col = "#2b2d31" if kind == "primer" else "#e8e9eb"
        g += rect(cx - 30, cy - 50, 60, 100, col, GR, 1, 'rx="6"')
        g += rect(cx - 14, cy - 66, 28, 18, OR, GR, .8, 'rx="3"')
        g += rect(cx - 26, cy - 18, 52, 40, "#fff", GR, .6)
        g += label(cx, cy + 6, "ПРАЙМЕР" if kind == "primer" else "АКТИВАТОР", 8.5, "middle", 700, GR)
    elif kind == "clip":
        A = Axo(W * .5, 30, 1.5)
        g += A.box(-20, 50, 0, 18, 0, 5, "url(#gSteel)", STEEL_D, STEEL_L, .7)
        g += A.box(-20, 50, 0, 50, 5, 9, "url(#gSteel)", STEEL_D, STEEL_L, .7)
        g += A.box(-20, 50, 40, 50, 9, 24, "url(#gSteel)", STEEL_D, STEEL_L, .7)
    elif kind == "washer":
        cx, cy = W * .5, H * .5
        g += f'<ellipse cx="{cx}" cy="{cy}" rx="48" ry="48" fill="#1e1f22" stroke="#000"/>'
        g += f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="34" fill="url(#gSteel)" stroke="{GR}"/>'
        g += f'<circle cx="{cx}" cy="{cy}" r="10" fill="#fff" stroke="{GR}"/>'
    return svg(W, H, g)


# =========================================================== mini icons for process steps (line style)
def mini(kind, W=260, H=118):
    """Small technical vignettes for step lists. Graphite line drawing + orange accent."""
    g = ""
    c = GR
    if kind == "mark":
        g += rect(20, 10, 220, 98, "url(#pCon)", "none", 0)
        g += ln(20, 50, 240, 50, OR, 1.6, 'stroke-dasharray="6 4"') + ln(110, 10, 110, 108, OR, 1.6, 'stroke-dasharray="6 4"')
        g += ln(190, 10, 190, 108, OR, 1.6, 'stroke-dasharray="6 4"')
        for x in (110, 190):
            g += f'<circle cx="{x}" cy="50" r="5" fill="none" stroke="{GR}" stroke-width="1.6"/>'
    elif kind == "bracket":
        g += rect(20, 10, 220, 98, "url(#pCon)", "none", 0)
        A = Axo(100, 22, 1.0)
        g += a_bracket(A, 0, 0, 0, 60, False, 44, 24)
        A = Axo(190, 22, 1.0)
        g += a_bracket(A, 0, 0, 0, 60, True, 44, 24)
    elif kind == "ins":
        g += rect(20, 10, 90, 98, "url(#pCon)", "none", 0)
        A = Axo(150, 22, 1.0)
        g += a_ins(A, -20, 90, 0, 80, 0, 40)
    elif kind == "mem":
        g += rect(20, 10, 80, 98, "url(#pIns)", "none", 0)
        g += rect(70, 10, 170, 98, "url(#pMem)", "none", 0)
        g += ln(70, 10, 70, 108, "#222", 1)
        g += f'<circle cx="90" cy="30" r="6" fill="#ccc" stroke="#333"/><circle cx="90" cy="88" r="6" fill="#ccc" stroke="#333"/>'
    elif kind == "profiles":
        A = Axo(70, 6, .8)
        g += a_lprofile(A, 0, 0, 125, 0, 40, 3, 22)
        A = Axo(180, 6, .8)
        g += a_tprofile(A, 0, 0, 125, 0, 40, 3, 32)
    elif kind == "hplprep":
        A = Axo(150, 14, 1.0)
        g += a_panel(A, -80, 80, 0, 80, 0, 8)
        x, y = A.p(-40, 20, 8)
        g += f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="{OR}" stroke-width="2"/>'
        x, y = A.p(40, 20, 8)
        g += f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="{OR}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="3" fill="{OR}"/>'
    elif kind == "panel":
        A = Axo(130, 10, .85)
        g += a_lprofile(A, 60, 0, 120, -40, 40, 3, 22)
        g += a_panel(A, -90, 40, 0, 120, 10, 8)
        g += arrow(40, 70, 75, 70, OR, 2.4)
    elif kind == "rivet":
        A = Axo(150, 10, .9)
        g += a_panel(A, -100, 60, 0, 110, 0, 8, [(-60, 20), (-60, 90), (20, 20), (20, 90)])
        x, y = A.p(20, 90, 8)
        g += f'<circle cx="{x}" cy="{y}" r="14" fill="none" stroke="{OR}" stroke-width="2"/>'
    elif kind == "geom":
        g += rect(40, 14, 180, 90, "url(#pHpl)", "#000", .8)
        g += ln(130, 14, 130, 104, "#111", 2) + ln(40, 59, 220, 59, "#111", 2)
        g += ln(10, 30, 250, 30, OR, 1.4, 'stroke-dasharray="3 3"') + ln(30, 6, 30, 112, OR, 1.4, 'stroke-dasharray="3 3"')
    elif kind == "final":
        g += rect(40, 14, 180, 90, "url(#pHpl)", "#000", .8)
        g += f'<circle cx="190" cy="40" r="22" fill="#fff" stroke="{OR}" stroke-width="2.5"/>'
        g += pl([(180, 40), (188, 48), (202, 32)], OR, 3)
    elif kind == "clean":
        g += rect(40, 14, 180, 90, "#e9eaec", MG, .8)
        g += pl([(60, 80), (100, 50), (140, 80), (180, 50)], OR, 2, 'stroke-dasharray="2 5" stroke-linecap="round"')
        g += rect(150, 28, 54, 34, "#fff", GR, 1.2, 'rx="4"')
    elif kind == "primer":
        g += rect(40, 40, 180, 30, "url(#gSteelV)", GR, .8)
        g += rect(70, 44, 100, 22, "#2b2d31", "none", 0, 'opacity=".8"')
        g += pl([(170, 30), (200, 10)], GR, 3) + rect(158, 26, 22, 12, OR, GR, .8)
    elif kind == "activator":
        g += rect(40, 40, 180, 30, "url(#gSteelV)", GR, .8)
        g += rect(70, 44, 100, 22, "#cfe3f5", "none", 0, 'opacity=".9"')
        g += rect(176, 30, 40, 24, "#fff", GR, 1, 'rx="4"')
    elif kind == "tape":
        g += rect(40, 40, 180, 30, "url(#gSteelV)", GR, .8)
        g += rect(40, 44, 180, 8, "#1b1c1e", "none", 0)
        g += rect(40, 58, 180, 8, "#1b1c1e", "none", 0)
        g += arrow(60, 96, 200, 96, OR, 2)
    elif kind == "glue":
        g += rect(40, 40, 180, 30, "url(#gSteelV)", GR, .8)
        g += rect(40, 44, 180, 6, "#1b1c1e", "none", 0)
        g += poly2([(40, 62), (220, 62), (220, 54), (40, 54)], OR, "#b84d10", .6)
        g += rect(190, 6, 50, 22, "#e6e6e6", GR, 1, 'rx="4"') + poly2([(190, 12), (170, 34), (176, 36), (194, 22)], "#ddd", GR, .8)
    elif kind == "press":
        g += rect(40, 14, 180, 90, "url(#pHpl)", "#000", .8)
        g += arrow(250, 59, 225, 59, OR, 3) + arrow(10, 59, 35, 59, OR, 3)
    elif kind == "cure":
        g += f'<circle cx="130" cy="59" r="42" fill="none" stroke="{GR}" stroke-width="2"/>'
        g += pl([(130, 30), (130, 59), (152, 70)], OR, 3)
    elif kind == "clip":
        g += rect(30, 50, 200, 14, "url(#gSteelV)", GR, .8)
        g += rect(60, 20, 150, 26, "url(#pHpl)", "#000", .8)
        g += rect(80, 40, 22, 22, "#b5bbc2", GR, .8) + rect(160, 40, 22, 22, "#b5bbc2", GR, .8)
        g += arrow(130, 6, 130, 18, OR, 2.4)
    elif kind == "adjust":
        g += rect(60, 14, 150, 90, "url(#pHpl)", "#000", .8)
        g += arrow(30, 80, 30, 40, OR, 2.4, True)
        g += f'<circle cx="230" cy="59" r="12" fill="none" stroke="{GR}" stroke-width="2"/>'
    elif kind == "screw":
        g += rect(40, 14, 180, 90, "url(#pHpl)", "#000", .8)
        for (x, y) in ((70, 34), (190, 34), (70, 84), (190, 84)):
            g += f'<circle cx="{x}" cy="{y}" r="7" fill="#26282b" stroke="#777"/><path d="M{x - 3} {y}h6M{x} {y - 3}v6" stroke="#999"/>'
    else:
        g += rect(40, 14, 180, 90, XL, LG, 1)
    return svg(W, H, g)
