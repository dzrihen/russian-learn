/* Curriculum loader — merges level data from RL_LEVEL_* globals */
(function (global) {
  "use strict";

  const LEVEL_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"];

  const loaded = {};
  let levels = [];
  let ready = false;
  const lessonIndex = {};

  function collectFromWindow() {
    levels = [];
    Object.keys(lessonIndex).forEach((k) => delete lessonIndex[k]);
    LEVEL_ORDER.forEach((id) => {
      const obj = global["RL_LEVEL_" + id];
      if (obj) {
        loaded[id] = true;
        levels.push(obj);
        (obj.units || []).forEach((u) => {
          (u.lessons || []).forEach((les) => {
            lessonIndex[les.id] = les;
          });
        });
      }
    });
    ready = levels.length > 0;
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const m = src.match(/([a-c][12])\.js$/i);
      if (m && global["RL_LEVEL_" + m[1].toUpperCase()]) {
        resolve();
        return;
      }
      const s = document.createElement("script");
      s.src = src;
      s.async = false;
      s.onload = () => resolve();
      s.onerror = () => reject(new Error("fail " + src));
      document.head.appendChild(s);
    });
  }

  const LEVEL_FILES = {
    A1: "./data/a1.js",
    A2: "./data/a2.js",
    B1: "./data/b1.js",
    B2: "./data/b2.js",
    C1: "./data/c1.js",
    C2: "./data/c2.js",
  };

  async function ensureLevel(levelId) {
    if (loaded[levelId] || global["RL_LEVEL_" + levelId]) {
      collectFromWindow();
      return;
    }
    const src = LEVEL_FILES[levelId];
    if (!src) return;
    await loadScript(src);
    collectFromWindow();
  }

  async function ensureAll() {
    for (const id of LEVEL_ORDER) {
      await ensureLevel(id);
    }
  }

  function getLevel(id) {
    return levels.find((l) => l.id === id) || null;
  }

  function lessonIdsForLevel(levelId) {
    const lv = getLevel(levelId);
    if (!lv) return [];
    const ids = [];
    (lv.units || []).forEach((u) => (u.lessons || []).forEach((l) => ids.push(l.id)));
    return ids;
  }

  function totalLessons() {
    return LEVEL_ORDER.reduce((acc, id) => acc + lessonIdsForLevel(id).length, 0);
  }

  function getLesson(id) {
    return lessonIndex[id] || null;
  }

  function isLevelComplete(levelId) {
    const ids = lessonIdsForLevel(levelId);
    if (!ids.length) return false;
    return ids.every((id) => RLProgress.isComplete(id));
  }

  function isLevelUnlocked(levelId) {
    const idx = LEVEL_ORDER.indexOf(levelId);
    if (idx <= 0) return true;
    const prev = LEVEL_ORDER[idx - 1];
    const ids = lessonIdsForLevel(prev);
    if (!ids.length) return true;
    const done = RLProgress.countCompleted(ids);
    return done >= Math.ceil(ids.length * 0.8) || isLevelComplete(prev);
  }

  function nextLevelId(levelId) {
    const idx = LEVEL_ORDER.indexOf(levelId);
    if (idx < 0 || idx >= LEVEL_ORDER.length - 1) return null;
    return LEVEL_ORDER[idx + 1];
  }

  function nextLesson() {
    const cur = (RLProgress.get().currentLevel) || "A1";
    const order = [cur].concat(LEVEL_ORDER.filter((x) => x !== cur));
    for (const lid of order) {
      if (!isLevelUnlocked(lid) && lid !== "A1") continue;
      const ids = lessonIdsForLevel(lid);
      for (const id of ids) {
        if (!RLProgress.isComplete(id)) return getLesson(id);
      }
    }
    return null;
  }

  // Collect immediately if scripts already present; else load
  collectFromWindow();
  const bootPromise = ready
    ? Promise.resolve()
    : ensureAll().then(() => { collectFromWindow(); ready = true; })
        .catch((e) => { console.error(e); collectFromWindow(); ready = levels.length > 0; });

  // Re-collect after short delay in case scripts still parsing
  setTimeout(collectFromWindow, 0);
  setTimeout(collectFromWindow, 100);

  global.RLCurriculum = {
    get levels() { return levels; },
    get ready() { return ready && levels.length > 0; },
    bootPromise,
    ensureLevel,
    ensureAll,
    getLevel,
    getLesson,
    lessonIdsForLevel,
    totalLessons,
    isLevelComplete,
    isLevelUnlocked,
    nextLevelId,
    nextLesson,
    LEVEL_ORDER,
    _collect: collectFromWindow,
  };
})(window);
