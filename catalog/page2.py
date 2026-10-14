# -*- coding: utf-8 -*-
"""Catalog v2 — minimal page system (9:16, 1080x1920)."""
import re
from vhatch import vectorize

OR, GR, DG, MG, LG, XL = "#F26A1B", "#1D1F22", "#4A4E55", "#8A8F96", "#E3E5E8", "#F4F5F6"

CSS = f"""
@page {{ size: 1080px 1920px; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #9ea3a8; }}
body {{ font-family: Inter, Manrope, Arial, sans-serif; color: {GR}; -webkit-print-color-adjust: exact; print-color-adjust: exact;
  font-feature-settings: "ss01", "cv11"; }}
.page {{ width: 1080px; height: 1920px; background: #fff; position: relative; overflow: hidden; page-break-after: always;
  margin: 0 auto 24px; padding: 150px 84px 0; }}
@media print {{ .page {{ margin: 0; }} html, body {{ background: #fff; }} }}
a {{ color: inherit; text-decoration: none; }}
.hd {{ position: absolute; top: 64px; left: 84px; right: 84px; display: flex; justify-content: space-between; align-items: center; }}
.hd img {{ height: 30px; display: block; }}
.hd .tag {{ font-size: 12px; letter-spacing: .32em; color: {MG}; text-transform: uppercase; }}
.ft {{ position: absolute; left: 84px; right: 84px; bottom: 56px; display: flex; justify-content: space-between; align-items: center;
  font-size: 14px; letter-spacing: .12em; color: {MG}; }}
.ft .pg {{ color: {GR}; font-weight: 600; letter-spacing: .04em; }}
.dark {{ background: {GR}; color: #fff; }}
.dark .ft, .dark .hd .tag {{ color: #9aa0a7; }} .dark .ft .pg {{ color: #fff; }}
.kick {{ font-size: 13px; letter-spacing: .3em; color: {OR}; font-weight: 600; text-transform: uppercase; }}
h1 {{ font-size: 54px; font-weight: 700; line-height: 1.04; letter-spacing: -.015em; text-transform: uppercase; margin-top: 14px; }}
.lead {{ font-size: 21px; line-height: 1.5; color: {DG}; margin-top: 22px; max-width: 800px; font-weight: 400; }}
.dark .lead {{ color: #b9bdc2; }}
h3 {{ font-size: 13px; letter-spacing: .26em; text-transform: uppercase; color: {MG}; font-weight: 600; margin-bottom: 16px; }}
.hr {{ height: 1px; background: {LG}; margin: 34px 0; }}
.dark .hr {{ background: #34373c; }}
.g2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }}
.g3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }}
.g4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }}
.it {{ display: grid; grid-template-columns: 56px 1fr; gap: 16px; align-items: start; }}
.it h4 {{ font-size: 18px; font-weight: 600; line-height: 1.25; }}
.it p, .tx {{ font-size: 15px; color: {DG}; line-height: 1.5; margin-top: 4px; }}
.dark .it p {{ color: #aab0b6; }}
.badge {{ display: inline-flex; width: 28px; height: 28px; border-radius: 50%; background: {OR}; color: #fff; font-size: 13px;
  font-weight: 700; align-items: center; justify-content: center; flex: none; }}
.lst {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0 40px; }}
.li {{ display: grid; grid-template-columns: 36px 1fr; gap: 10px; padding: 11px 0; border-bottom: 1px solid {LG}; align-items: start; }}
.li h4 {{ font-size: 16px; font-weight: 600; line-height: 1.3; padding-top: 4px; }}
.li p {{ font-size: 13px; color: {MG}; margin-top: 2px; line-height: 1.4; }}
.tile {{ background: {XL}; padding: 22px; position: relative; }}
.tile h4 {{ font-size: 17px; font-weight: 600; line-height: 1.25; }}
.tile p {{ font-size: 14px; color: {DG}; line-height: 1.45; margin-top: 6px; }}
.tile .meta {{ font-size: 12px; color: {OR}; letter-spacing: .1em; text-transform: uppercase; font-weight: 600; margin-top: 10px; }}
.tile .im {{ height: 150px; display: flex; align-items: center; justify-content: center; margin-bottom: 14px; }}
.tile .im img {{ max-width: 100%; max-height: 100%; object-fit: contain; mix-blend-mode: multiply; }}
.spec {{ display: grid; grid-template-columns: 1fr auto; padding: 14px 0; border-bottom: 1px solid {LG}; font-size: 17px; align-items: baseline; }}
.spec span:first-child {{ color: {DG}; }} .spec span:last-child {{ font-weight: 600; }}
.step {{ display: grid; grid-template-columns: 54px 64px 1fr; gap: 18px; align-items: center; padding: 15px 0; border-bottom: 1px solid {LG}; }}
.step .n {{ font-size: 15px; font-weight: 600; color: {OR}; letter-spacing: .08em; }}
.step h4 {{ font-size: 18px; font-weight: 600; }} .step p {{ font-size: 14.5px; color: {DG}; margin-top: 3px; line-height: 1.45; }}
.step .ph {{ width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; }}
.step .ph img {{ max-width: 64px; max-height: 64px; mix-blend-mode: multiply; }}
.note {{ font-size: 13.5px; color: {MG}; line-height: 1.55; border-left: 2px solid {OR}; padding-left: 14px; margin-top: 26px; }}
.warn {{ background: #FFF4EC; padding: 18px 22px; font-size: 15px; line-height: 1.5; color: {GR}; border-left: 3px solid {OR}; }}
table.t {{ width: 100%; border-collapse: collapse; }}
table.t th {{ font-size: 12px; letter-spacing: .2em; text-transform: uppercase; color: {MG}; font-weight: 600; text-align: left; padding: 0 12px 14px; border-bottom: 1px solid {GR}; }}
table.t td {{ font-size: 15.5px; padding: 15px 12px; border-bottom: 1px solid {LG}; vertical-align: top; line-height: 1.35; }}
table.t td:first-child {{ color: {DG}; font-size: 14px; }}
table.t .hl {{ background: #FFF4EC; font-weight: 600; }}
table.t th.hl {{ background: {OR}; color: #fff; }}
.pill {{ display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: .12em; color: {OR}; border: 1px solid {OR}; padding: 3px 8px; }}
.toc a {{ display: grid; grid-template-columns: 1fr 80px; padding: 19px 0; border-bottom: 1px solid #34373c; align-items: baseline; }}
.toc a span:first-child {{ font-size: 23px; font-weight: 500; }}
.toc a span:last-child {{ text-align: right; color: {OR}; font-size: 17px; font-weight: 600; }}
.toc .sub {{ font-size: 16px; color: #9aa0a7; padding-left: 0; }}
.fig {{ position: relative; }}
.fig img {{ display: block; width: 100%; }}
.ico {{ width: 56px; height: 56px; }}
.cap {{ font-size: 12px; color: {MG}; letter-spacing: .08em; margin-top: 8px; }}
.photo {{ background-size: cover; background-position: center; }}
.slot {{ background: {XL}; position: relative; overflow: hidden; }}
.slot .lb {{ position: absolute; left: 10px; bottom: 8px; font-size: 11px; letter-spacing: .14em; color: #fff; text-transform: uppercase;
  background: rgba(29,31,34,.55); padding: 3px 7px; }}
"""


class Book:
    def __init__(self):
        self.pages = []
        self.anchors = {}

    def add(self, body, tag="", dark=False, bare=False, cls="", anchor=None):
        n = len(self.pages) + 1
        if anchor:
            self.anchors.setdefault(anchor, n)
        logo = "img/brand/logo_white.png" if dark else "img/brand/logo.png"
        hd = "" if bare else f'<div class="hd"><a href="#p2"><img src="{logo}" alt="UZHPL"></a><div class="tag">{tag}</div></div>'
        ft = "" if bare else f'<div class="ft"><span>uzhpl.uz</span><a class="pg" href="#p2">{n:02d}</a></div>'
        self.pages.append(f'<section id="p{n}" class="page{" dark" if dark else ""} {cls}">{hd}{body}{ft}</section>')
        return n

    def html(self):
        body = "".join(self.pages)
        body = re.sub(r'#a-([\w.-]+)"', lambda m: f'#p{self.anchors.get(m.group(1), 2)}"', body)
        body = re.sub(r'\{\{pg:([\w.-]+)\}\}', lambda m: f'{self.anchors.get(m.group(1), 0):02d}', body)
        body = vectorize(body)
        return ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>UZHPL — Технический каталог</title><style>{CSS}</style></head><body>' + body + "</body></html>")


def title(h, kick="", lead=""):
    k = f'<div class="kick">{kick}</div>' if kick else ""
    l = f'<div class="lead">{lead}</div>' if lead else ""
    return f'<div>{k}<h1>{h}</h1>{l}</div>'
