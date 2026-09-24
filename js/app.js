/* App router + screens */
(function () {
  "use strict";

  const LEVEL_COLORS = {
    A1: "#58CC02",
    A2: "#1CB0F6",
    B1: "#CE82FF",
    B2: "#FF9600",
    C1: "#FF4B4B",
    C2: "#654ea3",
  };

  const appEl = document.getElementById("app");
  const navEl = document.getElementById("bottom-nav");
  let route = "home";
  let activeLevel = null;
  let lessonRunner = null;

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function showNav(v) {
    navEl.classList.toggle("hidden", !v);
  }

  function setActiveNav(name) {
    navEl.querySelectorAll(".nav-btn").forEach((b) => {
      b.classList.toggle("active", b.dataset.route === name);
    });
  }

  function statsBar() {
    const p = RLProgress.get();
    const total = RLCurriculum.totalLessons();
    const done = Object.keys(p.completed).length;
    const pct = total ? Math.round((done / total) * 100) : 0;
    return (
      '<div class="stats-bar">' +
      '<span class="stat-pill streak">🔥 ' +
      (p.streak || 0) +
      "</span>" +
      '<span class="stat-pill xp">⚡ ' +
      (p.xp || 0) +
      " XP</span>" +
      '<span class="stat-pill pct">✅ ' +
      pct +
      "%</span>" +
      '<span class="stat-pill vocab" title="מילים שנלמדו">📚 ' +
      ((RLCurriculum.vocabLearnedCount && RLCurriculum.vocabLearnedCount()) || 0) +
      "</span>" +
      "</div>"
    );
  }

  function installTipHtml() {
    if (RLProgress.get().installTipDismissed) return "";
    return (
      '<div class="install-tip" id="install-tip">' +
      '<div class="tip-body"><strong>התקן למסך הבית</strong>' +
      "<ol><li>ב־Chrome: תפריט ⋮ ← הוסף למסך הבית</li>" +
      "<li>ב־Safari: שתף □↑ ← הוסף למסך הבית</li></ol></div>" +
      '<button type="button" class="tip-dismiss" id="tip-x" aria-label="סגור">✕</button></div>'
    );
  }

  // ——— Screens ———

  function renderHome() {
    showNav(true);
    setActiveNav("home");
    const next = RLCurriculum.nextLesson();
    const p = RLProgress.get();
    const total = RLCurriculum.totalLessons();
    const done = Object.keys(p.completed).length;

    let continueHtml;
    if (next) {
      continueHtml =
        '<div class="continue-card">' +
        '<div class="label">המשך ללמוד · ' +
        next.level +
        "</div>" +
        '<div class="title">' +
        escape(next.titleHe) +
        "</div>" +
        '<button type="button" class="btn" id="btn-continue">המשך ←</button></div>';
    } else {
      continueHtml =
        '<div class="card"><h2>סיימת את כל השיעורים! 🎉</h2>' +
        '<p class="sub">אפשר לחזור ולתרגל שיעורים שהשלמת.</p>' +
        '<button type="button" class="btn btn-primary" id="btn-levels">לרמות</button></div>';
    }

    appEl.innerHTML =
      statsBar() +
      installTipHtml() +
      '<div class="hero"><div class="owl">🐻</div>' +
      "<h1>לומדים רוסית</h1>" +
      '<p class="sub" style="color:var(--muted)">מסלול עמוק A1→C2 · ~6500 שיעורים · אוצר מילים רחב</p></div>' +
      continueHtml +
      '<div class="card">' +
      "<h2>ההתקדמות שלך</h2>" +
      '<p class="sub">אתה בשיעור ' +
      Math.min(done + 1, total) +
      " מתוך " +
      total +
      "</p>" +
      '<div class="progress-track"><div class="progress-fill" style="width:' +
      (total ? Math.round((done / total) * 100) : 0) +
      '%"></div></div>' +
      '<p class="sub" style="margin-top:10px">' +
      done +
      " שיעורים הושלמו</p>" +
      '<button type="button" class="btn btn-ghost btn-sm" id="btn-path" style="margin-top:10px;width:100%">פתח מסלול</button>' +
      "</div>" +
      '<div class="card"><h2>הגדרות</h2>' +
      '<div class="toggle-row"><span>תעתיק (לטינית)</span>' +
      '<button type="button" class="toggle' +
      (p.settings.translit ? " on" : "") +
      '" id="tog-translit" aria-label="תעתיק"></button></div>' +
      '<div class="toggle-row"><span>צליל TTS</span>' +
      '<button type="button" class="toggle' +
      (p.settings.sound !== false ? " on" : "") +
      '" id="tog-sound" aria-label="צליל"></button></div>' +
      '<div class="toggle-row"><span>דיבור איטי ללומדים (~0.9)</span>' +
      '<button type="button" class="toggle' +
      (p.settings.speechRate !== "normal" ? " on" : "") +
      '" id="tog-slow" aria-label="קצב דיבור"></button></div>' +
      "</div>";

    const tipX = qs("#tip-x");
    if (tipX) {
      tipX.onclick = () => {
        RLProgress.dismissInstallTip();
        qs("#install-tip") && qs("#install-tip").remove();
      };
    }
    const bc = qs("#btn-continue");
    if (bc) bc.onclick = () => startLesson(next.id);
    const bl = qs("#btn-levels");
    if (bl) bl.onclick = () => navigate("levels");
    const bp = qs("#btn-path");
    if (bp) bp.onclick = () => navigate("path");
    qs("#tog-translit").onclick = function () {
      const on = !RLProgress.get().settings.translit;
      RLProgress.setSetting("translit", on);
      this.classList.toggle("on", on);
    };
    qs("#tog-sound").onclick = function () {
      const on = RLProgress.get().settings.sound === false;
      RLProgress.setSetting("sound", on);
      this.classList.toggle("on", on);
    };
    qs("#tog-slow").onclick = function () {
      const slow = RLProgress.get().settings.speechRate === "normal";
      RLProgress.setSetting("speechRate", slow ? "slow" : "normal");
      this.classList.toggle("on", slow);
    };
  }

  function renderLevels() {
    showNav(true);
    setActiveNav("levels");
    const levels = RLCurriculum.levels;
    let html = statsBar() + "<h1 style='margin-bottom:12px'>רמות CEFR</h1><div class='level-grid'>";
    levels.forEach((lv, i) => {
      const ids = RLCurriculum.lessonIdsForLevel(lv.id);
      const done = RLProgress.countCompleted(ids);
      const pct = ids.length ? Math.round((done / ids.length) * 100) : 0;
      const unlocked = i === 0 || RLCurriculum.isLevelUnlocked(lv.id);
      html +=
        '<button type="button" class="level-card' +
        (unlocked ? "" : " locked") +
        '" data-level="' +
        lv.id +
        '">' +
        '<div class="level-badge" style="background:' +
        (LEVEL_COLORS[lv.id] || "#58CC02") +
        '">' +
        lv.id +
        "</div>" +
        '<div class="level-info"><strong>' +
        escape(lv.titleHe) +
        "</strong>" +
        "<span>" +
        escape(lv.subtitleHe) +
        " · " +
        ids.length +
        " שיעורים</span>" +
        '<div class="progress-track"><div class="progress-fill" style="width:' +
        pct +
        '%;background:' +
        (LEVEL_COLORS[lv.id] || "#58CC02") +
        '"></div></div>' +
        "<span>" +
        done +
        "/" +
        ids.length +
        (unlocked ? "" : " 🔒") +
        "</span>" +
        (unlocked
          ? ""
          : (function () {
              const prev = RLCurriculum.LEVEL_ORDER[i - 1];
              const rem = RLCurriculum.remainingToUnlockNext
                ? RLCurriculum.remainingToUnlockNext(prev)
                : 0;
              return (
                '<span class="unlock-hint">נותרו ' +
                rem +
                " שיעורים ברמה " +
                prev +
                " לפני הפתיחה</span>"
              );
            })()) +
        "</div></button>";
    });
    html += "</div>";
    appEl.innerHTML = html;
    appEl.querySelectorAll(".level-card").forEach((btn) => {
      btn.onclick = () => {
        const id = btn.dataset.level;
        if (!RLCurriculum.isLevelUnlocked(id) && id !== "A1") {
          // still allow viewing path but gently
        }
        RLProgress.setLevel(id);
        activeLevel = id;
        navigate("path");
      };
    });
  }

  function renderPath() {
    showNav(true);
    setActiveNav("path");
    const levelId = activeLevel || RLProgress.get().currentLevel || "A1";
    activeLevel = levelId;
    const level = RLCurriculum.getLevel(levelId);
    if (!level) {
      appEl.innerHTML = "<p>רמה לא נמצאה</p>";
      return;
    }
    const ordered = RLCurriculum.lessonIdsForLevel(levelId);

    let html =
      '<div class="path-header">' +
      statsBar() +
      "<h1>" +
      levelId +
      " · " +
      escape(level.titleHe) +
      "</h1>" +
      '<p class="sub" style="color:var(--muted)">' +
      escape(level.subtitleHe) +
      "</p>" +
      '<button type="button" class="btn btn-ghost btn-sm" id="btn-back-levels" style="margin-top:8px">← כל הרמות</button>' +
      "</div><div class='path-units'>";

    (level.units || []).forEach((unit, ui) => {
      html +=
        '<div class="unit-banner"><div class="unit-num">יחידה ' +
        (ui + 1) +
        '</div><div class="unit-title">' +
        escape(unit.titleHe) +
        '</div><div class="unit-ru ru">' +
        escape(unit.titleRu || "") +
        "</div></div>";

      (unit.lessons || []).forEach((les) => {
        const st = RLProgress.lessonStatus(les.id, ordered);
        let cls = "locked";
        let ico = "🔒";
        if (st === "done") {
          cls = "done";
          ico = "★";
        } else if (st === "current") {
          cls = "current";
          ico = les.checkpoint ? "⚑" : "▶";
        } else if (st === "unlocked") {
          cls = "unlocked";
          ico = les.checkpoint ? "⚑" : "○";
        }
        if (les.checkpoint) {
          cls += " checkpoint";
          if (st === "done") ico = "⚑";
        }
        // Allow redo of done; allow current; block locked
        html +=
          '<div class="path-node-wrap">' +
          '<div><button type="button" class="path-node ' +
          cls +
          '" data-id="' +
          les.id +
          '" data-st="' +
          st +
          '">' +
          ico +
          '</button><div class="node-label">' +
          escape(les.titleHe) +
          "</div></div></div>";
      });
    });
    html += "</div>";
    appEl.innerHTML = html;
    qs("#btn-back-levels").onclick = () => navigate("levels");
    appEl.querySelectorAll(".path-node").forEach((btn) => {
      btn.onclick = () => {
        const st = btn.dataset.st;
        if (st === "locked") return;
        startLesson(btn.dataset.id);
      };
    });
  }

  function renderProgress() {
    showNav(true);
    setActiveNav("progress");
    const p = RLProgress.get();
    const total = RLCurriculum.totalLessons();
    const done = Object.keys(p.completed).length;
    const pct = total ? Math.round((done / total) * 100) : 0;

    let rows = "";
    RLCurriculum.levels.forEach((lv) => {
      const ids = RLCurriculum.lessonIdsForLevel(lv.id);
      const d = RLProgress.countCompleted(ids);
      const lp = ids.length ? Math.round((d / ids.length) * 100) : 0;
      rows +=
        '<div class="level-prog-row"><span class="tag">' +
        lv.id +
        '</span><div style="flex:1"><div class="progress-track"><div class="progress-fill" style="width:' +
        lp +
        "%;background:" +
        (LEVEL_COLORS[lv.id] || "#58CC02") +
        '"></div></div></div><span style="font-size:0.8rem;color:var(--muted)">' +
        d +
        "/" +
        ids.length +
        "</span></div>";
    });

    appEl.innerHTML =
      statsBar() +
      '<div class="card" style="text-align:center">' +
      '<div class="pct-big">' +
      pct +
      "%</div>" +
      '<div class="pct-label">אתה בשיעור ' +
      Math.min(done + 1, total) +
      " מתוך " +
      total +
      "</div>" +
      "<p>🔥 רצף: <strong>" +
      (p.streak || 0) +
      "</strong> ימים · ⚡ <strong>" +
      (p.xp || 0) +
      "</strong> XP</p>" +
      "<p class=\"sub\">מילים שנלמדו: <strong>" +
      ((RLCurriculum.vocabLearnedCount && RLCurriculum.vocabLearnedCount()) || 0) +
      "</strong>" +
      (window.RL_META && RL_META.bankSize ? " · מאגר קורס ≈ " + RL_META.bankSize : "") +
      "</p></div>" +
      '<div class="card"><h2>לפי רמה</h2>' +
      rows +
      "</div>" +
      '<div class="card"><h2>טיפ</h2><p class="sub">שיעור אחד ביום ≈ 4–5 שנים לסיום A1→C2. יסוד רחב, חזרות ושערי ביקורת — אל תמהרו.</p></div>';
  }

  function startLesson(lessonId) {
    const lesson = RLCurriculum.getLesson(lessonId);
    if (!lesson) return;
    showNav(false);
    if (lessonRunner && lessonRunner.destroy) lessonRunner.destroy();

    appEl.innerHTML = '<div id="lesson-root"></div>';
    const root = qs("#lesson-root");

    lessonRunner = RLEngine.runLesson(lesson, root, {
      onExit() {
        if (lessonRunner && lessonRunner.destroy) lessonRunner.destroy();
        lessonRunner = null;
        navigate("path");
      },
      onComplete({ xp, perfect, mistakes }) {
        RLProgress.completeLesson(lesson.id, xp, perfect);
        // ensure next level unlock is reflected
        const lvl = lesson.level;
        if (RLCurriculum.isLevelComplete(lvl)) {
          const next = RLCurriculum.nextLevelId(lvl);
          if (next) RLProgress.setLevel(next);
        }
        showCelebration(lesson, xp, perfect, mistakes);
      },
    });
  }

  function showCelebration(lesson, xp, perfect, mistakes) {
    showNav(false);
    appEl.innerHTML =
      '<div class="celeb">' +
      '<div class="big">' +
      (perfect ? "🏆" : "🎉") +
      "</div>" +
      "<h1>" +
      (perfect ? "שיעור מושלם!" : "שיעור הושלם!") +
      "</h1>" +
      "<p>" +
      escape(lesson.titleHe) +
      "</p>" +
      '<div class="xp-gain">+' +
      xp +
      " XP</div>" +
      (mistakes
        ? '<p class="sub" style="color:var(--muted)">טעויות: ' + mistakes + " — מצוין שהמשכת!</p>"
        : "") +
      '<button type="button" class="btn btn-primary" id="btn-next-les">השיעור הבא</button>' +
      '<button type="button" class="btn btn-ghost" id="btn-to-path" style="margin-top:8px">חזרה למסלול</button>' +
      "</div>";

    qs("#btn-to-path").onclick = () => navigate("path");
    qs("#btn-next-les").onclick = () => {
      const next = RLCurriculum.nextLesson();
      if (next) startLesson(next.id);
      else navigate("home");
    };
  }

  function escape(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function navigate(name) {
    route = name;
    if (name === "home") renderHome();
    else if (name === "path") renderPath();
    else if (name === "levels") renderLevels();
    else if (name === "progress") renderProgress();
  }

  navEl.querySelectorAll(".nav-btn").forEach((btn) => {
    btn.onclick = () => navigate(btn.dataset.route);
  });

  // Boot: wait for curriculum (may lazy-load)
  function boot() {
    if (!globalReady()) {
      appEl.innerHTML = '<div class="boot">טוען תוכן לימודי…</div>';
      setTimeout(boot, 50);
      return;
    }
    activeLevel = RLProgress.get().currentLevel || "A1";
    navigate("home");
  }

  function globalReady() {
    return (
      window.RLCurriculum &&
      window.RLProgress &&
      window.RLEngine &&
      window.RLSpeech &&
      RLCurriculum.ready
    );
  }

  boot();
})();
