/* Speech: TTS (ru-RU) + optional SpeechRecognition — learner-friendly pacing */
(function (global) {
  "use strict";

  let preferredVoice = null;
  let voicesReady = false;
  let userGesture = false;

  function markGesture() {
    userGesture = true;
  }
  if (typeof document !== "undefined") {
    ["pointerdown", "keydown", "touchstart"].forEach((ev) => {
      document.addEventListener(ev, markGesture, { once: true, capture: true });
    });
  }

  function scoreVoice(v) {
    const name = v.name || "";
    const lang = (v.lang || "").toLowerCase();
    let s = 0;
    if (lang === "ru-ru") s += 20;
    else if (lang.startsWith("ru")) s += 12;
    if (/google|microsoft|neural|enhanced|premium|natural/i.test(name)) s += 8;
    if (/milena|katya|irina|tatyana|elena|kira|oksana|natalia|dasha/i.test(name)) s += 6;
    if (/female|woman|женщин/i.test(name)) s += 2;
    if (/male|мужск|yuri|pavel|dmitri/i.test(name)) s -= 1;
    if (/compact|online \(natural\) compact/i.test(name)) s -= 2;
    return s;
  }

  function pickVoice() {
    if (typeof speechSynthesis === "undefined") return;
    const voices = speechSynthesis.getVoices() || [];
    const ru = voices.filter(
      (v) => (v.lang || "").toLowerCase().startsWith("ru") || /russian|русск/i.test(v.name || "")
    );
    ru.sort((a, b) => scoreVoice(b) - scoreVoice(a));
    preferredVoice = ru[0] || null;
    voicesReady = true;
  }

  if (typeof speechSynthesis !== "undefined") {
    pickVoice();
    speechSynthesis.onvoiceschanged = pickVoice;
  }

  function learnerRate() {
    try {
      const s = (global.RLProgress && RLProgress.get().settings) || {};
      if (s.speechRate === "normal") return 1.0;
      return 0.9; // slow default for learners
    } catch (e) {
      return 0.9;
    }
  }

  function speak(text, opts) {
    if (!text || typeof speechSynthesis === "undefined") return Promise.resolve({ ok: false });
    opts = opts || {};
    return new Promise((resolve) => {
      try {
        speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(String(text));
        u.lang = "ru-RU";
        u.rate = opts.rate != null ? opts.rate : learnerRate();
        u.pitch = opts.pitch != null ? opts.pitch : 1;
        if (preferredVoice) u.voice = preferredVoice;
        let settled = false;
        const done = (ok) => {
          if (settled) return;
          settled = true;
          resolve({ ok: !!ok });
        };
        u.onend = () => done(true);
        u.onerror = () => done(false);
        speechSynthesis.speak(u);
        // Some browsers silently no-op without a gesture; resolve after a short grace.
        setTimeout(() => {
          if (!settled && !speechSynthesis.speaking && !speechSynthesis.pending) {
            done(false);
          }
        }, 700);
      } catch (e) {
        resolve({ ok: false });
      }
    });
  }

  /** Try autoplay; returns whether speech likely started. Caller shows replay either way. */
  function autoPlay(text, opts) {
    if (!text) return Promise.resolve({ ok: false, blocked: false });
    try {
      const soundOn =
        !global.RLProgress || RLProgress.get().settings.sound !== false;
      if (!soundOn) return Promise.resolve({ ok: false, blocked: false });
    } catch (e) {}
    return speak(text, opts).then((r) => ({
      ok: !!(r && r.ok),
      blocked: !(r && r.ok) && !userGesture,
      needsGesture: !userGesture,
    }));
  }

  function stop() {
    try {
      if (typeof speechSynthesis !== "undefined") speechSynthesis.cancel();
    } catch (e) {}
  }

  function sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
  }

  /** Speak dialogue turns with a short pause between them. */
  async function speakTurns(texts, gapMs, opts) {
    const list = (texts || []).map((t) => String(t || "").trim()).filter(Boolean);
    const gap = gapMs == null ? 420 : gapMs;
    for (let i = 0; i < list.length; i++) {
      await speak(list[i], opts);
      if (i < list.length - 1 && gap > 0) await sleep(gap);
    }
  }

  const Rec =
    global.SpeechRecognition || global.webkitSpeechRecognition || null;

  function canRecognize() {
    return !!Rec;
  }

  function recognizeOnce(timeoutMs) {
    return new Promise((resolve) => {
      if (!Rec) {
        resolve({ ok: false, reason: "unsupported", transcript: "" });
        return;
      }
      let done = false;
      const finish = (result) => {
        if (done) return;
        done = true;
        try { r.stop(); } catch (e) {}
        resolve(result);
      };
      const r = new Rec();
      r.lang = "ru-RU";
      r.interimResults = false;
      r.maxAlternatives = 3;
      r.onresult = (ev) => {
        const alts = [];
        for (let i = 0; i < ev.results[0].length; i++) {
          alts.push(ev.results[0][i].transcript);
        }
        finish({ ok: true, transcript: alts[0] || "", alternatives: alts });
      };
      r.onerror = () => finish({ ok: false, reason: "error", transcript: "" });
      r.onend = () => finish({ ok: false, reason: "ended", transcript: "" });
      try {
        r.start();
      } catch (e) {
        finish({ ok: false, reason: "start_failed", transcript: "" });
      }
      setTimeout(() => finish({ ok: false, reason: "timeout", transcript: "" }), timeoutMs || 6000);
    });
  }

  function normalizeRu(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/[ё]/g, "е")
      .replace(/[^\u0400-\u04ff\s]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function looseMatch(heard, expected) {
    const a = normalizeRu(heard);
    const b = normalizeRu(expected);
    if (!a || !b) return false;
    if (a === b) return true;
    if (a.includes(b) || b.includes(a)) return true;
    const ta = new Set(a.split(" "));
    const tb = b.split(" ");
    const hit = tb.filter((t) => ta.has(t)).length;
    return hit >= Math.ceil(tb.length * 0.6);
  }

  global.RLSpeech = {
    speak,
    autoPlay,
    speakTurns,
    stop,
    canRecognize,
    recognizeOnce,
    normalizeRu,
    looseMatch,
    voicesReady: () => voicesReady,
    preferredVoiceName: () => (preferredVoice && preferredVoice.name) || null,
    hasUserGesture: () => userGesture,
    getRate: learnerRate,
  };
})(window);
