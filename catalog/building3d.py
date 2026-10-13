# -*- coding: utf-8 -*-
"""Perspective architectural renders of HPL-clad buildings (true pinhole projection)."""
import math, random
from lib import svg, OR

def _proj(W, H, f, hz):
    def P(x, y, z):
        return (W / 2 + f * x / z, hz - f * y / z)
    return P

def _poly(pts, fill, extra=""):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{d}" fill="{fill}" {extra}/>'

def building(W=936, H=1100, dark=False, variant=0, warm=True):
    rnd = random.Random(7 + variant)
    asp = W / H
    f = H * (0.62 if asp < .7 else 0.95)
    hz = H * 0.84                       # horizon (eye height 1.6 m)
    P = _proj(W, H, f, hz)
    eye = 1.6
    a = math.radians(38 if variant == 0 else 52)
    Lv = (-math.cos(a), 0, math.sin(a)); Rv = (math.sin(a), 0, math.cos(a))
    C = ((-3 if variant == 0 else 4) * (1 if asp < .7 else 1.6), -eye, 44 if asp > .7 else 33)
    def pt(u, w, h):
        return P(C[0] + u * Lv[0] + w * Rv[0], C[1] + h, C[2] + u * Lv[2] + w * Rv[2])
    Hb = 27.0; Lw = 42.0; Rw = 30.0
    pw, ph = 1.5, 1.0                    # panel module
    # palettes
    if variant == 0:
        lc, rc = (44, 46, 50), (140, 76, 44)       # graphite / copper-brown HPL
    else:
        lc, rc = (52, 54, 58), (78, 80, 84)
    sky0 = (("#1d2126", "#59606a", "#b59c7d") if dark else ("#9fb3c6", "#d6dde3", "#efe9df"))
    defs = f'''<defs><linearGradient id="bs{variant}{int(dark)}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{sky0[0]}"/><stop offset=".62" stop-color="{sky0[1]}"/><stop offset="1" stop-color="{sky0[2]}"/></linearGradient>
      <linearGradient id="gl{variant}{int(dark)}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{'#2b3a48' if dark else '#7f97ad'}"/><stop offset=".45" stop-color="{'#5d7286' if dark else '#c9d6e1'}"/><stop offset="1" stop-color="{'#151b21' if dark else '#4d5f70'}"/></linearGradient>
      <linearGradient id="gw{variant}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd59a"/><stop offset="1" stop-color="#d98a3d"/></linearGradient>
      <linearGradient id="gr{variant}{int(dark)}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{'#2a2a2b' if dark else '#b9b4ab'}"/><stop offset="1" stop-color="{'#111' if dark else '#8d887f'}"/></linearGradient>
      <linearGradient id="sh{variant}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient>
      </defs>'''
    s = defs + f'<rect width="{W}" height="{H}" fill="url(#bs{variant}{int(dark)})"/>'
    # distant skyline
    for i in range(14):
        x = i * W / 13 - 20; hh = rnd.uniform(.03, .09) * H
        s += f'<rect x="{x:.0f}" y="{hz - hh:.0f}" width="{W/12:.0f}" height="{hh:.0f}" fill="{"#30353b" if dark else "#b8c0c7"}" opacity=".7"/>'
    s += f'<rect x="0" y="{hz:.0f}" width="{W}" height="{H-hz:.0f}" fill="url(#gr{variant}{int(dark)})"/>'
    # ground shadow of building
    s += _poly([pt(0, 0, 0), pt(Lw, 0, 0), pt(Lw + 6, -8, 0), pt(6, -10, 0)], "#000", 'opacity=".22"')
    def shade(c, k):
        return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * k))) for v in c)
    # faces: left (lit), right (shade) ---------------------------------
    def face(side):
        out = ""
        Wd = Lw if side == "L" else Rw
        base = lc if side == "L" else rc
        light = 1.18 if side == "L" else .82
        if dark: light *= .78
        nu, nh = int(Wd / pw), int(Hb / ph)
        def q(u, h):
            return pt(u, 0, h) if side == "L" else pt(0, u, h)
        for i in range(nu):
            for j in range(nh):
                u0, u1 = i * pw + .012, (i + 1) * pw - .012
                h0, h1 = j * ph + .012, (j + 1) * ph - .012
                # window bands
                win = False
                if side == "L":
                    win = (j % 4 in (1, 2)) and (i % 5 in (1, 2, 3)) and j > 0
                else:
                    win = (j % 4 == 2) and j > 0
                if j == 0:
                    col = "url(#gl%s%d)" % (variant, int(dark))
                    if dark and warm and i % 3: col = f"url(#gw{variant})"
                elif win:
                    col = f"url(#gw{variant})" if (dark and warm and rnd.random() < .45) else "url(#gl%s%d)" % (variant, int(dark))
                else:
                    k = light * rnd.uniform(.93, 1.07) * (1 - .10 * (j / nh))
                    col = shade(base, k)
                out += _poly([q(u0, h0), q(u1, h0), q(u1, h1), q(u0, h1)], col)
                if not win and j > 0 and variant == 0:
                    for (uu, hh) in ((u0 + .18, h1 - .14), (u1 - .18, h1 - .14), (u0 + .18, h0 + .14), (u1 - .18, h0 + .14)):
                        x, y = q(uu, hh)
                        r = max(.4, f * .03 / (C[2] + uu * (Lv[2] if side == 'L' else Rv[2])))
                        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#ffffff" opacity=".25"/>'
        # window mullions/frames depth line
        out += _poly([q(0, Hb), q(Wd, Hb), q(Wd, Hb + .35), q(0, Hb + .35)], "#d8d8d6" if not dark else "#6b6e72")
        return out
    # draw farther face first
    s += face("R") + face("L")
    # roof edge highlight & corner
    x0, y0 = pt(0, 0, 0); x1, y1 = pt(0, 0, Hb + .35)
    s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{"#e9e4dc" if not dark else "#9a9488"}" stroke-width="1.6"/>'
    # cantilever canopy over entrance
    s += _poly([pt(6, 0, 3.6), pt(16, 0, 3.6), pt(16, -2.5, 3.6), pt(6, -2.5, 3.6)], "#e8e6e1" if not dark else "#3a3c40")
    s += _poly([pt(6, -2.5, 3.6), pt(16, -2.5, 3.6), pt(16, -2.5, 3.3), pt(6, -2.5, 3.3)], OR)
    # trees
    for (u, w, sz) in ((-4, -9, 1.0), (22, -7, .8), (-2, 12, .9)):
        bx, by = pt(u, w, 0); tx, ty = pt(u, w, 6 * sz)
        rr = abs(ty - by) * .38
        s += f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx:.0f}" y2="{ty + rr*.4:.0f}" stroke="#2b2620" stroke-width="{max(1.5, rr*.08):.1f}"/>'
        s += f'<ellipse cx="{tx:.0f}" cy="{ty + rr*.2:.0f}" rx="{rr*.8:.0f}" ry="{rr:.0f}" fill="{"#2b3530" if dark else "#5d6b54"}" opacity="{.55 if dark else .9}"/>'
    s += f'<rect y="{hz:.0f}" width="{W}" height="{H-hz:.0f}" fill="url(#sh{variant})"/>'
    return svg(W, H, s, extra='preserveAspectRatio="xMidYMid slice" style="display:block;height:100%"')
