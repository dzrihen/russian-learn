/* Hebrew transliteration helper (copied from js/engine.js for stories/chat) */
(function (global) {
// --- Hebrew transliteration for whole sentences (rule-based, Russian) ---
  const RU_HE = { б:"ב",в:"ב",г:"ג",д:"ד",ж:"ז׳",з:"ז",к:"ק",л:"ל",м:"מ",н:"נ",п:"\uE001",р:"ר",с:"ס",т:"ט",ф:"פ",х:"ח",ц:"צ",ч:"צ׳",ш:"ש",щ:"שצ׳",й:"י",ъ:"",ь:"" };
  function heFinals(s) {
    return s.replace(/מ(?=$)/, "ם").replace(/נ(?=$)/, "ן").replace(/פ(?=$)/, "ף").replace(/צ(?=$)/, "ץ").replace(/\uE001/g, "פ");
  }
  function wordToHe(w) {
    const s = w.toLowerCase();
    const V = "аеёиоуыэюя";
    let out = "";
    for (let i = 0; i < s.length; i++) {
      const c = s[i];
      const first = i === 0;
      const prev = s[i - 1] || "";
      const afterVowel = first || V.includes(prev) || prev === "ь" || prev === "ъ";
      const last = i === s.length - 1;
      if (c === "а") out += "א";
      else if (c === "о") out += first ? "או" : "ו";
      else if (c === "у") out += first ? "או" : "ו";
      else if (c === "ы") out += "י";
      else if (c === "и") out += first ? "אי" : "י";
      else if (c === "э") out += "א";
      else if (c === "е") out += last ? "יה" : "יֶ";
      else if (c === "ё") out += afterVowel ? "יו" : "יו";
      else if (c === "я") out += first ? "יא" : "יא";
      else if (c === "ю") out += "יו";
      else if (RU_HE[c] != null) out += RU_HE[c];
      else out += c;
    }
    return heFinals(out);
  }
  function sentenceHeTranslit(text) {
    return String(text || "").split(/\s+/).map(function (tok) {
      const m = tok.match(/^([^\p{L}]*)([\p{L}-]+)([^\p{L}]*)$/u);
      if (!m) return tok.replace(/[^?!,.…]/g, "");
      return m[2].split("-").map(wordToHe).join("־") + m[3].replace(/[^?!,]/g, "");
    }).filter(Boolean).join(" ");
  }

  
  global.RLHeTl = function (text) { return sentenceHeTranslit(text); };
})(window);
