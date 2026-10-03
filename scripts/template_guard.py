# -*- coding: utf-8 -*-
"""Guard rails for template-generated sentences (Russian).

Root cause of «Мне нужен страна.» / «Сколько стоит подруга?» / «Без тарелка
трудно.» / «Тема разговора — идеализм.»: the old generators
(vocab_bank.generate_lemma_sentences / natural_rows_for_lemma, called with
theme=None) filled open slot frames with *any* unused bank lemma in its
dictionary form — regardless of part of speech, gender, case or the unit's
topic — and padded advanced units with meta sentences that talk *about* a
word («Давайте разберём слово «X»») instead of using it.  The Hebrew side was
built the same way («זו שאלה די משפטי», «יהיה צריך לטייל/לנסוע שוב»).

This module is the single source of truth for:
  * SAFE_NOUNS     – the only words allowed into a slot (concrete nouns with
                     verified Hebrew gloss, Hebrew gender and the Russian
                     accusative form, so case agreement is always right)
  * TEMPLATES      – the only slot templates still in use, each limited to
                     the noun categories that make sense in it
  * slot_ok()      – hard rejection rules (POS, placeholders, whitelist)
  * LEGACY_FRAMES / classify_legacy() – detector for old generated items
"""
import re

FUNC_POS = {"conj", "prep", "pron", "adv", "intj", "v", "adj", "num", "phrase", "other"}
PLACEHOLDER_RE = re.compile(r"[0-9]")
# Hebrew side of a bank entry / generated row that is not real Hebrew
HE_PLACEHOLDER_RE = re.compile(r"[0-9A-Za-zА-Яа-яЁёΑ-Ωα-ωά-ώ]|עניין/|לפעול/|קשור ל-")

# lemma -> (hebrew, hebrew gender m/f/p, category, russian accusative form)
SAFE_NOUNS = {
    # food & drink
    "хлеб": ("לחם", "m", "food", "хлеб"), "чай": ("תה", "m", "food", "чай"),
    "кофе": ("קפה", "m", "food", "кофе"), "молоко": ("חלב", "m", "food", "молоко"),
    "сыр": ("גבינה", "f", "food", "сыр"), "рис": ("אורז", "m", "food", "рис"),
    "суп": ("מרק", "m", "food", "суп"), "салат": ("סלט", "m", "food", "салат"),
    "сок": ("מיץ", "m", "food", "сок"), "торт": ("עוגה", "f", "food", "торт"),
    "мороженое": ("גלידה", "f", "food", "мороженое"), "яблоко": ("תפוח", "m", "food", "яблоко"),
    "банан": ("בננה", "f", "food", "банан"), "апельсин": ("תפוז", "m", "food", "апельсин"),
    "вода": ("מים", "p", "food", "воду"), "рыба": ("דג", "m", "food", "рыбу"),
    "курица": ("עוף", "m", "food", "курицу"), "шоколад": ("שוקולד", "m", "food", "шоколад"),
    # household / personal objects
    "ключ": ("מפתח", "m", "object", "ключ"), "зонт": ("מטרייה", "f", "object", "зонт"),
    "сумка": ("תיק", "m", "object", "сумку"), "телефон": ("טלפון", "m", "object", "телефон"),
    "ложка": ("כף", "f", "object", "ложку"), "вилка": ("מזלג", "m", "object", "вилку"),
    "нож": ("סכין", "f", "object", "нож"), "тарелка": ("צלחת", "f", "object", "тарелку"),
    "чашка": ("ספל", "m", "object", "чашку"), "полотенце": ("מגבת", "f", "object", "полотенце"),
    "мыло": ("סבון", "m", "object", "мыло"), "ручка": ("עט", "m", "object", "ручку"),
    "книга": ("ספר", "m", "object", "книгу"), "тетрадь": ("מחברת", "f", "object", "тетрадь"),
    "билет": ("כרטיס", "m", "object", "билет"), "очки": ("משקפיים", "p", "object", "очки"),
    "паспорт": ("דרכון", "m", "object", "паспорт"), "кошелёк": ("ארנק", "m", "object", "кошелёк"),
}

# Slot templates still allowed: (id, russian, hebrew, allowed categories)
TEMPLATES = [
    ("want",  "Я хочу {acc}.",              "אני רוצה {he}.",        {"food"}),
    ("give",  "Дайте, пожалуйста, {acc}.",  "תנו לי {he}, בבקשה.",   {"food", "object"}),
    ("have",  "У нас дома есть {nom}.",     "יש לנו {he} בבית.",     {"food", "object"}),
    ("where", "Где {nom}?",                 "איפה ה{he}?",           {"object"}),
]
HE_THIS = {"m": "זה", "f": "זאת", "p": "אלה"}


def norm(s):
    return (s or "").strip().lower().replace("ё", "е")


_SAFE_N = {norm(k): k for k in SAFE_NOUNS}


def slot_ok(entry, tmpl_id=None):
    """True only if a bank entry may fill a slot of template tmpl_id."""
    lem = entry.get("lemma") or ""
    if not lem or PLACEHOLDER_RE.search(lem):
        return False
    if entry.get("pos") in FUNC_POS:
        return False
    if HE_PLACEHOLDER_RE.search(entry.get("he") or ""):
        return False
    key = _SAFE_N.get(norm(lem))
    if not key:
        return False
    if tmpl_id:
        for tid, _, _, cats in TEMPLATES:
            if tid == tmpl_id:
                return SAFE_NOUNS[key][2] in cats
    return True


def render(tmpl_id, lemma):
    key = _SAFE_N.get(norm(lemma))
    if not key:
        return None
    he, g, cat, acc = SAFE_NOUNS[key]
    for tid, t_ru, t_he, cats in TEMPLATES:
        if tid == tmpl_id and cat in cats:
            return t_ru.format(nom=key, acc=acc), t_he.format(he=he, this=HE_THIS[g])
    return None


def safe_forms():
    out = set()
    for lem in SAFE_NOUNS:
        for t in TEMPLATES:
            r = render(t[0], lem)
            if r:
                out.add(r[0])
    return out


# ---- detector for items produced by the OLD generator -------------------
# Every open frame the old vocab_bank used (TEMPLATES_A1, TEMPLATES_ADV and
# natural_rows_for_lemma).  {x} = slot.
LEGACY_FRAMES = [
    'Это {x} {x}.', 'Это {x}.', 'Где {x}?', 'У меня есть {x}.', 'Мне нужен {x}.', 'Я хочу {x}.',
    'Я люблю {x}.', 'Сегодня я хочу {x}.', 'Мы ищем {x}.',
    'Он покупает {x}.', 'Она пьёт чай и берёт {x}.', 'Сколько стоит {x}?',
    'Мой {x} дома.', 'Ваш {x} здесь?', 'Я не понимаю слово «{x}».', 'Можно {x}?',
    'Дайте, пожалуйста, {x}.', 'Я живу рядом — вижу {x}.', 'После работы я хочу {x}.',
    'Без {x} трудно.', 'Кстати, где {x}?', 'Сначала нужно {x}.', 'Вот мой {x}.',
    'Это не {x}.', 'Тема разговора — {x}.', 'Сегодня речь о теме «{x}».',
    'Меня интересует тема «{x}».', 'Давайте разберём слово «{x}».',
    'В новостях часто встречается слово «{x}».', 'Для меня «{x}» — важная тема.',
    'Без понятия «{x}» трудно понять текст.', 'Ключевое слово здесь — «{x}».',
    'В отчёте отдельный раздел — {x}.', 'В отчёте отдельный раздел — «{x}».',
    'Кстати, давайте уточним термин «{x}».', 'Стоит {x} заранее.', 'Я планирую {x}.',
    'Сейчас нужно {x}.', 'Пора {x}.', 'Лучше не {x} в спешке.', 'Придётся {x} ещё раз.',
    'Многие предпочитают {x}.', 'Эксперты советуют {x} осторожно.',
    'Я стараюсь {x} каждый день.', 'Это довольно {x} вопрос.', 'Нам нужен {x} ответ.',
    'Это довольно {x} подход.', 'Это {x} случай, не исключение.', 'Перед нами {x} выбор.',
    'Перед нами довольно {x} пример.', 'Мы действуем {x}.', 'Он ответил {x}.',
    'Сделайте это {x}.', 'Всё прошло {x}.',
]


def _frame_re(f):
    if "{x} {x}" in f:  # adjective + noun frame: capture both words as one slot
        return re.compile("^" + re.escape(f.replace("{x} {x}", "{x}")).replace(re.escape("{x}"), r"(?P<s>\S+ .+?)") + "$")
    return re.compile("^" + re.escape(f).replace(re.escape("{x}"), "(?P<s>.+?)") + "$")


LEGACY_PATTERNS = [(f, _frame_re(f)) for f in LEGACY_FRAMES]
META_WORDS = ("слово", "тем", "термин", "понятия", "раздел")
VERB_FRAMES = {f for f in LEGACY_FRAMES if any(f.startswith(p) for p in (
    "Я хочу", "Сегодня я хочу", "После работы", "Можно", "Сначала", "Стоит", "Я планирую",
    "Сейчас нужно", "Пора", "Лучше не", "Придётся", "Многие", "Эксперты", "Я стараюсь"))}
MASC_ONLY = {"Мне нужен {x}.", "Мой {x} дома.", "Вот мой {x}.", "Ваш {x} здесь?"}
ACC_FRAMES = {"Он покупает {x}.", "Она пьёт чай и берёт {x}.", "Я живу рядом — вижу {x}.",
              "Мы ищем {x}.", "Я люблю {x}."}
OBJECT_FRAMES = {"Сколько стоит {x}?", "Он покупает {x}.", "Она пьёт чай и берёт {x}.",
                 "Дайте, пожалуйста, {x}.", "Мой {x} дома.", "Ваш {x} здесь?", "Без {x} трудно."}
NON_OBJECT_THEMES = {"people", "places", "time", "body", "weather", "society", "abstract",
                     "nuance", "mastery", "discourse", "daily"}
INDECL = re.compile(r"(о|е|и|у|ю|э)$")
# Hebrew built by the same frames: adjective gender clash, "(מושלם)" glosses, pseudo-words
HE_BROKEN_RE = re.compile(
    r"\(מושלם\)|עניין/|לפעול/|קשור ל-|[A-Za-zА-Яа-яЁёΑ-Ωα-ωά-ώ]"
    r"|^(זו שאלה די|זו גישה די|אנחנו צריכים תשובה|לפנינו בחירה|לפנינו דוגמה די) [^ ]*[^התי \.]\.$"
)


def _fem_or_neut(w):
    return bool(re.search(r"(а|я|о|е|ь|ы|и)$", w))


def classify_legacy(ru, he, bank_by_lemma=None, safe=None):
    """Return (frame, reason) for an old generated row, or None."""
    if safe and ru in safe:
        return None
    for f, rx in LEGACY_PATTERNS:
        m = rx.match(ru or "")
        if not m:
            continue
        s = m.group("s")
        e = (bank_by_lemma or {}).get(norm(s)) or {}
        if any(w in f for w in META_WORDS) or f.startswith("Тема разговора"):
            return f, "meta filler (talks about the word instead of using it)"
        if HE_PLACEHOLDER_RE.search(he or "") or PLACEHOLDER_RE.search(s):
            return f, "placeholder / pseudo-word"
        if f in VERB_FRAMES and " " not in s and re.search(r"(ть|ти|чь|ться|тись)$", s):
            return f, "bare infinitive in a generic frame"
        if HE_BROKEN_RE.search(he or ""):
            return f, "broken Hebrew (gender clash / gloss in slot)"
        if f == "Без {x} трудно." and not INDECL.search(s):
            return f, "case error (nominative after без)"
        if f in MASC_ONLY and _fem_or_neut(s.split()[-1]):
            return f, "gender agreement error"
        if f in ACC_FRAMES and re.search(r"(а|я)$", s):
            return f, "case error (nominative instead of accusative)"
        if f == "Это {x} {x}.":
            adj, _, noun = s.partition(" ")
            if re.search(r"(ый|ий|ой)$", adj) and re.search(r"(а|я|о|е|ие)$", noun):
                return f, "gender agreement error"
        if f in OBJECT_FRAMES and e.get("theme") in NON_OBJECT_THEMES:
            return f, "person/place/abstract noun in object slot"
        return f, "retired template (off-topic filler)"
    return None
