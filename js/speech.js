/* Speech: TTS (ru-RU) + optional SpeechRecognition */
(function (global) {
  "use strict";

  let preferredVoice = null;
  let voicesReady = false;

  function pickVoice() {
    const voices = speechSynthesis.getVoices() || [];
    const ru = voices.filter((v) => (v.lang || "").toLowerCase().startsWith("ru"));
    preferredVoice =
      ru.find((v) => /female|milena|katya|irina|tatyana/i.test(v.name)) ||
      ru[0] ||
      null;
    voicesReady = true;
  }

  if (typeof speechSynthesis !== "undefined") {
    pickVoice();
    speechSynthesis.onvoiceschanged = pickVoice;
  }

  function speak(text, opts) {
    if (!text || typeof speechSynthesis === "undefined") return Promise.resolve();
    opts = opts || {};
    return new Promise((resolve) => {
      try {
        speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(String(text));
        u.lang = "ru-RU";
        u.rate = opts.rate != null ? opts.rate : 0.92;
        u.pitch = opts.pitch != null ? opts.pitch : 1;
        if (preferredVoice) u.voice = preferredVoice;
        u.onend = () => resolve();
        u.onerror = () => resolve();
        speechSynthesis.speak(u);
      } catch (e) {
        resolve();
      }
    });
  }

  function stop() {
    try {
      if (typeof speechSynthesis !== "undefined") speechSynthesis.cancel();
    } catch (e) {}
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

  /** Normalize Russian for loose compare */
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
    // token overlap
    const ta = new Set(a.split(" "));
    const tb = b.split(" ");
    const hit = tb.filter((t) => ta.has(t)).length;
    return hit >= Math.ceil(tb.length * 0.6);
  }

  global.RLSpeech = {
    speak,
    stop,
    canRecognize,
    recognizeOnce,
    normalizeRu,
    looseMatch,
    voicesReady: () => voicesReady,
  };
})(window);
