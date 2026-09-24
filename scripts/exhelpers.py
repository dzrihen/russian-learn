
"""Exercise builders for curriculum generation."""
def words_of(ru: str):
    return ru.replace("?", "").replace("!", "").replace(".", "").replace(",", "").split()

WRONG_POOL = [
    "אני רעב", "מחר נלך", "זה יקר מדי", "הוא לא בבית", "יש לי כלב",
    "האוטובוס מאחר", "אני לא מבין", "תודה רבה", "בוקר טוב", "לילה טוב",
    "איפה השירותים", "כמה זה עולה", "אני גר בתל אביב", "היא מורה",
    "מזג האוויר חם", "אני אוהב קפה", "בוא נלך הביתה", "סליחה על האיחור",
]

def pick_wrong(correct_he, n=3):
    out = []
    for w in WRONG_POOL:
        if w != correct_he and w not in out:
            out.append(w)
        if len(out) >= n:
            break
    while len(out) < n:
        out.append("לא נכון")
    return out

def listen_choice(ru, he, wrong, translit=None, tip=None):
    choices = [{"he": he, "correct": True}] + [{"he": w, "correct": False} for w in wrong[:3]]
    ex = {"type": "listen_choice", "ru": ru, "choices": choices}
    if translit: ex["translit"] = translit
    if tip: ex["tip"] = tip
    return ex

def listen_order(ru, tip=None):
    ex = {"type": "listen_order", "ru": ru, "words": words_of(ru)}
    if tip: ex["tip"] = tip
    return ex

def sentence_build(he, ru, distractors=None, tip=None):
    ex = {"type": "sentence_build", "he": he, "ru": ru, "words": words_of(ru),
          "distractors": distractors or []}
    if tip: ex["tip"] = tip
    return ex

def translate(he, ru, distractors=None, tip=None):
    ex = {"type": "translate_he_ru", "he": he, "ru": ru, "words": words_of(ru),
          "distractors": distractors or []}
    if tip: ex["tip"] = tip
    return ex

def fill_blank(sentence, answer, options, he=None, tip=None):
    opts = []
    for o in options:
        if isinstance(o, dict):
            opts.append(o)
        else:
            opts.append({"ru": o, "correct": o == answer})
    if not any(o.get("correct") for o in opts):
        opts.append({"ru": answer, "correct": True})
    ex = {"type": "fill_blank", "sentence": sentence, "answer": answer, "options": opts}
    if he: ex["he"] = he
    if tip: ex["tip"] = tip
    return ex

def match_pairs(pairs, tip=None):
    ex = {"type": "match_pairs", "pairs": pairs}
    if tip: ex["tip"] = tip
    return ex

def speak_repeat(ru, he=None, translit=None, tip=None):
    ex = {"type": "speak_repeat", "ru": ru}
    if he: ex["he"] = he
    if translit: ex["translit"] = translit
    if tip: ex["tip"] = tip
    return ex

def dialogue(turns, distractors, tip=None):
    ex = {"type": "dialogue", "turns": turns, "distractors": distractors}
    if tip: ex["tip"] = tip
    return ex

def alphabet_intro(letter, name_he, example, example_he, tip=None):
    ex = {"type": "alphabet", "letter": letter, "nameHe": name_he,
          "example": example, "exampleHe": example_he}
    if tip: ex["tip"] = tip
    return ex

def alphabet_quiz(prompt_he, answer, choices, tip=None):
    ch = [{"ch": c, "correct": c == answer} for c in choices]
    ex = {"type": "alphabet", "promptHe": prompt_he, "quiz": {"answer": answer, "choices": ch}}
    if tip: ex["tip"] = tip
    return ex

def lesson(lid, level, unit_id, title_he, title_ru, exercises, xp=15):
    return {"id": lid, "level": level, "unitId": unit_id, "titleHe": title_he,
            "titleRu": title_ru, "xp": xp, "exercises": exercises}

def exercises_from_phrases(phrases, grammar_tip=None, include_dialogue=None):
    exs = []
    p0 = phrases[0]
    exs.append(listen_choice(p0["ru"], p0["he"], pick_wrong(p0["he"]), p0.get("translit"), grammar_tip))
    if len(phrases) > 1:
        exs.append(listen_order(phrases[1]["ru"]))
    p = phrases[min(2, len(phrases)-1)]
    exs.append(sentence_build(p["he"], p["ru"], p.get("distractors", ["и", "но", "уже", "очень"])))
    p = phrases[min(3, len(phrases)-1)]
    exs.append(translate(p["he"], p["ru"], p.get("distractors", ["мы", "вы", "они"])))
    for p in phrases:
        if p.get("blank"):
            exs.append(fill_blank(p["blank"], p["answer"], p["options"], p.get("he"), p.get("tip")))
            break
    else:
        ws = words_of(phrases[0]["ru"])
        if len(ws) >= 2:
            ans = ws[-1]
            sent = " ".join(ws[:-1] + ["___"])
            exs.append(fill_blank(sent, ans, [ans, "дом", "хорошо", "сейчас"], phrases[0]["he"]))
    pairs = [{"ru": x["ru"], "he": x["he"]} for x in phrases[:4]]
    if len(pairs) >= 3:
        exs.append(match_pairs(pairs))
    p = phrases[min(1, len(phrases)-1)]
    exs.append(speak_repeat(p["ru"], p["he"], p.get("translit")))
    p = phrases[min(4, len(phrases)-1)]
    exs.append(listen_choice(p["ru"], p["he"], pick_wrong(p["he"]), p.get("translit")))
    p = phrases[min(5, len(phrases)-1)] if len(phrases) > 5 else phrases[-1]
    exs.append(sentence_build(p["he"], p["ru"], ["да", "нет", "пожалуйста"]))
    p = phrases[-1]
    exs.append(speak_repeat(p["ru"], p["he"], p.get("translit")))
    if include_dialogue:
        exs.insert(6, include_dialogue)
    if len(phrases) > 2:
        exs.append(listen_order(phrases[2]["ru"]))
    return exs[:14]

def make_unit_lessons(level, unit_id, unit_idx, lesson_specs):
    lessons = []
    for i, spec in enumerate(lesson_specs):
        title_he, title_ru, phrases = spec[0], spec[1], spec[2]
        tip = spec[3] if len(spec) > 3 else None
        dlg = spec[4] if len(spec) > 4 else None
        lid = f"{level.lower()}-u{unit_idx:02d}-l{i+1:02d}"
        exs = exercises_from_phrases(phrases, tip, dlg)
        lessons.append(lesson(lid, level, unit_id, title_he, title_ru, exs, xp=12 + (i % 5)))
    return lessons

def phrases(*rows):
    out = []
    for r in rows:
        d = {"ru": r[0], "he": r[1]}
        if len(r) > 2 and r[2]:
            d["translit"] = r[2]
        out.append(d)
    return out

def theme_bank(level_prefix, themes):
    units = []
    for uid, the, tru, specs in themes:
        unit_idx = int(uid.split("u")[1])
        lessons = make_unit_lessons(level_prefix, uid, unit_idx, specs)
        units.append({"id": uid, "titleHe": the, "titleRu": tru, "lessons": lessons})
    return units
