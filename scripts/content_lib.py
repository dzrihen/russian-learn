# -*- coding: utf-8 -*-
"""Shared Russian–Hebrew phrase banks and template expanders."""
from exhelpers import phrases, dialogue

def dlg(*pairs, distractors=None):
    """pairs: (speaker, ru) alternating; speaker 'n' or 'u'"""
    turns = []
    for sp, ru in pairs:
        turns.append({"speaker": "npc" if sp == "n" else "user", "ru": ru})
    return dialogue(turns, distractors or ["Я не знаю", "Повторите", "Где это?"])

# ——— reusable vocab bits ———
PEOPLE = [
    ("я", "אני"), ("ты", "אתה/את"), ("он", "הוא"), ("она", "היא"),
    ("мы", "אנחנו"), ("вы", "אתם/אתן"), ("они", "הם/הן"),
    ("мой друг", "החבר שלי"), ("моя мама", "אמא שלי"), ("мой папа", "אבא שלי"),
    ("моя сестра", "אחותי"), ("мой брат", "אחי"), ("учитель", "מורה"),
]
PLACES = [
    ("дом", "בית"), ("школа", "בית ספר"), ("работа", "עבודה"), ("магазин", "חנות"),
    ("кафе", "בית קפה"), ("парк", "פארק"), ("музей", "מוזיאון"), ("вокзал", "תחנה"),
    ("аптека", "בית מרקחת"), ("банк", "בנק"), ("улица", "רחוב"), ("город", "עיר"),
    ("больница", "בית חולים"), ("библиотека", "ספרייה"), ("кино", "קולנוע"),
]
FOODS = [
    ("хлеб", "לחם"), ("молоко", "חלב"), ("вода", "מים"), ("чай", "תה"), ("кофе", "קפה"),
    ("сыр", "גבינה"), ("мясо", "בשר"), ("рыба", "דג"), ("суп", "מרק"), ("салат", "סלט"),
    ("яблоко", "תפוח"), ("банан", "בננה"), ("рис", "אורז"), ("масло", "חמאה/שמן"),
    ("сок", "מיץ"), ("торт", "עוגה"), ("мороженое", "גלידה"), ("овощи", "ירקות"),
]
ADJS = [
    ("большой", "גדול"), ("маленький", "קטן"), ("хороший", "טוב"), ("плохой", "רע"),
    ("новый", "חדש"), ("старый", "ישן"), ("дорогой", "יקר"), ("дешёвый", "זול"),
    ("горячий", "חם"), ("холодный", "קר"), ("вкусный", "טעים"), ("красивый", "יפה"),
]
TIMES = [
    ("сегодня", "היום"), ("завтра", "מחר"), ("вчера", "אתמול"), ("сейчас", "עכשיו"),
    ("утром", "בבוקר"), ("днём", "בצהריים"), ("вечером", "בערב"), ("ночью", "בלילה"),
    ("всегда", "תמיד"), ("иногда", "לפעמים"), ("часто", "לעתים קרובות"), ("редко", "לעתים רחוקות"),
]

def expand_patterns(patterns):
    """patterns: list of (ru_tpl, he_tpl, slots_dict_list) or simple (ru, he, translit?)"""
    out = []
    for p in patterns:
        if len(p) >= 2 and "{" not in p[0]:
            row = [p[0], p[1]]
            if len(p) > 2: row.append(p[2])
            out.append(tuple(row))
        else:
            # already concrete
            out.append(p)
    return out

def chunk_lessons(title_base_he, title_base_ru, all_phrase_rows, per=6, biases=None, tip=None, dialogues=None):
    """Split a big phrase list into lesson specs of `per` phrases each with overlap."""
    biases = biases or ["listen", "balanced", "speak", "build", "balanced"]
    specs = []
    i = 0
    lesson_i = 0
    n = len(all_phrase_rows)
    step = max(3, per - 2)  # overlap for repetition
    while i < n:
        chunk = all_phrase_rows[i:i + per]
        if len(chunk) < 4 and lesson_i > 0:
            break
        if len(chunk) < 4:
            # pad from start
            chunk = all_phrase_rows[:per]
        ph = phrases(*chunk)
        bias = biases[lesson_i % len(biases)]
        th = f"{title_base_he} · {lesson_i + 1}"
        tr = f"{title_base_ru} {lesson_i + 1}"
        dlg = None
        if dialogues and lesson_i < len(dialogues):
            dlg = dialogues[lesson_i]
        elif lesson_i % 3 == 1 and len(chunk) >= 4:
            dlg = dialogue(
                [
                    {"speaker": "npc", "ru": chunk[0][0]},
                    {"speaker": "user", "ru": chunk[1][0]},
                    {"speaker": "npc", "ru": chunk[2][0]},
                    {"speaker": "user", "ru": chunk[3][0]},
                ],
                ["Не знаю", "Помогите", "Сколько это?"],
            )
        specs.append((th, tr, ph, tip, dlg, bias, False))
        lesson_i += 1
        i += step
        if lesson_i > 40:  # safety
            break
    return specs

def with_checkpoint(specs, every=8, pool_phrases=None, unit_label="חזרה"):
    """Insert checkpoint lessons every `every` regular lessons."""
    out = []
    buf = []
    count = 0
    cp_i = 0
    for spec in specs:
        out.append(spec)
        count += 1
        # collect phrases from this lesson
        for p in spec[2]:
            buf.append((p["ru"], p["he"], p.get("translit")))
        if count % every == 0:
            cp_i += 1
            # take last unique-ish phrases
            seen = set()
            pool = []
            for row in reversed(buf):
                if row[0] not in seen:
                    seen.add(row[0])
                    pool.append(row)
                if len(pool) >= 8:
                    break
            pool = list(reversed(pool))
            if len(pool) < 6 and pool_phrases:
                pool = pool_phrases[:8]
            if len(pool) >= 6:
                out.append((
                    f"שער {unit_label} {cp_i}",
                    f"Контроль {cp_i}",
                    phrases(*pool),
                    "שער חזרה — חובה לעבור כדי להמשיך",
                    None,
                    "listen",
                    True,
                ))
    return out
