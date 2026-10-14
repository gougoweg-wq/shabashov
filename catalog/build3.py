# -*- coding: utf-8 -*-
"""UZHPL technical catalog v3 (minimal, RU) -> uzhpl-catalog.html"""
import os
from page2 import Book, title, OR, GR, DG, MG, LG, XL
from icons import icon
from drawings2 import callout_fig, legend, panel_layout, formats_svg, ijoint, glue_prep, rivet_sec
from sections import node, principle_section, glue_section, hidden_principle, screw_detail, interior_node
from lib import svg

HERE = os.path.dirname(os.path.abspath(__file__))
b = Book()
P = "ПО ПРОЕКТУ"


# ------------------------------------------------------------------ helpers
def legend3(items):
    return '<div style="margin-top:18px">' + legend(items, 3) + '</div>'


def cfig(name, keys, w=780):
    return (f'<div class="fig" style="margin:18px auto 0;width:{w}px">'
            f'{callout_fig(name, keys, crop=(150, 40, 1050, 1420))}</div>')


def band(src, h, cap="", fit="cover", pos="center", mt=34):
    c = f'<div class="cap">{cap}</div>' if cap else ""
    return (f'<div style="margin-top:{mt}px"><div style="height:{h}px;overflow:hidden;background:{XL}">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:{fit};object-position:{pos};display:block"></div>{c}</div>')


def img(src, h=150, fit="contain"):
    return f'<img src="{src}" alt="" style="width:100%;height:{h}px;object-fit:{fit};display:block;mix-blend-mode:multiply">'


def bg(src, h, pos="center", extra=""):
    return f'<div class="photo" style="height:{h}px;background-image:url({src});background-position:{pos};{extra}"></div>'


def ic(n, s=48, color=GR):
    return icon(n, s, color=color)


def tile(vis, name, desc="", meta="", h=150):
    m = f'<div class="meta">{meta}</div>' if meta else ""
    return f'<div class="tile"><div class="im" style="height:{h}px">{vis}</div><h4>{name}</h4><p>{desc}</p>{m}</div>'


def toolcard(src, name, desc, meta="", h=150):
    return tile(f'<img src="{src}" style="max-height:{h}px">', name, desc, meta, h)


def item(icn, name, desc):
    return f'<div class="it"><div>{ic(icn, 48)}</div><div><h4>{name}</h4><p>{desc}</p></div></div>'


def steps(lst, start=1):
    out = ""
    for i, (a, d, v) in enumerate(lst):
        vis = ic(v[2:], 50) if v.startswith("i:") else f'<img src="{v[2:]}" alt="">'
        out += f'<div class="step"><div class="n">{i + start:02d}</div><div class="ph">{vis}</div><div><h4>{a}</h4><p>{d}</p></div></div>'
    return f'<div style="margin-top:30px">{out}</div>'


def recs(lst):
    return '<div style="margin-top:34px">' + "".join(
        f'<div class="spec" style="grid-template-columns:44px 1fr auto;gap:10px;padding:17px 0">'
        f'<span style="color:{OR};font-weight:600;font-size:14px">{i + 1:02d}</span>'
        f'<span><b style="color:{GR};font-weight:600">{a}</b><br><span style="font-size:15px;color:{DG}">{d}</span></span>'
        f'<span>{f"<span class=pill>{p}</span>" if p else ""}</span></div>' for i, (a, d, p) in enumerate(lst)) + '</div>'


def divider(key, name, photo, meaning, apply, how, fastening, subs):
    rows = "".join(f'<a href="#a-{key}.{i + 1}"><span>{t}</span><span>{{{{pg:{key}.{i + 1}}}}}</span></a>' for i, t in enumerate(subs))
    body = (f'<div style="position:absolute;left:0;right:0;top:0;height:760px">{bg(photo, 760)}</div>'
            f'<div style="position:absolute;left:0;right:0;top:560px;height:200px;background:linear-gradient(180deg,rgba(29,31,34,0),#1D1F22)"></div>'
            f'<div style="margin-top:600px">{title(name, "Система крепления")}'
            f'<div class="lead" style="margin-top:18px">{meaning}</div>'
            f'<div class="g3" style="margin-top:34px">'
            f'<div><h3 style="color:{OR}">Крепление панели</h3><div style="font-size:16px;line-height:1.5">{fastening}</div></div>'
            f'<div><h3 style="color:{OR}">Как работает</h3><div style="font-size:16px;line-height:1.5;color:#c9ccd0">{how}</div></div>'
            f'<div><h3 style="color:{OR}">Применение</h3><div style="font-size:16px;line-height:1.5;color:#c9ccd0">{apply}</div></div></div>'
            f'<div class="toc" style="margin-top:40px;border-top:1px solid #34373c">{rows}</div></div>')
    b.add(body, name.replace("<br>", " "), dark=True, anchor=key)


def result(photo, name, sub, dark=True):
    col = "#fff" if dark else GR
    grad = "linear-gradient(180deg,rgba(29,31,34,0) 55%,rgba(29,31,34,.85))" if dark else "linear-gradient(180deg,rgba(255,255,255,0) 55%,rgba(255,255,255,.9))"
    body = (f'<div style="position:absolute;inset:0">{bg(photo, 1920)}</div><div style="position:absolute;inset:0;background:{grad}"></div>'
            f'<div style="position:absolute;left:84px;right:84px;bottom:150px;color:{col}"><div class="kick">Готовый результат</div>'
            f'<div style="font-size:64px;font-weight:700;line-height:1.02;text-transform:uppercase;margin-top:14px">{name}</div>'
            f'<div style="font-size:20px;margin-top:18px;max-width:760px;line-height:1.5;opacity:.85">{sub}</div></div>'
            f'<div style="position:absolute;right:84px;top:72px;font-size:11px;letter-spacing:.24em;color:{col};opacity:.7">ВИЗУАЛИЗАЦИЯ</div>')
    b.add(body, "", dark=dark)


V = "img/v2/"
MB = "img/mbe/"
TL = "img/tools/"

# =================================================================== 01 COVER
cover = (f'<div style="position:absolute;inset:0">{bg(V + "cover.png", 1920, "center")}</div>'
         f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,.92) 0%,rgba(255,255,255,.55) 30%,rgba(255,255,255,0) 52%)"></div>'
         f'<div style="position:absolute;left:84px;top:84px"><img src="img/brand/logo.png" style="height:46px" alt="UZHPL"></div>'
         f'<div style="position:absolute;left:84px;top:300px;right:84px">'
         f'<div style="width:56px;height:3px;background:{OR}"></div>'
         f'<div style="font-size:64px;font-weight:700;line-height:1.05;letter-spacing:-.015em;margin-top:34px;text-transform:uppercase">Фасадные<br>и интерьерные<br>системы HPL</div>'
         f'<div style="font-size:26px;font-weight:400;color:{DG};margin-top:26px">Технический каталог</div></div>'
         f'<div style="position:absolute;left:84px;bottom:76px;font-size:15px;letter-spacing:.14em;color:{GR}">uzhpl.uz</div>')
b.add(cover, bare=True)

# =================================================================== 02 CONTENTS
toc = [("about", "О компании UZHPL"), ("product", "Панель FAÇADE UZHPL"), ("formats", "Форматы и сравнение"),
       ("vent", "Как устроен вентилируемый фасад"), ("vent2", "Принцип работы вентфасада"), ("systems", "Фасадные системы"),
       ("choose", "Как выбрать систему"), ("rivet", "Заклёпочная система"), ("glue", "Клеевая система"),
       ("hidden", "Скрытая система"), ("screw", "Винтовая система"), ("nodes", "Фасадные узлы"),
       ("interior", "Интерьерные системы"), ("tools", "Инструменты UZHPL"), ("qc", "Технадзор и контроль качества"),
       ("recs", "Рекомендации UZHPL"), ("start", "Как начать проект")]
rows = "".join(f'<a href="#a-{k}"><span>{t}</span><span>{{{{pg:{k}}}}}</span></a>' for k, t in toc)
b.add(f'{title("Содержание")}<div class="toc" style="margin-top:56px;border-top:1px solid #34373c">{rows}</div>'
      f'<div class="note" style="color:#8a9097;margin-top:36px">Размеры, шаги и нагрузки с пометкой «ПО ПРОЕКТУ», «ПО РАСЧЁТУ» или «НА ОБЪЕКТЕ» '
      f'определяются проектом фасада и инструкциями производителей панели и крепежа. Каталог не заменяет проект.</div>', "Содержание", dark=True)

# =================================================================== ABOUT
chain = [("project", "Проект", "Подбор решения под архитектурную задачу"), ("engineering", "Инженерия", "Расчёт подсистемы, раскладка, узлы"),
         ("material", "Материал", "HPL-панели и полный комплект подсистемы"), ("processing", "Обработка", "Раскрой, сверление, фрезерование"),
         ("logistics", "Логистика", "Комплектная поставка на объект"), ("montage", "Монтаж", "Бригады, обученные немецкой технологии"),
         ("supervision", "Технадзор", "Контроль специалистов из Германии")]
ch = '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:0;margin-top:46px;border-top:1px solid ' + LG + '">'
for i, (n, a, d) in enumerate(chain):
    ch += (f'<div style="padding:26px 12px 0 0;position:relative">{ic(n, 46)}<div style="font-size:12px;color:{OR};font-weight:600;letter-spacing:.14em;margin-top:16px">{i + 1:02d}</div>'
           f'<div style="font-size:17px;font-weight:600;margin-top:4px">{a}</div><div style="font-size:13px;color:{DG};margin-top:6px;line-height:1.4">{d}</div>'
           + (f'<div style="position:absolute;top:-5px;left:0;width:9px;height:9px;border-radius:50%;background:{OR}"></div>') + '</div>')
ch += '</div>'
pillars = [("germany", "Немецкая технология", "Монтаж HPL по стандартам и инструкциям европейских производителей систем."),
           ("supervision", "Технадзор из Германии", "Наши специалисты контролируют каждый этап — от подсистемы до сдачи."),
           ("material", "Всё в одной поставке", "Панели, подсистема, крепёж, клеевые системы и инструмент.")]
b.add(title("О компании UZHPL", "", "UZHPL — интегратор HPL-панелей с полным циклом применения: от подбора материала и инженерии до монтажа по немецкой технологии и технадзора. Один подрядчик — одна ответственность.")
      + ch + '<div class="hr" style="margin-top:56px"></div>'
      + '<div class="g3">' + "".join(item(n, a, d) for n, a, d in pillars) + '</div>'
      + f'<div style="margin-top:56px;display:grid;grid-template-columns:1.25fr 1fr;gap:20px">{bg("img/brand/residential.jpg", 640, "center 60%")}{bg("img/brand/facade3d_a.jpg", 640)}</div>',
      "О компании", anchor="about")

# =================================================================== PRODUCT
layers = [("UV Film Grade 6", "Защита от выгорания (EN 438-2)"), ("Deco Paper", "Декоративный слой — цвет и текстура"),
          ("Melamine Resin", "Прочность поверхности"), ("Kraft Paper", "Основа — задаёт толщину"), ("Phenolic Resin", "Водостойкость и плотность")]
specs = [("Плотность", "1450–1500 кг/м³"), ("Толщина фасадных панелей", "6 / 8 / 10 мм"), ("Водопоглощение", "≤ 6 %"),
         ("Светостойкость", "EN 438-2, Grade 6"), ("Пожарный класс", "B-s1, d0"), ("Экологичность", "E1 / E0"),
         ("Прочность на изгиб", "97 МПа"), ("Термостойкость", "−40 … +80 °C"), ("Срок службы", "20+ лет")]
b.add(title("Панель<br>FAÇADE UZHPL", "Продукт", "Компактная HPL-панель высокого давления с УФ-стабилизированным финишным слоем. Устойчива к влаге, солнцу и перепадам температур; не требует обработки после монтажа.")
      + f'<div style="margin-top:44px">{bg("img/brand/panels.jpg", 560, "center 45%")}</div>'
      + '<div class="g2" style="margin-top:44px;gap:56px"><div><h3>Структура панели</h3>'
      + "".join(f'<div class="spec" style="grid-template-columns:20px 1fr"><span style="width:10px;height:10px;background:{c};margin-top:6px;display:block"></span>'
                f'<span><b style="color:{GR};font-weight:600">{a}</b><br><span style="font-size:14px;color:{MG}">{d}</span></span></div>'
                for (a, d), c in zip(layers, ["#cfe0ea", "#8a4a2a", "#d8d2c4", "#b88a52", "#4a3322"]))
      + f'<div class="cap" style="color:{OR};margin-top:14px;font-weight:600">ПРЕССОВАНИЕ 1430 PSI · 150 °C</div></div>'
      + '<div><h3>Технические параметры</h3>' + "".join(f'<div class="spec"><span>{a}</span><span>{v}</span></div>' for a, v in specs) + '</div></div>'
      + '<div class="note">Параметры — по каталогу UZHPL HPL 2026–2027, подтверждены протоколами испытаний. Копии сертификатов — по запросу.</div>',
      "Продукт", anchor="product")

# =================================================================== FORMATS & COMPARISON
cmp = [("Вес, кг/м²", "7–12", "4–6", "25–35", "40–80"), ("Монтаж", "Простой", "Простой", "Средний", "Сложный"),
       ("Светостойкость", "Высокая", "Низкая", "Средняя", "Высокая"), ("Нагрев на солнце", "Низкий", "Сильный", "Средний", "Сильный"),
       ("Цена", "Средняя", "Низкая", "Средняя", "Высокая"), ("Ремонт", "Замена панели", "Замена кассеты", "Сложно", "Сложно"),
       ("Выбор декоров", "1000+", "RAL", "Ограничен", "Натуральный")]
th = "".join(f'<th{" class=hl" if i == 1 else ""}>{h}</th>' for i, h in enumerate(["", "HPL", "АКП", "Фиброцемент", "Камень"]))
tb = "".join("<tr>" + "".join(f'<td{" class=hl" if i == 1 else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in cmp)
b.add(title("Форматы<br>и сравнение", "Продукт", "Стандартные листы и раскрой под проект. Основной фасадный формат — 1220 × 3050 мм.")
      + f'<div style="margin-top:46px">{formats_svg()}</div>'
      + '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:6px;align-items:center"><span class="cap" style="margin:0 10px 0 0">ТОЛЩИНЫ, ММ</span>'
      + "".join(f'<span style="padding:7px 14px;font-size:15px;font-weight:600;border:1px solid {OR if t in ("6", "8", "10") else LG};color:{OR if t in ("6", "8", "10") else GR}">{t}</span>'
                for t in "3 4 6 8 10 12 16 18 25".split()) + '</div>'
      + f'<p class="tx" style="margin-top:12px">Фасад — 6 / 8 / 10 мм (выделено). Другие толщины и раскрой под проект — по запросу.</p>'
      + f'<div class="hr"></div><h3>HPL против альтернатив</h3><table class="t">{th}{tb}</table>'
      + '<div class="note">Данные — усреднённые по рынку фасадных материалов (каталог UZHPL HPL 2026–2027).</div>',
      "Форматы", anchor="formats")

# =================================================================== VENT FACADE
vent_keys = ["wall", "pad", "bracket", "anchor", "ins", "dowel", "mem", "lprof", "tprof", "prof_rivet", "epdm", "panel", "fastener"]
vent_leg = [("Несущая стена", "основание — проверяется по проекту"), ("Терморазрывная прокладка", "паронит под кронштейн"),
            ("Кронштейн", "несущий / опорный"), ("Анкерный болт", "крепит кронштейн к стене"),
            ("Утеплитель", "минеральная (базальтовая) вата"), ("Тарельчатый дюбель", "крепит утеплитель"),
            ("Ветрозащитная мембрана", "паропроницаемая"), ("L-профиль", "на поле панели"), ("T-профиль", "на стыке панелей"),
            ("Заклёпка профиль — кронштейн", "фиксирует профиль"), ("EPDM-лента", "на полку профиля"), ("HPL-панель", "1220 × 3050 мм"),
            ("Крепёж панели", "заклёпка / винт / клей / кляммер")]
b.add(title("Как устроен<br>вентилируемый фасад", "Основы", "Слои от стены наружу. Между утеплителем и панелью — вентилируемый зазор.")
      + cfig('expl_rivet', vent_keys, 700) + legend3(vent_leg),
      "Вентфасад", anchor="vent")

b.add(title("Принцип работы", "Основы", "Воздух входит у цоколя, движется в зазоре за панелями и выходит у парапета — утеплитель остаётся сухим, фасад «дышит».")
      + f'<div class="fig" style="margin-top:30px">{principle_section(936, 860)}</div>'
      + '<div class="g2" style="margin-top:30px;gap:30px 40px">'
      + item("membrane", "Вентиляция", "Непрерывный зазор от цоколя до парапета; входы и выходы воздуха не перекрываются.")
      + item("insulation", "Сухой утеплитель", "Пар выходит через мембрану и уносится потоком воздуха.")
      + item("pad", "Без мостиков холода", "Паронитовая прокладка разделяет кронштейн и стену.")
      + item("layout", "Свобода движения", "Панель расширяется от тепла: одна фиксированная точка, остальные — скользящие.") + '</div>',
      "Вентфасад", anchor="vent2")

# =================================================================== SYSTEMS OVERVIEW
SYS = [("rivet", "Заклёпочная", "Фасадная заклёпка Ø5 с головкой в цвет панели", "Видимый крепёж с аккуратным ритмом. Самая распространённая и ремонтопригодная система."),
       ("glue", "Клеевая", "Активатор · праймер · двусторонняя лента · клей", "Чистая плоскость без крепежа на лицевой стороне."),
       ("hidden", "Скрытая", "Кляммер (клипса) на анкере с подрезкой", "Панель навешивается на горизонтальные направляющие. Крепёж не виден."),
       ("screw", "Винтовая", "Фасадный винт с окрашенной головкой", "Видимый механический крепёж; простая замена панели.")]
cards = ""
for k, n, f, d in SYS:
    cards += (f'<a href="#a-{k}" class="tile" style="padding:0;display:block"><div style="height:470px;overflow:hidden;background:#fff">'
              f'<img src="{V}sys_{k}.png" style="width:100%;height:100%;object-fit:cover;object-position:center 40%"></div>'
              f'<div style="padding:20px 22px 22px"><h4 style="font-size:22px">{n} система</h4>'
              f'<div style="font-size:14px;margin-top:8px"><span style="color:{OR};font-weight:600">Крепление: </span>{f}</div>'
              f'<p>{d}</p></div></a>')
b.add(title("Фасадные системы", "Обзор", "Подсистема у всех систем одна. Отличается только то, на что крепится панель. Показано на двух панелях 1220 × 3050 мм.")
      + f'<div class="g2" style="margin-top:40px;gap:20px">{cards}</div>', "Системы", anchor="systems")

# =================================================================== CHOOSE
sel = [("Вид крепежа", "Заклёпки в цвет панели", "Не виден", "Не виден", "Винты в цвет панели"),
       ("Крепление панели", "Заклёпка Ø5", "Лента + клей", "Кляммер + анкер", "Фасадный винт"),
       ("Замена панели", "Просто", "Сложно", "Средне", "Просто"),
       ("Скорость монтажа", "Высокая", "Ниже: выдержка, отверждение", "Средняя", "Высокая"),
       ("Подготовка панели", "Отверстия Ø10", "Шлифовка, праймер", "Фрезерование (ЧПУ)", "Отверстия"),
       ("Условия монтажа", "По инструкции", "Строго: t° и влажность", "По инструкции", "По инструкции"),
       ("Лучше всего для", "Большинства объектов", "Чистой архитектуры", "Премиальных фасадов", "Ремонтопригодных фасадов")]
th = "".join(f"<th>{h}</th>" for h in ["", "Заклёпочная", "Клеевая", "Скрытая", "Винтовая"])
tb = "".join("<tr>" + "".join(f'<td{" style=font-weight:600" if i == 0 else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in sel)
b.add(title("Как выбрать<br>систему", "Выбор", "Короткое сравнение для архитектора и заказчика. Окончательный выбор — по проекту, ветровым нагрузкам и бюджету.")
      + f'<table class="t" style="margin-top:46px">{th}{tb}</table>'
      + '<div class="g4" style="margin-top:46px">' + "".join(
          f'<a href="#a-{k}" style="display:block"><div style="height:340px;overflow:hidden"><img src="{V}macro_{k}.png" style="width:100%;height:100%;object-fit:cover"></div>'
          f'<div style="font-size:14px;font-weight:600;margin-top:10px">{n}</div><div class="cap" style="margin-top:2px">{c}</div></a>'
          if k in ("rivet", "screw") else
          f'<a href="#a-{k}" style="display:block"><div style="height:340px;overflow:hidden"><img src="{V}wall_{k}.png" style="width:100%;height:100%;object-fit:cover"></div>'
          f'<div style="font-size:14px;font-weight:600;margin-top:10px">{n}</div><div class="cap" style="margin-top:2px">{c}</div></a>'
          for k, n, c in [("rivet", "Заклёпочная", "головки в цвет панели"), ("glue", "Клеевая", "крепёж не виден"),
                          ("hidden", "Скрытая", "крепёж не виден"), ("screw", "Винтовая", "головки винтов")]) + '</div>'
      + '<div class="note">Не уверены, какую систему выбрать? Пришлите фасады и площадь — инженер UZHPL подберёт решение.</div>',
      "Выбор системы", anchor="choose")

# gallery: 4 images per system + description
GAL = {"rivet": [("bw_rivet", "Общий вид фасада"), ("wall_rivet_close", "Ритм заклёпок на панелях 1220 × 3050"), ("sys_rivet", "Монтаж панели на L/T-профили"), ("macro_rivet", "Заклёпки у вертикального стыка")],
       "glue": [("bw_glue", "Общий вид фасада"), ("wall_glue", "Чистая плоскость без крепежа"), ("sys_glue", "Лента и клеевой валик на профилях"), ("expl_glue", "Состав системы")],
       "hidden": [("bw_hidden", "Общий вид фасада"), ("wall_hidden", "Крепёж не виден"), ("sys_hidden", "Горизонтальные направляющие"), ("expl_hidden", "Кляммеры на направляющих")],
       "screw": [("bw_screw", "Общий вид фасада"), ("wall_screw", "Головки винтов в цвет панели"), ("sys_screw", "Монтаж панели на профили"), ("macro_screw", "Винты у вертикального стыка")]}
DESC = {"rivet": "Заклёпки с окрашенной головкой образуют ровный графичный ритм. Подходит для жилых, общественных и промышленных зданий.",
        "glue": "Монолитная плоскость без единого видимого элемента крепления. Для современной архитектуры и крупных однотонных плоскостей.",
        "hidden": "Панели навешиваются на кляммеры — фасад выглядит как цельная плоскость, панель можно снять.",
        "screw": "Аналог заклёпочной системы с винтовым крепежом; подходит для объектов, где важна простая замена панели."}
# real project photos: drop up to 4 images into img/projects/<system>/ (sorted by name) — they replace the renders
def gal_items(k):
    real = sorted(f for f in os.listdir(os.path.join(HERE, "img", "projects", k))
                  if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))) if os.path.isdir(os.path.join(HERE, "img", "projects", k)) else []
    items = [(f"img/projects/{k}/{f}", os.path.splitext(f)[0].split("_", 1)[-1].replace("-", " ")) for f in real[:4]]
    return items + [(f"{V}{im}.png", c) for im, c in GAL[k][len(items):]]


gal = ""
for k, n, f, d in SYS:
    gal += (f'<div style="display:grid;grid-template-columns:230px 1fr;gap:24px;padding:22px 0;border-bottom:1px solid {LG}">'
            f'<div><div class="kick" style="font-size:11px">Система</div><div style="font-size:22px;font-weight:700;margin-top:6px">{n}</div>'
            f'<p class="tx" style="margin-top:10px">{DESC[k]}</p></div>'
            f'<div class="g4" style="gap:10px">' + "".join(
                f'<div><div class="slot" style="height:250px"><img src="{im}" style="width:100%;height:100%;object-fit:cover"></div>'
                f'<div class="cap" style="margin-top:6px;line-height:1.35">{c}</div></div>' for im, c in gal_items(k)) + '</div></div>')
b.add(title("Как выглядит<br>каждая система", "Выбор", "По четыре вида на каждую систему: общий вид, плоскость фасада, монтаж и узел крепления.")
      + f'<div style="margin-top:30px">{gal}</div>', "Выбор системы")


# =================================================================== FACADE NODE DATA (shared)
node_pages = [
    ("outer_corner", "Внешний угол", ["Угловой профиль за швом; панели не касаются друг друга", "Шов на углу открытый или с угловым профилем", "Крепление обеих панелей у угла — по схеме системы"]),
    ("inner_corner", "Внутренний угол", ["Внутренний угловой профиль", "Зазор для температурного движения", "Крепление каждой панели к своему профилю"]),
    ("window_reveal", "Оконный откос", ["HPL-откос до оконного блока", "Утеплитель откоса без пустот", "Примыкание к окну — герметизация по проекту"]),
    ("window_head", "Верхний оконный узел", ["Нижняя панель (софит) над окном", "Вход воздуха в вентзазор", "Зазор у оконного блока — ПО ПРОЕКТУ"]),
    ("window_sill", "Нижний оконный узел", ["Отлив с уклоном и капельником", "Выход воздуха из зазора под отливом", "Вынос отлива за плоскость фасада — ПО ПРОЕКТУ"]),
    ("base", "Цоколь", ["Перфорированный цокольный профиль", "Вход воздуха и защита от грызунов", "Отметка над отмосткой — ПО ПРОЕКТУ"]),
    ("parapet", "Парапет", ["Парапетная крышка с уклоном внутрь", "Выход воздуха под крышкой", "Вынос крышки — ПО ПРОЕКТУ"]),
    ("top", "Верхнее примыкание", ["Примыкание к перекрытию / козырьку", "Выход воздуха из зазора", "Отлив — ПО ПРОЕКТУ"]),
    ("hjoint", "Горизонтальный стык", ["Открытый горизонтальный шов", "Профиль непрерывный по высоте", "Ширина шва — ПО ПРОЕКТУ"]),
    ("vjoint", "Вертикальный стык", ["Шов над T-профилем с EPDM-лентой", "Крепление обеих панелей к полкам T-профиля", "Ширина шва — ПО ПРОЕКТУ"]),
]
N3D = {"outer_corner": "n_outer_corner", "inner_corner": "n_inner_corner", "window_reveal": "n_window", "window_head": "n_window",
       "window_sill": "n_window", "base": "n_base", "parapet": "n_parapet", "top": "n_parapet", "hjoint": "n_hjoint", "vjoint": "n_vjoint"}


def nodes_page(key, sysname, fix, kinds):
    b.add(title("Основные узлы", sysname) + '<div class="g2" style="margin-top:26px;gap:12px">'
          + "".join(f'<div>{node(k, 900, 720, fix)}</div>' for k in kinds) + '</div>'
          + f'<div class="note" style="margin-top:16px">Принципиальные схемы. Зазоры, шаг крепления и отступы — {P} / ПО РАСЧЁТУ.</div>',
          sysname, anchor=f"{key}.4")


# =================================================================== RIVET SYSTEM
divider("rivet", "Заклёпочная<br>система", V + "bw_rivet.png",
        "Классическая и самая надёжная система для HPL: панель механически крепится к алюминиевой подсистеме фасадными заклёпками. Головки окрашены в цвет панели и образуют аккуратный ритм.",
        "Жилые, общественные, промышленные здания; высотные объекты; фасады, где важна ремонтопригодность.",
        "Одна фиксированная точка задаёт положение панели, остальные — скользящие: панель свободно «дышит» при нагреве.",
        "Фасадная заклёпка Ø5 мм, головка Ø16 мм в цвет панели (L-профиль на поле панели, T-профиль на стыке).",
        ["Конструкция", "Компоненты", "Принцип работы", "Основные узлы", "Подготовка HPL", "Монтаж", "Инструменты", "Рекомендации"])
rk = ["wall", "pad", "bracket", "anchor", "ins", "dowel", "mem", "lprof", "tprof", "prof_rivet", "epdm", "panel", "fastener"]
b.add(title("Конструкция", "Заклёпочная система", "Нумерация — от стены к панели.")
      + cfig('expl_rivet', rk)
      + legend3([("Несущая стена", ""), ("Терморазрывная прокладка", "паронит, под кронштейн"), ("Кронштейн", "несущий и опорный"),
                ("Анкерный болт", "кронштейн → стена"), ("Утеплитель", "базальтовая вата"), ("Тарельчатый дюбель", "утеплитель → стена"),
                ("Ветрозащитная мембрана", ""), ("L-профиль", "на поле панели"), ("T-профиль", "на стыке панелей"),
                ("Заклёпка профиль — кронштейн", ""), ("EPDM-лента", "на полку профиля"), ("HPL-панель", "1220 × 3050 мм"),
                ("Фасадная заклёпка", "в цвет панели")]), "Заклёпочная система", anchor="rivet.1")

comps = [(f'<img src="{MB}rivet_painted.jpg" style="height:140px">', "Фасадная заклёпка", "AlMg5, Ø5 мм, головка Ø16 мм в цвет панели; стержень — нержавеющая сталь.", "длина 16–33 мм — по пакету"),
         (f'<img src="{MB}fix_sleeve.jpg" style="height:110px">', "Гильза фиксированной точки", "Ø10 × 6 мм, отверстие Ø5,1. Одна фикс. точка на панель.", "алюминий / A2"),
         (f'<img src="img/c_lprofile.png" style="height:130px">', "L-профиль", "Вертикальный профиль на поле панели.", "алюминий · по расчёту"),
         (f'<img src="img/c_tprofile.png" style="height:130px">', "T-профиль", "Профиль вертикального стыка двух панелей.", "алюминий · по расчёту"),
         (f'<img src="img/c_bracket_fixed.png" style="height:130px">', "Кронштейн", "Несущий (вес) и опорный (ветер, движение).", "шаг — по расчёту"),
         (ic("pad", 90), "Терморазрывная прокладка", "Паронит под опорную пластину кронштейна.", "под каждый кронштейн"),
         (f'<img src="img/c_anchor.png" style="height:120px">', "Анкерный болт", "Крепит кронштейн к основанию.", "тип — по основанию"),
         (f'<img src="{MB}rivet_alu.jpg" style="height:140px">', "Заклёпка профиль — кронштейн", "Соединяет профиль с кронштейном.", "по системе"),
         (f'<img src="{MB}epdm.jpg" style="height:130px">', "EPDM-лента", "Толщина 0,75 / 1,3 мм; ширина 70 / 110 / 135 мм. Стойкость к УФ — 20 лет.", "на полку профиля"),
         (f'<img src="img/c_insulation.png" style="height:120px">', "Утеплитель", "Минеральная (базальтовая) вата.", "толщина — по расчёту"),
         (ic("dowel", 90), "Тарельчатый дюбель", "Крепит утеплитель и мембрану к стене.", "по расчёту"),
         (f'<img src="img/c_membrane.png" style="height:120px">', "Ветрозащитная мембрана", "Защищает утеплитель от ветра, пропускает пар.", "паропроницаемая")]
b.add(title("Компоненты системы", "Заклёпочная система")
      + f'<div style="margin-top:34px;display:grid;grid-template-columns:1.3fr 1fr;gap:20px">{bg("img/brand/panels.jpg", 330, "center 40%")}'
      + f'<div class="tile" style="display:flex;flex-direction:column;justify-content:center"><div class="kick">HPL-панель</div><h4 style="font-size:26px;margin-top:10px">FAÇADE UZHPL</h4>'
      + f'<p>Формат 1220 × 3050 мм, толщина 6 / 8 / 10 мм. Отверстия под заклёпки — по монтажной карте.</p></div></div>'
      + '<div class="g4" style="margin-top:20px;gap:14px">' + "".join(tile(v, n, d, m, 130) for v, n, d, m in comps) + '</div>'
      + '<div class="note">Длина заклёпки = толщина панели + профиля (зона зажима). Отверстие в профиле — Ø5,1 мм; в панели — по инструкции производителя (оснастка MBE: Ø10 мм).</div>',
      "Заклёпочная система", anchor="rivet.2")

b.add(title("Принцип работы", "Заклёпочная система", "Схема на панели 1220 × 3050 мм. Панель не зажата жёстко: она расширяется от фиксированной точки.")
      + f'<div style="display:grid;grid-template-columns:420px 1fr;gap:34px;margin-top:34px"><div>{panel_layout("rivet", 420, 1000)}</div><div>'
      + f'<div class="g2" style="gap:14px">{rivet_sec(True)}{rivet_sec(False)}</div>'
      + '<div style="margin-top:26px;display:grid;gap:22px">'
      + item("sleeve", "Фиксированная точка", "Одна на панель. Гильза Ø10 × 6 заполняет отверстие — панель не смещается.")
      + item("layout", "Скользящие точки", "Отверстие в панели больше стержня заклёпки — панель свободно движется при нагреве.")
      + item("rivet", "Наконечник G3", "Специальный наконечник заклёпочника оставляет зазор под головкой: заклёпка не прижимает панель.")
      + item("epdm", "EPDM-лента", "Защищает профиль и шов, разделяет панель и металл.") + '</div></div></div>'
      + '<div class="note">Шаг крепления, отступы от кромок и количество точек — ПО РАСЧЁТУ ветровой нагрузки и инструкции производителя.</div>',
      "Заклёпочная система", anchor="rivet.3")

names = {k: n for k, n, _ in node_pages}
idx = "".join(f'<a href="#a-nodes.{i + 1}" class="tile" style="padding:14px;display:block"><div style="height:170px">'
              f'<img src="img/n_{N3D[k][2:]}.png" style="width:100%;height:100%;object-fit:contain"></div>'
              f'<div style="display:flex;gap:10px;align-items:center;margin-top:8px"><span class="badge">{i + 1}</span><h4 style="font-size:16px">{names[k]}</h4></div>'
              f'<p style="margin-top:4px;font-size:13px">Разрез и детали — стр. {{{{pg:nodes.{i + 1}}}}} →</p></a>' for i, (k, _, _) in enumerate(node_pages))
b.add(title("Основные узлы", "Заклёпочная система", "10 типовых узлов. Нажмите на узел — откроется страница с разрезом.")
      + f'<div class="g2" style="margin-top:30px;gap:14px">{idx}</div>', "Заклёпочная система", anchor="rivet.4")

b.add(title("Подготовка HPL", "Заклёпочная система", "Панели готовятся в цехе UZHPL по монтажной карте — на объект приходит комплект, готовый к монтажу.")
      + steps([("Обмер", "Фактические размеры по месту — УТОЧНЯЕТСЯ НА ОБЪЕКТЕ.", "i:measure"),
               ("Раскрой", "Погружная пила с направляющей шиной, твердосплавный диск; лист поддерживается по всей длине.", "i:saw"),
               ("Сверление отверстий Ø10", "Сверло VHM с центрирующим острием — чистые края без сколов.", "i:drillbit"),
               ("Обработка кромок", "Снятие заусенцев, лёгкая фаска.", "i:edge"),
               ("Гильзы фиксированных точек", "Установка гильзы Ø10 × 6 в отверстие фиксированной точки.", "i:sleeve"),
               ("Маркировка и очистка", "Номер панели по раскладке; защитная плёнка снимается после монтажа.", "i:mark")])
      + '<h3 style="margin-top:40px">Оснастка цеха</h3><div class="g3" style="gap:14px">'
      + toolcard(TL + "festool_ts55.jpg", "Погружная пила + шина", "Раскрой листа 1220 × 3050 мм без сколов.", "раскрой", 120)
      + toolcard(MB + "vhm_drill.jpg", "Сверло VHM Ø10", "Твердосплавное, с центрирующим острием.", "отверстия в HPL", 90)
      + toolcard(MB + "fix_sleeve.jpg", "Гильза Ø10 × 6", "Отверстие 5,1 мм — фиксированная точка.", "фикс. точка", 110) + '</div>'
      + '<div class="note">Не увеличивать отверстия и не менять отступы от кромок без разрешения производителя.</div>',
      "Заклёпочная система", anchor="rivet.5")

b.add(title("Монтаж", "Заклёпочная система", "Последовательность работ на объекте.")
      + steps([("Разметка", "Оси и отметки кронштейнов по проекту — лазерный уровень.", "i:level"),
               ("Кронштейны", "Паронитовая прокладка → кронштейн → анкерный болт.", "i:bracket"),
               ("Утеплитель", "Плиты без щелей, крепление тарельчатыми дюбелями.", "i:insulation"),
               ("Мембрана", "Нахлёст и крепление — по инструкции.", "i:membrane"),
               ("L/T-профили", "Выставить в плоскость, закрепить заклёпками к кронштейнам.", "i:profile"),
               ("EPDM-лента", "На полки профилей по всей длине.", "i:epdm"),
               ("Перенос отверстий", "Пружинный кондуктор 5,1 / 10 мм: сверлит профиль через отверстие панели строго по центру.", f"p:{MB}spring_jig.jpg"),
               ("Фиксированная точка", "Первой ставится заклёпка в гильзу фикс. точки.", "i:sleeve"),
               ("Скользящие точки", "Заклёпочник с наконечником G3 — без зажима панели.", f"p:{MB}mouth_g3.jpg"),
               ("Контроль", "Плоскость, швы, головки, свобода движения панели; фото.", "i:check")])
      + band(V + "wall_rivet2.png", 400, "Заклёпки в цвет панели на панелях 1220 × 3050 мм"),
      "Заклёпочная система", anchor="rivet.6")


b.add(title("Инструменты", "Заклёпочная система", "Специальная оснастка для заклёпочного фасада HPL (MBE / Trespa) и электроинструмент.")
      + '<div class="g3" style="margin-top:34px;gap:14px">'
      + toolcard(MB + "accubird_pro.jpg", "Заклёпочник AccuBird PRO", "Аккумуляторный, 18 В, усилие 10 000 Н, ход 25 мм. Для заклёпок до Ø5 мм.", "MBE")
      + toolcard(MB + "mouth_g3.jpg", "Наконечник G3", "Для алюминиевых заклёпок Ø5, головка Ø16. Монтаж без зажима панели. Резьба M10 × 1.", "скользящие точки")
      + toolcard(MB + "spring_jig.jpg", "Пружинный кондуктор", "Одноручный, 5,1 / 10 мм: центрирует сверление профиля через отверстие панели.", "перенос отверстий")
      + toolcard(MB + "buegel_jig.jpg", "Скобовый кондуктор", "Панель Ø10 / профиль Ø5,1 мм; вариант с эксцентриком.", "перенос отверстий")
      + toolcard(MB + "vhm_drill.jpg", "Сверло VHM для HPL", "Твердосплавное, с центрирующим острием: Ø8 / Ø10 / Ø13 мм.", "отверстия в панели", 90)
      + toolcard(MB + "hss_drill.jpg", "Сверло HSS Ø5,1", "Для алюминиевой подсистемы, для кондукторов.", "отверстия в профиле")
      + toolcard(MB + "fix_sleeve.jpg", "Гильзы фикс. точек", "Ø10 × 6 мм с отверстием 5,1 и с пазом 5,2 × 7.", "фиксированная точка", 110)
      + toolcard(TL + "festool_ts55.jpg", "Погружная пила + шина", "Точный раскрой HPL на объекте; твердосплавный диск.", "раскрой", 120)
      + toolcard(TL + "m_hammer.jpg", "Перфоратор", "Отверстия под анкерные болты кронштейнов.", "подсистема", 120)
      + toolcard(TL + "guide_rail.jpg", "Направляющая шина", "Прямой рез по всей длине листа 3050 мм.", "раскрой", 120)
      + toolcard(TL + "m_drill.jpg", "Дрель-шуруповёрт", "Сверление профиля через кондуктор.", "подсистема", 120)
      + toolcard(MB + "paint_pen.jpg", "Лак-карандаш", "Подкраска головок заклёпок в цвет панели.", "финиш", 120)
      + '</div>', "Заклёпочная система", anchor="rivet.7")

b.add(title("Рекомендации UZHPL", "Заклёпочная система")
      + recs([("Расчёт проекта", "Подсистема, шаг кронштейнов, профилей и заклёпок — только по расчёту.", "ПО РАСЧЁТУ"),
              ("Одна фиксированная точка", "Остальные точки — скользящие. Нельзя зажимать все точки.", ""),
              ("Наконечник G3", "Скользящие точки — только специальным наконечником.", ""),
              ("Центровка отверстий", "Профиль сверлится через панель кондуктором — строго по центру.", ""),
              ("Подбор заклёпки", "Длина — по зоне зажима: панель + профиль.", "ПО СИСТЕМЕ"),
              ("Вентзазор", "Непрерывный от цоколя до парапета.", "ПО РАСЧЁТУ"),
              ("EPDM-лента", "На все полки профилей под панелями.", ""),
              ("Подкраска", "Повреждения головок — лак-карандашем в цвет.", ""),
              ("Защитная плёнка", "Снимать сразу после монтажа панели.", "")])
      + band(V + "macro_rivet.png", 600, "Вертикальный стык: T-профиль, EPDM-лента, заклёпки обеих панелей"), "Заклёпочная система", anchor="rivet.8")
result(V + "b_rivet.png", "Заклёпочный<br>фасад", "Панели 1220 × 3050 мм, заклёпки в цвет панели. Ровный ритм крепежа — часть архитектуры.")

# =================================================================== GLUE SYSTEM
divider("glue", "Клеевая<br>система", V + "bw_glue.png",
        "Панель приклеивается к алюминиевой подсистеме фасадным клеевым комплектом. Лицевая сторона полностью чистая — ни одного видимого элемента крепления.",
        "Современная архитектура, крупные однотонные плоскости, объекты с высокими требованиями к эстетике.",
        "Двусторонняя лента мгновенно фиксирует панель, клей набирает прочность и становится несущим соединением.",
        "Активатор / очиститель · праймер · двусторонняя лента · клей (колбаса или картридж).",
        ["Конструкция", "Компоненты", "Принцип работы", "Основные узлы", "Подготовка HPL", "Монтаж", "Инструменты", "Рекомендации"])
gk = ["wall", "pad", "bracket", "anchor", "ins", "dowel", "mem", "lprof", "tprof", "prof_rivet", "primer", "epdm", "tape", "bead", "panel"]
b.add(title("Конструкция", "Клеевая система", "Нумерация — от стены к панели.")
      + cfig('expl_glue', gk)
      + legend3([("Несущая стена", ""), ("Паронитовая прокладка", "под кронштейн"), ("Кронштейн", ""), ("Анкерный болт", "кронштейн → стена"),
                ("Базальтовый утеплитель", ""), ("Тарельчатый дюбель", ""), ("Ветрозащитная мембрана", ""), ("L-профиль", "на поле панели"),
                ("T-профиль", "на стыке"), ("Заклёпка профиль — кронштейн", ""), ("Активатор + праймер", "зоны склейки профиля"),
                ("EPDM-лента", "в зоне шва"), ("Двусторонняя лента", "временная фиксация"), ("Клеевой валик", "постоянное соединение"), ("HPL-панель", "1220 × 3050 мм")]),
      "Клеевая система", anchor="glue.1")
gcomps = [(MB + "adh_bag.jpg", "Клей (колбаса)", "Чёрный, 600 мл — ок. 13,3 п. м валика. Постоянное соединение.", "MBE Panel-loc"),
          (MB + "adh_cart.jpg", "Клей (картридж)", "Чёрный, 290 мл — ок. 6,4 п. м валика.", "MBE Panel-loc"),
          (MB + "foam_tape.jpg", "Двусторонняя лента", "Вспененная 12 × 3 мм, рулон 25 м. Мгновенная фиксация панели.", "временная фиксация"),
          (MB + "primer_close.jpg", "Праймер (прозрачный)", "Тыльная сторона панели и профиль при натуральном шве.", "праймер"),
          (MB + "primer_alu.jpg", "Праймер Alu (чёрный)", "Обработка алюминиевого профиля при чёрном шве.", "праймер"),
          (MB + "cleaner.jpg", "Очиститель / активатор", "Очистка и обезжиривание, удаление пыли и свежего клея.", "активатор")]
b.add(title("Компоненты системы", "Клеевая система", "Только компоненты одной системы — клей, праймер, лента и очиститель одного производителя.")
      + f'<div style="margin-top:30px">{bg(MB + "glue_kit.jpg", 320, "center", "background-size:contain;background-repeat:no-repeat")}</div>'
      + '<div class="g3" style="margin-top:20px;gap:14px">' + "".join(toolcard(s, n, d, m, 120) for s, n, d, m in gcomps) + '</div>'
      + '<div class="note">Система MBE Panel-loc имеет строительный допуск Z-10.8-350. Совместимость с конкретной панелью и профилем — подтверждать до начала работ.</div>',
      "Клеевая система", anchor="glue.2")
b.add(title("Принцип работы", "Клеевая система", "Два слоя — две задачи: лента держит сразу, клей держит навсегда.")
      + f'<div class="fig" style="margin-top:30px">{glue_section(936, 560)}</div>'
      + '<div class="g2" style="margin-top:34px;gap:30px 40px">'
      + item("tape", "Временная фиксация", "Двусторонняя лента удерживает панель в проектном положении, пока клей набирает прочность.")
      + item("glue", "Постоянное соединение", "Треугольный клеевой валик — несущий шов; эластичный клей компенсирует температурное движение.")
      + item("primer", "Адгезия", "Шлифовка, очистка и праймер на панели и профиле — основа надёжной склейки.")
      + item("thermo", "Условия", "Температура и влажность — строго по инструкции; фиксируются в журнале.") + '</div>'
      + band(V + "wall_glue.png", 380, "Результат: на лицевой стороне нет крепежа"),
      "Клеевая система", anchor="glue.3")
nodes_page("glue", "Клеевая система", "glue", ["outer_corner", "inner_corner", "window_reveal", "window_head", "base", "parapet", "hjoint", "vjoint"])
b.add(title("Подготовка HPL", "Клеевая система", "Панель обрабатывается полностью до того, как клей наносится на профиль.")
      + f'<div class="fig" style="margin-top:34px">{glue_prep()}</div>'
      + '<div class="warn" style="margin-top:20px"><b>Важно:</b> к моменту нанесения клеевого валика на профиль тыльная сторона HPL уже должна быть отшлифована, очищена и обработана праймером — клей наносится непосредственно перед установкой панели.</div>'
      + steps([("Разметка положения панели", "По раскладке фасада, номер панели.", "i:mark"), ("Разметка профилей", "Линии профилей на тыльной стороне.", "i:layout"),
               ("Шлифование", "Зоны контакта — шлифовальная бумага P220.", "i:sand"), ("Очистка", "Безворсовая салфетка + очиститель.", "i:clean"),
               ("Праймер", "Только в зонах контакта; выдержка по инструкции.", "i:primer")]),
      "Клеевая система", anchor="glue.5")
b.add(title("Монтаж", "Клеевая система", "Подготовленная панель устанавливается на подготовленные профили.")
      + steps([("Подготовка профиля", "Шлифовка Scotch-Brite, очистка, активатор / праймер.", "i:sand"),
               ("Выдержка", "Время испарения праймера — по инструкции.", "i:clock"),
               ("Двусторонняя лента", "Вдоль профиля, без натяжения; плёнку не снимать до установки.", "i:tape"),
               ("Клеевой валик", "Треугольный валик параллельно ленте, непрерывно.", "i:glue"),
               ("Установка панели", "Снять плёнку ленты, выставить по разметке в пределах открытого времени клея.", "i:install"),
               ("Прижим", "Прижать по линиям профилей до контакта с лентой.", "i:press"),
               ("Отверждение", "Не нагружать соединение до набора прочности.", "i:clock"),
               ("Журнал", "Температура, влажность, партии материалов.", "i:doc")])
      + band(V + "sys_glue.png", 560, "Лента и клеевой валик на подготовленных профилях; панель 1220 × 3050 мм", "contain"), "Клеевая система", anchor="glue.6")
b.add(title("Инструменты", "Клеевая система")
      + '<div class="g3" style="margin-top:34px;gap:14px">'
      + toolcard(MB + "glue_kit.jpg", "Комплект Panel-loc", "Клей, праймеры, очиститель, лента, аппликаторы.", "MBE", 120)
      + tile(ic("glue", 90), "Аккумуляторный пистолет", "Для картриджей 290 мл и колбас 600 мл, регулировка скорости.", "нанесение клея", 120)
      + tile(ic("primer", 90), "Аппликаторы для праймера", "Ручка, ванночка, сменные подушки / валики.", "праймер", 120)
      + tile(ic("thermo", 90), "Термогигрометр", "Контроль температуры и влажности воздуха.", "условия", 120)
      + tile(ic("thermo", 90), "ИК-термометр", "Температура поверхности панели и профиля, точка росы.", "условия", 120)
      + tile(ic("sand", 90), "Абразив", "Scotch-Brite Very Fine — профиль; бумага P220 — панель.", "шлифовка", 120)
      + toolcard(TL + "festool_ts55.jpg", "Погружная пила + шина", "Раскрой панелей.", "раскрой", 110)
      + tile(ic("clean", 90), "Безворсовые салфетки", "Очистка зон склейки.", "очистка", 120)
      + toolcard(TL + "clamp.jpg", "Струбцины", "Временная фиксация при подготовке.", "фиксация", 120)
      + '</div>' + band(V + "macro_glue.png", 470, "Вертикальный стык: панели на T-профиле — лента и клей скрыты за панелью"), "Клеевая система", anchor="glue.7")
b.add(title("Рекомендации UZHPL", "Клеевая система")
      + recs([("Только одна система", "Клей, праймер, очиститель и лента — одного производителя.", ""),
              ("Совместимость", "Проверить для конкретной панели и профиля.", ""),
              ("Условия нанесения", "Температура и влажность — строго по инструкции.", "ПО ИНСТРУКЦИИ"),
              ("Сначала панель", "HPL подготовлен до нанесения клея на профиль.", ""),
              ("Время выдержки", "Праймер — время испарения; клей — открытое время.", "ПО ИНСТРУКЦИИ"),
              ("Геометрия валика", "Треугольный, непрерывный; размер — по системе.", "ПО СИСТЕМЕ"),
              ("Пробная адгезия", "Тест на объекте перед началом работ.", ""),
              ("Защита", "От дождя и прямого солнца во время работ.", ""),
              ("Журнал", "Условия и партии материалов — для гарантии.", "")])
      + band(V + "expl_glue.png", 600, "Состав клеевой системы: профиль с праймером, лента, клеевой валик, панель", "cover", "center 70%"), "Клеевая система", anchor="glue.8")
result(V + "b_glue.png", "Клеевой<br>фасад", "Монолитная плоскость без видимого крепежа — фасад читается как единая поверхность.")

# =================================================================== HIDDEN SYSTEM
divider("hidden", "Скрытая<br>система", V + "bw_hidden.png",
        "Панель с тыльной обработкой навешивается на горизонтальные направляющие через кляммеры (клипсы). Принцип — как в скрытой механической системе Trespa: анкер с подрезкой в тыльной стороне панели + кляммер.",
        "Премиальные фасады, сложная архитектура, объекты, где панель должна сниматься без следов.",
        "Кляммеры закреплены на панели и навешиваются сверху на направляющую; регулировочный винт выставляет плоскость.",
        "Кляммер (клипса) на анкере с подрезкой в тыльной стороне панели → горизонтальная направляющая.",
        ["Конструкция", "Принцип навески", "Основные узлы", "Монтаж"])
hk = ["wall", "pad", "bracket", "anchor", "ins", "dowel", "mem", "lprof", "tprof", "prof_rivet", "rail", "clip", "panel"]
b.add(title("Конструкция", "Скрытая система")
      + cfig('expl_hidden', hk)
      + legend3([("Несущая стена", ""), ("Паронитовая прокладка", ""), ("Кронштейн", ""), ("Анкерный болт", ""), ("Утеплитель", ""),
                ("Тарельчатый дюбель", ""), ("Ветрозащитная мембрана", ""), ("Вертикальный профиль", ""), ("Вертикальный профиль на стыке", ""),
                ("Заклёпка профиль — кронштейн", ""), ("Горизонтальная направляющая", "крепится к вертикальным профилям"),
                ("Кляммер (клипса)", "на тыльной стороне панели"), ("HPL-панель", "с тыльной обработкой")]), "Скрытая система", anchor="hidden.1")
b.add(title("Принцип навески", "Скрытая система", "Кляммер закреплён анкером с подрезкой в тыльной стороне панели и навешивается сверху на направляющую.")
      + f'<div style="display:grid;grid-template-columns:330px 1fr;gap:30px;margin-top:30px"><div>{panel_layout("hidden", 330, 760)}</div>'
      + f'<div>{hidden_principle(936, 620)}</div></div>'
      + '<div class="g2" style="margin-top:30px;gap:28px 40px">'
      + item("clip", "Кляммер (клипса)", "Алюминиевый зацеп; положение и количество — по системе и расчёту.")
      + item("cnc", "Тыльная обработка", "Отверстия под анкеры с подрезкой — на ЧПУ, глубина по системе.")
      + item("level", "Регулировка", "Регулировочный винт кляммера выставляет панель в плоскость.")
      + item("sleeve", "Фиксация", "Одна точка фиксируется от смещения; остальные свободно скользят по направляющей.") + '</div>'
      + '<div class="note">Остаточная толщина панели, глубина отверстия и тип анкера — строго по инструкции системы. Обработка выполняется на ЧПУ в цехе UZHPL.</div>',
      "Скрытая система", anchor="hidden.2")
nodes_page("hidden", "Скрытая система", "hidden", ["outer_corner", "inner_corner", "window_reveal", "window_head", "base", "parapet", "hjoint", "vjoint"])
b.anchors["hidden.3"] = b.anchors.pop("hidden.4")
b.add(title("Монтаж", "Скрытая система")
      + steps([("Разметка и кронштейны", "Оси, паронит, кронштейны, анкерные болты.", "i:bracket"),
               ("Утеплитель и мембрана", "Утеплитель на дюбелях, мембрана.", "i:insulation"),
               ("Вертикальные профили", "Выставить в плоскость, закрепить заклёпками.", "i:profile"),
               ("Горизонтальные направляющие", "По отметкам, строго горизонтально.", "i:level"),
               ("Обработка панелей на ЧПУ", "Отверстия под анкеры с подрезкой на тыльной стороне.", "i:cnc"),
               ("Кляммеры на панель", "Анкеры + кляммеры по монтажной карте.", "i:clip"),
               ("Навеска панели", "Сверху вниз на направляющую.", "i:install"),
               ("Регулировка и фиксация", "Плоскость, швы, точка фиксации.", "i:check")])
      + band(V + "sys_hidden.png", 680, "Горизонтальные направляющие и кляммеры на тыльной стороне панели 1220 × 3050 мм", "contain"), "Скрытая система", anchor="hidden.4")

# =================================================================== SCREW SYSTEM
divider("screw", "Винтовая<br>система", V + "bw_screw.png",
        "Подсистема — как у заклёпочной системы; панель крепится фасадными винтами с окрашенной головкой. Видимый механический крепёж, простая замена панели.",
        "Объекты, где важна ремонтопригодность; фасады на деревянной подсистеме; балконные ограждения.",
        "Как и с заклёпками: одна фиксированная точка, остальные — скользящие. Винт не перетягивается.",
        "Фасадный винт с окрашенной головкой (Ø12–16 мм) или балконный винт M5 с гайкой.",
        ["Конструкция", "Компоненты и крепёжный узел", "Узлы и монтаж"])
sk = ["wall", "pad", "bracket", "anchor", "ins", "dowel", "mem", "lprof", "tprof", "prof_rivet", "epdm", "panel", "fastener"]
b.add(title("Конструкция", "Винтовая система")
      + cfig('expl_screw', sk)
      + legend3([("Несущая стена", ""), ("Паронитовая прокладка", ""), ("Кронштейн", ""), ("Анкерный болт", ""), ("Утеплитель", ""),
                ("Тарельчатый дюбель", ""), ("Ветрозащитная мембрана", ""), ("L-профиль", ""), ("T-профиль", "на стыке"),
                ("Заклёпка профиль — кронштейн", ""), ("EPDM-лента", ""), ("HPL-панель", "1220 × 3050 мм"), ("Фасадный винт", "в цвет панели")]),
      "Винтовая система", anchor="screw.1")
b.add(title("Компоненты<br>и крепёжный узел", "Винтовая система")
      + f'<div class="fig" style="margin-top:30px">{screw_detail(936, 520)}</div>'
      + '<div class="g3" style="margin-top:24px;gap:14px">'
      + toolcard(MB + "screw_painted.jpg", "Фасадный винт", "Нерж. сталь A2 / A4, привод ISR 20, головка Ø12–16 мм в цвет панели. Для деревянной подсистемы: 4,8 × 38 … 5,5 × 65 мм.", "MBE")
      + toolcard(MB + "balcony.jpg", "Балконный винт M5", "С колпачковой гайкой или резьбовой втулкой — для алюминиевой и стальной подсистемы. Момент затяжки 2–4 Н·м.", "MBE")
      + toolcard(MB + "fix_sleeve.jpg", "Гильза фикс. точки", "Одна фиксированная точка на панель.", "фикс. точка", 110)
      + '</div>'
      + '<div class="warn" style="margin-top:20px">Монтаж без зажима: как только головка винта села на панель — остановить завинчивание, без дополнительного момента. Не заменять фасадный крепёж обычными саморезами.</div>'
      + band(V + "macro_screw.png", 380, "Фасадные винты у вертикального стыка", mt=24),
      "Винтовая система", anchor="screw.2")
b.add(title("Узлы и монтаж", "Винтовая система") + '<div class="g2" style="margin-top:30px;gap:16px">'
      + "".join(f'<div>{node(k, 900, 720, "screw")}</div>' for k in ["outer_corner", "vjoint"]) + '</div>'
      + steps([("Подсистема", "Как у заклёпочной системы: паронит, кронштейны, утеплитель, мембрана, L/T-профили, EPDM.", "i:profile"),
               ("Отверстия в панели", "Фиксированная точка — с гильзой, скользящие — увеличенные.", "i:drillbit"),
               ("Отверстия в профиле", "Через панель, по центру — кондуктором.", "i:drill"),
               ("Крепление", "Сначала фикс. точка, затем скользящие; без перетяжки.", "i:screw"),
               ("Контроль", "Плоскость, швы, свобода движения панели.", "i:check")])
      + band(V + "wall_screw.png", 380, "Винтовой фасад: головки винтов в цвет панели"), "Винтовая система", anchor="screw.3")

# =================================================================== FACADE NODES
rows = "".join(f'<a href="#a-nodes.{i + 1}"><span>{n}</span><span>{{{{pg:nodes.{i + 1}}}}}</span></a>' for i, (_, n, _) in enumerate(node_pages))
b.add(f'<div style="margin-top:120px">{title("Фасадные<br>узлы", "Раздел", "Отдельная страница на каждый узел: разрез, 3D-вид и данные проекта. Показано для заклёпочной системы.")}'
      f'<div class="toc" style="margin-top:56px;border-top:1px solid #34373c">{rows}</div></div>', "Фасадные узлы", dark=True, anchor="nodes")
for i, (k, n, pts) in enumerate(node_pages):
    b.add(title(n, "Фасадный узел") + f'<div class="fig" style="margin-top:34px">{node(k, 900, 720, "rivet")}</div>'
          + f'<div style="display:grid;grid-template-columns:1.1fr 1fr;gap:36px;margin-top:30px"><div style="background:{XL};padding:18px">'
          + f'<div class="cap" style="margin:0">3D-ВИД УЗЛА</div><div style="height:600px;margin-top:8px"><img src="img/{N3D[k]}.png" style="width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply"></div></div>'
          + '<div><h3>Ключевые элементы</h3>' + "".join(f'<div class="li" style="grid-template-columns:36px 1fr"><span class="badge">{j + 1}</span><h4>{t}</h4></div>' for j, t in enumerate(pts))
          + '<h3 style="margin-top:30px">Данные проекта</h3>' + "".join(f'<div class="spec" style="font-size:15px"><span>{a}</span><span class="pill">{c}</span></div>'
                                                                         for a, c in [("Шаг крепления", "ПО РАСЧЁТУ"), ("Ширина швов", P), ("Вентзазор", "ПО РАСЧЁТУ"), ("Фактические размеры", "НА ОБЪЕКТЕ")])
          + '</div></div>', "Фасадные узлы", anchor=f"nodes.{i + 1}")

# =================================================================== INTERIOR
apps = [("Стены", "F-35"), ("Потолки", "F-38"), ("Мебель", "F-54"), ("Перегородки", "F-12"), ("Санузлы", "F-24"), ("Рецепции", "F-32"), ("Декор. панели", "F-72"), ("Лаборатории", "F-20")]
methods = [("glue", "Клеевой", "На ровное подготовленное основание (ГКЛ, бетон, фанера) — монтажный клей по системе."),
           ("screw", "Механический", "На металлический или деревянный каркас — винты / заклёпки с компенсационными отверстиями."),
           ("clip", "Скрытый", "Клипсы, кляммеры или подвесные профили — панель снимается без следов."),
           ("cnc", "Мебельная обработка", "Раскрой, кромки, фрезеровка под фурнитуру на ЧПУ.")]
b.add(title("Интерьерные<br>системы", "Интерьер", "HPL в интерьере: стойкость к влаге, ударам и химии. Решение подбирается отдельно от фасада.")
      + '<div class="g4" style="margin-top:36px;gap:12px">' + "".join(
          f'<div><div class="photo" style="height:150px;background-image:url(img/decor/{d}.jpg)"></div><div style="font-size:15px;font-weight:600;margin-top:8px">{a}</div></div>' for a, d in apps) + '</div>'
      + '<div class="hr"></div><h3>Способы монтажа</h3><div class="g2" style="gap:26px 40px">' + "".join(item(i, a, d) for i, a, d in methods) + '</div>'
      + '<div class="hr"></div><h3>Правила установки</h3><div class="g2" style="gap:0 40px">' + "".join(
          f'<div class="spec" style="font-size:15px;grid-template-columns:1fr"><span>{t}</span></div>' for t in [
              "Компенсационные зазоры по периметру и в стыках — ПО ПРОЕКТУ", "Панель не зажимается жёстко: отверстия больше крепежа",
              "Основание ровное и сухое; во влажных зонах — вентилируемый зазор", "Кромки обработаны: фаска или радиус",
              "Крепёж — нержавеющий во влажных помещениях", "Защитная плёнка снимается после монтажа"]) + '</div>',
      "Интерьер", anchor="interior")
b.add(title("Стыки и углы", "Интерьер", "HPL обрабатывается как массив: стыки и углы можно решить без профилей или с декоративными элементами.")
      + '<div class="g2" style="margin-top:34px;gap:16px">' + "".join(f'<div>{ijoint(k)}</div>' for k in ["tongue", "gasket", "hprof", "shadow", "miter", "corner", "open", "edge"]) + '</div>'
      + '<div class="note">Шпунт / паз — HPL фрезеруется и одна панель заходит в другую. Угол 45° — усовка на ЧПУ. Резиновый уплотнитель или декоративный профиль закрывают шов и компенсируют движение.</div>',
      "Интерьер")
b.add(title("Интерьерные узлы", "Интерьер") + '<div class="g2" style="margin-top:34px;gap:16px">'
      + "".join(interior_node(k) for k in ["in_corner", "out_corner", "joint", "ceiling", "floor", "door", "furniture", "wall_junction"]) + '</div>'
      + '<div class="note">Компенсационные зазоры и шаг крепления в интерьере — ПО ПРОЕКТУ и инструкции производителя панели.</div>', "Интерьер")

# =================================================================== TOOLS UZHPL
b.add(title("Инструменты<br>UZHPL", "Инструменты", "Профессиональный инструмент и оснастка, которыми работают наши бригады.")
      + '<h3 style="margin-top:36px">Раскрой и обработка</h3><div class="g3" style="gap:14px">'
      + toolcard(TL + "festool_ts55.jpg", "Погружная пила Festool TS 55", "Раскрой HPL с направляющей шиной, твердосплавный диск.", "раскрой", 120)
      + toolcard(TL + "guide_rail.jpg", "Направляющая шина", "Прямой рез без сколов по всей длине листа 3050 мм.", "раскрой", 120)
      + toolcard(TL + "mafell_kss40.jpg", "Mafell KSS 40", "Аккумуляторная торцовочная пила на шине — точный рез на объекте.", "раскрой", 120)
      + '</div><h3 style="margin-top:30px">Заклёпки и сверление (MBE / Trespa)</h3><div class="g3" style="gap:14px">'
      + toolcard(MB + "accubird_pro.jpg", "AccuBird PRO", "18 В, 10 000 Н, ход 25 мм.", "заклёпочник", 120)
      + toolcard(MB + "mouth_g3.jpg", "Наконечники G3 / G7 / G10", "G3 — Al-заклёпки Ø5 / головка 16; G7 — нерж.; G10 — с большой шайбой.", "без зажима", 110)
      + toolcard(MB + "spring_jig.jpg", "Кондукторы", "Пружинный 5,1 / 10 и скобовый — центровка отверстий.", "перенос отверстий", 110)
      + '</div><h3 style="margin-top:30px">Подсистема и монтаж</h3><div class="g4" style="gap:12px">'
      + toolcard(TL + "m_hammer.jpg", "Перфоратор", "Под анкеры.", "", 100)
      + toolcard(TL + "m_drill.jpg", "Дрель-шуруповёрт", "Сверление, крепёж.", "", 100)
      + toolcard(TL + "m_grinder.jpg", "УШМ", "Резка профилей.", "", 100)
      + toolcard(TL + "clamp.jpg", "Струбцины", "Фиксация.", "", 100)
      + '</div><h3 style="margin-top:30px">Сверление и финиш</h3><div class="g4" style="gap:12px">'
      + toolcard(MB + "vhm_drill.jpg", "Сверло VHM", "Ø8 / 10 / 13 мм для HPL.", "", 70)
      + toolcard(MB + "hss_drill.jpg", "Сверло HSS Ø5,1", "Для алюминия.", "", 100)
      + toolcard(TL + "m_jigsaw.jpg", "Лобзик", "Вырезы по месту.", "", 100)
      + toolcard(MB + "paint_pen.jpg", "Лак-карандаш", "Подкраска головок.", "", 100)
      + '</div>', "Инструменты", anchor="tools")

# =================================================================== QC / SUPERVISION
qc = [("Подсистема", "Кронштейны, анкеры, паронит, плоскость профилей"), ("Утеплитель и мембрана", "Без щелей, дюбели, нахлёсты"),
      ("Геометрия", "Раскладка и размеры панелей по проекту"), ("Плоскость", "Отклонения — в допусках проекта"),
      ("Швы", "Равномерная ширина, прямолинейность"), ("Крепёж", "Тип, длина, фикс. / скользящие точки"),
      ("Клеевые работы", "Условия, журнал, отверждение"), ("Поверхность", "Без сколов и царапин; плёнка снята"),
      ("Вентиляция", "Входы и выходы воздуха открыты"), ("Документация", "Фотоотчёт каждого этапа, акт")]
b.add(title("Технадзор<br>и контроль качества", "Качество", "Контроль выполняют наши специалисты из Германии.")
      + '<div class="g2" style="margin-top:40px;gap:20px">'
      + f'<div class="tile" style="padding:30px">{ic("germany", 56)}<h4 style="font-size:22px;margin-top:16px">При монтаже UZHPL</h4><p style="font-size:15.5px">Технадзор включён: немецкие специалисты контролируют каждый этап — от разметки до сдачи объекта.</p></div>'
      + f'<div class="tile" style="padding:30px;background:{GR};color:#fff">{ic("supervision", 56, "#fff")}<h4 style="font-size:22px;margin-top:16px">Технадзор как услуга</h4><p style="font-size:15.5px;color:#b9bdc2">Если монтаж выполняет другой подрядчик — предоставляем технический надзор отдельно.</p></div></div>'
      + '<div class="g2" style="margin-top:34px;gap:0 40px">' + "".join(
          f'<div class="li" style="grid-template-columns:36px 1fr"><span style="width:22px;height:22px;border:2px solid {GR};position:relative;margin-top:4px;display:block">'
          f'<span style="position:absolute;left:5px;top:0;width:6px;height:12px;border:solid {OR};border-width:0 3px 3px 0;transform:rotate(45deg)"></span></span>'
          f'<div><h4>{a}</h4><p>{d}</p></div></div>' for a, d in qc) + '</div>'
      + band(V + "bw_rivet.png", 470, "Приёмка: плоскость, швы и крепёж проверяются по каждой панели"), "Качество", anchor="qc")

# =================================================================== RECOMMENDATIONS
b.add(title("Рекомендации UZHPL", "Рекомендации", "Короткие инженерные правила для всех систем.")
      + recs([("Проект прежде монтажа", "Расчёт подсистемы и ветровых нагрузок — до начала работ.", "ПО РАСЧЁТУ"),
              ("Одна система", "Панель, профили, крепёж и клей — подтверждённые системой.", ""),
              ("Фиксированная и скользящие точки", "Не зажимать панель жёстко.", ""),
              ("Вентзазор", "Непрерывный, входы и выходы открыты.", "ПО РАСЧЁТУ"),
              ("Отступы от кромок", "Не менять без разрешения производителя.", "ПО ИНСТРУКЦИИ"),
              ("Терморазрыв", "Паронит под каждым кронштейном.", ""),
              ("Крепёж", "Только фасадный; проверить контактную коррозию.", ""),
              ("Температура", "Учитывать при монтаже швов и клеевых работах.", "ПО ИНСТРУКЦИИ"),
              ("Документация", "Журнал работ и фотоотчёт.", "")])
      + band(V + "b_dusk.png", 640, "", "cover", "center 40%"), "Рекомендации", anchor="recs")

# =================================================================== START A PROJECT
qr = open(os.path.join(HERE, "img", "qr.svg")).read()
qr = qr[qr.index("<svg"):]
cta = [("phone", "Заявка", "Звонок или сообщение менеджеру"), ("doc", "Исходные данные", "Фасады или фото объекта, площадь, адрес, сроки"),
       ("material", "Подбор решения", "Система крепления, декор, образцы панелей"), ("engineering", "Расчёт и КП", "Подсистема, раскрой, комплектация, монтаж"),
       ("processing", "Производство", "Раскрой и обработка HPL, комплектная поставка"), ("montage", "Монтаж и технадзор", "Монтаж, контроль, фотоотчёт, сдача")]
cgrid = '<div class="g3" style="margin-top:40px;gap:0">' + "".join(
    f'<div style="padding:28px 24px 28px 0;border-top:1px solid {LG}">{ic(n, 44)}<div style="font-size:13px;color:{OR};font-weight:600;letter-spacing:.14em;margin-top:16px">{i + 1:02d}</div>'
    f'<div style="font-size:20px;font-weight:600;margin-top:4px">{a}</div><div style="font-size:14.5px;color:{DG};margin-top:6px;line-height:1.45">{d}</div></div>' for i, (n, a, d) in enumerate(cta)) + '</div>'
b.add(title("Как начать<br>проект", "Контакты", "Шесть шагов от запроса до готового фасада.") + cgrid
      + f'<div style="margin-top:46px;display:grid;grid-template-columns:1fr 300px;background:{GR};color:#fff">'
      + f'<div style="padding:44px"><div class="kick">Свяжитесь с нами</div><div style="font-size:42px;font-weight:700;margin-top:16px;line-height:1.2">+998 77 003 28 82<br>+998 78 122 31 51</div>'
      + f'<div style="font-size:20px;margin-top:20px;color:#c9ccd0">info@uzhpl.uz · sales@uzhpl.uz</div>'
      + f'<div style="font-size:15px;color:#8a9097;margin-top:20px;line-height:1.6">Для быстрого расчёта пришлите: фасады или фото объекта, площадь облицовки, желаемый декор, адрес и сроки.</div></div>'
      + f'<div style="background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:28px"><div style="width:220px">{qr}</div>'
      + f'<div style="color:{GR};font-size:13px;font-weight:700;letter-spacing:.2em;margin-top:12px">UZHPL.UZ</div></div></div>'
      + '<h3 style="margin-top:50px">Что вы получаете</h3><div class="g3" style="gap:30px">'
      + item("layout", "Техническое решение", "Система крепления, узлы, раскладка панелей 1220 × 3050 мм.")
      + item("material", "Образцы декоров", "Подбор декора и толщины по каталогу UZHPL; образцы в шоуруме.")
      + item("doc", "Коммерческое предложение", "Панели, подсистема, обработка, монтаж и технадзор — в одном КП.") + '</div>'
      + band(V + "bw_hidden.png", 300, "", "cover", "center 35%", 44), "Контакты", anchor="start")

# =================================================================== LAST PAGE
last = (f'<div style="position:absolute;inset:0">{bg("img/brand/facade3d_b.jpg", 1920)}</div>'
        f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(29,31,34,.2) 0%,rgba(29,31,34,.1) 40%,rgba(29,31,34,.94) 70%)"></div>'
        f'<div style="position:absolute;left:84px;top:84px"><img src="img/brand/logo_white.png" style="height:52px"></div>'
        f'<div style="position:absolute;left:84px;right:84px;bottom:110px;color:#fff">'
        f'<div style="font-size:44px;font-weight:700;line-height:1.1;text-transform:uppercase">HPL-решения<br>для архитектуры</div>'
        f'<div class="g3" style="margin-top:46px;gap:30px;border-top:1px solid rgba(255,255,255,.2);padding-top:30px">'
        f'<div><div class="kick" style="font-size:11px">Офис и шоурум</div><div style="font-size:16px;line-height:1.6;margin-top:10px;color:#d4d6d9">Узбекистан, Ташкент,<br>Мирзо-Улугбекский район,<br>ул. Паркент, 235</div></div>'
        f'<div><div class="kick" style="font-size:11px">Телефоны</div><div style="font-size:16px;line-height:1.6;margin-top:10px;color:#d4d6d9">+998 77 003 28 82<br>+998 78 122 31 51</div></div>'
        f'<div><div class="kick" style="font-size:11px">Почта и сайт</div><div style="font-size:16px;line-height:1.6;margin-top:10px;color:#d4d6d9">info@uzhpl.uz<br>sales@uzhpl.uz<br>uzhpl.uz</div></div></div>'
        f'<div style="font-size:13px;color:#8a9097;margin-top:30px">Образцы декоров, расчёт проектов и доставка по Узбекистану и СНГ.</div></div>')
b.add(last, bare=True, cls="dark")

open(os.path.join(HERE, "uzhpl-catalog.html"), "w").write(b.html())
print(len(b.pages), "pages")
