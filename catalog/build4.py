# -*- coding: utf-8 -*-
"""UZHPL technical catalog v4 -> uzhpl-catalog.html

v2 structure and illustrations (exploded assemblies, bold principle drawings, picture-per-step montage,
component and tool cards) + all v3 content (35-point review), light theme, strict grid."""
import os
from page4 import Book, title, OR, GR, DG, MG, LG, XL
from icons import icon
from draw import mini
from draw4 import callout_svg, exploded2, panel_scheme
from drawings2 import formats_svg, ijoint
from sections import (node, principle_section, rivet_detail, panel_processing, hidden_principle, glue_section,
                      screw_detail, interior_node)
from lib import svg

HERE = os.path.dirname(os.path.abspath(__file__))
b = Book()
P = "ПО ПРОЕКТУ"
V, MB, TL = "img/v2/", "img/mbe/", "img/tools/"


# ------------------------------------------------------------------ visuals
def vis(k, h=104):
    """'p:path' photo/render · 'c:x' component render · 't:x' tool render · 'm:x' v2 vignette · 'i:x' line icon"""
    t, v = k[:1], k[2:]
    if t == "m":
        return f'<div style="width:100%;height:{h}px">{mini(v)}</div>'
    if t == "i":
        return icon(v, 64)
    src = {"p": v, "c": f"img/c_{v}.png", "t": f"img/t_{v}.png"}[t]
    return f'<img src="{src}" alt="">'


def card(k, name, desc="", meta="", n=None, h=150, f=False, span=1, cls=""):
    no = f'<span class="no badge">{n}</span>' if n else ""
    m = f'<div class="meta">{meta}</div>' if meta else ""
    st = f' style="grid-column:span {span}"' if span > 1 else ""
    return (f'<div class="card{" f" if f else ""} {cls}"{st}>{no}<div class="im" style="height:{h}px">{vis(k, h)}</div>'
            f'<h4>{name}</h4>{f"<p>{desc}</p>" if desc else ""}{m}</div>')


def steps(lst, compact=False):
    return (f'<div class="steps{" c" if compact else ""}">' + "".join(
        f'<div class="step"><div class="sn">{i + 1:02d}</div><div class="si">{vis(k)}</div><div><h4>{a}</h4><p>{d}</p></div></div>'
        for i, (a, d, k) in enumerate(lst)) + '</div>')


def recs(lst):
    return '<div>' + "".join(
        f'<div class="rec"><div class="rn">{i + 1:02d}</div><div><h4>{a}</h4><p>{d}</p></div>'
        f'<div>{f"<span class=pill>{p}</span>" if p else ""}</div></div>' for i, (a, d, p) in enumerate(lst)) + '</div>'


def legend(items, cols=3):
    return (f'<div class="lg" style="grid-template-columns:repeat({cols},1fr);margin-top:8px">' + "".join(
        f'<div class="li"><span class="badge">{i + 1}</span><div><h4>{a}</h4>{f"<p>{d}</p>" if d else ""}</div></div>'
        for i, (a, d) in enumerate(items)) + '</div>')


def item(icn, name, desc):
    return f'<div class="it"><div>{icon(icn, 48)}</div><div><h4>{name}</h4><p>{desc}</p></div></div>'


def bg(src, h, pos="center", extra=""):
    return f'<div class="photo" style="height:{h}px;background-image:url({src});background-position:{pos};{extra}"></div>'


def construction(key, sysname, sysk, keys, leg, lead, w=830):
    b.add(title("Конструкция", sysname, lead)
          + f'<div style="width:{w}px;margin:-20px auto 10px">{callout_svg(sysk, keys)}</div>' + legend(leg),
          sysname, anchor=key)


def divider(key, name, photo, meaning, fastening, how, apply, subs):
    rows = "".join(f'<a href="#a-{key}.{i + 1}"><span>{t}</span><span>{{{{pg:{key}.{i + 1}}}}}</span></a>' for i, t in enumerate(subs))
    body = (f'<div style="position:absolute;left:0;right:0;top:0;height:800px">{bg(photo, 800)}</div>'
            f'<div style="position:absolute;left:0;right:0;top:0;height:200px;background:linear-gradient(180deg,rgba(0,0,0,.28),rgba(0,0,0,0))"></div>'
            f'<div style="margin-top:676px"><div class="kick">Система крепления</div>'
            f'<h1 style="font-size:64px">{name}</h1><div class="lead">{meaning}</div>'
            f'<div class="g3" style="margin-top:34px">'
            + "".join(f'<div style="border-top:3px solid {OR};padding-top:14px"><div style="font-size:12px;letter-spacing:.22em;font-weight:700;color:{MG};text-transform:uppercase">{h}</div>'
                      f'<div style="font-size:15.5px;line-height:1.5;margin-top:10px">{t}</div></div>'
                      for h, t in (("Крепление панели", fastening), ("Как работает", how), ("Применение", apply)))
            + f'</div><div class="toc" style="margin-top:34px;border-top:1px solid {LG}">{rows}</div></div>')
    b.add(body, name.replace("<br>", " "), cls="photo-pg", anchor=key, light_logo=True)


def result(photo, name, sub):
    body = (f'<div style="position:absolute;left:0;right:0;top:0;height:1380px">{bg(photo, 1380, "center 30%")}</div>'
            f'<div style="position:absolute;left:84px;top:64px"><img src="img/brand/logo_white.png" style="height:28px"></div>'
            f'<div style="position:absolute;left:84px;right:84px;top:1440px"><div class="kick">Готовый результат</div>'
            f'<div style="font-size:64px;font-weight:800;line-height:1.02;text-transform:uppercase;margin-top:14px;letter-spacing:-.02em">{name}</div>'
            f'<div class="lead" style="margin-top:16px">{sub}</div></div>'
            f'<div class="ft"><span>uzhpl.uz</span><span class="pg">{len(b.pages) + 1:02d}</span></div>')
    b.add(body, bare=True)


# ================================================================== COVER
b.add(f'<div style="position:absolute;inset:0">{bg(V + "cover.png", 1920)}</div>'
      f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,.94) 0%,rgba(255,255,255,.6) 30%,rgba(255,255,255,0) 52%)"></div>'
      f'<div style="position:absolute;left:84px;top:84px"><img src="img/brand/logo.png" style="height:46px" alt="UZHPL"></div>'
      f'<div style="position:absolute;left:84px;top:300px;right:84px"><div style="width:56px;height:4px;background:{OR}"></div>'
      f'<div style="font-size:66px;font-weight:800;line-height:1.02;letter-spacing:-.02em;margin-top:34px;text-transform:uppercase">Фасадные<br>и интерьерные<br>системы HPL</div>'
      f'<div style="font-size:26px;color:{DG};margin-top:26px">Технический каталог</div></div>'
      f'<div style="position:absolute;left:84px;bottom:76px;font-size:15px;letter-spacing:.14em">uzhpl.uz</div>', bare=True)

# ================================================================== CONTENTS
toc = [("about", "О компании UZHPL"), ("product", "Панель FAÇADE UZHPL"), ("formats", "Форматы и сравнение"),
       ("vent", "Как устроен вентилируемый фасад"), ("systems", "Фасадные системы"), ("choose", "Как выбрать систему"),
       ("rivet", "Заклёпочная система"), ("glue", "Клеевая система"), ("hidden", "Скрытая система"), ("screw", "Винтовая система"),
       ("nodes", "Фасадные узлы"), ("interior", "Интерьерные системы"), ("tools", "Инструменты UZHPL"),
       ("qc", "Технадзор и контроль качества"), ("recs", "Рекомендации UZHPL"), ("start", "Как начать проект")]
rows = "".join(f'<a href="#a-{k}"><span>{t}</span><span>{{{{pg:{k}}}}}</span></a>' for k, t in toc)
b.add(title("Содержание", "Каталог", "Нажмите на раздел, чтобы перейти к нему. Логотип и номер страницы ведут обратно сюда.")
      + f'<div class="toc" style="border-top:2px solid {GR}">{rows}</div>'
      + '<div class="note">Размеры, шаги и нагрузки с пометкой «ПО ПРОЕКТУ», «ПО РАСЧЁТУ» или «НА ОБЪЕКТЕ» определяются проектом фасада '
        'и инструкциями производителей панели и крепежа. Каталог не заменяет проект.</div>', "Содержание")

# ================================================================== ABOUT
chain = [("project", "Проект", "Решение под архитектурную задачу"), ("engineering", "Инженерия", "Расчёт подсистемы, раскладка, узлы"),
         ("material", "Материал", "HPL-панели и комплект подсистемы"), ("processing", "Обработка", "Раскрой, сверление, фрезерование"),
         ("logistics", "Логистика", "Комплектная поставка на объект"), ("montage", "Монтаж", "Бригады по немецкой технологии"),
         ("supervision", "Технадзор", "Контроль специалистов из Германии")]
ch = f'<div style="display:grid;grid-template-columns:repeat(7,1fr);border-top:2px solid {GR}">'
for i, (n, a, d) in enumerate(chain):
    ch += (f'<div style="padding:24px 12px 0 0;position:relative">{icon(n, 46)}'
           f'<div style="font-size:12px;color:{OR};font-weight:700;letter-spacing:.14em;margin-top:16px">{i + 1:02d}</div>'
           f'<div style="font-size:17px;font-weight:700;margin-top:4px">{a}</div><div style="font-size:13px;color:{DG};margin-top:6px;line-height:1.4">{d}</div>'
           f'<div style="position:absolute;top:-6px;left:0;width:10px;height:10px;border-radius:50%;background:{OR}"></div></div>')
ch += '</div>'
b.add(title("О компании UZHPL", "Компания", "Интегратор HPL-панелей с полным циклом: от подбора материала и инженерии до монтажа по немецкой технологии и технадзора. Один подрядчик — одна ответственность.")
      + ch + '<div class="hr" style="margin-top:44px"></div><div class="g3">'
      + item("germany", "Немецкая технология", "Монтаж по стандартам и инструкциям европейских производителей систем.")
      + item("supervision", "Технадзор из Германии", "Специалисты контролируют каждый этап — от подсистемы до сдачи.")
      + item("material", "Всё в одной поставке", "Панели, подсистема, крепёж, клеевые системы и инструмент.") + '</div>'
      + f'<div style="margin-top:44px;display:grid;grid-template-columns:1.3fr 1fr;gap:24px">{bg("img/brand/residential.jpg", 600, "center 60%")}{bg("img/brand/facade3d_a.jpg", 600)}</div>',
      "О компании", anchor="about")

# ================================================================== PRODUCT
layers = [("UV Film Grade 6", "Защита от выгорания (EN 438-2)", "#cfe0ea"), ("Deco Paper", "Декоративный слой — цвет и текстура", "#8a4a2a"),
          ("Melamine Resin", "Прочность поверхности", "#d8d2c4"), ("Kraft Paper", "Основа — задаёт толщину", "#b88a52"),
          ("Phenolic Resin", "Водостойкость и плотность", "#4a3322")]
specs = [("Плотность", "1450–1500 кг/м³"), ("Толщина фасадных панелей", "6 / 8 / 10 мм"), ("Водопоглощение", "≤ 6 %"),
         ("Светостойкость", "EN 438-2, Grade 6"), ("Пожарный класс", "B-s1, d0"), ("Экологичность", "E1 / E0"),
         ("Прочность на изгиб", "97 МПа"), ("Термостойкость", "−40 … +80 °C"), ("Срок службы", "20+ лет")]
b.add(title("Панель<br>FAÇADE UZHPL", "Продукт", "Компактная HPL-панель высокого давления с УФ-стабилизированным финишным слоем. Не требует обработки после монтажа.")
      + bg("img/brand/panels.jpg", 520, "center 45%")
      + '<div class="g2" style="margin-top:40px;gap:48px"><div><h3>Структура панели</h3>'
      + "".join(f'<div class="spec" style="grid-template-columns:30px 1fr"><span style="width:16px;height:16px;background:{c};display:block;margin-top:4px"></span>'
                f'<span><b style="color:{GR}">{a}</b><br><span style="font-size:14px;color:{MG};font-weight:400">{d}</span></span></div>' for a, d, c in layers)
      + f'<div class="cap" style="color:{OR};font-weight:700">ПРЕССОВАНИЕ 1430 PSI · 150 °C</div></div>'
      + '<div><h3>Технические параметры</h3>' + "".join(f'<div class="spec"><span>{a}</span><span>{v}</span></div>' for a, v in specs) + '</div></div>'
      + '<div class="note">Параметры — по каталогу UZHPL HPL 2026–2027, подтверждены протоколами испытаний. Копии сертификатов — по запросу.</div>',
      "Продукт", anchor="product")

# ================================================================== FORMATS
fm = [("Минимальный", "915 × 2135", "1,95"), ("Популярный", "1220 × 2800", "3,42"), ("Основной фасадный", "1220 × 3050", "3,72"), ("Максимальный", "1830 × 4270", "7,81")]
cmp = [("Вес, кг/м²", "7–12", "4–6", "25–35", "40–80"), ("Монтаж", "Простой", "Простой", "Средний", "Сложный"),
       ("Светостойкость", "Высокая", "Низкая", "Средняя", "Высокая"), ("Нагрев на солнце", "Низкий", "Сильный", "Средний", "Сильный"),
       ("Цена", "Средняя", "Низкая", "Средняя", "Высокая"), ("Ремонт", "Замена панели", "Замена кассеты", "Сложно", "Сложно"),
       ("Выбор декоров", "1000+", "RAL", "Ограничен", "Натуральный")]
th = "".join(f'<th{" class=hl" if i == 1 else ""}>{h}</th>' for i, h in enumerate(["Параметр", "HPL", "АКП", "Фиброцемент", "Камень"]))
tb = "".join("<tr>" + "".join(f'<td{" class=hl" if i == 1 else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in cmp)
b.add(title("Форматы<br>и сравнение", "Продукт", "Стандартные листы и раскрой под проект. Основной фасадный формат — 1220 × 3050 мм.")
      + '<div class="g4">' + "".join(
          f'<div class="card{" f" if "3050" in s else ""}" style="padding:20px;{"border:2px solid " + OR if "3050" in s else ""}"><div style="font-size:11.5px;letter-spacing:.16em;color:{OR if "3050" in s else MG};font-weight:700;text-transform:uppercase">{a}</div>'
          f'<div style="font-size:26px;font-weight:800;margin-top:10px">{s}</div><p>мм · {m} м²</p></div>' for a, s, m in fm) + '</div>'
      + f'<div style="margin-top:20px">{formats_svg()}</div>'
      + '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:4px;align-items:center"><span class="cap" style="margin:0 10px 0 0">ТОЛЩИНЫ, ММ</span>'
      + "".join(f'<span style="padding:7px 14px;font-size:15px;font-weight:700;border:1px solid {OR if t in ("6", "8", "10") else LG};color:{OR if t in ("6", "8", "10") else GR}">{t}</span>'
                for t in "3 4 6 8 10 12 16 18 25".split()) + '<span class="cap" style="margin:0 0 0 10px">фасад — 6 / 8 / 10</span></div>'
      + f'<div class="hr"></div><h3>HPL против альтернатив</h3><table class="t">{th}{tb}</table>'
      + '<div class="note">Данные — усреднённые по рынку фасадных материалов (каталог UZHPL HPL 2026–2027).</div>',
      "Форматы", anchor="formats")

# ================================================================== VENT FACADE
KEYS = {"rivet": ["wall", "pad", "bracket", "anchor", "ins", "dowel", "mem", "lprof", "tprof", "prof_rivet", "epdm", "panel", "fastener"],
        "glue": ["wall", "pad", "bracket", "anchor", "ins", "dowel", "mem", "lprof", "tprof", "prof_rivet", "primer", "epdm", "tape", "bead", "panel"],
        "hidden": ["wall", "pad", "bracket", "anchor", "ins", "dowel", "mem", "lprof", "tprof", "prof_rivet", "rail", "clip", "panel"],
        "screw": ["wall", "pad", "bracket", "anchor", "ins", "dowel", "mem", "lprof", "tprof", "prof_rivet", "epdm", "panel", "fastener"]}
BASE = [("Несущая стена", "основание — по проекту"), ("Паронитовая прокладка", "терморазрыв под кронштейном"), ("Кронштейн", "несущий / опорный"),
        ("Анкерный болт", "кронштейн → стена"), ("Утеплитель", "базальтовая вата"), ("Тарельчатый дюбель", "утеплитель и мембрана → стена"),
        ("Ветрозащитная мембрана", "паропроницаемая"), ("L-профиль", "на поле панели"), ("T-профиль", "на стыке панелей"),
        ("Заклёпка профиль — кронштейн", "фиксирует профиль")]
construction("vent", "Основы", "rivet", KEYS["rivet"],
             BASE + [("EPDM-лента", "на полку профиля"), ("HPL-панель", "1220 × 3050 мм"), ("Крепёж панели", "заклёпка / винт / клей / кляммер")],
             "Слои от стены наружу. Между мембраной и панелью — вентилируемый зазор (синие стрелки).")
b.pages[-1] = b.pages[-1].replace('<h1>Конструкция</h1>', '<h1>Как устроен<br>вентилируемый фасад</h1>')
b.add(title("Принцип работы", "Основы", "Воздух входит у цоколя, движется в зазоре за панелями и выходит у парапета — утеплитель остаётся сухим.")
      + f'<div style="margin-top:-12px">{principle_section(936, 860)}</div><div class="g2" style="margin-top:24px;gap:28px 40px">'
      + item("membrane", "Вентиляция", "Непрерывный зазор от цоколя до парапета; входы и выходы воздуха не перекрываются.")
      + item("insulation", "Сухой утеплитель", "Пар выходит через мембрану и уносится потоком воздуха.")
      + item("pad", "Без мостиков холода", "Паронитовая прокладка разделяет кронштейн и стену.")
      + item("layout", "Свобода движения", "Одна фиксированная точка, остальные — скользящие: панель «дышит» при нагреве.") + '</div>',
      "Основы", anchor="vent2")

# ================================================================== SYSTEMS OVERVIEW
SYS = [("rivet", "Заклёпочная", "Фасадная заклёпка Ø5, головка в цвет панели", "Видимый аккуратный ритм крепежа. Самая распространённая и ремонтопригодная система."),
       ("glue", "Клеевая", "Активатор, праймер, двусторонняя лента и клей", "Чистая плоскость: на лицевой стороне нет крепежа."),
       ("hidden", "Скрытая", "Кляммер на анкере с подрезкой в тыльной стороне", "Панель навешивается на горизонтальные направляющие. Крепёж не виден."),
       ("screw", "Винтовая", "Фасадный винт с окрашенной головкой", "Видимый механический крепёж; простая замена панели.")]
sec = {"rivet": node("vjoint", 900, 720, "rivet", " "), "glue": node("vjoint", 900, 720, "glue", " "),
       "hidden": hidden_principle(936, 620), "screw": screw_detail(936, 520)}
def expl_fill(k):
    from lib import DEFS
    return (f'<svg viewBox="190 70 556 760" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">'
            f'{DEFS}{exploded2(k)[0]}</svg>')


cards = ""
for k, n, f, d in SYS:
    cards += (f'<a href="#a-{k}" class="card" style="padding:20px"><div style="display:grid;grid-template-columns:1.15fr 1fr;gap:12px;align-items:center;height:420px">'
              f'<div style="height:400px">{expl_fill(k)}</div><div class="frame" style="padding:4px">{sec[k]}</div></div>'
              f'<h4 style="font-size:22px;margin-top:14px">{n} система</h4>'
              f'<p style="font-size:14.5px"><b style="color:{OR}">Крепление: </b>{f}</p><p>{d}</p>'
              f'<div class="meta">Подробнее — стр. {{{{pg:{k}}}}} →</div></a>')
b.add(title("Фасадные системы", "Обзор", "Подсистема у всех систем общая: кронштейны, утеплитель, мембрана, L/T-профили. Отличается только узел «панель — профиль».")
      + f'<div class="g2">{cards}</div>', "Системы", anchor="systems")

# ================================================================== CHOOSE + GALLERY
sel = [("Вид крепежа", "Заклёпки в цвет панели", "Не виден", "Не виден", "Винты в цвет панели"),
       ("Крепление панели", "Заклёпка Ø5", "Лента + клей", "Кляммер + анкер", "Фасадный винт"),
       ("Замена панели", "Просто", "Сложно", "Средне", "Просто"),
       ("Скорость монтажа", "Высокая", "Ниже: выдержка", "Средняя", "Высокая"),
       ("Подготовка панели", "Отверстия Ø10", "Шлифовка, праймер", "Фрезерование ЧПУ", "Отверстия"),
       ("Условия монтажа", "По инструкции", "Строго: t° и влажность", "По инструкции", "По инструкции"),
       ("Лучше всего для", "Большинства объектов", "Чистой архитектуры", "Премиальных фасадов", "Ремонтопригодных фасадов")]
th = "".join(f"<th>{h}</th>" for h in ["", "Заклёпочная", "Клеевая", "Скрытая", "Винтовая"])
tb = "".join("<tr>" + "".join(f'<td>{c}</td>' for c in r) + "</tr>" for r in sel)
thumbs = [("rivet", "macro_rivet", "Заклёпочная", "головки в цвет панели"), ("glue", "wall_glue", "Клеевая", "крепёж не виден"),
          ("hidden", "wall_hidden", "Скрытая", "крепёж не виден"), ("screw", "macro_screw", "Винтовая", "головки винтов")]
b.add(title("Как выбрать<br>систему", "Выбор", "Короткое сравнение для архитектора и заказчика. Окончательный выбор — по проекту, ветровым нагрузкам и бюджету.")
      + f'<table class="t">{th}{tb}</table><div class="g4" style="margin-top:40px">' + "".join(
          f'<a href="#a-{k}"><div style="height:330px;overflow:hidden"><img src="{V}{im}.png" style="width:100%;height:100%;object-fit:cover"></div>'
          f'<div style="font-size:16px;font-weight:700;margin-top:12px">{n}</div><div class="cap" style="margin-top:2px">{c}</div></a>' for k, im, n, c in thumbs) + '</div>'
      + '<div class="note">Не уверены, какую систему выбрать? Пришлите фасады и площадь — инженер UZHPL подберёт решение.</div>',
      "Выбор системы", anchor="choose")

GAL = {"rivet": [("bw_rivet", "Общий вид фасада"), ("wall_rivet_close", "Ритм заклёпок на панелях 1220 × 3050"), ("sys_rivet", "Панель на L/T-профилях"), ("macro_rivet", "Заклёпки у вертикального стыка")],
       "glue": [("bw_glue", "Общий вид фасада"), ("wall_glue", "Чистая плоскость без крепежа"), ("sys_glue", "Лента и клей на профилях"), ("macro_glue", "Стык: крепёж скрыт за панелью")],
       "hidden": [("bw_hidden", "Общий вид фасада"), ("wall_hidden", "Крепёж не виден"), ("sys_hidden", "Горизонтальные направляющие"), ("macro_hidden", "Кляммеры за панелью")],
       "screw": [("bw_screw", "Общий вид фасада"), ("wall_screw", "Головки винтов в цвет панели"), ("sys_screw", "Панель на L/T-профилях"), ("macro_screw", "Винты у вертикального стыка")]}
DESC = {"rivet": "Ровный графичный ритм окрашенных заклёпок. Жилые, общественные и промышленные здания.",
        "glue": "Монолитная плоскость без видимого крепежа. Современная архитектура, крупные однотонные плоскости.",
        "hidden": "Панели на кляммерах: фасад как цельная плоскость, панель можно снять без следов.",
        "screw": "Видимый винтовой крепёж; объекты, где важна простая замена панели."}


def gal_items(k):
    d = os.path.join(HERE, "img", "projects", k)
    real = sorted(f for f in os.listdir(d) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))) if os.path.isdir(d) else []
    items = [(f"img/projects/{k}/{f}", os.path.splitext(f)[0].split("_", 1)[-1].replace("-", " ")) for f in real[:4]]
    return items + [(f"{V}{im}.png", c) for im, c in GAL[k][len(items):]]


gal = ""
for k, n, f, d in SYS:
    gal += (f'<div style="display:grid;grid-template-columns:216px 1fr;gap:24px;padding:20px 0;border-bottom:1px solid {LG}">'
            f'<div><div class="kick" style="font-size:11px">Система</div><div style="font-size:22px;font-weight:800;margin-top:6px;text-transform:uppercase">{n}</div>'
            f'<p style="font-size:14px;color:{DG};line-height:1.5;margin-top:10px">{DESC[k]}</p></div><div class="g4" style="gap:10px">' + "".join(
                f'<div><div style="height:240px;overflow:hidden;background:{XL}"><img src="{im}" style="width:100%;height:100%;object-fit:cover"></div>'
                f'<div class="cap">{c}</div></div>' for im, c in gal_items(k)) + '</div></div>')
b.add(title("Как выглядит<br>каждая система", "Выбор", "Четыре вида на каждую систему: общий вид, плоскость фасада, монтаж и узел крепления.")
      + f'<div style="border-top:2px solid {GR}">{gal}</div>', "Выбор системы")

# ================================================================== FACADE NODES (shared data)
node_pages = [
    ("outer_corner", "Внешний угол", ["Угловой профиль за швом; панели не касаются друг друга", "Шов на углу открытый или с угловым профилем", "Крепление обеих панелей у угла — по схеме системы"]),
    ("inner_corner", "Внутренний угол", ["Внутренний угловой профиль", "Зазор для температурного движения", "Каждая панель крепится к своему профилю"]),
    ("window_reveal", "Оконный откос", ["HPL-откос до оконного блока", "Утеплитель откоса без пустот", "Примыкание к окну — герметизация по проекту"]),
    ("window_head", "Верхний оконный узел", ["Нижняя панель (софит) над окном", "Вход воздуха в вентзазор", "Зазор у оконного блока — ПО ПРОЕКТУ"]),
    ("window_sill", "Нижний оконный узел", ["Отлив с уклоном и капельником", "Выход воздуха из зазора под отливом", "Вынос отлива — ПО ПРОЕКТУ"]),
    ("base", "Цоколь", ["Перфорированный цокольный профиль", "Вход воздуха и защита от грызунов", "Отметка над отмосткой — ПО ПРОЕКТУ"]),
    ("parapet", "Парапет", ["Парапетная крышка с уклоном внутрь", "Выход воздуха под крышкой", "Вынос крышки — ПО ПРОЕКТУ"]),
    ("top", "Верхнее примыкание", ["Примыкание к перекрытию / козырьку", "Выход воздуха из зазора", "Отлив — ПО ПРОЕКТУ"]),
    ("hjoint", "Горизонтальный стык", ["Открытый горизонтальный шов", "Профиль непрерывный по высоте", "Ширина шва — ПО ПРОЕКТУ"]),
    ("vjoint", "Вертикальный стык", ["Шов над T-профилем с EPDM-лентой", "Крепление обеих панелей к полкам T-профиля", "Ширина шва — ПО ПРОЕКТУ"]),
]
N3D = {"outer_corner": "n_outer_corner", "inner_corner": "n_inner_corner", "window_reveal": "n_window", "window_head": "n_window",
       "window_sill": "n_window", "base": "n_base", "parapet": "n_parapet", "top": "n_parapet", "hjoint": "n_hjoint", "vjoint": "n_vjoint"}
NAMES = {k: n for k, n, _ in node_pages}


def nodes_grid(key, sysname, fix, kinds, lead):
    b.add(title("Основные узлы", sysname, lead) + '<div class="g2" style="gap:16px">'
          + "".join(f'<div class="frame">{node(k, 900, 720, fix)}</div>' for k in kinds) + '</div>'
          + f'<div class="note">Принципиальные схемы. Зазоры, шаг крепления и отступы — {P} / ПО РАСЧЁТУ. Подробно каждый узел — в разделе «Фасадные узлы».</div>',
          sysname, anchor=key)


def principle(key, sysname, sysk, lead, right):
    b.add(title("Принцип работы", sysname, lead)
          + f'<div style="display:grid;grid-template-columns:400px 1fr;gap:32px"><div>{panel_scheme(sysk, 400, 1000)}</div><div>{right}</div></div>',
          sysname, anchor=key)


# ================================================================== RIVET
divider("rivet", "Заклёпочная<br>система", V + "bw_rivet.png",
        "Классическая и самая надёжная система для HPL: панель механически крепится к алюминиевой подсистеме фасадными заклёпками.",
        "Фасадная заклёпка Ø5 мм, головка Ø16 мм в цвет панели. L-профиль на поле панели, T-профиль на стыке.",
        "Одна фиксированная точка задаёт положение панели, остальные — скользящие: панель свободно «дышит» при нагреве.",
        "Жилые, общественные и промышленные здания; высотные объекты; фасады, где важна ремонтопригодность.",
        ["Конструкция", "Компоненты", "Принцип работы", "Основные узлы", "Подготовка HPL", "Монтаж", "Инструменты", "Рекомендации"])
construction("rivet.1", "Заклёпочная система", "rivet", KEYS["rivet"],
             BASE + [("EPDM-лента", "на полку профиля"), ("HPL-панель", "1220 × 3050 мм"), ("Фасадная заклёпка", "в цвет панели")],
             "Разнесённый вид. Нумерация — от стены к панели.")
b.add(title("Компоненты системы", "Заклёпочная система", "Каждый элемент — одна функция. Типоразмеры подбираются по расчёту и инструкции производителя.")
      + '<div class="g4" style="gap:16px">'
      + f'<div class="card f" style="grid-column:span 2;padding:0"><div style="height:200px">{bg("img/brand/panels.jpg", 200, "center 40%")}</div>'
        f'<div style="padding:16px 18px"><h4 style="margin:0">HPL-панель FAÇADE UZHPL</h4><p>1220 × 3050 мм, 6 / 8 / 10 мм. Отверстия Ø10 — по монтажной карте.</p></div></div>'
      + card("p:" + MB + "rivet_painted.jpg", "Фасадная заклёпка", "AlMg5, Ø5 мм, головка Ø16 мм в цвет панели; стержень — нерж. сталь.", "длина 16–33 мм", 1, 112)
      + card("p:" + MB + "fix_sleeve.jpg", "Гильза фикс. точки", "Ø10 × 6 мм, отверстие Ø5,1. Одна на панель.", "фикс. точка", 2, 112)
      + card("c:lprofile", "L-профиль", "Вертикальный профиль на поле панели.", "алюминий", 3, 112)
      + card("c:tprofile", "T-профиль", "Профиль вертикального стыка двух панелей.", "алюминий", 4, 112)
      + card("c:bracket_fixed", "Кронштейн несущий", "Фиксированная опора: воспринимает вес.", "шаг — по расчёту", 5, 112)
      + card("c:bracket_sliding", "Кронштейн опорный", "Скользящая опора: ветер и движение.", "шаг — по расчёту", 6, 112)
      + card("c:gasket", "Паронитовая прокладка", "Терморазрыв под каждым кронштейном.", "под кронштейн", 7, 112)
      + card("c:anchor", "Анкерный болт", "Крепит кронштейн к основанию.", "тип — по основанию", 8, 112)
      + card("p:" + MB + "rivet_alu.jpg", "Заклёпка профиль — кронштейн", "Соединяет профиль с кронштейном.", "по системе", 9, 112)
      + card("p:" + MB + "epdm.jpg", "EPDM-лента", "0,75 / 1,3 мм; 70 / 110 / 135 мм. Стойкость к УФ — 20 лет.", "на полку профиля", 10, 112)
      + card("c:insulation", "Утеплитель", "Минеральная (базальтовая) вата.", "толщина — по расчёту", 11, 112)
      + card("c:dowel", "Тарельчатый дюбель", "Крепит утеплитель и мембрану.", "по расчёту", 12, 112)
      + card("c:membrane", "Ветрозащитная мембрана", "Защищает утеплитель, пропускает пар.", "паропроницаемая", 13, 112)
      + card("p:" + MB + "mouth_g3.jpg", "Наконечник G3", "Для заклёпочника: оставляет зазор под головкой.", "скользящие точки", 14, 112)
      + '</div><div class="note">Длина заклёпки = зона зажима (панель + профиль). Отверстие в профиле — Ø5,1 мм, в панели — Ø10 мм (оснастка MBE).</div>',
      "Заклёпочная система", anchor="rivet.2")
principle("rivet.3", "Заклёпочная система", "rivet", "Схема на панели 1220 × 3050 мм. Панель не зажата жёстко — она расширяется от фиксированной точки.",
          f'<div style="display:grid;gap:16px">{rivet_detail(476, 330, True)}{rivet_detail(476, 330, False)}</div>'
          + '<div style="display:grid;gap:18px;margin-top:24px">'
          + item("sleeve", "Фиксированная точка (оранжевая)", "Одна на панель. Гильза Ø10 × 6 заполняет отверстие — панель не смещается.")
          + item("layout", "Скользящие точки (белые)", "Отверстие Ø10 больше стержня Ø5 — панель движется при нагреве.")
          + item("rivet", "Наконечник G3", "Оставляет зазор под головкой: заклёпка не прижимает панель.") + '</div>'
          + '<div class="note">Шаг, отступы от кромок и количество точек — ПО РАСЧЁТУ ветровой нагрузки и инструкции производителя.</div>')
idx = "".join(f'<a href="#a-nodes.{i + 1}" class="card f" style="padding:14px"><div style="height:172px"><img src="img/{N3D[k]}.png" style="width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply"></div>'
              f'<div style="display:flex;gap:10px;align-items:center;margin-top:8px"><span class="badge">{i + 1}</span><h4 style="font-size:16px;margin:0">{NAMES[k]}</h4></div>'
              f'<p style="font-size:13px">Разрез и детали — стр. {{{{pg:nodes.{i + 1}}}}} →</p></a>' for i, (k, _, _) in enumerate(node_pages))
b.add(title("Основные узлы", "Заклёпочная система", "10 типовых узлов. Нажмите на узел — откроется страница с разрезом.")
      + f'<div class="g2" style="gap:14px">{idx}</div>', "Заклёпочная система", anchor="rivet.4")
b.add(title("Подготовка HPL", "Заклёпочная система", "Панели готовятся в цехе UZHPL по монтажной карте — на объект приходит комплект, готовый к монтажу.")
      + f'<div class="frame" style="margin-bottom:24px">{panel_processing(936, 560)}</div>'
      + steps([("Обмер", "Фактические размеры по месту — УТОЧНЯЕТСЯ НА ОБЪЕКТЕ.", "t:tape"),
               ("Раскрой", "Погружная пила с шиной, твердосплавный диск; лист поддерживается по всей длине.", "p:" + TL + "festool_ts55.jpg"),
               ("Сверление Ø10", "Сверло VHM с центрирующим острием — чистые края без сколов.", "p:" + MB + "vhm_drill.jpg"),
               ("Кромки", "Снятие заусенцев, лёгкая фаска.", "t:deburr"),
               ("Гильза фикс. точки", "Гильза Ø10 × 6 в отверстие фиксированной точки.", "p:" + MB + "fix_sleeve.jpg"),
               ("Маркировка", "Номер панели по раскладке; плёнка снимается после монтажа.", "m:final")], True),
      "Заклёпочная система", anchor="rivet.5")
b.add(title("Монтаж", "Заклёпочная система", "Последовательность работ на объекте.")
      + steps([("Разметка", "Оси и отметки кронштейнов по проекту — лазерный уровень.", "t:laser"),
               ("Кронштейны", "Паронитовая прокладка → кронштейн → анкерный болт.", "m:bracket"),
               ("Утеплитель", "Плиты без щелей, крепление тарельчатыми дюбелями.", "m:ins"),
               ("Мембрана", "Нахлёст и крепление дюбелями — по инструкции.", "m:mem"),
               ("L/T-профили", "Выставить в плоскость, закрепить заклёпками к кронштейнам.", "m:profiles"),
               ("EPDM-лента", "На полки профилей по всей длине.", "p:" + MB + "epdm.jpg"),
               ("Перенос отверстий", "Пружинный кондуктор 5,1 / 10: профиль сверлится через отверстие панели строго по центру.", "p:" + MB + "spring_jig.jpg"),
               ("Фиксированная точка", "Первой ставится заклёпка в гильзу фиксированной точки.", "p:" + MB + "fix_sleeve.jpg"),
               ("Скользящие точки", "AccuBird PRO с наконечником G3 — без зажима панели.", "p:" + MB + "accubird_pro.jpg"),
               ("Контроль", "Плоскость, швы, головки, свобода движения панели; фото.", "m:geom")]),
      "Заклёпочная система", anchor="rivet.6")
b.add(title("Инструменты", "Заклёпочная система", "Оснастка MBE / Trespa для заклёпочного фасада и электроинструмент бригад UZHPL.")
      + '<div class="g3" style="gap:16px">'
      + card("p:" + MB + "accubird_pro.jpg", "Gesipa AccuBird PRO", "Аккумуляторный заклёпочник: 18 В, 10 000 Н, ход 25 мм.", "заклёпки Ø5", 1, 150, True)
      + card("p:" + MB + "mouth_g3.jpg", "Наконечник G3", "Al-заклёпки Ø5, головка 16. Монтаж без зажима панели.", "скользящие точки", 2, 150, True)
      + card("p:" + MB + "spring_jig.jpg", "Пружинный кондуктор", "5,1 / 10 мм: центрирует сверление профиля через отверстие панели.", "перенос отверстий", 3, 150, True)
      + card("p:" + MB + "buegel_jig.jpg", "Скобовый кондуктор", "Панель Ø10 / профиль Ø5,1; вариант с эксцентриком.", "перенос отверстий", 4, 150, True)
      + card("p:" + MB + "vhm_drill.jpg", "Сверло VHM для HPL", "Твердосплавное, центрирующее острие: Ø8 / 10 / 13.", "отверстия в панели", 5, 150, True)
      + card("p:" + MB + "hss_drill.jpg", "Сверло HSS Ø5,1", "Для алюминиевой подсистемы и кондукторов.", "отверстия в профиле", 6, 150, True)
      + card("p:" + TL + "festool_ts55.jpg", "Festool TS 55", "Погружная пила, твердосплавный диск.", "раскрой", 7, 150, True)
      + card("p:" + TL + "guide_rail.jpg", "Направляющая шина", "Прямой рез по всей длине 3050 мм.", "раскрой", 8, 150, True)
      + card("p:" + TL + "m_hammer.jpg", "Перфоратор", "Отверстия под анкерные болты.", "подсистема", 9, 150, True)
      + card("p:" + TL + "m_drill.jpg", "Дрель-шуруповёрт", "Сверление профиля через кондуктор.", "подсистема", 10, 150, True)
      + card("t:laser", "Лазерный уровень", "Разметка осей и плоскости.", "разметка", 11, 150, True)
      + card("p:" + MB + "paint_pen.jpg", "Лак-карандаш", "Подкраска головок в цвет панели.", "финиш", 12, 150, True)
      + '</div>', "Заклёпочная система", anchor="rivet.7")
b.add(title("Рекомендации UZHPL", "Заклёпочная система", "Правила, которые определяют качество и срок службы заклёпочного фасада.")
      + recs([("Расчёт проекта", "Подсистема, шаг кронштейнов, профилей и заклёпок — только по расчёту.", "ПО РАСЧЁТУ"),
              ("Одна фиксированная точка", "Остальные — скользящие. Нельзя зажимать все точки.", ""),
              ("Наконечник G3", "Скользящие точки — только специальным наконечником.", ""),
              ("Центровка отверстий", "Профиль сверлится через панель кондуктором — строго по центру.", ""),
              ("Подбор заклёпки", "Длина — по зоне зажима: панель + профиль.", "ПО СИСТЕМЕ"),
              ("Вентзазор", "Непрерывный от цоколя до парапета.", "ПО РАСЧЁТУ"),
              ("EPDM-лента", "На все полки профилей под панелями.", ""),
              ("Подкраска", "Повреждения головок — лак-карандашом в цвет.", ""),
              ("Защитная плёнка", "Снимать сразу после монтажа панели.", "")])
      + f'<div style="margin-top:28px;height:470px;overflow:hidden"><img src="{V}wall_rivet2.png" style="width:100%;height:100%;object-fit:cover"></div>',
      "Заклёпочная система", anchor="rivet.8")
result(V + "b_rivet.png", "Заклёпочный<br>фасад", "Панели 1220 × 3050 мм, заклёпки в цвет панели. Ровный ритм крепежа — часть архитектуры.")

# ================================================================== GLUE
divider("glue", "Клеевая<br>система", V + "bw_glue.png",
        "Панель приклеивается к алюминиевой подсистеме фасадным клеевым комплектом. Лицевая сторона полностью чистая.",
        "Активатор / очиститель → праймер → двусторонняя лента → клей (колбаса или картридж).",
        "Лента мгновенно фиксирует панель, клей набирает прочность и становится несущим соединением.",
        "Современная архитектура, крупные однотонные плоскости, объекты с высокими требованиями к эстетике.",
        ["Конструкция", "Компоненты", "Принцип работы", "Основные узлы", "Подготовка HPL", "Монтаж", "Инструменты", "Рекомендации"])
construction("glue.1", "Клеевая система", "glue", KEYS["glue"],
             BASE + [("Активатор + праймер", "зоны склейки профиля"), ("EPDM-лента", "в зоне шва"), ("Двусторонняя лента", "временная фиксация"),
                     ("Клеевой валик", "постоянное соединение"), ("HPL-панель", "1220 × 3050 мм")],
             "Разнесённый вид. Нумерация — от стены к панели.")
b.add(title("Компоненты системы", "Клеевая система", "Клей, праймер, лента и очиститель — только одной системы (MBE Panel-loc, допуск Z-10.8-350).")
      + '<div class="g4" style="gap:16px">'
      + f'<div class="card f" style="grid-column:span 2;padding:0"><div style="height:200px;background:#fff;display:flex;align-items:center;justify-content:center"><img src="{MB}glue_kit.jpg" style="max-height:190px;max-width:100%"></div>'
        f'<div style="padding:16px 18px"><h4 style="margin:0">Комплект Panel-loc</h4><p>Клей, праймеры, очиститель, лента и аппликаторы одной системы.</p></div></div>'
      + card("p:" + MB + "adh_bag.jpg", "Клей (колбаса)", "Чёрный, 600 мл — ок. 13,3 п. м валика.", "постоянное", 1, 112)
      + card("p:" + MB + "adh_cart.jpg", "Клей (картридж)", "Чёрный, 290 мл — ок. 6,4 п. м валика.", "постоянное", 2, 112)
      + card("p:" + MB + "foam_tape.jpg", "Двусторонняя лента", "Вспененная 12 × 3 мм, рулон 25 м.", "временная фиксация", 3, 112)
      + card("p:" + MB + "primer_close.jpg", "Праймер прозрачный", "Тыльная сторона панели, профиль.", "праймер", 4, 112)
      + card("p:" + MB + "primer_alu.jpg", "Праймер Alu (чёрный)", "Алюминиевый профиль при чёрном шве.", "праймер", 5, 112)
      + card("p:" + MB + "cleaner.jpg", "Очиститель / активатор", "Обезжиривание, удаление пыли и свежего клея.", "активатор", 6, 112)
      + card("c:lprofile", "L-профиль", "На поле панели.", "алюминий", 7, 112)
      + card("c:tprofile", "T-профиль", "На стыке панелей.", "алюминий", 8, 112)
      + card("c:bracket_fixed", "Кронштейн", "Несущий / опорный.", "шаг — по расчёту", 9, 112)
      + card("c:gasket", "Паронитовая прокладка", "Под кронштейн.", "терморазрыв", 10, 112)
      + card("c:anchor", "Анкерный болт", "Кронштейн → стена.", "по основанию", 11, 112)
      + card("c:insulation", "Базальтовый утеплитель", "С тарельчатыми дюбелями.", "по расчёту", 12, 112)
      + card("c:membrane", "Ветрозащитная мембрана", "Паропроницаемая.", "", 13, 112)
      + card("p:" + MB + "epdm.jpg", "EPDM-лента", "В зоне вертикального шва.", "на профиль", 14, 112)
      + '</div><div class="note">Совместимость клея с конкретной панелью и профилем — подтверждать до начала работ.</div>',
      "Клеевая система", anchor="glue.2")
principle("glue.3", "Клеевая система", "glue", "Тыльная сторона панели 1220 × 3050: на каждой линии профиля — зона праймера, лента и клеевой валик.",
          f'<div class="frame">{glue_section(936, 620)}</div><div style="display:grid;gap:20px;margin-top:26px">'
          + item("tape", "Лента — сразу", "Двусторонняя лента удерживает панель в проектном положении, пока клей набирает прочность.")
          + item("glue", "Клей — навсегда", "Треугольный валик — несущий эластичный шов, компенсирует температурное движение.")
          + item("primer", "Адгезия", "Шлифовка, очистка и праймер на панели и профиле.")
          + item("thermo", "Условия", "Температура и влажность — строго по инструкции, фиксируются в журнале.") + '</div>'
          + f'<div style="margin-top:26px;height:330px;overflow:hidden;background:{XL}"><img src="{V}sys_glue.png" style="width:100%;height:100%;object-fit:cover;object-position:center 45%"></div>'
          + '<div class="cap">Лента и клеевой валик на подготовленных профилях.</div>')
nodes_grid("glue.4", "Клеевая система", "glue", ["outer_corner", "inner_corner", "window_reveal", "base", "parapet", "vjoint"],
           "Клеевое крепление в типовых узлах: панель приклеена к полкам профилей.")
b.add(title("Подготовка HPL", "Клеевая система", "Панель обрабатывается полностью до того, как клей наносится на профиль.")
      + steps([("Разметка положения панели", "По раскладке фасада; номер панели.", "m:mark"),
               ("Разметка линий профилей", "Линии профилей на тыльной стороне панели.", "m:profiles"),
               ("Шлифование зон контакта", "Бумага P220 — панель; Scotch-Brite — профиль.", "m:hplprep"),
               ("Очистка", "Безворсовая салфетка + очиститель / активатор.", "p:" + MB + "cleaner.jpg"),
               ("Праймер", "Только в зонах контакта; выдержка по инструкции.", "p:" + MB + "primer_close.jpg")])
      + '<div class="warn" style="margin-top:28px"><b>Важно:</b> к моменту нанесения клея на профиль тыльная сторона HPL уже отшлифована, очищена и обработана праймером. Клей наносится непосредственно перед установкой панели.</div>'
      + f'<div style="margin-top:28px;height:420px;overflow:hidden;background:{XL}"><img src="{V}macro_glue.png" style="width:100%;height:100%;object-fit:cover"></div>'
      + '<div class="cap">Вертикальный стык клеевого фасада: панели на T-профиле, лента и клей скрыты за панелью.</div>',
      "Клеевая система", anchor="glue.5")
b.add(title("Монтаж", "Клеевая система", "Подготовленная панель устанавливается на подготовленные профили.")
      + steps([("Подготовка профиля", "Шлифовка Scotch-Brite, очистка, активатор / праймер.", "m:clean"),
               ("Выдержка", "Время испарения праймера — по инструкции.", "m:cure"),
               ("Двусторонняя лента", "Вдоль профиля, без натяжения; плёнку не снимать до установки.", "p:" + MB + "foam_tape.jpg"),
               ("Клеевой валик", "Треугольный, параллельно ленте, непрерывно.", "p:" + MB + "adh_cart.jpg"),
               ("Установка панели", "Снять плёнку ленты, выставить по разметке в пределах открытого времени.", "m:panel"),
               ("Прижим", "Прижать по линиям профилей до контакта с лентой.", "m:press"),
               ("Отверждение", "Не нагружать соединение до набора прочности.", "m:cure"),
               ("Журнал и контроль", "Температура, влажность, партии материалов; плоскость и швы.", "m:final")]),
      "Клеевая система", anchor="glue.6")
b.add(title("Инструменты", "Клеевая система", "Оснастка для клеевых работ и подготовки панелей.")
      + '<div class="g3" style="gap:16px">'
      + card("p:" + MB + "glue_kit.jpg", "Комплект Panel-loc", "Клей, праймеры, очиститель, лента, аппликаторы.", "MBE", 1, 150, True)
      + card("t:gun", "Пистолет для клея", "Под картридж 290 мл и колбасу 600 мл.", "нанесение клея", 2, 150, True)
      + card("t:brush", "Аппликатор праймера", "Ручка, ванночка, сменные подушки.", "праймер", 3, 150, True)
      + card("i:thermo", "Термогигрометр", "Температура и влажность воздуха.", "условия", 4, 150, True)
      + card("t:wipes", "Безворсовые салфетки", "Очистка зон склейки.", "очистка", 5, 150, True)
      + card("p:" + TL + "festool_ts55.jpg", "Festool TS 55", "Раскрой панелей.", "раскрой", 6, 150, True)
      + card("t:suction", "Вакуумные захваты", "Точная установка панели.", "монтаж", 7, 150, True)
      + card("p:" + TL + "clamp.jpg", "Струбцины", "Фиксация при подготовке.", "фиксация", 8, 150, True)
      + card("t:laser", "Лазерный уровень", "Разметка.", "разметка", 9, 150, True)
      + card("t:gloves", "Перчатки", "Работа с химией.", "защита", 10, 150, True)
      + card("t:mask", "Респиратор", "Работа с праймером.", "защита", 11, 150, True)
      + card("t:glasses", "Защитные очки", "Нанесение составов.", "защита", 12, 150, True)
      + '</div>', "Клеевая система", anchor="glue.7")
b.add(title("Рекомендации UZHPL", "Клеевая система", "Клеевой фасад прощает меньше ошибок — соблюдайте последовательность и условия.")
      + recs([("Только одна система", "Клей, праймер, очиститель и лента — одного производителя.", ""),
              ("Совместимость", "Проверить для конкретной панели и профиля.", ""),
              ("Условия нанесения", "Температура и влажность — строго по инструкции.", "ПО ИНСТРУКЦИИ"),
              ("Сначала панель", "HPL подготовлен до нанесения клея на профиль.", ""),
              ("Время выдержки", "Праймер — время испарения; клей — открытое время.", "ПО ИНСТРУКЦИИ"),
              ("Геометрия валика", "Треугольный, непрерывный; размер — по системе.", "ПО СИСТЕМЕ"),
              ("Пробная адгезия", "Тест на объекте перед началом работ.", ""),
              ("Защита", "От дождя и прямого солнца во время работ.", ""),
              ("Журнал", "Условия и партии материалов — для гарантии.", "")])
      + f'<div style="margin-top:28px;height:470px;overflow:hidden"><img src="{V}wall_glue.png" style="width:100%;height:100%;object-fit:cover"></div>',
      "Клеевая система", anchor="glue.8")
result(V + "b_glue.png", "Клеевой<br>фасад", "Монолитная плоскость без видимого крепежа — фасад читается как единая поверхность.")

# ================================================================== HIDDEN
divider("hidden", "Скрытая<br>система", V + "bw_hidden.png",
        "Панель с тыльной обработкой навешивается на горизонтальные направляющие через кляммеры — как в скрытой механической системе Trespa.",
        "Кляммер (клипса) на анкере с подрезкой в тыльной стороне панели → горизонтальная направляющая.",
        "Кляммеры навешиваются сверху на направляющую; регулировочный винт выставляет плоскость.",
        "Премиальные фасады, сложная архитектура, объекты, где панель должна сниматься без следов.",
        ["Конструкция", "Принцип навески", "Основные узлы", "Монтаж"])
construction("hidden.1", "Скрытая система", "hidden", KEYS["hidden"],
             BASE[:7] + [("Вертикальный профиль", ""), ("Вертикальный профиль на стыке", ""), ("Заклёпка профиль — кронштейн", ""),
                         ("Горизонтальная направляющая", "крепится к вертикальным профилям"), ("Кляммер (клипса)", "на тыльной стороне панели"),
                         ("HPL-панель", "с тыльной обработкой")],
             "Разнесённый вид. Нумерация — от стены к панели.")
principle("hidden.2", "Скрытая система", "hidden", "Кляммеры на тыльной стороне панели 1220 × 3050 навешиваются сверху на направляющие.",
          f'<div class="frame">{hidden_principle(936, 620)}</div><div class="g2" style="gap:16px;margin-top:20px">'
          + card("c:panel_groove", "Тыльная обработка", "Отверстия под анкер с подрезкой — на ЧПУ.", "ЧПУ", 1, 110)
          + card("c:clip", "Кляммер (клипса)", "Положение и количество — по системе.", "по системе", 2, 110) + '</div>'
          + '<div style="display:grid;gap:18px;margin-top:22px">'
          + item("level", "Регулировка", "Регулировочный винт кляммера выставляет панель в плоскость.")
          + item("sleeve", "Фиксация", "Одна точка фиксируется от смещения (оранжевая), остальные скользят по направляющей.") + '</div>'
          + f'<div style="margin-top:24px;height:300px;overflow:hidden;background:{XL}"><img src="{V}macro_hidden.png" style="width:100%;height:100%;object-fit:cover"></div>'
          + '<div class="cap">Стык скрытого фасада: крепёж за панелью.</div>')
nodes_grid("hidden.3", "Скрытая система", "hidden", ["outer_corner", "inner_corner", "window_reveal", "base", "parapet", "vjoint"],
           "Общая подсистема; точная геометрия кляммеров и направляющих — по документации системы.")
b.add(title("Монтаж", "Скрытая система", "Последовательность работ на объекте.")
      + steps([("Разметка и кронштейны", "Оси, паронит, кронштейны, анкерные болты.", "m:bracket"),
               ("Утеплитель и мембрана", "Утеплитель на дюбелях, мембрана.", "m:ins"),
               ("Вертикальные профили", "Выставить в плоскость, закрепить заклёпками.", "m:profiles"),
               ("Горизонтальные направляющие", "По отметкам, строго горизонтально.", "m:geom"),
               ("Обработка панелей на ЧПУ", "Отверстия под анкеры с подрезкой на тыльной стороне.", "t:cnc"),
               ("Кляммеры на панель", "Анкеры + кляммеры по монтажной карте.", "m:clip"),
               ("Навеска панели", "Сверху вниз на направляющую.", "m:panel"),
               ("Регулировка и фиксация", "Плоскость, швы, точка фиксации.", "m:adjust")], True)
      + f'<div style="margin-top:26px;height:420px;overflow:hidden;background:{XL}"><img src="{V}sys_hidden.png" style="width:100%;height:100%;object-fit:contain"></div>'
      + '<div class="cap">Горизонтальные направляющие и кляммеры на панели 1220 × 3050 мм.</div>',
      "Скрытая система", anchor="hidden.4")
result(V + "b_hidden.png", "Скрытый<br>фасад", "Панели на кляммерах: цельная плоскость без видимого крепежа, панель снимается без следов.")

# ================================================================== SCREW
divider("screw", "Винтовая<br>система", V + "bw_screw.png",
        "Подсистема — как у заклёпочной системы; панель крепится фасадными винтами с окрашенной головкой.",
        "Фасадный винт с окрашенной головкой Ø12–16 мм или балконный винт M5 с гайкой.",
        "Одна фиксированная точка, остальные — скользящие. Винт не перетягивается: головка садится на панель без зажима.",
        "Объекты, где важна ремонтопригодность; деревянная подсистема; балконные ограждения.",
        ["Конструкция", "Компоненты и крепёжный узел", "Узлы и монтаж"])
construction("screw.1", "Винтовая система", "screw", KEYS["screw"],
             BASE + [("EPDM-лента", "на полку профиля"), ("HPL-панель", "1220 × 3050 мм"), ("Фасадный винт", "в цвет панели")],
             "Разнесённый вид. Подсистема та же, что у заклёпочной системы.")
b.add(title("Компоненты<br>и крепёжный узел", "Винтовая система", "Крепёж MBE для винтового монтажа HPL.")
      + f'<div class="frame">{screw_detail(936, 500)}</div><div class="g3" style="gap:16px;margin-top:20px">'
      + card("p:" + MB + "screw_painted.jpg", "Фасадный винт", "A2 / A4, привод ISR 20, головка Ø12–16 в цвет панели. Дерево: 4,8 × 38 … 5,5 × 65.", "MBE", 1, 130)
      + card("p:" + MB + "balcony.jpg", "Балконный винт M5", "С колпачковой гайкой или втулкой — алюминий и сталь. Момент 2–4 Н·м.", "MBE", 2, 130)
      + card("p:" + MB + "fix_sleeve.jpg", "Гильза фикс. точки", "Одна фиксированная точка на панель.", "фикс. точка", 3, 130)
      + card("c:lprofile", "L / T-профиль", "Подсистема — как у заклёпочной.", "алюминий", 4, 130)
      + card("p:" + MB + "epdm.jpg", "EPDM-лента", "На полку профиля под панелью.", "на профиль", 5, 130)
      + card("p:" + MB + "paint_pen.jpg", "Лак-карандаш", "Подкраска головок.", "финиш", 6, 130)
      + '</div><div class="warn" style="margin-top:22px">Монтаж без зажима: как только головка села на панель — остановить завинчивание. Не заменять фасадный крепёж обычными саморезами.</div>',
      "Винтовая система", anchor="screw.2")
b.add(title("Узлы и монтаж", "Винтовая система", "Узлы — как у заклёпочной системы, крепление панели — винтами.")
      + '<div class="g2" style="gap:16px">' + "".join(f'<div class="frame">{node(k, 900, 720, "screw")}</div>' for k in ["outer_corner", "vjoint"]) + '</div>'
      + '<div style="margin-top:24px"></div>'
      + steps([("Подсистема", "Паронит, кронштейны, утеплитель, мембрана, L/T-профили, EPDM.", "m:profiles"),
               ("Отверстия в панели", "Фиксированная точка — с гильзой, скользящие — увеличенные.", "p:" + MB + "vhm_drill.jpg"),
               ("Отверстия в профиле", "Через панель, по центру — кондуктором.", "p:" + MB + "spring_jig.jpg"),
               ("Крепление", "Сначала фикс. точка, затем скользящие; без перетяжки.", "p:" + MB + "screw_painted.jpg"),
               ("Контроль", "Плоскость, швы, свобода движения панели.", "m:geom")], True),
      "Винтовая система", anchor="screw.3")
result(V + "b_screw.png", "Винтовой<br>фасад", "Винты с окрашенной головкой в цвет панели — аккуратный и ремонтопригодный фасад.")

# ================================================================== FACADE NODES
rows = "".join(f'<a href="#a-nodes.{i + 1}"><span>{n}</span><span>{{{{pg:nodes.{i + 1}}}}}</span></a>' for i, (_, n, _) in enumerate(node_pages))
b.add(title("Фасадные узлы", "Раздел", "Отдельная страница на каждый узел: разрез, 3D-вид и данные проекта. Показано для заклёпочной системы.")
      + f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:30px"><div style="background:{XL};height:330px;padding:16px"><img src="img/n_vjoint.png" style="width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply"></div>'
        f'<div style="background:{XL};height:330px;padding:16px"><img src="img/n_window.png" style="width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply"></div></div>'
      + f'<div class="toc" style="border-top:2px solid {GR}">{rows}</div>', "Фасадные узлы", anchor="nodes")
for i, (k, n, pts) in enumerate(node_pages):
    b.add(title(n, "Фасадный узел", short=True) + f'<div class="frame">{node(k, 900, 720, "rivet")}</div>'
          + f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-top:28px"><div style="background:{XL};padding:16px">'
          + f'<div class="cap" style="margin:0">3D-ВИД УЗЛА</div><div style="height:520px;margin-top:6px"><img src="img/{N3D[k]}.png" style="width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply"></div></div>'
          + '<div><h3>Ключевые элементы</h3>' + "".join(f'<div class="rec" style="grid-template-columns:40px 1fr;padding:12px 0"><span class="badge">{j + 1}</span><h4 style="font-size:16px;padding-top:4px">{t}</h4></div>' for j, t in enumerate(pts))
          + '<h3 style="margin-top:28px">Данные проекта</h3>' + "".join(f'<div class="spec" style="font-size:15px"><span>{a}</span><span class="pill">{c}</span></div>'
                                                                         for a, c in [("Шаг крепления", "ПО РАСЧЁТУ"), ("Ширина швов", P), ("Вентзазор", "ПО РАСЧЁТУ"), ("Фактические размеры", "НА ОБЪЕКТЕ")])
          + '</div></div>', "Фасадные узлы", anchor=f"nodes.{i + 1}")

# ================================================================== INTERIOR
rooms = [("i_walls", "Стены", "VIRGINIA WALNUT"), ("i_ceiling", "Потолки", "DUNE OAK"), ("i_furniture", "Мебель", "GRAPHITE + ELEGANT OAK"),
         ("i_partitions", "Перегородки", "SMOKE GRAY + WALNUT"), ("i_sanitary", "Санузлы", "PEARL WHITE + GRAPHITE"),
         ("i_reception", "Рецепции", "BLACK GALAXY + OAK"), ("i_decorative", "Декоративные панели", "DUNE OAK, рейка")]
methods = [("glue", "Клеевой", "На ровное основание (ГКЛ, бетон, фанера) — монтажный клей по системе."),
           ("screw", "Механический", "Каркас + винты / заклёпки с компенсационными отверстиями."),
           ("clip", "Скрытый", "Клипсы, кляммеры или подвесные профили — снимается без следов."),
           ("cnc", "Мебельная обработка", "Раскрой, кромки, фрезеровка под фурнитуру на ЧПУ.")]
b.add(title("Интерьерные<br>системы", "Интерьер", "HPL в интерьере: стойкость к влаге, ударам и химии. Решение подбирается отдельно от фасада.")
      + '<div class="g4" style="gap:12px">' + "".join(
          f'<div><div class="photo" style="height:190px;background-image:url(img/{im}.jpg)"></div><div style="font-size:15px;font-weight:700;margin-top:8px">{a}</div>'
          f'<div class="cap" style="margin-top:2px">{d}</div></div>' for im, a, d in rooms)
      + f'<div><div class="photo" style="height:190px;background-image:url(img/decor/F-72.jpg)"></div><div style="font-size:15px;font-weight:700;margin-top:8px">Ваш проект</div>'
        f'<div class="cap" style="margin-top:2px">декор и способ монтажа под задачу</div></div></div>'
      + '<div class="hr"></div><h3>Способы монтажа</h3><div class="g2" style="gap:26px 40px">' + "".join(item(i, a, d) for i, a, d in methods) + '</div>'
      + '<div class="hr"></div><h3>Правила установки</h3><div class="g2" style="gap:0 40px">' + "".join(
          f'<div class="spec" style="font-size:15px;grid-template-columns:1fr"><span>{t}</span></div>' for t in [
              "Компенсационные зазоры по периметру и в стыках — ПО ПРОЕКТУ", "Панель не зажимается жёстко: отверстия больше крепежа",
              "Основание ровное и сухое; во влажных зонах — вентзазор", "Кромки обработаны: фаска или радиус",
              "Крепёж — нержавеющий во влажных помещениях", "Защитная плёнка снимается после монтажа"]) + '</div>',
      "Интерьер", anchor="interior")
b.add(title("Стыки и углы", "Интерьер", "HPL обрабатывается как массив: стыки и углы решаются без профилей или с декоративными элементами.")
      + '<div class="g2" style="gap:16px">' + "".join(f'<div class="frame">{ijoint(k)}</div>' for k in ["tongue", "gasket", "hprof", "shadow", "miter", "corner", "open", "edge"]) + '</div>'
      + '<div class="note">Шпунт / паз — HPL фрезеруется, одна панель заходит в другую. Угол 45° — усовка на ЧПУ. Резиновый уплотнитель или декоративный профиль закрывают шов и компенсируют движение.</div>',
      "Интерьер")
b.add(title("Интерьерные узлы", "Интерьер", "Типовые примыкания: углы, потолок, пол, дверной проём, мебель и перегородки.")
      + '<div class="g2" style="gap:16px">' + "".join(f'<div class="frame">{interior_node(k)}</div>' for k in ["in_corner", "out_corner", "joint", "ceiling", "floor", "door", "furniture", "wall_junction"]) + '</div>'
      + '<div class="note">Компенсационные зазоры и шаг крепления в интерьере — ПО ПРОЕКТУ и инструкции производителя панели.</div>', "Интерьер")

# ================================================================== TOOLS UZHPL
groups = [("Раскрой", [("p:" + TL + "festool_ts55.jpg", "Festool TS 55"), ("p:" + TL + "guide_rail.jpg", "Направляющая шина"), ("p:" + TL + "mafell_kss40.jpg", "Mafell KSS 40"), ("p:" + TL + "m_jigsaw.jpg", "Лобзик")]),
          ("Сверление", [("p:" + MB + "vhm_drill.jpg", "Сверло VHM Ø8/10/13"), ("p:" + MB + "hss_drill.jpg", "Сверло HSS Ø5,1"), ("p:" + MB + "spring_jig.jpg", "Пружинный кондуктор"), ("p:" + MB + "buegel_jig.jpg", "Скобовый кондуктор")]),
          ("Заклёпки", [("p:" + MB + "accubird_pro.jpg", "Gesipa AccuBird PRO"), ("p:" + MB + "mouth_g3.jpg", "Наконечник G3"), ("p:" + MB + "mouth_g7.jpg", "Наконечник G7"), ("p:" + MB + "paint_pen.jpg", "Лак-карандаш")]),
          ("Подсистема", [("p:" + TL + "m_hammer.jpg", "Перфоратор"), ("p:" + TL + "m_drill.jpg", "Дрель-шуруповёрт"), ("p:" + TL + "m_grinder.jpg", "УШМ"), ("p:" + TL + "clamp.jpg", "Струбцины")]),
          ("Клей и разметка", [("p:" + MB + "glue_kit.jpg", "Panel-loc"), ("t:gun", "Пистолет для клея"), ("i:thermo", "Термогигрометр"), ("t:laser", "Лазерный уровень")])]
gr = ""
for gname, items in groups:
    gr += (f'<div style="display:grid;grid-template-columns:150px 1fr;gap:20px;padding:14px 0;border-bottom:1px solid {LG};align-items:center">'
           f'<div style="font-size:13px;letter-spacing:.2em;font-weight:700;text-transform:uppercase">{gname}</div><div class="g4" style="gap:12px">'
           + "".join(f'<div class="card f" style="padding:10px"><div class="im" style="height:118px">{vis(k)}</div><h4 style="font-size:14px;margin-top:8px">{n}</h4></div>' for k, n in items)
           + '</div></div>')
b.add(title("Инструменты<br>UZHPL", "Инструменты", "Профессиональный инструмент и оснастка, которыми работают бригады UZHPL.")
      + f'<div style="border-top:2px solid {GR}">{gr}</div>'
      + '<div class="note">Фото оснастки — MBE / Trespa. 3D-иллюстрации пистолета, аппликатора, захватов, уровня и СИЗ — модели Sketchfab (CC BY): I. Bouwen, M. Antonov, Chenchanchong, P. Wubben, A. Sagidullin, D. Korablyov, vinigor.</div>',
      "Инструменты", anchor="tools")

# ================================================================== QC
qc = [("Подсистема", "Кронштейны, анкеры, паронит, плоскость профилей"), ("Утеплитель и мембрана", "Без щелей, дюбели, нахлёсты"),
      ("Геометрия", "Раскладка и размеры панелей по проекту"), ("Плоскость", "Отклонения — в допусках проекта"),
      ("Швы", "Равномерная ширина, прямолинейность"), ("Крепёж", "Тип, длина, фикс. / скользящие точки"),
      ("Клеевые работы", "Условия, журнал, отверждение"), ("Поверхность", "Без сколов и царапин; плёнка снята"),
      ("Вентиляция", "Входы и выходы воздуха открыты"), ("Документация", "Фотоотчёт каждого этапа, акт")]
stages = ["Основание", "Подсистема", "Обработка", "Монтаж", "Сдача"]
b.add(title("Технадзор<br>и контроль качества", "Качество", "Контроль выполняют специалисты UZHPL из Германии.")
      + '<div class="g2">'
      + f'<div class="card f" style="padding:28px">{icon("germany", 56)}<h4 style="font-size:22px;margin-top:16px">При монтаже UZHPL</h4><p style="font-size:15.5px">Технадзор включён: специалисты из Германии контролируют каждый этап — от разметки до сдачи объекта.</p></div>'
      + f'<div class="card" style="padding:28px;border:2px solid {OR}">{icon("supervision", 56)}<h4 style="font-size:22px;margin-top:16px">Технадзор как услуга</h4><p style="font-size:15.5px">Если монтаж выполняет другой подрядчик — предоставляем технический надзор отдельно.</p></div></div>'
      + f'<h3 style="margin-top:36px">Контроль на каждом этапе</h3><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px">' + "".join(
          f'<div style="border-top:3px solid {OR if i == 4 else GR};padding-top:12px"><div style="font-size:12px;color:{OR};font-weight:700;letter-spacing:.14em">{i + 1:02d}</div>'
          f'<div style="font-size:16px;font-weight:700;margin-top:4px">{s}</div></div>' for i, s in enumerate(stages)) + '</div>'
      + '<h3 style="margin-top:36px">Чек-лист приёмки</h3><div class="g2" style="gap:0 40px">' + "".join(
          f'<div class="lg"><div class="li"><span style="width:22px;height:22px;border:2px solid {GR};position:relative;margin-top:3px;display:block">'
          f'<span style="position:absolute;left:5px;top:0;width:6px;height:12px;border:solid {OR};border-width:0 3px 3px 0;transform:rotate(45deg)"></span></span>'
          f'<div><h4>{a}</h4><p>{d}</p></div></div></div>' for a, d in qc) + '</div>'
      + f'<div style="margin-top:30px;height:330px;overflow:hidden"><img src="{V}wall_rivet.png" style="width:100%;height:100%;object-fit:cover;object-position:center 30%"></div>',
      "Качество", anchor="qc")

# ================================================================== RECOMMENDATIONS
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
      + f'<div style="margin-top:28px;height:470px;overflow:hidden"><img src="{V}b_dusk.png" style="width:100%;height:100%;object-fit:cover;object-position:center 40%"></div>',
      "Рекомендации", anchor="recs")

# ================================================================== START
qr = open(os.path.join(HERE, "img", "qr.svg")).read()
qr = qr[qr.index("<svg"):]
cta = [("phone", "Заявка", "Звонок или сообщение менеджеру"), ("doc", "Исходные данные", "Фасады или фото объекта, площадь, адрес, сроки"),
       ("material", "Подбор решения", "Система крепления, декор, образцы панелей"), ("engineering", "Расчёт и КП", "Подсистема, раскрой, комплектация, монтаж"),
       ("processing", "Производство", "Раскрой и обработка HPL, комплектная поставка"), ("montage", "Монтаж и технадзор", "Монтаж, контроль, фотоотчёт, сдача")]
b.add(title("Как начать<br>проект", "Контакты", "Шесть шагов от запроса до готового фасада.")
      + f'<div class="g3" style="gap:0;border-top:2px solid {GR}">' + "".join(
          f'<div style="padding:26px 24px 26px 0;border-bottom:1px solid {LG}">{icon(n, 44)}<div style="font-size:12px;color:{OR};font-weight:700;letter-spacing:.14em;margin-top:14px">{i + 1:02d}</div>'
          f'<div style="font-size:19px;font-weight:700;margin-top:4px">{a}</div><div style="font-size:14.5px;color:{DG};margin-top:6px;line-height:1.45">{d}</div></div>' for i, (n, a, d) in enumerate(cta)) + '</div>'
      + f'<div style="margin-top:40px;display:grid;grid-template-columns:1fr 280px;border:2px solid {GR}">'
      + f'<div style="padding:38px"><div class="kick">Свяжитесь с нами</div><div style="font-size:40px;font-weight:800;margin-top:14px;line-height:1.2">+998 77 003 28 82<br>+998 78 122 31 51</div>'
      + f'<div style="font-size:19px;margin-top:16px;color:{DG}">info@uzhpl.uz · sales@uzhpl.uz</div>'
      + f'<div style="font-size:14.5px;color:{MG};margin-top:16px;line-height:1.6">Для быстрого расчёта пришлите: фасады или фото объекта, площадь облицовки, желаемый декор, адрес и сроки.</div></div>'
      + f'<div style="background:{XL};display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px"><div style="width:200px">{qr}</div>'
      + f'<div style="font-size:13px;font-weight:700;letter-spacing:.2em;margin-top:12px">UZHPL.UZ</div></div></div>'
      + '<h3 style="margin-top:40px">Что вы получаете</h3><div class="g3">'
      + item("layout", "Техническое решение", "Система крепления, узлы, раскладка панелей 1220 × 3050 мм.")
      + item("material", "Образцы декоров", "Подбор декора и толщины; образцы в шоуруме.")
      + item("doc", "Коммерческое предложение", "Панели, подсистема, обработка, монтаж и технадзор — в одном КП.") + '</div>',
      "Контакты", anchor="start")

# ================================================================== LAST PAGE (light)
b.add(f'<div style="position:absolute;left:0;right:0;top:0;height:1180px">{bg("img/brand/facade3d_b.jpg", 1180, "center 35%")}</div>'
      f'<div style="position:absolute;left:84px;top:84px"><img src="img/brand/logo_white.png" style="height:48px"></div>'
      f'<div style="position:absolute;left:84px;right:84px;top:1250px">'
      f'<div style="font-size:48px;font-weight:800;line-height:1.08;text-transform:uppercase;letter-spacing:-.01em">HPL-решения<br>для архитектуры</div>'
      f'<div class="g3" style="margin-top:44px;border-top:2px solid {GR};padding-top:28px">'
      f'<div><div class="kick" style="font-size:11px">Офис и шоурум</div><div style="font-size:16px;line-height:1.6;margin-top:10px">Узбекистан, Ташкент,<br>Мирзо-Улугбекский район,<br>ул. Паркент, 235</div></div>'
      f'<div><div class="kick" style="font-size:11px">Телефоны</div><div style="font-size:16px;line-height:1.6;margin-top:10px">+998 77 003 28 82<br>+998 78 122 31 51</div></div>'
      f'<div><div class="kick" style="font-size:11px">Почта и сайт</div><div style="font-size:16px;line-height:1.6;margin-top:10px">info@uzhpl.uz<br>sales@uzhpl.uz<br>uzhpl.uz</div></div></div>'
      f'<div style="font-size:13.5px;color:{MG};margin-top:30px">Образцы декоров, расчёт проектов и доставка по Узбекистану и СНГ.</div></div>', bare=True)

open(os.path.join(HERE, "uzhpl-catalog.html"), "w").write(b.html())
print(len(b.pages), "pages")
