# -*- coding: utf-8 -*-
"""2D architectural section drawings of facade nodes.

Local frame of one facade strip: x = outward from wall face (0), y = along the facade.
Same build-up everywhere so every node reads identically:
  wall  x<0 | insulation 0..100 | membrane 100 | ventilated gap 100..150 | profile 146..150 | HPL 150..160
Dimensions that depend on the project are labelled ПО ПРОЕКТУ / ПО РАСЧЁТУ.
"""
from lib import *

WALL = 150
INSD = 100
PF = 150      # profile face
T = 10        # panel thickness (drawing)


def g(body, tf=""):
    return f'<g transform="{tf}">{body}</g>' if tf else body


def strip(y0, y1, mode="vert", fix="rivet", brackets=(), panels=(), ins=None, wall=True,
          prof=None, rivets=(), vent=True, mem=True):
    """mode: 'vert' (vertical section) or 'plan' (horizontal section)."""
    s = ""
    iy0, iy1 = ins if ins else (y0, y1)
    if wall:
        s += rect(-WALL, y0, WALL, y1 - y0, "url(#hCon)", GR, 1.6)
    s += rect(0, iy0, INSD, iy1 - iy0, "url(#hIns)" if mode == "vert" else "url(#hInsV)", INS_D, .8)
    if mem:
        s += mem2([(INSD + 2, iy0), (INSD + 2, iy1)])
    off = 3 if fix == "glue" else 0
    pf = PF
    # brackets
    for by in brackets:
        if mode == "vert":
            s += rect(0, by - 30, 4, 60, "url(#gSteel)", GR, .9)               # wall plate
            s += rect(0, by - 2, pf - 30, 4, "#c8cdd3", GR, .9)                 # arm
            s += rect(-6, by - 34, 6, 68, "#2a2b2d", "none", 0)                 # thermal gasket
            s += anchor2_h(4, by + 18, 70)
        else:
            s += rect(-6, by - 34, 6, 68, "#2a2b2d", "none", 0)
            s += rect(0, by - 30, 4, 60, "url(#gSteel)", GR, .9)
            s += rect(0, by + 26, pf - 32, 4, "#c8cdd3", GR, .9)
            s += anchor2_h(4, by - 6, 70)
    # profile
    if prof:
        p0, p1 = prof
        if mode == "vert":
            s += rect(pf - 34, p0, 4, p1 - p0, "#c8cdd3", GR, .8)              # web (seen)
            s += rect(pf - 4, p0, 4, p1 - p0, "url(#gSteelV)", GR, .9)          # flange
            if fix == "hidden":
                pass
        else:
            for by in brackets:
                # L or T profile cross-section attached to bracket arm
                s += rect(pf - 34, by + 18, 4, 4, "none", "none", 0)
                s += pl([(pf - 30, by + 30), (pf - 30, by + 30), (pf - 30, by + 26)], GR, 0)
                s += rect(pf - 34, by - 4, 4, 34, "#c8cdd3", GR, .8)            # web along x? (plan)
    # glue layers
    for (a, b) in panels:
        if fix == "glue":
            # tape + adhesive bead along profile flange in vertical; in plan as two small blocks
            if mode == "vert" and prof:
                s += rect(pf, max(a, prof[0]) + 4, 3, min(b, prof[1]) - max(a, prof[0]) - 8, OR, "none", 0)
        if fix in ("rivet", "screw") and mode == "vert" and prof:
            s += rect(pf - 1, max(a, prof[0]), 2.5, min(b, prof[1]) - max(a, prof[0]), "#111", "none", 0)
        s += rect(pf + off, a, T, b - a, HPL, "#000", .8)
    for ry in rivets:
        if fix == "rivet":
            s += rect(pf + off + T, ry - 8, 4, 16, "#9aa0a7", GR, .7) + rect(pf - 10, ry - 2.5, T + 10, 5, "#c3c8ce", GR, .5)
        elif fix == "screw":
            s += rect(pf + T, ry - 9, 5, 18, "#26282b", "#000", .7) + rect(pf + T, ry - 11, 2, 22, "#555", "none", 0)
            s += rect(pf - 16, ry - 3, T + 16, 6, "#c3c8ce", GR, .5)
    return s


def frame(W, H, body, title="", scale_note="М 1:5 · СХЕМА"):
    t = (label(24, 34, title, 15, "start", 700, GR, 1.5) + label(W - 24, 34, scale_note, 11, "end", 600, MG, 1.5)
         + ln(24, 48, W - 24, 48, LG, 1)) if title else ""
    return svg(W, H, rect(.5, .5, W - 1, H - 1, "#fff", LG, 1) + t + body)


def cl(px, py, tx, ty, n, text, anchor="start"):
    return callout(px, py, tx, ty, text, anchor, n, 13)


# ------------------------------------------------------------------ individual nodes
def node(kind, W=900, H=720, fix="rivet", title=None, big=False):
    s = ""
    if kind == "outer_corner":
        o = "translate(330,330)"
        st1 = strip(0, 330, "plan", fix, brackets=(120,), panels=((-160, 330),), ins=(-100, 330), prof=None)
        st2 = strip(-300, 0, "plan", fix, brackets=(-200,), panels=((-300, -14),), ins=(-300, 0), prof=None)
        body = st1 + g(st2, "rotate(-90)")
        # corner insulation and corner angle profile
        body += rect(0, -100, 100, 100, "url(#hIns)", INS_D, .8)
        body += mem2([(102, 330), (102, -102), (-300, -102)])
        body += pl([(PF - 4, -40), (PF - 4, -PF + 4), (40 - 0, -PF + 4)], "#9aa0a7", 5)
        body += rect(PF, -PF - T, T, 0, "none", "none", 0)
        # profiles cross-sections
        body += _lsec(PF, 120) + g(_lsec(PF, -200), "rotate(-90)")
        if fix == "rivet":
            body += _riv(PF + T, 20) + _riv(PF + T, 200)
            body += g(_riv(PF + T, -60) + _riv(PF + T, -230), "rotate(-90)")
        if fix == "glue":
            body += rect(PF, -140, 3, 120, OR, "none", 0) + g(rect(PF, -110, 3, 90, OR, "none", 0), "rotate(-90)")
        body += _air_dot(125, 250) + _air_dot(-250, -125)
        s += g(body, o)
        s += cl(330 + PF + 5, 330 + 260, 610, 560, 1, "HPL-панель")
        s += cl(330 + PF - 4, 330 - 100, 610, 270, 2, "Угловой профиль")
        s += cl(330 + 50, 330 + 200, 610, 610, 3, "Утеплитель")
        s += cl(330 + 102, 330 + 160, 610, 460, 4, "Мембрана")
        s += cl(330 + 30, 330 + 120, 610, 510, 5, "Кронштейн + анкер")
        s += cl(330 - 80, 330 + 200, 610, 660, 6, "Несущая стена", "start")
        s += cl(330 + PF + T + 2, 330 - PF - 2, 610, 210, 7, "Шов / зазор — ПО ПРОЕКТУ")
        s += dim(330 + PF + T + 30, 330 + 0, 330 + PF + T + 30, 330 - PF - T, "ПО ПРОЕКТУ", vertical=True)
        title = title or "ВНЕШНИЙ УГОЛ · ГОРИЗОНТАЛЬНЫЙ РАЗРЕЗ"
    elif kind == "inner_corner":
        o = "translate(170,190)"
        st1 = strip(176, 520, "plan", fix, brackets=(330,), panels=((PF + T + 14, 520),), ins=(0, 520))
        st2 = strip(-560, -176, "plan", fix, brackets=(-400,), panels=((-560, -PF),), ins=(-560, -0))
        body = st1 + rect(-WALL, -WALL, WALL, 176 + WALL, "url(#hCon)", GR, 1.6) + g(st2, "rotate(90)")
        body += rect(0, 0, 100, 176, "url(#hIns)", INS_D, .8)
        body += mem2([(102, 520), (102, 102), (560, 102)])
        body += _lsec(PF, 330) + g(_lsec(PF, -400), "rotate(90)")
        body += pl([(PF - 4, PF + 50), (PF - 4, PF - 4), (PF + 50, PF - 4)], "#9aa0a7", 5)
        if fix == "rivet":
            body += _riv(PF + T, 250) + _riv(PF + T, 440) + g(_riv(PF + T, -300) + _riv(PF + T, -480), "rotate(90)")
        s += g(body, o)
        s += cl(170 + PF + 5, 190 + 470, 520, 620, 1, "HPL-панель")
        s += cl(170 + PF - 4, 190 + PF + 30, 560, 560, 2, "Внутренний угловой профиль")
        s += cl(170 + 50, 190 + 300, 520, 670, 3, "Утеплитель")
        s += cl(170 + PF + T + 7, 190 + PF + T + 7, 560, 500, 4, "Шов — ПО ПРОЕКТУ")
        title = title or "ВНУТРЕННИЙ УГОЛ · ГОРИЗОНТАЛЬНЫЙ РАЗРЕЗ"
    elif kind in ("window_head", "window_sill", "window_reveal"):
        if kind == "window_reveal":
            # plan: wall ends at opening y=300; reveal panel returns to window frame
            o = "translate(180,90)"
            body = strip(-30, 300, "plan", fix, brackets=(120,), panels=((-30, 300 + T + 4),), ins=(-30, 300))
            body += _lsec(PF, 120)
            body += rect(-WALL, 300, WALL, 0, "none", "none", 0)
            # window frame
            body += rect(-110, 360, 60, 90, "#e9ebee", GR, 1.4) + rect(-100, 450, 40, 140, "#cfe3f5", GR, 1)
            body += label(-80, 620, "ОКОННЫЙ БЛОК", 11, "middle", 700, MG, 1)
            # reveal insulation & panel
            body += rect(-50, 300, 150, 40, "url(#hIns)", INS_D, .8)
            body += rect(-50, 340 + 6, PF + T + 4 + 50, T, HPL, "#000", .8)
            body += pl([(PF - 4, 260), (PF - 4, 340), (-40, 340)], "#9aa0a7", 4)
            body += rect(-56, 340, 6, 30, "#2a2b2d", "none", 0)
            if fix == "rivet":
                body += _riv(PF + T, 40) + _riv(PF + T, 220)
            s += g(body, o)
            s += cl(180 + PF + 5, 90 + 100, 560, 160, 1, "HPL-панель фасада")
            s += cl(180 + 60, 90 + 351, 560, 380, 2, "HPL-откос")
            s += cl(180 + PF - 4, 90 + 300, 560, 300, 3, "Угловой профиль откоса")
            s += cl(180 + 20, 90 + 320, 560, 440, 4, "Утеплитель откоса")
            s += cl(180 - 53, 90 + 355, 560, 500, 5, "Примыкание / герметизация")
            s += cl(180 - 80, 90 + 480, 560, 560, 6, "Оконный блок")
            s += dim(180 - 50, 90 + 640, 180 + PF + T + 4, 90 + 640, "ПО ПРОЕКТУ")
            title = title or "ОКОННЫЙ ОТКОС · ГОРИЗОНТАЛЬНЫЙ РАЗРЕЗ"
        elif kind == "window_head":
            o = "translate(200,70)"
            body = strip(0, 330, "vert", fix, brackets=(120,), panels=((0, 330 + T + 6),), prof=(0, 330), rivets=(60, 260), ins=(0, 330))
            # opening below 330
            body += rect(-WALL, 330, WALL, 0, "none", "none", 0)
            body += rect(-50, 330, 150, 40, "url(#hIns)", INS_D, .8)
            body += rect(-50, 376, PF + T + 6 + 50, T, "#1f2023", "#000", .8)   # soffit panel (perforated)
            for xx in range(-30, PF, 22):
                body += rect(xx, 378, 8, 6, "#6b7077", "none", 0)
            body += rect(-110, 400, 60, 80, "#e9ebee", GR, 1.4) + rect(-100, 480, 40, 120, "#cfe3f5", GR, 1)
            body += air([(130, 420), (130, 360), (125, 250)], 2.2)
            s += g(body, o)
            s += cl(200 + PF + 5, 70 + 180, 560, 170, 1, "HPL-панель")
            s += cl(200 + 60, 70 + 381, 560, 400, 2, "Нижняя панель (перфорация / зазор)")
            s += cl(200 + 80, 70 + 160, 560, 230, 3, "Подсистема")
            s += cl(200 - 80, 70 + 500, 560, 470, 4, "Оконный блок")
            s += cl(200 + 130, 70 + 380, 560, 530, 5, "Приток воздуха в зазор")
            s += dim(200 + PF + T + 40, 70 + 330, 200 + PF + T + 40, 70 + 386, "ПО ПРОЕКТУ", vertical=True)
            title = title or "ВЕРХНИЙ ОКОННЫЙ УЗЕЛ · ВЕРТИКАЛЬНЫЙ РАЗРЕЗ"
        else:
            o = "translate(200,70)"
            body = rect(-110, 0, 60, 120, "#cfe3f5", GR, 1) + rect(-120, 120, 70, 70, "#e9ebee", GR, 1.4)
            body += label(-80, -10, "ОКНО", 11, "middle", 700, MG, 1)
            body += strip(230, 620, "vert", fix, brackets=(400,), panels=((230, 620),), prof=(230, 620), rivets=(290, 520), ins=(230, 620))
            body += rect(-50, 190, 150, 40, "url(#hIns)", INS_D, .8)
            # sill flashing with slope + drip
            body += pl([(-55, 186), (PF + T + 40, 206), (PF + T + 40, 236)], "#5b6067", 4)
            body += air([(125, 650), (125, 300)], 2.2)
            s += g(body, o)
            s += cl(200 + 100, 70 + 196, 560, 160, 1, "Отлив с уклоном и капельником")
            s += cl(200 + PF + 5, 70 + 450, 560, 450, 2, "HPL-панель")
            s += cl(200 + 30, 70 + 210, 560, 250, 3, "Утеплитель под отливом")
            s += cl(200 - 85, 70 + 160, 560, 330, 4, "Оконный блок")
            s += cl(200 + 125, 70 + 560, 560, 560, 5, "Выход воздуха из зазора")
            s += dim(200 + PF + T + 60, 70 + 206, 200 + PF + T + 60, 70 + 236, "ПО ПРОЕКТУ", vertical=True)
            title = title or "НИЖНИЙ ОКОННЫЙ УЗЕЛ (ОТЛИВ) · ВЕРТИКАЛЬНЫЙ РАЗРЕЗ"
    elif kind == "base":
        o = "translate(200,60)"
        body = strip(0, 470, "vert", fix, brackets=(140, 400), panels=((0, 470),), prof=(0, 480), rivets=(60, 280, 440), ins=(0, 470))
        body += rect(-WALL, 470, WALL, 120, "url(#hCon)", GR, 1.6)
        # starter perforated profile
        body += pl([(102, 486), (PF + T + 6, 486), (PF + T + 6, 476)], "#5b6067", 3)
        for xx in range(108, PF + T, 10):
            body += ln(xx, 482, xx, 490, "#fff", 2)
        # ground
        body += rect(-WALL - 30, 590, 520, 0, "none", "none", 0)
        body += pl([(-WALL - 30, 600), (420, 600)], GR, 2)
        body += rect(-WALL - 30, 600, 560, 40, "url(#hBrick)", "none", 0)
        body += air([(126, 560), (126, 500), (126, 380)], 2.2)
        s += g(body, o)
        s += cl(200 + PF + 5, 60 + 200, 560, 160, 1, "HPL-панель")
        s += cl(200 + 130, 60 + 486, 560, 470, 2, "Перфорированный цокольный профиль")
        s += cl(200 + 126, 60 + 540, 560, 530, 3, "Приток воздуха, защита от грызунов")
        s += cl(200 + 50, 60 + 300, 560, 230, 4, "Утеплитель")
        s += cl(200 - 60, 60 + 560, 560, 590, 5, "Цоколь / отмостка — ПО ПРОЕКТУ")
        s += dim(200 + PF + T + 50, 60 + 486, 200 + PF + T + 50, 60 + 600, "ПО ПРОЕКТУ", vertical=True)
        title = title or "ЦОКОЛЬНЫЙ УЗЕЛ · ВЕРТИКАЛЬНЫЙ РАЗРЕЗ"
    elif kind in ("parapet", "top"):
        o = "translate(230,120)"
        body = strip(110, 580, "vert", fix, brackets=(250, 480), panels=((60, 580),), prof=(60, 580), rivets=(120, 330, 530), ins=(110, 580))
        if kind == "parapet":
            body += rect(-WALL, 110, WALL, 0, "none", "none", 0)
            body += rect(-WALL, 40, WALL, 70, "url(#hCon)", GR, 1.6)
            body += rect(0, 40, 100, 70, "url(#hIns)", INS_D, .8)
            body += pl([(-WALL - 30, 30), (-WALL - 30, 20), (PF + T + 30, 20), (PF + T + 30, 70)], "#5b6067", 4)
            body += air([(126, 600), (126, 80), (180, 40)], 2.2)
            body += rect(-WALL - 260, 110, 110, 18, "#ddd", GR, 1)
        else:
            body += rect(-WALL, 20, WALL, 90, "url(#hCon)", GR, 1.6)
            body += rect(-WALL - 220, 20, 220, 30, "url(#hCon)", GR, 1.6)
            body += pl([(PF + T + 30, 70), (PF + T + 30, 0), (-WALL - 100, 0)], "#5b6067", 4)
            body += air([(126, 600), (126, 80), (190, 24)], 2.2)
        s += g(body, o)
        s += cl(230 + 40, 120 + 20, 600, 120, 1, "Парапетная крышка / отлив" if kind == "parapet" else "Верхний отлив / примыкание")
        s += cl(230 + PF + 5, 120 + 400, 600, 400, 2, "HPL-панель")
        s += cl(230 + 180, 120 + 40, 600, 200, 3, "Выход воздуха из зазора")
        s += cl(230 + 50, 120 + 300, 600, 300, 4, "Утеплитель")
        s += dim(230 + PF + T + 60, 120 + 20, 230 + PF + T + 60, 120 + 70, "ПО ПРОЕКТУ", vertical=True)
        title = title or ("ПАРАПЕТ · ВЕРТИКАЛЬНЫЙ РАЗРЕЗ" if kind == "parapet" else "ВЕРХНЕЕ ПРИМЫКАНИЕ · ВЕРТИКАЛЬНЫЙ РАЗРЕЗ")
    elif kind == "hjoint":
        o = "translate(220,80)"
        body = strip(0, 600, "vert", fix, brackets=(130, 470), panels=((0, 290), (304, 600)), prof=(0, 600), rivets=(60, 240, 360, 540), ins=(0, 600))
        body += air([(126, 620), (126, 0)], 2.2)
        s += g(body, o)
        s += cl(220 + PF + T, 80 + 297, 600, 300, 1, "Открытый горизонтальный шов")
        s += cl(220 + PF + 5, 80 + 150, 600, 160, 2, "HPL-панель (верхняя)")
        s += cl(220 + PF + 5, 80 + 450, 600, 450, 3, "HPL-панель (нижняя)")
        s += cl(220 + PF - 2, 80 + 520, 600, 530, 4, "Профиль подсистемы (непрерывный)")
        s += dim(220 + PF + T + 60, 80 + 290, 220 + PF + T + 60, 80 + 304, "ПО ПРОЕКТУ", vertical=True)
        title = title or "ГОРИЗОНТАЛЬНЫЙ СТЫК · ВЕРТИКАЛЬНЫЙ РАЗРЕЗ"
    elif kind == "vjoint":
        o = "translate(170,170)"
        body = rect(-WALL, -60, WALL, 560, "url(#hCon)", GR, 1.6)
        body += rect(0, -60, INSD, 560, "url(#hInsV)", INS_D, .8) + mem2([(102, -60), (102, 500)])
        body += _tsec(PF, 220, half=60)
        body += rect(-6, 220 - 34, 6, 68, "#2a2b2d", "none", 0) + rect(0, 220 - 30, 4, 60, "url(#gSteel)", GR, .9)
        body += rect(0, 220 + 26, PF - 32, 4, "#c8cdd3", GR, .9) + anchor2_h(4, 214, 70)
        body += rect(PF, -60, T, 273, HPL, "#000", .8) + rect(PF, 227, T, 273, HPL, "#000", .8)
        if fix == "rivet":
            body += _riv(PF + T, 180) + _riv(PF + T, 260)
        if fix == "glue":
            body += rect(PF - 0, 150, 3, 50, OR, "none", 0) + rect(PF, 240, 3, 50, OR, "none", 0)
        s += g(body, o)
        s += cl(170 + PF + T, 170 + 220, 560, 230, 1, "Вертикальный шов")
        s += cl(170 + PF + 5, 170 + 60, 560, 120, 2, "HPL-панель")
        s += cl(170 + PF - 4, 170 + 270, 560, 330, 3, "T-профиль (рядовой стык)")
        s += cl(170 + 60, 170 + 400, 560, 420, 4, "Утеплитель")
        s += cl(170 + 30, 170 + 250, 560, 500, 5, "Кронштейн + терморазрыв")
        s += dim(170 + PF + T + 40, 170 + 213, 170 + PF + T + 40, 170 + 227, "ПО ПРОЕКТУ", vertical=True)
        title = title or "ВЕРТИКАЛЬНЫЙ СТЫК · ГОРИЗОНТАЛЬНЫЙ РАЗРЕЗ"
    return frame(W, H, s, title)


def _lsec(x, y, web=34, fl=60):
    """L profile in plan at bracket y: web along x attached to bracket arm, flange along y at panel."""
    return (rect(x - web, y + 26, web - 4, 4, "#c8cdd3", GR, .8) +
            rect(x - 4, y - fl / 2 + 10, 4, fl, "url(#gSteelV)", GR, .9))


def _tsec(x, y, half=40, web=34):
    return (rect(x - web, y - 2, web - 4, 4, "#c8cdd3", GR, .8) +
            rect(x - 4, y - half, 4, half * 2, "url(#gSteelV)", GR, .9))


def _riv(x, y):
    return rect(x, y - 8, 4, 16, "#9aa0a7", GR, .7) + rect(x - T - 10, y - 2.5, T + 10, 5, "#c3c8ce", GR, .5)


def _air_dot(a, b):
    return ""


# ------------------------------------------------------------------ principle diagrams
def principle_section(W=936, H=860):
    """Vertical section of whole facade height with airflow (in at base, out at top)."""
    s = ""
    o = "translate(250,60)"
    body = strip(40, 740, "vert", "rivet", brackets=(150, 450, 680), panels=((40, 250), (262, 500), (512, 740)),
                 prof=(40, 740), rivets=(80, 220, 300, 470, 550, 710), ins=(40, 740))
    body += air([(125, 790), (125, 20)], 3)
    body += air([(-260, 0), (-260, 0)], 1)
    for yy in (420, 600):
        body += air([(78, yy), (58, yy - 40)], 1.8, "3 4")   # vapour out of insulation
    s += g(body, o)
    s += label(250 + 125, 60 + 810, "ВХОД ВОЗДУХА", 13, "middle", 700, BL, 1.5)
    s += label(250 + 125, 60 + 0, "ВЫХОД ВОЗДУХА", 13, "middle", 700, BL, 1.5)
    s += cl(250 - 75, 60 + 600, 600, 640, 1, "Несущая стена")
    s += cl(250 + 50, 60 + 340, 600, 330, 2, "Утеплитель")
    s += cl(250 + 102, 60 + 380, 600, 390, 3, "Мембрана (пароприницаемая)".replace("приницаемая", "проницаемая"))
    s += cl(250 + 125, 60 + 330, 600, 450, 4, "Вентилируемый зазор")
    s += cl(250 + PF + 5, 60 + 160, 600, 200, 5, "HPL-панель")
    s += cl(250 + PF + T, 60 + 256, 600, 260, 6, "Открытый шов")
    s += cl(250 + 60, 60 + 450, 600, 520, 7, "Кронштейн + анкер")
    s += cl(250 + 80, 60 + 420, 600, 580, 8, "Отвод влаги из утеплителя")
    s += dim(250 + 100, 60 + 760, 250 + PF, 60 + 760, "ПО РАСЧЁТУ", 30)
    return svg(W, H, s)


def fixed_sliding(W=936, H=560):
    """Panel elevation with fixed point (round hole) + sliding points (oversized holes) and expansion arrows."""
    s = ""
    px, py, pw, ph = 140, 60, 520, 420
    s += rect(px, py, pw, ph, "url(#pHpl)", "#000", 1)
    # profile centrelines
    for x in (px + 60, px + pw / 2, px + pw - 60):
        s += ln(x, py - 30, x, py + ph + 30, MG, 1, 'stroke-dasharray="10 5 2 5"')
    pts = []
    for x in (px + 60, px + pw / 2, px + pw - 60):
        for y in (py + 50, py + ph / 2, py + ph - 50):
            pts.append((x, y))
    fx, fy = px + pw / 2, py + ph / 2
    for (x, y) in pts:
        if (x, y) == (fx, fy):
            s += f'<circle cx="{x}" cy="{y}" r="15" fill="{OR}"/><circle cx="{x}" cy="{y}" r="6" fill="#fff"/>'
        else:
            s += f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="#fff" stroke-width="2"/><circle cx="{x}" cy="{y}" r="6" fill="#fff"/>'
    # expansion arrows from fixed point
    for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        L = 70 if dx == 0 or dy == 0 else 50
        s += arrow(fx + dx * 24, fy + dy * 24, fx + dx * (24 + L), fy + dy * (24 + L), OR, 2.2)
    # legend
    lx = px + pw + 40
    s += f'<circle cx="{lx + 15}" cy="{py + 60}" r="15" fill="{OR}"/><circle cx="{lx + 15}" cy="{py + 60}" r="6" fill="#fff"/>'
    s += label(lx + 42, py + 56, "ФИКСИРОВАННАЯ", 14, "start", 700) + label(lx + 42, py + 76, "ТОЧКА · 1 на панель", 13, "start", 400, DG)
    s += f'<circle cx="{lx + 15}" cy="{py + 140}" r="15" fill="{HPL}" stroke="{GR}"/><circle cx="{lx + 15}" cy="{py + 140}" r="6" fill="#fff"/>'
    s += label(lx + 42, py + 136, "СКОЛЬЗЯЩИЕ", 14, "start", 700) + label(lx + 42, py + 156, "ТОЧКИ · отв. увеличенный", 13, "start", 400, DG)
    s += arrow(lx, py + 220, lx + 60, py + 220, OR, 2.2)
    s += label(lx + 72, py + 216, "ТЕМПЕРАТУРНОЕ", 14, "start", 700) + label(lx + 72, py + 236, "ДВИЖЕНИЕ", 14, "start", 700)
    s += label(lx, py + 300, "Диаметры отверстий,", 13, "start", 400, DG)
    s += label(lx, py + 320, "отступы от кромок и шаг —", 13, "start", 400, DG)
    s += label(lx, py + 340, "ПО ИНСТРУКЦИИ СИСТЕМЫ", 13, "start", 700, OR)
    s += label(lx, py + 360, "И ПО РАСЧЁТУ", 13, "start", 700, OR)
    s += dim(px, py + ph + 50, px + 60, py + ph + 50, "ПО ПРОЕКТУ", 0, 11)
    return svg(W, H, s)


def rivet_detail(W=440, H=380, fixed=True):
    """Close cross-section rivet through panel + profile with sleeve (fixed) or oversized hole (sliding)."""
    s = rect(0, 0, W, H, XL, "none", 0)
    x0 = 120
    s += rect(x0, 40, 40, 300, HPL, "#000", 1)                      # panel
    s += rect(x0 + 40, 40, 10, 300, "url(#gSteelV)", GR, 1)         # profile flange
    hole = 8 if fixed else 18
    s += rect(x0, 190 - hole, 40, hole * 2, "#fff", "none", 0)
    s += rect(x0 + 40, 182, 10, 16, "#fff", "none", 0)
    if fixed:
        s += rect(x0, 182, 40, 16, OR, "none", 0, 'opacity=".9"')   # fixed-point sleeve
    s += f'<path d="M{x0 - 4} 150 Q{x0 - 26} 190 {x0 - 4} 230 Z" fill="url(#gSteel)" stroke="{GR}"/>'
    s += rect(x0 - 4, 184, 60, 12, "#c3c8ce", GR, .8)
    s += f'<path d="M{x0 + 50} 178 q14 12 0 24" fill="#c3c8ce" stroke="{GR}"/>'
    s += label(W / 2 + 40, 30, "ФИКСИРОВАННАЯ ТОЧКА" if fixed else "СКОЛЬЗЯЩАЯ ТОЧКА", 14, "middle", 700, OR if fixed else GR, 1)
    s += label(x0 + 70, 365, "Отверстие в панели: " + ("с втулкой фикс. точки" if fixed else "увеличенное"), 12, "middle", 500, DG)
    s += callout(x0 + 20, 120, 300, 110, "HPL", "start", None, 13)
    s += callout(x0 + 45, 280, 300, 290, "Профиль", "start", None, 13)
    s += callout(x0 - 15, 190, 300, 200, "Заклёпка", "start", None, 13)
    if not fixed:
        s += arrow(x0 + 20, 150, x0 + 20, 166, OR, 2, True) if False else arrow(x0 + 20, 120 + 30, x0 + 20, 172, OR, 2)
    return svg(W, H, s)


def panel_processing(W=936, H=620):
    """Exploded panel: cut lines, edge distances, fixed/sliding holes, groove (hidden)."""
    s = ""
    A = Axo(470, 90, 1.0, U=(0.85, 0.32), D=(-0.55, 0.30))
    s += a_panel(A, -330, 220, 0, 380, 0, 12)
    # cut line
    for (u0, v0, u1, v1) in ((-330, -40, -330, 420), (220, -40, 220, 420), (-370, 0, 260, 0), (-370, 380, 260, 380)):
        s += A.line((u0, v0, 12), (u1, v1, 12), OR, 1.6, "8 5")
    # holes
    for u in (-280, -55, 170):
        for v in (50, 190, 330):
            x, y = A.p(u, v, 12)
            if (u, v) == (-55, 190):
                s += f'<ellipse cx="{x}" cy="{y}" rx="9" ry="8" fill="{OR}"/><ellipse cx="{x}" cy="{y}" rx="3.5" ry="3" fill="#fff"/>'
            else:
                s += f'<ellipse cx="{x}" cy="{y}" rx="9" ry="8" fill="none" stroke="#fff" stroke-width="1.6"/><ellipse cx="{x}" cy="{y}" rx="3.5" ry="3" fill="#fff"/>'
    # edge distance dims
    a, b = A.p(-330, 50, 12), A.p(-280, 50, 12)
    s += f'<line x1="{a[0]}" y1="{a[1] - 30}" x2="{b[0]}" y2="{b[1] - 30}" stroke="{OR}" stroke-width="1.2" marker-start="url(#tick)" marker-end="url(#tick)"/>'
    s += label(a[0] - 10, a[1] - 46, "ОТСТУП ОТ КРОМКИ — ПО ИНСТРУКЦИИ", 12, "start", 700, OR)
    s += callout(*A.p(220, 300, 6), 680, 470, "Кромка: удаление заусенцев", "start", None, 13)
    s += callout(*A.p(-55, 190, 12), 680, 120, "Фиксированная точка", "start", None, 13)
    s += callout(*A.p(170, 190, 12), 680, 170, "Скользящие точки", "start", None, 13)
    s += callout(*A.p(0, 380, 12), 680, 540, "Линия раскроя по карте", "start", None, 13)
    return svg(W, H, s)


def hidden_principle(W=936, H=620):
    """Section: panel with rear undercut anchor -> clip -> horizontal rail -> vertical profile."""
    s = ""
    o = "translate(240,40)"
    b = rect(-WALL, 0, WALL, 540, "url(#hCon)", GR, 1.6)
    b += rect(0, 0, 100, 540, "url(#hIns)", INS_D, .8) + mem2([(102, 0), (102, 540)])
    b += rect(0, 220, 4, 60, "url(#gSteel)", GR, .9) + rect(0, 248, 116, 4, "#c8cdd3", GR, .9) + anchor2_h(4, 266, 70)
    b += rect(116, 0, 4, 540, "url(#gSteelV)", GR, .9)                 # vertical profile
    for yy in (110, 380):
        b += pl([(120, yy + 20), (140, yy + 20), (140, yy), (152, yy - 8)], "#8a9097", 5)   # rail hook
        b += pl([(178, yy - 20), (160, yy - 20), (160, yy - 2), (150, yy + 6)], "#5b6067", 5)  # clip on panel
        b += rect(178, yy - 26, 18, 14, "#9aa0a7", GR, .8)                # undercut anchor in panel
    b += rect(178, 0, 14, 540, HPL, "#000", .8)
    b += arrow(200 + 30, 140, 200 + 30, 100, OR, 2.4)
    s += g(b, o)
    s += label(240 + 230 + 14, 40 + 120, "навеска сверху вниз", 12, "start", 600, OR)
    s += cl(240 + 186, 40 + 450, 600, 470, 1, "HPL-панель (тыльная обработка)")
    s += cl(240 + 187, 40 + 104, 620, 60, 2, "Скрытый анкер / паз")
    s += cl(240 + 168, 40 + 92, 620, 130, 3, "Клипса (кляймер)")
    s += cl(240 + 140, 40 + 125, 620, 200, 4, "Несущая направляющая")
    s += cl(240 + 118, 40 + 300, 620, 300, 5, "Вертикальный профиль")
    s += cl(240 + 60, 40 + 250, 620, 380, 6, "Кронштейн + анкер")
    s += cl(240 + 50, 40 + 420, 620, 540, 7, "Утеплитель + мембрана")
    return svg(W, H, s)


def glue_section(W=936, H=560):
    """Adhesive joint close-up: profile flange, tape (temporary), bead (permanent), panel."""
    s = rect(0, 0, W, H, "#fff", "none", 0)
    x = 330
    s += rect(x - 160, 40, 150, 480, "url(#hIns)", INS_D, .8)
    s += rect(x - 10, 40, 10, 480, "url(#gSteelV)", GR, 1)             # flange
    s += rect(x - 70, 270, 60, 6, "#c8cdd3", GR, .8)
    for y0 in (60, 300):
        s += rect(x, y0, 6, 40, "#1b1c1e", "#000", .5)                 # tape
        s += poly2([(x, y0 + 60), (x + 6, y0 + 60), (x + 6, y0 + 120), (x, y0 + 120)], OR, "#b84d10", .6)  # bead
        s += rect(x, y0 + 150, 6, 40, "#1b1c1e", "#000", .5)
    s += rect(x + 6, 40, 30, 480, HPL, "#000", .8)
    s += f'<rect x="{x - 14}" y="40" width="4" height="480" fill="#7aa9d8" opacity=".5"/>'
    s += label(W - 300, 70, "ВРЕМЕННАЯ ФИКСАЦИЯ", 13, "start", 700, GR, 1.4)
    s += label(W - 300, 92, "Двусторонняя лента — удерживает", 13, "start", 400, DG)
    s += label(W - 300, 110, "панель до отверждения клея", 13, "start", 400, DG)
    s += label(W - 300, 170, "ПОСТОЯННОЕ СОЕДИНЕНИЕ", 13, "start", 700, OR, 1.4)
    s += label(W - 300, 192, "Клеевой валик (треугольный шов)", 13, "start", 400, DG)
    s += label(W - 300, 210, "— несущее соединение", 13, "start", 400, DG)
    s += callout(x + 3, 80, W - 320, 80, "", "end")
    s += callout(x + 3, 390, W - 320, 180, "", "end")
    s += callout(x - 5, 460, 120, 470, "Профиль: очистка, праймер", "end", None, 13)
    s += callout(x + 20, 240, W - 320, 300, "HPL: очистка + праймер / активатор", "start", None, 13)
    s += dim(x + 60, 360, x + 60, 420, "ПО СИСТЕМЕ", 0, 11, vertical=True)
    s += label(W - 300, 380, "Толщина и геометрия шва, время", 13, "start", 400, DG)
    s += label(W - 300, 398, "выдержки и отверждения —", 13, "start", 400, DG)
    s += label(W - 300, 416, "ПО ИНСТРУКЦИИ ПРОИЗВОДИТЕЛЯ", 13, "start", 700, OR)
    return svg(W, H, s)


def screw_detail(W=936, H=520):
    s = ""
    x = 300
    s += rect(x - 200, 40, 160, 440, "url(#hIns)", INS_D, .8)
    s += rect(x - 12, 40, 12, 440, "url(#gSteelV)", GR, 1)
    s += rect(x, 40, 34, 440, HPL, "#000", .8)
    for y in (140, 360):
        s += rect(x + 34, y - 22, 6, 44, "#26282b", "#000", .8)        # head (colour)
        s += rect(x + 30, y - 16, 4, 32, "#3b3e43", "none", 0)          # washer/EPDM
        s += rect(x - 30, y - 5, 64, 10, "#c3c8ce", GR, .6)
        for k in range(x - 28, x + 30, 7):
            s += ln(k, y - 5, k + 4, y + 5, "#7d838a", .7)
    s += rect(x, 340, 34, 40, "#fff", "none", 0, 'opacity=".0"')
    s += callout(x + 40, 140, 620, 120, "Фасадный винт с окрашенной головкой", "start", 1, 13)
    s += callout(x + 32, 160, 620, 190, "Шайба / уплотнение — по системе", "start", 2, 13)
    s += callout(x + 17, 260, 620, 260, "HPL-панель", "start", 3, 13)
    s += callout(x - 6, 300, 620, 330, "Профиль подсистемы", "start", 4, 13)
    s += label(620, 410, "Без перетяжки: панель должна", 13, "start", 400, DG)
    s += label(620, 430, "сохранять предусмотренное движение", 13, "start", 400, DG)
    s += label(620, 460, "ТИП / ДЛИНА КРЕПЕЖА — ПО РАСЧЁТУ", 13, "start", 700, OR)
    return svg(W, H, s)


# ------------------------------------------------------------------ interior nodes
def interior_node(kind, W=440, H=330):
    s = rect(0, 0, W, H, "#fff", LG, 1)
    t = 14
    if kind == "in_corner":
        s += rect(40, 60, 40, 260, "url(#hBrick)", GR, 1) + rect(40, 280, 360, 40, "url(#hBrick)", GR, 1)
        s += rect(80, 60, 6, 214, OR, "none", 0) + rect(86, 60, t, 206, HPL, "#000", .8)
        s += rect(120, 274, 280, 6, OR, "none", 0) + rect(120, 260, 280, t, HPL, "#000", .8)
        s += label(W / 2, 40, "ВНУТРЕННИЙ УГОЛ", 13, "middle", 700, GR, 1)
    elif kind == "out_corner":
        s += rect(60, 80, 280, 240, "url(#hBrick)", GR, 1)
        s += rect(60, 66, 280, t, HPL, "#000", .8) + rect(340, 66, t, 254, HPL, "#000", .8)
        s += f'<circle cx="347" cy="73" r="10" fill="none" stroke="{OR}" stroke-width="2"/>'
        s += label(W / 2, 40, "ВНЕШНИЙ УГОЛ · фреза / профиль", 13, "middle", 700, GR, 1)
    elif kind == "joint":
        s += rect(40, 220, 360, 40, "url(#hBrick)", GR, 1)
        s += rect(40, 200, 360, 20, "#d8cbb0", GR, .6)
        s += rect(40, 186, 170, t, HPL, "#000", .8) + rect(222, 186, 178, t, HPL, "#000", .8)
        s += dim(210, 160, 222, 160, "ПО ПРОЕКТУ", 0, 11)
        s += label(W / 2, 40, "СТЫК ПАНЕЛЕЙ · компенсационный зазор", 13, "middle", 700, GR, 1)
    elif kind == "ceiling":
        s += rect(40, 60, 360, 40, "url(#hCon)", GR, 1)
        s += rect(80, 100, 6, 60, "#9aa0a7", GR, .6) + rect(300, 100, 6, 60, "#9aa0a7", GR, .6)
        s += rect(60, 160, 330, 8, "url(#gSteelV)", GR, .8) + rect(40, 168, 360, t, HPL, "#000", .8)
        s += rect(380, 182, 20, 140, "url(#hBrick)", GR, 1)
        s += label(W / 2, 40, "ПОТОЛОК · подвес + каркас", 13, "middle", 700, GR, 1)
    elif kind == "floor":
        s += rect(40, 60, 40, 240, "url(#hBrick)", GR, 1) + rect(40, 300, 360, 30, "url(#hCon)", GR, 1)
        s += rect(80, 60, 6, 220, "#d8cbb0", "none", 0) + rect(86, 60, t, 226, HPL, "#000", .8)
        s += dim(110, 286, 110, 300, "ЗАЗОР", 0, 10, vertical=True)
        s += rect(100, 260, 20, 40, "#cfd3d8", GR, .8)
        s += label(W / 2, 40, "ПРИМЫКАНИЕ К ПОЛУ · плинтус / зазор", 13, "middle", 700, GR, 1)
    elif kind == "door":
        s += rect(40, 80, 140, 40, "url(#hBrick)", GR, 1)
        s += rect(40, 120, 140, t, HPL, "#000", .8)
        s += rect(180, 60, 24, 100, "#e7e2d8", GR, 1) + rect(204, 100, 200, 16, "#e9ebee", GR, 1)
        s += rect(166, 80, t, 54, HPL, "#000", .8)
        s += label(W / 2, 40, "ДВЕРНОЙ ПРОЁМ · наличник HPL", 13, "middle", 700, GR, 1)
    elif kind == "furniture":
        s += rect(80, 120, 280, 26, HPL, "#000", .8)
        s += rect(80, 146, 26, 160, HPL, "#000", .8) + rect(334, 146, 26, 160, HPL, "#000", .8)
        s += f'<path d="M80 120 q0 -6 6 -6" stroke="{OR}" stroke-width="2" fill="none"/>'
        s += rect(100, 146, 8, 8, "#9aa0a7", GR, .6) + rect(326, 146, 8, 8, "#9aa0a7", GR, .6)
        s += label(W / 2, 40, "МЕБЕЛЬНАЯ КРОМКА · фаска / радиус", 13, "middle", 700, GR, 1)
    elif kind == "wall_junction":
        s += rect(40, 180, 360, 40, "url(#hBrick)", GR, 1)
        s += rect(200, 60, 40, 120, "url(#hBrick)", GR, 1)
        s += rect(40, 166, 150, t, HPL, "#000", .8) + rect(250, 166, 150, t, HPL, "#000", .8)
        s += rect(186, 60, t, 106, HPL, "#000", .8) + rect(240, 60, t, 106, HPL, "#000", .8)
        s += label(W / 2, 40, "ПРИМЫКАНИЕ ПЕРЕГОРОДКИ", 13, "middle", 700, GR, 1)
    return svg(W, H, s)
