# -*- coding: utf-8 -*-
"""Page shell, CSS and reusable layout blocks (9:16, 1080x1920)."""
from lib import *

CSS = f"""
@page {{ size: 1080px 1920px; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #9ea3a8; }}
body {{ font-family: Inter, 'Inter Display', Manrope, Arial, sans-serif; color: {GR};
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 1080px; height: 1920px; background: #fff; position: relative; overflow: hidden;
  page-break-after: always; margin: 0 auto 24px; padding: 64px 72px 0; }}
@media print {{ .page {{ margin: 0; }} html, body {{ background: #fff; }} }}

/* ---------- header / footer ---------- */
.hd {{ display: flex; justify-content: space-between; align-items: center; height: 56px;
  border-bottom: 1px solid {LG}; padding-bottom: 18px; }}
.hd .tag {{ font-size: 13px; letter-spacing: .22em; color: {MG}; text-transform: uppercase; text-align: right; line-height: 1.5; }}
.ft {{ position: absolute; left: 72px; right: 72px; bottom: 44px; display: flex; justify-content: space-between;
  align-items: center; font-size: 13px; color: {MG}; letter-spacing: .14em; border-top: 1px solid {LG}; padding-top: 16px; }}
.ft b {{ color: {GR}; font-weight: 700; letter-spacing: .02em; font-size: 15px; }}
.ft .pg {{ font-weight: 700; color: {GR}; font-size: 15px; letter-spacing: .04em; }}

/* ---------- logo ---------- */
.logo {{ font-weight: 800; font-size: 38px; letter-spacing: -.02em; color: {GR}; line-height: 1; display: inline-flex; align-items: center; gap: 18px; }}
.logo .l {{ position: relative; display: inline-block; }}
.logo .l::after {{ content: ""; position: absolute; width: .3em; height: .3em; background: {OR};
  border-radius: 50%; right: -.2em; top: -.24em; }}
.logo .claim {{ font-size: 11px; font-weight: 500; letter-spacing: .38em; color: {MG}; border-left: 1px solid {LG};
  padding-left: 16px; line-height: 1.6; }}
.logo.w {{ color: #fff; }}
.logo.w .claim {{ color: #b7bbc0; border-color: #555; }}

/* ---------- titles ---------- */
.ttl {{ margin-top: 54px; display: grid; grid-template-columns: auto 1fr; column-gap: 26px; align-items: start; }}
.ttl .n {{ font-size: 88px; font-weight: 300; color: {OR}; line-height: .86; letter-spacing: -.04em; }}
.ttl h1 {{ font-size: 64px; font-weight: 800; line-height: .98; letter-spacing: -.025em; text-transform: uppercase; }}
.ttl .sub {{ grid-column: 2; margin-top: 18px; font-size: 22px; color: {DG}; line-height: 1.4; max-width: 760px; font-weight: 400; }}
.kicker {{ font-size: 13px; letter-spacing: .3em; color: {OR}; font-weight: 700; text-transform: uppercase; margin-bottom: 14px; grid-column: 2; }}
h2.sec {{ font-size: 15px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: {GR};
  display: flex; align-items: center; gap: 14px; margin: 0 0 18px; }}
h2.sec::before {{ content: ""; width: 26px; height: 3px; background: {OR}; }}
.rule {{ height: 1px; background: {LG}; margin: 30px 0; }}

/* ---------- blocks ---------- */
.fig {{ margin-top: 30px; position: relative; }}
.legend {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px 40px; margin-top: 18px; }}
.li {{ display: grid; grid-template-columns: 34px 1fr; gap: 12px; align-items: start; }}
.li .b {{ width: 30px; height: 30px; border-radius: 50%; background: {OR}; color: #fff; font-weight: 700; font-size: 15px;
  display: flex; align-items: center; justify-content: center; }}
.li .t {{ font-size: 17px; font-weight: 700; line-height: 1.2; padding-top: 4px; }}
.li .t small {{ display: block; font-size: 14px; color: {MG}; font-weight: 400; margin-top: 3px; line-height: 1.35; }}

.cards {{ display: grid; gap: 16px; }}
.c2 {{ grid-template-columns: 1fr 1fr; }} .c3 {{ grid-template-columns: 1fr 1fr 1fr; }} .c4 {{ grid-template-columns: repeat(4,1fr); }}
.c5 {{ grid-template-columns: repeat(5,1fr); }}
.card {{ border: 1px solid {LG}; background: #fff; position: relative; padding: 18px 18px 18px; }}
.card.g {{ background: {XL}; border-color: {XL}; }}
.card .no {{ position: absolute; top: 14px; left: 14px; }}
.card .im {{ height: 170px; display: flex; align-items: center; justify-content: center; }}
.card h4 {{ font-size: 17px; font-weight: 700; line-height: 1.2; margin-top: 10px; }}
.card p {{ font-size: 14px; color: {DG}; line-height: 1.4; margin-top: 6px; }}
.card .meta {{ font-size: 12px; letter-spacing: .14em; color: {MG}; text-transform: uppercase; margin-top: 10px; }}
.badge {{ display: inline-flex; width: 30px; height: 30px; border-radius: 50%; background: {OR}; color: #fff;
  font-size: 14px; font-weight: 700; align-items: center; justify-content: center; }}
.badge.k {{ background: {GR}; }}

.steps {{ display: grid; gap: 0; }}
.step {{ display: grid; grid-template-columns: 70px 260px 1fr; gap: 24px; align-items: center; padding: 16px 0;
  border-bottom: 1px solid {LG}; }}
.step .sn {{ font-size: 40px; font-weight: 300; color: {OR}; letter-spacing: -.03em; }}
.step .si {{ height: 118px; background: {XL}; display: flex; align-items: center; justify-content: center; }}
.step h4 {{ font-size: 20px; font-weight: 700; }}
.step p {{ font-size: 15px; color: {DG}; margin-top: 6px; line-height: 1.45; }}

.rec {{ display: grid; grid-template-columns: 64px 1fr; gap: 22px; padding: 20px 0; border-bottom: 1px solid {LG}; align-items: start; }}
.rec .rn {{ font-size: 15px; font-weight: 700; color: {OR}; letter-spacing: .1em; padding-top: 4px; }}
.rec h4 {{ font-size: 21px; font-weight: 700; }}
.rec p {{ font-size: 16px; color: {DG}; margin-top: 6px; line-height: 1.45; }}
.pill {{ display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: .14em; color: {OR};
  border: 1px solid {OR}; padding: 3px 8px; margin-left: 8px; vertical-align: 3px; }}

.note {{ font-size: 13px; color: {MG}; line-height: 1.5; border-left: 3px solid {OR}; padding-left: 14px; margin-top: 22px; }}
.dark {{ background: {GR}; color: #fff; }}
.dark .ft {{ border-color: #3b3e43; color: #8b9096; }} .dark .ft b, .dark .ft .pg {{ color: #fff; }}
.dark .hd {{ border-color: #3b3e43; }}
.chip {{ font-size: 12px; letter-spacing: .18em; text-transform: uppercase; font-weight: 700; color: {MG}; }}
.big-n {{ font-size: 240px; font-weight: 200; color: {OR}; letter-spacing: -.06em; line-height: .8; }}
.checks {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0 40px; }}
.ck {{ display: grid; grid-template-columns: 34px 1fr auto; gap: 14px; padding: 18px 0; border-bottom: 1px solid {LG}; align-items: center; }}
.ck .box {{ width: 26px; height: 26px; border: 2px solid {GR}; position: relative; }}
.ck .box::after {{ content: ""; position: absolute; left: 7px; top: 1px; width: 7px; height: 14px; border: solid {OR};
  border-width: 0 3px 3px 0; transform: rotate(45deg); }}
.ck h4 {{ font-size: 18px; font-weight: 700; }} .ck p {{ font-size: 14px; color: {DG}; margin-top: 3px; line-height: 1.35; }}
.ck .m {{ font-size: 11px; letter-spacing: .14em; color: {MG}; text-transform: uppercase; text-align: right; }}
.toc-row {{ display: grid; grid-template-columns: 90px 1fr 80px; padding: 17px 0; border-bottom: 1px solid #3b3e43; align-items: baseline; }}
.toc-row .a {{ color: {OR}; font-size: 22px; font-weight: 300; }} .toc-row .b {{ font-size: 21px; font-weight: 600; letter-spacing: .01em; }}
.toc-row .c {{ text-align: right; color: #8b9096; font-size: 15px; }}
"""

LOGO = '<span>UZHP<span class="l">L</span></span>'


def logo(white=False, claim=True, size=None):
    st = f' style="font-size:{size}px"' if size else ""
    c = '<span class="claim">BUILD<br>GUARANTEED</span>' if claim else ""
    return f'<div class="logo{" w" if white else ""}"{st}>{LOGO}{c}</div>'


class Book:
    def __init__(self):
        self.pages = []

    def add(self, body, tag="ФАСАДНЫЕ СИСТЕМЫ HPL", dark=False, bare=False, cls=""):
        n = len(self.pages) + 1
        hd = "" if bare else f'<div class="hd">{logo(dark)}<div class="tag">{tag}</div></div>'
        ft = "" if bare else (f'<div class="ft"><span class="pg">{n:02d}</span>'
                              f'<span><b>UZHPL</b> &nbsp;|&nbsp; HPL FACADE &amp; INTERIOR SYSTEMS</span><span>UZHPL.UZ</span></div>')
        self.pages.append(f'<section class="page{" dark" if dark else ""} {cls}">{hd}{body}{ft}</section>')
        return n

    def html(self):
        return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>UZHPL Технический каталог</title><style>{CSS}</style></head><body>'
                + "".join(self.pages) + "</body></html>")


def title(n, h, sub="", kicker=""):
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    s = f'<div class="sub">{sub}</div>' if sub else ""
    return f'<div class="ttl">{"<div></div>" + k if k else ""}<div class="n">{n}</div><h1>{h}</h1>{s}</div>'


def legend(items, cols=2):
    out = "".join(f'<div class="li"><div class="b">{i + 1 if not isinstance(it, tuple) or len(it) < 3 else it[2]}</div>'
                  f'<div class="t">{it[0] if isinstance(it, tuple) else it}'
                  f'{"<small>" + it[1] + "</small>" if isinstance(it, tuple) and it[1] else ""}</div></div>'
                  for i, it in enumerate(items))
    return f'<div class="legend" style="grid-template-columns:repeat({cols},1fr)">{out}</div>'


def card(no, name, desc, img, meta="", g=False, h=170):
    nob = f'<span class="badge no">{no}</span>' if no != "" else ""
    m = f'<div class="meta">{meta}</div>' if meta else ""
    return (f'<div class="card{" g" if g else ""}">{nob}<div class="im" style="height:{h}px">{img}</div>'
            f'<h4>{name}</h4><p>{desc}</p>{m}</div>')


def step(n, name, desc, img):
    return (f'<div class="step"><div class="sn">{n}</div><div class="si">{img}</div>'
            f'<div><h4>{name}</h4><p>{desc}</p></div></div>')


def rec(n, name, desc, pill=""):
    p = f'<span class="pill">{pill}</span>' if pill else ""
    return f'<div class="rec"><div class="rn">{n}</div><div><h4>{name}{p}</h4><p>{desc}</p></div></div>'
