# -*- coding: utf-8 -*-
"""Minimal line icon set (48x48, 1.8px graphite stroke, one orange accent)."""
G = "#1D1F22"
O = "#F26A1B"

_P = {
    # company / process
    "project": f'<rect x="9" y="6" width="30" height="36" rx="1"/><path d="M15 15h18M15 21h18M15 27h10"/><path d="M30 33l6-6 3 3-6 6h-3z" stroke="{O}"/>',
    "engineering": f'<circle cx="24" cy="10" r="3"/><path d="M22.5 12.5L12 40M25.5 12.5L36 40M15 32h18"/><path d="M8 40h32" stroke="{O}"/>',
    "material": f'<path d="M6 30l18 8 18-8"/><path d="M6 24l18 8 18-8"/><path d="M6 18l18-8 18 8-18 8z" stroke="{O}"/>',
    "processing": f'<circle cx="24" cy="24" r="14"/><circle cx="24" cy="24" r="3" stroke="{O}"/><path d="M24 6v4M24 38v4M6 24h4M38 24h4M11.3 11.3l2.8 2.8M33.9 33.9l2.8 2.8M11.3 36.7l2.8-2.8M33.9 14.1l2.8-2.8"/>',
    "logistics": f'<path d="M4 14h24v18H4zM28 20h9l7 7v5H28z"/><circle cx="12" cy="35" r="3.5" stroke="{O}"/><circle cx="36" cy="35" r="3.5" stroke="{O}"/>',
    "montage": f'<path d="M10 30a14 14 0 0 1 28 0"/><path d="M6 30h36v4H6z"/><path d="M24 16v-4M18 18v6M30 18v6" stroke="{O}"/>',
    "supervision": f'<path d="M24 5l15 6v11c0 10-6.5 17-15 21-8.5-4-15-11-15-21V11z"/><path d="M17 24l5 5 9-10" stroke="{O}"/>',
    "service": f'<circle cx="24" cy="24" r="17"/><path d="M24 13v11l7 5" stroke="{O}"/>',
    # preparation / work steps
    "measure": f'<rect x="6" y="16" width="24" height="20" rx="4"/><circle cx="18" cy="26" r="4"/><path d="M30 32h12v-6" stroke="{O}"/><path d="M34 32v-3M38 32v-3"/>',
    "mark": f'<path d="M8 40l4-12 20-20 8 8-20 20z"/><path d="M28 12l8 8"/><path d="M8 40l4-1-3-3z" stroke="{O}"/><path d="M26 42h14" stroke="{O}"/>',
    "saw": f'<circle cx="20" cy="26" r="13"/><circle cx="20" cy="26" r="3"/><path d="M33 14l9-6M33 14v-6h9" stroke="{O}"/><path d="M4 40h40"/>',
    "drill": f'<path d="M8 14h20v12H8z"/><path d="M14 26l-3 14h8l2-14"/><path d="M28 18h6M34 20h10" stroke="{O}"/>',
    "drillbit": f'<path d="M6 24h14"/><path d="M20 20h16l6 4-6 4H20z"/><path d="M24 20l3 8M30 20l3 8" stroke="{O}"/>',
    "edge": f'<path d="M6 34h30l6-6V14"/><path d="M6 28h28l2-2V14"/><path d="M36 28l6 6" stroke="{O}"/><path d="M40 10l-6 4" stroke="{O}"/>',
    "sleeve": f'<ellipse cx="24" cy="16" rx="12" ry="5"/><path d="M12 16v14c0 2.8 5.4 5 12 5s12-2.2 12-5V16"/><ellipse cx="24" cy="16" rx="4" ry="1.7" stroke="{O}"/>',
    "clean": f'<path d="M14 18h12v24H14z"/><path d="M17 18v-6h6v6M23 12h6l3 3" /><path d="M34 14l6-2M34 18h7M34 22l6 2" stroke="{O}"/>',
    "sand": f'<path d="M8 28h32v10H8z"/><path d="M12 28c0-6 4-10 12-10s12 4 12 10"/><path d="M8 42h32" stroke="{O}" stroke-dasharray="2 3"/>',
    "primer": f'<path d="M16 6h10v14H16z"/><path d="M14 20h14l-2 6H16z"/><path d="M17 26v4c0 2 1 3 4 3s4-1 4-3v-4"/><path d="M8 42c8-4 24-4 32 0" stroke="{O}"/>',
    "activator": f'<path d="M18 6h8v6h-8z"/><path d="M15 12h14l3 6v24H12V18z"/><path d="M16 26h12v8H16z" stroke="{O}"/>',
    "tape": f'<circle cx="20" cy="22" r="13"/><circle cx="20" cy="22" r="5"/><path d="M33 22v16h11" stroke="{O}"/>',
    "glue": f'<path d="M6 16h24v10H6z"/><path d="M30 19h6l6 2-6 2h-6"/><path d="M14 26v8l-4 6M20 26l2 10" /><path d="M42 21c0 6-4 10-4 14" stroke="{O}"/>',
    "clock": f'<circle cx="24" cy="24" r="17"/><path d="M24 13v11l7 5" stroke="{O}"/>',
    "thermo": f'<path d="M20 8a4 4 0 0 1 8 0v20a8 8 0 1 1-8 0z"/><circle cx="24" cy="34" r="3" stroke="{O}"/><path d="M24 31V16" stroke="{O}"/><path d="M34 12h6M34 18h6M34 24h6"/>',
    "check": f'<circle cx="24" cy="24" r="17"/><path d="M16 24l6 6 11-12" stroke="{O}"/>',
    "level": f'<rect x="4" y="18" width="40" height="12" rx="2"/><rect x="19" y="21" width="10" height="6" rx="3" stroke="{O}"/><path d="M24 21v6"/>',
    "install": f'<path d="M8 6v36M8 14h6M8 34h6"/><path d="M16 8l20 4v28l-20-4z"/><path d="M38 24h6M41 21l3 3-3 3" stroke="{O}"/>',
    "rivet": f'<path d="M10 14c0-4 6-6 14-6s14 2 14 6z"/><path d="M20 14v20h8V14"/><path d="M24 34v8" stroke="{O}"/><circle cx="24" cy="43" r="1.5" stroke="{O}"/>',
    "screw": f'<path d="M12 12h24v4H12z"/><path d="M20 16h8v18l-4 8-4-8z"/><path d="M20 20l8 3M20 25l8 3M20 30l8 3" stroke="{O}"/>',
    "clip": f'<path d="M10 8h20v6H16v20h-6z"/><path d="M30 14v4h-8v18h18" stroke="{O}"/>',
    "wall": f'<path d="M6 10h36v28H6z"/><path d="M6 19h36M6 28h36M18 10v9M30 19v9M18 28v10"/><path d="M42 10v28" stroke="{O}"/>',
    "bracket": f'<path d="M10 8v32h6V14h22V8z"/><circle cx="13" cy="20" r="1.5" stroke="{O}"/><circle cx="13" cy="32" r="1.5" stroke="{O}"/><path d="M26 11h6" stroke="{O}"/>',
    "insulation": f'<path d="M6 12h36v24H6z"/><path d="M6 20c6-4 12 4 18 0s12-4 18 0M6 28c6-4 12 4 18 0s12-4 18 0" stroke="{O}"/>',
    "membrane": f'<path d="M8 8h26l6 6v26H8z"/><path d="M34 8v6h6"/><path d="M14 18l4 4-4 4M22 18l4 4-4 4" stroke="{O}"/>',
    "profile": f'<path d="M14 6v36h20v-4H18V6z"/><path d="M28 14h6" stroke="{O}"/>',
    "anchor": f'<path d="M24 6v28"/><path d="M18 10h12"/><path d="M20 30l4 12 4-12" stroke="{O}"/><path d="M20 16l8 3M20 21l8 3M20 26l8 3"/>',
    "dowel": f'<path d="M8 10h32v4H8z"/><path d="M22 14h4v26l-2 3-2-3z"/><path d="M24 18v18" stroke="{O}"/>',
    "epdm": f'<path d="M6 16h36v6H6z"/><path d="M6 22h36v10H6z" stroke="{O}"/><path d="M14 32v6M34 32v6"/>',
    "panel": f'<path d="M12 4h24v40H12z"/><path d="M12 36h24" stroke="{O}"/>',
    "pad": f'<path d="M10 12h24v24H10z"/><path d="M14 8h24v24" stroke="{O}"/>',
    "layout": f'<path d="M8 4h32v40H8z"/><circle cx="14" cy="12" r="2"/><circle cx="34" cy="12" r="2"/><circle cx="24" cy="24" r="2.6" stroke="{O}"/><circle cx="14" cy="36" r="2"/><circle cx="34" cy="36" r="2"/>',
    "doc": f'<path d="M10 4h20l8 8v32H10z"/><path d="M30 4v8h8"/><path d="M16 22h16M16 28h16M16 34h10" stroke="{O}"/>',
    "phone": f'<path d="M14 6h20v36H14z"/><path d="M20 10h8"/><circle cx="24" cy="37" r="2" stroke="{O}"/>',
    "mail": f'<path d="M6 12h36v24H6z"/><path d="M6 12l18 14 18-14" stroke="{O}"/>',
    "pin": f'<path d="M24 44s14-14 14-24a14 14 0 0 0-28 0c0 10 14 24 14 24z"/><circle cx="24" cy="20" r="5" stroke="{O}"/>',
    "web": f'<circle cx="24" cy="24" r="17"/><path d="M7 24h34M24 7c-6 6-6 28 0 34M24 7c6 6 6 28 0 34" /><path d="M10 15h28M10 33h28" stroke="{O}"/>',
    "cnc": f'<path d="M6 36h36v6H6z"/><path d="M10 36V10h28v26"/><path d="M20 10v12h8V10"/><path d="M24 22v6" stroke="{O}"/><path d="M14 32h20" stroke="{O}"/>',
    "press": f'<path d="M14 8h20v32H14z"/><path d="M4 24h7M8 20l4 4-4 4M44 24h-7M40 20l-4 4 4 4" stroke="{O}"/>',
    "gear": f'<circle cx="24" cy="24" r="6" stroke="{O}"/><path d="M24 6v6M24 36v6M6 24h6M36 24h6M11 11l4 4M33 33l4 4M11 37l4-4M33 15l4-4"/><circle cx="24" cy="24" r="12"/>',
    "germany": f'<path d="M24 5l15 6v11c0 10-6.5 17-15 21-8.5-4-15-11-15-21V11z"/><path d="M15 18h18" /><path d="M14 25h20" stroke="{O}"/><path d="M15 32h18" stroke="#c9a227"/>',
    "safety": f'<path d="M8 28a16 16 0 0 1 32 0"/><path d="M4 28h40v5H4z"/><path d="M24 12v8" stroke="{O}"/>',
}


def icon(name, size=48, sw=1.8, color=G):
    body = _P.get(name, _P["check"])
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">{body}</svg>')
