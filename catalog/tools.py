# -*- coding: utf-8 -*-
"""Tool drawings — flat technical product style (graphite body, steel, orange accent)."""
from lib import *

B = "url(#gBody)"   # tool body
B2 = "url(#gBody2)"
OR = "url(#gOrT)"


def tool(kind, W=240, H=160):
    s = ""
    if kind == "laser":
        s += rect(80, 40, 80, 80, B, "#000", 1, 'rx="10"') + rect(90, 50, 60, 36, OR, "none", 0, 'rx="4"')
        s += rect(98, 56, 44, 24, "#1d2a20", "none", 0) + ln(30, 68, 98, 68, "#3ad06a", 1.6) + ln(142, 68, 210, 68, "#3ad06a", 1.6)
        s += rect(96, 120, 48, 12, B2, "none", 0)
    elif kind == "drill":
        s += rect(60, 40, 120, 40, B, "#000", 1, 'rx="12"') + rect(180, 52, 22, 16, "#9aa0a7", GR, .8)
        s += ln(202, 60, 236, 60, "#7d838a", 4) + poly2([(100, 80), (130, 80), (122, 128), (96, 128)], B2, "#000", 1)
        s += rect(84, 128, 60, 22, OR, "#000", 1, 'rx="4"')
    elif kind == "riveter":
        s += rect(40, 50, 110, 34, B, "#000", 1, 'rx="8"') + rect(150, 58, 34, 18, "#9aa0a7", GR, .8)
        s += rect(184, 61, 26, 12, OR, GR, .8)   # special mouthpiece
        s += poly2([(70, 84), (100, 84), (92, 136), (66, 136)], B2, "#000", 1) + rect(56, 136, 52, 18, OR, "#000", 1, 'rx="4"')
        s += label(197, 98, "НАКОНЕЧНИК", 8, "middle", 700, OR)
    elif kind == "hand_riveter":
        s += pl([(40, 70), (150, 60), (210, 64)], B, 10) + pl([(40, 100), (150, 70)], OR, 10)
        s += rect(200, 58, 26, 12, "#9aa0a7", GR, .8)
    elif kind == "drillbit":
        s += rect(30, 74, 60, 12, "#9aa0a7", GR, .8)
        s += f'<path d="M90 74 L200 74 L215 80 L200 86 L90 86 Z" fill="url(#gSteel)" stroke="{GR}"/>'
        for x in range(96, 200, 12):
            s += ln(x, 74, x + 8, 86, "#7d838a", 1)
        s += label(120, 120, "HPL / КОМПАКТ", 10, "middle", 700, OR)
    elif kind == "jig":
        s += rect(70, 40, 100, 20, B, "#000", 1) + rect(110, 60, 20, 60, "#9aa0a7", GR, 1)
        s += rect(60, 120, 120, 10, OR, "#000", .8) + ln(120, 20, 120, 140, MG, 1, 'stroke-dasharray="4 3"')
    elif kind == "saw":
        s += f'<circle cx="120" cy="86" r="52" fill="url(#gSteel)" stroke="{GR}"/>'
        for a in range(0, 360, 15):
            import math
            x, y = 120 + 52 * math.cos(math.radians(a)), 86 + 52 * math.sin(math.radians(a))
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="{GR}"/>'
        s += f'<circle cx="120" cy="86" r="12" fill="{B}"/>' + rect(60, 30, 120, 26, B, "#000", 1, 'rx="6"')
        s += rect(150, 22, 50, 14, OR, "#000", .8, 'rx="3"')
    elif kind == "tracksaw":
        s += rect(20, 110, 200, 10, "#9aa0a7", GR, .8) + rect(60, 60, 120, 50, B, "#000", 1, 'rx="8"')
        s += rect(80, 44, 60, 18, OR, "#000", .8, 'rx="4"')
    elif kind == "cnc":
        s += rect(20, 100, 200, 30, "#d9dce0", GR, 1) + rect(30, 40, 180, 14, B, "#000", 1)
        s += rect(30, 54, 10, 76, B2, "none", 0) + rect(200, 54, 10, 76, B2, "none", 0)
        s += rect(104, 54, 32, 34, OR, "#000", 1) + rect(116, 88, 8, 12, "#9aa0a7", GR, .6)
        s += rect(50, 92, 140, 8, HPL, "none", 0)
    elif kind == "router":
        s += rect(80, 30, 80, 60, B, "#000", 1, 'rx="10"') + rect(70, 90, 100, 16, OR, "#000", 1)
        s += rect(114, 106, 12, 24, "#9aa0a7", GR, .8)
    elif kind == "tape":
        s += rect(60, 40, 90, 90, B, "#000", 1, 'rx="16"') + f'<circle cx="105" cy="85" r="22" fill="{OR}"/>'
        s += rect(150, 110, 70, 14, "#e9c84a", GR, .8)
        for x in range(156, 220, 8):
            s += ln(x, 110, x, 116, GR, .8)
    elif kind == "level":
        s += rect(20, 66, 200, 30, "url(#gSteelV)", GR, 1) + rect(100, 72, 40, 18, "#cfe8b7", GR, .8)
        s += ln(120, 72, 120, 90, GR, .8) + rect(20, 66, 18, 30, OR, "none", 0)
    elif kind == "clamp":
        s += pl([(60, 40), (180, 40), (180, 60)], "#9aa0a7", 8) + pl([(60, 40), (60, 120)], "#9aa0a7", 8)
        s += rect(160, 60, 40, 40, OR, "#000", 1, 'rx="4"') + ln(180, 100, 180, 130, "#7d838a", 5)
        s += rect(36, 116, 50, 12, B, "none", 0) + rect(160, 130, 40, 10, B, "none", 0)
    elif kind == "suction":
        s += rect(60, 50, 120, 24, B, "#000", 1, 'rx="8"')
        s += f'<ellipse cx="80" cy="100" rx="34" ry="12" fill="{OR}" stroke="#000"/>'
        s += f'<ellipse cx="160" cy="100" rx="34" ry="12" fill="{OR}" stroke="#000"/>'
        s += rect(74, 74, 12, 20, B2, "none", 0) + rect(154, 74, 12, 20, B2, "none", 0)
    elif kind == "gun":
        s += rect(80, 50, 140, 30, "url(#gSteelV)", GR, 1, 'rx="4"') + ln(30, 65, 80, 65, "#7d838a", 5)
        s += poly2([(90, 80), (120, 80), (112, 136), (86, 136)], B, "#000", 1) + rect(60, 90, 30, 46, OR, "#000", 1, 'rx="4"')
        s += poly2([(220, 58), (236, 64), (236, 66), (220, 72)], "#ddd", GR, .8)
    elif kind == "brush":
        s += rect(40, 74, 110, 14, "#b27b4a", GR, .8) + rect(150, 64, 30, 34, "#9aa0a7", GR, .8)
        s += rect(180, 60, 34, 42, "#2b2d31", "#000", .8)
    elif kind == "wipes":
        for i in range(3):
            s += rect(60 + i * 8, 50 + i * 10, 120, 60, "#fff", MG, 1)
        s += label(140, 100, "БЕЗВОРСОВЫЕ", 9, "middle", 700, MG)
    elif kind == "knife":
        s += rect(40, 74, 130, 24, OR, "#000", 1, 'rx="8"') + poly2([(170, 78), (214, 80), (198, 94), (170, 94)], "url(#gSteel)", GR, 1)
    elif kind == "glasses":
        s += f'<ellipse cx="88" cy="86" rx="40" ry="26" fill="#cfe3f5" stroke="{B}" stroke-width="5"/>'
        s += f'<ellipse cx="160" cy="86" rx="40" ry="26" fill="#cfe3f5" stroke="{B}" stroke-width="5"/>'
        s += ln(118, 80, 130, 80, B, 5) + ln(48, 80, 20, 70, B, 5) + ln(200, 80, 228, 70, B, 5)
    elif kind == "ear":
        s += f'<path d="M60 110 Q120 10 180 110" fill="none" stroke="{B}" stroke-width="8"/>'
        s += rect(40, 96, 40, 50, OR, "#000", 1, 'rx="12"') + rect(160, 96, 40, 50, OR, "#000", 1, 'rx="12"')
    elif kind == "gloves":
        s += f'<path d="M80 140 L80 70 Q80 54 92 54 L92 40 Q100 30 108 40 L108 50 L116 36 Q124 28 130 38 L128 54 L140 44 Q150 40 150 54 L140 90 L150 80 Q164 76 160 92 L140 140 Z" fill="{B}" stroke="#000"/>'
        s += rect(80, 120, 60, 20, OR, "none", 0)
    elif kind == "mask":
        s += f'<path d="M70 70 Q120 30 170 70 L160 120 Q120 140 80 120 Z" fill="#e9ebee" stroke="{B}" stroke-width="2"/>'
        s += f'<circle cx="95" cy="104" r="14" fill="{OR}"/><circle cx="145" cy="104" r="14" fill="{OR}"/>'
    elif kind == "boots":
        s += f'<path d="M70 40 L120 40 L124 110 L190 118 Q200 130 190 140 L70 140 Z" fill="{B}" stroke="#000"/>'
        s += rect(70, 132, 120, 8, OR, "none", 0)
    elif kind == "hammerdrill":
        s += rect(50, 46, 140, 36, B, "#000", 1, 'rx="8"') + rect(30, 56, 20, 16, "#9aa0a7", GR, .8) + ln(0, 64, 30, 64, "#7d838a", 5)
        s += poly2([(150, 82), (180, 82), (176, 136), (150, 136)], B2, "#000", 1) + rect(120, 40, 50, 10, OR, "none", 0)
    elif kind == "calipers":
        s += rect(30, 70, 190, 14, "url(#gSteelV)", GR, 1) + rect(40, 40, 10, 70, "#9aa0a7", GR, .8)
        s += rect(110, 40, 40, 70, OR, "#000", 1, 'rx="3"') + rect(118, 50, 24, 14, "#1d2a20", "none", 0)
    elif kind == "square":
        s += pl([(60, 30), (60, 130), (200, 130)], "#9aa0a7", 14) + pl([(60, 30), (60, 130)], OR, 14)
    elif kind == "hygro":
        s += rect(80, 30, 80, 110, B, "#000", 1, 'rx="10"') + rect(92, 44, 56, 40, "#1d2a20", "none", 0)
        s += label(120, 70, "23°C 45%", 10, "middle", 700, "#3ad06a") + f'<circle cx="120" cy="112" r="10" fill="{OR}"/>'
    elif kind == "deburr":
        s += rect(40, 72, 120, 20, B, "#000", 1, 'rx="10"') + rect(160, 76, 40, 12, "#9aa0a7", GR, .8)
        s += f'<path d="M200 76 q16 6 0 12" fill="{OR}"/>'
    elif kind == "vacuum":
        s += rect(70, 40, 100, 90, B, "#000", 1, 'rx="14"') + rect(84, 54, 72, 14, OR, "none", 0)
        s += f'<path d="M170 100 Q220 100 220 140" fill="none" stroke="{B2}" stroke-width="10"/>'
    elif kind == "wrench":
        s += pl([(50, 120), (180, 50)], "#9aa0a7", 14) + f'<circle cx="190" cy="44" r="18" fill="#9aa0a7" stroke="{GR}"/>'
        s += f'<circle cx="190" cy="44" r="8" fill="#fff"/>' + pl([(50, 120), (90, 98)], OR, 14)
    sh = f'<ellipse cx="{W/2}" cy="{H-12}" rx="{W*.36}" ry="7" fill="#000" opacity=".22" filter="url(#fSoft)"/>'
    return svg(W, H, sh + f'<g filter="url(#fDrop)">{s}</g>')
