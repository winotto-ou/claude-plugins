#!/usr/bin/env python3
"""Mechanical Finnish check with Voikko: spelling, suggestions, grammar findings.

Usage:
    python3 voikko_check.py TEXTFILE [--analyze] [--json]
    cat text.txt | python3 voikko_check.py - [--analyze] [--json]

Output is a compact report (or JSON with --json). Voikko flags are hints to
verify against Kielitoimiston sanakirja / ohjepankki, not verdicts: proper
names, new words and rare compounds are often flagged although correct.

Requires libvoikko + the Finnish dictionary:
    Debian/Ubuntu:  sudo apt-get install libvoikko1 voikko-fi && pip install libvoikko
    macOS:          brew install libvoikko  (dictionary: see https://voikko.puimula.org/)
"""
import json
import re
import sys

INSTALL_HINT = (
    "Voikko is not available in this environment.\n"
    "Install: apt-get install libvoikko1 voikko-fi && pip install libvoikko "
    "(macOS: brew install libvoikko). Continue the review without the mechanical pass."
)

TOKEN_RE = re.compile(r"[A-Za-zÅÄÖåäöÉéÜüŠšŽž0-9][A-Za-zÅÄÖåäöÉéÜüŠšŽž0-9'’\-\.:]*")


def load_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as f:
        return f.read()


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        print(__doc__)
        return 2
    text = load_text(args[0])

    try:
        import libvoikko  # type: ignore
        v = libvoikko.Voikko("fi")
    except Exception as e:  # ImportError or VoikkoException (no dictionary)
        print(INSTALL_HINT)
        print(f"({type(e).__name__}: {e})")
        return 3

    # --- spelling -----------------------------------------------------------
    seen = {}
    for m in TOKEN_RE.finditer(text):
        tok = m.group(0).strip(".:'’-")
        if not tok or tok.isdigit() or tok in seen:
            continue
        # Skip tokens with digits or abbreviation-like colon forms (EU:n, 5:ssä)
        if re.search(r"\d", tok) or ":" in m.group(0):
            continue
        if not v.spell(tok):
            line = text.count("\n", 0, m.start()) + 1
            seen[tok] = {
                "word": tok,
                "line": line,
                "suggestions": v.suggest(tok)[:5],
            }

    # --- grammar ------------------------------------------------------------
    grammar = []
    for para in [p for p in re.split(r"\n\s*\n", text) if p.strip()]:
        try:
            errors = v.grammarErrors(para, "fi")
        except TypeError:  # older bindings without language arg
            errors = v.grammarErrors(para)
        for err in errors:
            snippet = para[err.startPos : err.startPos + err.errorLen]
            grammar.append(
                {
                    "code": err.errorCode,
                    "description": err.shortDescription,
                    "text": snippet,
                    "suggestions": list(err.suggestions)[:3],
                    "context": para[max(0, err.startPos - 30) : err.startPos + err.errorLen + 30].replace("\n", " "),
                }
            )

    # --- optional morphology ------------------------------------------------
    analyses = {}
    if "--analyze" in flags:
        for tok in seen:
            analyses[tok] = [
                {k: a.get(k) for k in ("BASEFORM", "CLASS", "SIJAMUOTO", "NUMBER", "WORDBASES") if k in a}
                for a in v.analyze(tok)
            ]

    report = {"unknown_words": list(seen.values()), "grammar": grammar, "analyses": analyses}

    if "--json" in flags:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print("== Voikko: tuntemattomat / mahdollisesti väärin kirjoitetut sanat ==")
    if not seen:
        print("(ei löytynyt)")
    for item in seen.values():
        sug = ", ".join(item["suggestions"]) or "–"
        print(f"rivi {item['line']}: {item['word']}  → ehdotukset: {sug}")
    print()
    print("== Voikko: kielioppitarkistimen huomiot ==")
    if not grammar:
        print("(ei löytynyt)")
    for g in grammar:
        sug = f"  → {', '.join(g['suggestions'])}" if g["suggestions"] else ""
        print(f"[{g['code']}] {g['description']}: ”{g['text']}”{sug}\n    …{g['context']}…")
    if analyses:
        print()
        print("== Morfologinen analyysi (tuntemattomille sanoille) ==")
        for w, a in analyses.items():
            print(f"{w}: {a if a else 'ei analyysiä'}")
    print()
    print("Huom. Voikon merkinnät ovat tarkistettavia vihjeitä, eivät tuomioita: erisnimet, uudissanat ja harvinaiset yhdyssanat ovat usein oikein.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
