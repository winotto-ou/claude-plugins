# Lähteet – Finnish language sources and how to use them

All sources below are published or maintained by **Kotimaisten kielten keskus (Kotus)**, the Institute for the Languages of Finland, or are built on its data. Kotus's Kielitoimisto (Language Office) maintains the norms of standard written Finnish (yleiskieli); the **suomen kielen lautakunta** (Finnish language board) issues the official recommendations that the ohjepankki and the dictionary implement.

## 1. Kielitoimiston ohjepankki (primary)

- URL: https://kielitoimistonohjepankki.fi/
- What: ~630 official guidance articles (ohjeet) in five areas — *Merkit, numerot ja lyhenteet*; *Nimet*; *Sana* (yhdyssanat, alkukirjain, taivutus, vierassanat…); *Lause* (objekti, sijamuodon valinta, lauseenvastikkeet, passiivi…); *Teksti* (tyyli, otsikot, luettelot). Also *Hyvän virkakielen ohjeita* (`/vk/`) and *Hyvän nimistön opas* (`/hno/`).
- URL patterns: article `https://kielitoimistonohjepankki.fi/ohje/<slug>/`; topic page `https://kielitoimistonohjepankki.fi/aihepiiri/<alaryhmä>/`; site search `https://kielitoimistonohjepankki.fi/?s=<hakusana>`; recent changes `https://kielitoimistonohjepankki.fi/viimeaikaisia-muutoksia/`.
- Full index of all articles with titles, grouped by topic: `ohjepankki-index.md` (snapshot of the sitemap, 2026-09-06; refresh by re-reading the sitemap at `https://kielitoimistonohjepankki.fi/sitemap.xml`).
- Status: the online, continuously updated successor of the printed *Kielitoimiston oikeinkirjoitusopas* and *Kielitoimiston kielioppiopas*. Treat it as the norm.
- Licence: CC BY-NC-ND 4.0, © Kotimaisten kielten keskus. Cite as: *Ohjeen otsikko. Kielitoimiston ohjepankki. URL. Viitattu pp.kk.vvvv.*

## 2. Kielitoimiston sanakirja

- URL: https://www.kielitoimistonsanakirja.fi/ — direct word link `https://www.kielitoimistonsanakirja.fi/#/<sana>`
- What: the official dictionary of contemporary standard Finnish, 100 000+ headwords, with spelling, inflection type, meaning, usage examples and style labels (ark., vanh., halv.). Free.
- Access: single-page app; its search API requires a session token and is not openly usable. Use it by linking, or open it in a browser tool and read the entry. Do not claim to have checked the dictionary unless you actually read the entry.
- Use for: does this word exist in standard Finnish, how is it spelled, which inflection, is it colloquial.

## 3. Voikko

- URL: https://voikko.puimula.org/ — source https://github.com/voikko/corevoikko
- What: free Finnish spell checker, grammar checker, hyphenator and morphological analyser (the engine behind LibreOffice's and many Linux tools' Finnish checking). Word data derives from Kotus word lists (Joukahainen/voikko-fi).
- Install: Debian/Ubuntu `apt-get install libvoikko1 voikko-fi` then `pip install libvoikko`; macOS `brew install libvoikko` (dictionary via `voikko-fi`); Windows: see the Voikko site.
- Script: `scripts/voikko_check.py <file>` prints misspellings with suggestions, grammar findings and (with `--analyze`) morphological analyses.
- Limits: it does not know all proper names, new words or rare compounds, and its grammar checker covers only a handful of mechanical error types. Its flags are hints to verify, not verdicts.

## 4. VISK – Iso suomen kielioppi (verkkoversio)

- URL: https://kaino.kotus.fi/visk/ (also https://scripta.kotus.fi/visk/)
- What: the comprehensive *descriptive* grammar of Finnish (Hakulinen et al. 2004), free online, ~1 700 numbered sections. Describes how Finnish is used, including variation; it is not a rule book.
- Use for: deep questions about syntax, morphology, clause types, when the ohjepankki does not give a rule. Cite by § number, e.g. *VISK § 925*.

## 5. Kielikello

- URL: https://kielikello.fi/
- What: Kotus's language-care journal (since 1968), free online. Articles explain recommendations, rule changes and the reasoning behind them; the language board's decisions are published here.
- Use for: background, history of a rule, borderline cases discussed in depth. Secondary to the ohjepankki for the current norm.

## 6. Suomen kielen lautakunta – suositukset ja kannanotot

- URL: https://kotus.fi/kotus/lausunnot-suositukset-ja-kannanotot/suomen-kielen-lautakunnan-suosituksia-ja-kannanotot/
- What: the board's formal recommendations and statements. Rarely needed directly; the ohjepankki reflects them.

## Not used

- Printed *Kielitoimiston oikeinkirjoitusopas* / *kielioppiopas* / *nimiopas*: paid books; the ohjepankki is their updated online form.
- Commercial online "oikoluku" tools and generic grammar-checker sites: not authoritative.
- Unofficial guides (e.g. jkorpela.fi *Nykyajan kielenopas*): useful background, but always confirm against the ohjepankki before citing a rule.
