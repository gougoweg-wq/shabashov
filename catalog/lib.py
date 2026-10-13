# -*- coding: utf-8 -*-
"""UZHPL catalog — shared SVG drawing library.

All technical drawings share one visual language:
graphite / gray construction lines, white ground, orange numbered markers,
subtle blue airflow arrows. Axonometric views use one fixed oblique projection.
"""
import math

OR = "#F26A1B"      # signature orange
GR = "#1D1F22"      # graphite
DG = "#3A3D42"      # dark gray
MG = "#8A8F96"      # mid gray
LG = "#D9DCE0"      # light gray
XL = "#F2F3F5"      # extra light
BL = "#3D8FD6"      # airflow blue
INS = "#D9B866"     # mineral wool
INS_D = "#B8963F"
STEEL = "#C9CED4"
STEEL_D = "#9AA1A9"
STEEL_L = "#E6E9EC"
HPL = "#2B2D31"
HPL_S = "#1A1B1E"
HPL_T = "#45484E"
CON = "#B9B9B4"
CON_S = "#9C9C97"
CON_T = "#CFCFCA"
MEM = "#4A4E55"

DEFS = f"""
<defs>
 <pattern id="pCon" width="22" height="22" patternUnits="userSpaceOnUse">
  <rect width="22" height="22" fill="{CON}"/>
  <circle cx="4" cy="6" r="1.1" fill="#8f8f8a"/><circle cx="15" cy="3" r=".7" fill="#a3a39e"/>
  <circle cx="11" cy="15" r="1.4" fill="#9a9a95"/><circle cx="19" cy="18" r=".8" fill="#8a8a85"/>
  <circle cx="6" cy="19" r=".6" fill="#a8a8a3"/>
 </pattern>
 <pattern id="pConS" width="22" height="22" patternUnits="userSpaceOnUse">
  <rect width="22" height="22" fill="{CON_S}"/>
  <circle cx="5" cy="9" r="1" fill="#82827d"/><circle cx="16" cy="16" r="1.2" fill="#85857f"/>
 </pattern>
 <pattern id="pIns" width="26" height="12" patternUnits="userSpaceOnUse">
  <rect width="26" height="12" fill="{INS}"/>
  <path d="M0 6 Q6.5 0 13 6 T26 6" fill="none" stroke="{INS_D}" stroke-width="1" opacity=".75"/>
  <path d="M0 11 Q6.5 7 13 11 T26 11" fill="none" stroke="#e8cf8a" stroke-width=".8"/>
 </pattern>
 <pattern id="pInsS" width="26" height="12" patternUnits="userSpaceOnUse">
  <rect width="26" height="12" fill="{INS_D}"/>
  <path d="M0 6 Q6.5 0 13 6 T26 6" fill="none" stroke="#9d7c2d" stroke-width="1"/>
 </pattern>
 <pattern id="pHpl" width="40" height="40" patternUnits="userSpaceOnUse">
  <rect width="40" height="40" fill="{HPL}"/>
  <path d="M3 7l9 2M22 30l10-3M28 9l5 6M6 31l4-6" stroke="#34373c" stroke-width="1"/>
  <circle cx="17" cy="18" r=".8" fill="#3a3d42"/><circle cx="35" cy="35" r=".7" fill="#3a3d42"/>
 </pattern>
 <pattern id="pMem" width="10" height="10" patternUnits="userSpaceOnUse">
  <rect width="10" height="10" fill="{MEM}"/><path d="M0 10L10 0" stroke="#565b62" stroke-width="1"/>
 </pattern>
 <!-- section hatches (2D drawings) -->
 <pattern id="hCon" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="12" height="12" fill="#ECECEA"/><line x1="0" y1="0" x2="0" y2="12" stroke="{MG}" stroke-width="1"/>
 </pattern>
 <pattern id="hIns" width="16" height="14" patternUnits="userSpaceOnUse">
  <rect width="16" height="14" fill="#F6EED6"/>
  <path d="M0 7 L4 1 L8 13 L12 1 L16 7" fill="none" stroke="{INS_D}" stroke-width=".9"/>
 </pattern>
 <pattern id="hInsV" width="14" height="16" patternUnits="userSpaceOnUse">
  <rect width="14" height="16" fill="#F6EED6"/>
  <path d="M7 0 L1 4 L13 8 L1 12 L7 16" fill="none" stroke="{INS_D}" stroke-width=".9"/>
 </pattern>
 <pattern id="hBrick" width="24" height="12" patternUnits="userSpaceOnUse">
  <rect width="24" height="12" fill="#ECECEA"/><path d="M0 0H24M0 6H24M6 0V6M18 6V12" stroke="{MG}" stroke-width=".8"/>
 </pattern>
 <linearGradient id="gSteel" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#EEF0F2"/><stop offset=".55" stop-color="{STEEL}"/><stop offset="1" stop-color="#AEB4BB"/>
 </linearGradient>
 <linearGradient id="gSteelV" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#B3B9C0"/><stop offset=".45" stop-color="#EEF0F2"/><stop offset="1" stop-color="#A9AFB6"/>
 </linearGradient>
 <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#C9CED3"/><stop offset=".6" stop-color="#E7E8E8"/><stop offset="1" stop-color="#F1EEE9"/>
 </linearGradient>
 <linearGradient id="gSkyDark" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#2A2D31"/><stop offset=".65" stop-color="#4A4E54"/><stop offset="1" stop-color="#7d7a74"/>
 </linearGradient>
 <linearGradient id="gGlass" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#5d6670"/><stop offset=".5" stop-color="#8e99a3"/><stop offset="1" stop-color="#3f464e"/>
 </linearGradient>
 <linearGradient id="gGlassWarm" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#e9b877"/><stop offset="1" stop-color="#b77a3c"/>
 </linearGradient>
 <linearGradient id="gShade" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#000" stop-opacity=".0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/>
 </linearGradient>
 <marker id="aBl" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
  <path d="M0 0L10 5L0 10z" fill="{BL}"/></marker>
 <marker id="aOr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
  <path d="M0 0L10 5L0 10z" fill="{OR}"/></marker>
 <marker id="aGr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
  <path d="M0 0L10 5L0 10z" fill="{GR}"/></marker>
 <marker id="tick" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto">
  <path d="M2 8L8 2" stroke="{GR}" stroke-width="1.4"/></marker>
</defs>
"""


def svg(w, h, body, cls="", extra=""):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" width="100%" '
            f'xmlns="http://www.w3.org/2000/svg" {extra}>{DEFS}{body}</svg>')


# ------------------------------------------------------------------ markers
def num(x, y, n, r=15, fs=None):
    fs = fs or int(r * 1.05)
    return (f'<g><circle cx="{x}" cy="{y}" r="{r}" fill="{OR}"/>'
            f'<text x="{x}" y="{y + fs * 0.36}" text-anchor="middle" font-size="{fs}" '
            f'font-weight="700" fill="#fff" font-family="Inter">{n}</text></g>')


def leader(x1, y1, x2, y2, n=None, r=13):
    s = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GR}" stroke-width="1"/>'
         f'<circle cx="{x1}" cy="{y1}" r="3" fill="{GR}"/>')
    if n is not None:
        s += num(x2, y2, n, r)
    return s


def label(x, y, text, size=15, anchor="start", weight=500, color=GR, ls=0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" font-family="Inter">{text}</text>')


def callout(px, py, tx, ty, text, anchor="start", n=None, size=14):
    """Leader from point to label (text with optional orange number)."""
    s = (f'<polyline points="{px},{py} {tx},{ty}" fill="none" stroke="{GR}" stroke-width=".9"/>'
         f'<circle cx="{px}" cy="{py}" r="2.6" fill="{GR}"/>')
    off = 8 if anchor == "start" else -8
    if n is not None:
        cx = tx + (14 if anchor == "start" else -14)
        s += num(cx, ty, n, 11, 12)
        off += 26 if anchor == "start" else -26
    s += label(tx + off, ty + 5, text, size, anchor)
    return s


def dim(x1, y1, x2, y2, text, off=0, size=12, vertical=False):
    """Dimension line with ticks. text e.g. 'ПО ПРОЕКТУ'."""
    s = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GR}" stroke-width=".8" '
         f'marker-start="url(#tick)" marker-end="url(#tick)"/>')
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if vertical:
        s += (f'<text x="{mx - 7}" y="{my}" font-size="{size}" fill="{OR}" font-weight="600" '
              f'font-family="Inter" text-anchor="middle" transform="rotate(-90 {mx - 7} {my})">{text}</text>')
    else:
        s += label(mx, my - 7 + off, text, size, "middle", 600, OR)
    return s


def air(points, w=2.2, dash=None):
    d = " ".join(f"{x},{y}" for x, y in points)
    da = f'stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline points="{d}" fill="none" stroke="{BL}" stroke-width="{w}" '
            f'stroke-linecap="round" {da} marker-end="url(#aBl)" opacity=".9"/>')


def arrow(x1, y1, x2, y2, color=OR, w=2.4, both=False):
    m = "aOr" if color == OR else ("aBl" if color == BL else "aGr")
    st = f'marker-start="url(#{m})"' if both else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" '
            f'marker-end="url(#{m})" {st}/>')


# ------------------------------------------------------------------ axonometry
class Axo:
    """Oblique axonometry. u = along wall (right), v = down, d = out of wall (toward viewer)."""

    def __init__(self, ox, oy, s=1.0, U=(0.80, 0.30), D=(-0.62, 0.36)):
        self.ox, self.oy, self.s, self.U, self.D = ox, oy, s, U, D

    def p(self, u, v, d):
        s = self.s
        return (self.ox + s * (u * self.U[0] + d * self.D[0]),
                self.oy + s * (u * self.U[1] + v + d * self.D[1]))

    def poly(self, pts, fill, stroke=GR, sw=0.8, op=1):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in (self.p(*q) for q in pts))
        return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" opacity="{op}"/>'

    def box(self, u0, u1, v0, v1, d0, d1, front, side, top, sw=0.8, stroke=GR):
        """Front face at d=d1, top face v=v0, right face u=u1 (visible faces)."""
        return (self.poly([(u0, v0, d0), (u1, v0, d0), (u1, v0, d1), (u0, v0, d1)], top, stroke, sw) +
                self.poly([(u1, v0, d0), (u1, v1, d0), (u1, v1, d1), (u1, v0, d1)], side, stroke, sw) +
                self.poly([(u0, v0, d1), (u1, v0, d1), (u1, v1, d1), (u0, v1, d1)], front, stroke, sw))

    def line(self, a, b, color=GR, w=1, dash=None):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        da = f'stroke-dasharray="{dash}"' if dash else ""
        return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}" {da}/>'

    def dot(self, u, v, d, r=4.2, fill="#B9BEC4"):
        x, y = self.p(u, v, d)
        return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r}" ry="{r * .9}" fill="{fill}" stroke="#55595f" stroke-width=".8"/>'
                f'<ellipse cx="{x - r * .3:.1f}" cy="{y - r * .3:.1f}" rx="{r * .35}" ry="{r * .3}" fill="#fff" opacity=".7"/>')

    def pt(self, u, v, d):
        return self.p(u, v, d)


# Reusable parts in axonometry -------------------------------------------------
def a_bracket(A, u, v, d0, ext, sliding=False, h=46, w=26):
    """L-bracket: plate on wall + flange out along d. sliding -> longer slot."""
    s = A.box(u, u + w, v, v + h, d0, d0 + 4, STEEL, STEEL_D, STEEL_L, .7)
    s += A.box(u + w - 4, u + w, v, v + h, d0 + 4, d0 + ext, "url(#gSteel)", STEEL_D, STEEL_L, .7)
    # anchor head on wall plate
    s += A.dot(u + w * .42, v + h * .5, d0 + 4, 3.2, "#8f959c")
    # slot on flange (drawn on right face)
    sl = .55 if sliding else .3
    a, b = A.p(u + w, v + h * .5, d0 + ext * .35), A.p(u + w, v + h * .5, d0 + ext * (.35 + sl))
    s += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#5c6168" stroke-width="5" stroke-linecap="round"/>'
    return s


def a_lprofile(A, u, v0, v1, d0, flange=40, t=3, web=22):
    """Vertical L-profile: web attached to bracket flange (plane u=const), face flange at d=d0+flange."""
    s = A.box(u, u + t, v0, v1, d0, d0 + flange, STEEL_D, "url(#gSteelV)", STEEL_L, .7)
    s += A.box(u - web, u + t, v0, v1, d0 + flange - t, d0 + flange, "url(#gSteelV)", STEEL_D, STEEL_L, .7)
    return s


def a_tprofile(A, u, v0, v1, d0, flange=40, t=3, half=40):
    s = A.box(u, u + t, v0, v1, d0, d0 + flange, STEEL_D, "url(#gSteelV)", STEEL_L, .7)
    s += A.box(u - half, u + half + t, v0, v1, d0 + flange - t, d0 + flange, "url(#gSteelV)", STEEL_D, STEEL_L, .7)
    return s


def a_panel(A, u0, u1, v0, v1, d0, t=8, rivets=None):
    s = A.box(u0, u1, v0, v1, d0, d0 + t, "url(#pHpl)", HPL_S, HPL_T, .9, "#111")
    for (u, v) in rivets or []:
        s += A.dot(u, v, d0 + t, 4.3)
    return s


def a_wall(A, u0, u1, v0, v1, d0, d1):
    s = A.box(u0, u1, v0, v1, d0, d1, "url(#pCon)", "url(#pConS)", CON_T, 1)
    return s


def a_ins(A, u0, u1, v0, v1, d0, d1):
    s = A.box(u0, u1, v0, v1, d0, d1, "url(#pIns)", "url(#pInsS)", "#E7CE8A", .8)
    # board joints
    mid = (v0 + v1) / 2
    s += A.line((u0, mid, d1), (u1, mid, d1), INS_D, .8)
    return s


def a_mem(A, u0, u1, v0, v1, d0, d1=None):
    d1 = d1 if d1 is not None else d0 + 2
    return A.box(u0, u1, v0, v1, d0, d1, "url(#pMem)", "#33363b", "#5d6168", .7)


# ------------------------------------------------------------------ 2D section helpers
def rect(x, y, w, h, fill, stroke=GR, sw=1, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def poly2(pts, fill="none", stroke=GR, sw=1.2, extra=""):
    d = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def pl(pts, stroke=GR, sw=1.2, extra=""):
    d = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polyline points="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def ln(x1, y1, x2, y2, stroke=GR, sw=1, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def hpl2(x, y, w, h):
    return rect(x, y, w, h, HPL, "#000", .8)


def mem2(points):
    return pl(points, MEM, 2.2, 'stroke-dasharray="9 4"')


def rivet2_h(x, y, length=26, head=14, left=True):
    """Rivet in plan, panel face on the left side at x (head outside)."""
    sgn = -1 if left else 1
    return (rect(min(x, x + sgn * 4), y - head / 2, 4, head, "#9aa0a7", GR, .8) +
            rect(min(x, x - sgn * length), y - 2.5, length, 5, "#c3c8ce", GR, .7))


def rivet2_v(x, y, length=26, head=14, up=True):
    sgn = -1 if up else 1
    return (rect(x - head / 2, min(y, y + sgn * 4), head, 4, "#9aa0a7", GR, .8) +
            rect(x - 2.5, min(y, y - sgn * length), 5, length, "#c3c8ce", GR, .7))


def anchor2_h(x, y, length=70, into_left=True):
    """Anchor going into wall (wall to the left of x)."""
    sgn = -1 if into_left else 1
    x2 = x + sgn * length
    s = ln(x, y, x2, y, "#6b7077", 5, 'stroke-linecap="butt"')
    for i in range(6, int(length), 7):
        xx = x + sgn * i
        s += ln(xx, y - 4, xx + sgn * 3, y + 4, "#fff", .7)
    s += rect(min(x, x - sgn * 6), y - 7, 6, 14, "#8f959c", GR, .7)
    return s


def flow_hint(x, y0, y1, n=3, gap=0):
    s = ""
    for i in range(n):
        yy0 = y0 - i * 0
        s += air([(x, y0), (x, y1)], 2)
    return s
