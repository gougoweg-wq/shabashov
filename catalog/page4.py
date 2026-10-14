# -*- coding: utf-8 -*-
"""Catalog v4 page system: light, strict 12-column grid, v2-style cards/steps, v3 header/footer.

Grid: page 1080 x 1920, side margins 84 px, content width 912 px, gutter 24 px.
Vertical rhythm: header 64-120, title block 168-404 (fixed height), content 404-1800, footer 1840.
"""
import re
from vhatch import vectorize

OR, GR, DG, MG, LG, XL = "#F26A1B", "#1D1F22", "#4A4E55", "#8A8F96", "#E3E5E8", "#F4F5F6"
WARM = "#FFF4EC"

CSS = f"""
@page {{ size: 1080px 1920px; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #9ea3a8; }}
body {{ font-family: Inter, Manrope, Arial, sans-serif; color: {GR}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 1080px; height: 1920px; background: #fff; position: relative; overflow: hidden; page-break-after: always;
  margin: 0 auto 24px; padding: 168px 84px 0; }}
@media print {{ .page {{ margin: 0; }} html, body {{ background: #fff; }} }}
a {{ color: inherit; text-decoration: none; }}

.hd {{ position: absolute; top: 60px; left: 84px; right: 84px; height: 44px; display: flex; justify-content: space-between;
  align-items: center; border-bottom: 1px solid {LG}; padding-bottom: 14px; }}
.hd img {{ height: 28px; display: block; }}
.hd .tag {{ font-size: 12px; letter-spacing: .3em; color: {MG}; text-transform: uppercase; }}
.ft {{ position: absolute; left: 84px; right: 84px; bottom: 52px; display: flex; justify-content: space-between; align-items: center;
  font-size: 14px; letter-spacing: .14em; color: {MG}; border-top: 1px solid {LG}; padding-top: 16px; }}
.ft .pg {{ color: {GR}; font-weight: 700; letter-spacing: .04em; }}
.photo-pg .hd, .photo-pg .ft {{ border-color: rgba(255,255,255,.35); }}

/* title block: fixed height so content starts on the same line on every page */
.tb {{ height: 236px; }}
.tb.s {{ height: 176px; }}
.kick {{ font-size: 13px; letter-spacing: .3em; color: {OR}; font-weight: 700; text-transform: uppercase; }}
h1 {{ font-size: 56px; font-weight: 800; line-height: 1.02; letter-spacing: -.02em; text-transform: uppercase; margin-top: 12px; }}
.lead {{ font-size: 20px; line-height: 1.5; color: {DG}; margin-top: 18px; max-width: 820px; }}
h3 {{ font-size: 13px; letter-spacing: .24em; text-transform: uppercase; color: {GR}; font-weight: 700; margin-bottom: 16px;
  display: flex; align-items: center; gap: 12px; }}
h3::before {{ content: ""; width: 24px; height: 3px; background: {OR}; }}
.hr {{ height: 1px; background: {LG}; margin: 32px 0; }}

.g2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }}
.g3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
.g4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }}
.g6 {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 24px; }}

/* v2-style card */
.card {{ border: 1px solid {LG}; background: #fff; position: relative; padding: 18px; display: flex; flex-direction: column; }}
.card.f {{ background: {XL}; border-color: {XL}; }}
.card .no {{ position: absolute; top: 14px; left: 14px; z-index: 2; }}
.card .im {{ display: flex; align-items: center; justify-content: center; overflow: hidden; }}
.card .im img {{ max-width: 100%; max-height: 100%; object-fit: contain; display: block; }}
.card h4 {{ font-size: 17px; font-weight: 700; line-height: 1.25; margin-top: 12px; }}
.card p {{ font-size: 14px; color: {DG}; line-height: 1.45; margin-top: 6px; }}
.card .meta {{ font-size: 11.5px; letter-spacing: .14em; color: {OR}; text-transform: uppercase; font-weight: 700; margin-top: auto; padding-top: 10px; }}
.badge {{ display: inline-flex; width: 28px; height: 28px; border-radius: 50%; background: {OR}; color: #fff; font-size: 13px;
  font-weight: 700; align-items: center; justify-content: center; flex: none; }}

/* steps with a picture (v2) */
.step {{ display: grid; grid-template-columns: 64px 220px 1fr; gap: 24px; align-items: center; padding: 14px 0; border-bottom: 1px solid {LG}; }}
.step:first-child {{ border-top: 1px solid {LG}; }}
.step .sn {{ font-size: 34px; font-weight: 300; color: {OR}; letter-spacing: -.02em; }}
.step .si {{ height: 104px; background: {XL}; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
.step .si img {{ max-width: 92%; max-height: 92%; object-fit: contain; display: block; }}
.step h4 {{ font-size: 19px; font-weight: 700; }}
.step p {{ font-size: 15px; color: {DG}; margin-top: 5px; line-height: 1.45; }}
.steps.c .step {{ padding: 10px 0; }} .steps.c .step .si {{ height: 88px; }}

/* legend */
.lg {{ display: grid; gap: 0 32px; }}
.lg .li {{ display: grid; grid-template-columns: 34px 1fr; gap: 10px; padding: 10px 0; border-bottom: 1px solid {LG}; align-items: start; }}
.lg .li h4 {{ font-size: 16px; font-weight: 700; line-height: 1.25; padding-top: 4px; }}
.lg .li p {{ font-size: 13px; color: {MG}; margin-top: 2px; line-height: 1.35; }}

/* icon item */
.it {{ display: grid; grid-template-columns: 52px 1fr; gap: 16px; align-items: start; }}
.it h4 {{ font-size: 18px; font-weight: 700; line-height: 1.25; }}
.it p {{ font-size: 15px; color: {DG}; line-height: 1.5; margin-top: 4px; }}

.rec {{ display: grid; grid-template-columns: 56px 1fr auto; gap: 16px; padding: 18px 0; border-bottom: 1px solid {LG}; align-items: start; }}
.rec:first-child {{ border-top: 1px solid {LG}; }}
.rec .rn {{ font-size: 15px; font-weight: 700; color: {OR}; letter-spacing: .1em; padding-top: 3px; }}
.rec h4 {{ font-size: 19px; font-weight: 700; }}
.rec p {{ font-size: 15px; color: {DG}; margin-top: 4px; line-height: 1.45; }}
.pill {{ display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: .12em; color: {OR}; border: 1px solid {OR}; padding: 4px 9px; white-space: nowrap; }}

.spec {{ display: grid; grid-template-columns: 1fr auto; padding: 13px 0; border-bottom: 1px solid {LG}; font-size: 17px; align-items: baseline; }}
.spec span:first-child {{ color: {DG}; }} .spec span:last-child {{ font-weight: 700; }}
.note {{ font-size: 13.5px; color: {MG}; line-height: 1.55; border-left: 3px solid {OR}; padding-left: 14px; margin-top: 24px; }}
.warn {{ background: {WARM}; padding: 18px 22px; font-size: 15.5px; line-height: 1.5; border-left: 3px solid {OR}; }}
table.t {{ width: 100%; border-collapse: collapse; }}
table.t th {{ font-size: 12px; letter-spacing: .16em; text-transform: uppercase; color: {MG}; font-weight: 700; text-align: left; padding: 0 12px 14px; border-bottom: 2px solid {GR}; }}
table.t td {{ font-size: 15.5px; padding: 15px 12px; border-bottom: 1px solid {LG}; vertical-align: top; line-height: 1.35; }}
table.t td:first-child {{ font-weight: 700; font-size: 14.5px; }}
table.t .hl {{ background: {WARM}; font-weight: 700; }}
table.t th.hl {{ background: {OR}; color: #fff; }}
.toc a {{ display: grid; grid-template-columns: 1fr 80px; padding: 18px 0; border-bottom: 1px solid {LG}; align-items: baseline; }}
.toc a span:first-child {{ font-size: 22px; font-weight: 600; }}
.toc a span:last-child {{ text-align: right; color: {OR}; font-size: 17px; font-weight: 700; }}
.cap {{ font-size: 12.5px; color: {MG}; letter-spacing: .06em; margin-top: 8px; line-height: 1.4; }}
.photo {{ background-size: cover; background-position: center; }}
.frame {{ border: 1px solid {LG}; }}
"""


class Book:
    def __init__(self):
        self.pages = []
        self.anchors = {}

    def add(self, body, tag="", bare=False, cls="", anchor=None, light_logo=False):
        n = len(self.pages) + 1
        if anchor:
            self.anchors.setdefault(anchor, n)
        logo = "img/brand/logo_white.png" if light_logo else "img/brand/logo.png"
        hd = "" if bare else f'<div class="hd"><a href="#p2"><img src="{logo}" alt="UZHPL"></a><div class="tag">{tag}</div></div>'
        ft = "" if bare else f'<div class="ft"><span>uzhpl.uz</span><a class="pg" href="#p2">{n:02d}</a></div>'
        self.pages.append(f'<section id="p{n}" class="page {cls}">{hd}{body}{ft}</section>')
        return n

    def html(self):
        body = "".join(self.pages)
        body = re.sub(r'#a-([\w.-]+)"', lambda m: f'#p{self.anchors.get(m.group(1), 2)}"', body)
        body = re.sub(r'\{\{pg:([\w.-]+)\}\}', lambda m: f'{self.anchors.get(m.group(1), 0):02d}', body)
        body = vectorize(body)
        return ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>UZHPL — Технический каталог</title><style>{CSS}</style></head><body>' + body + "</body></html>")


def title(h, kick="", lead="", short=False):
    k = f'<div class="kick">{kick}</div>' if kick else ""
    l = f'<div class="lead">{lead}</div>' if lead else ""
    return f'<div class="tb{" s" if short else ""}">{k}<h1>{h}</h1>{l}</div>'
