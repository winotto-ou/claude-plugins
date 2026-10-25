---
name: estonian-proofreading
description: "Use when proofreading, editing or checking Estonian text — jw.org translations, articles, subtitles — or when answering a question about Estonian spelling, compound words, capitalisation, punctuation, case forms, abbreviations or word choice. TRIGGER on: 'toimeta', 'korrektuur', 'keeletoimetus', 'kas see on õige', 'kas nii võib öelda', 'kokku või lahku', 'mis käändes', 'proofread', 'check my Estonian', or when the user pastes Estonian prose and asks what is wrong with it."
---

# Estonian proofreading with the et-proof tools

## Overview

The „Eesti keelenõu” connector (et-proof) exposes EKI's own data: Ekilex (ÕS, EKI ühendsõnastik 2026, term bases), the EKI teatmik with the keelenõuvakk questions, and the Eesti keele käsiraamat (EKI 2020), which treats grammar and syntax — commas above all — more deeply than the teatmik. Your job is to find errors **that EKI documents** and hand the translator a decision, not a rewrite.

**Core principle: the tools prove errors. They never clear text.** A tool that returns nothing means you have no evidence — not that the sentence is fine.

## Tool names

The tools may carry a prefix depending on how they were added. In the one-connection „Winotto (kõik ühes)” setup every tool starts with its service prefix: `keelenou_` (Eesti keelenõu, e.g. `keelenou_scan_text`), `suomi_` (Soome keelenõu), `jw_` (jw.org otsing), `algkeeled_` (Piibli algkeeled), `postkast_` (Postkast), `ariregister_` (Äriregister). In Claude Code the name is longer and ends with `__scan_text`. Match a tool by the name it ends with.

## Tools

| Tool | Use for |
|---|---|
| `scan_text(text, max_words=400)` | **first pass over a whole text**: returns only unknown forms, words with an EKI recommendation or warning value state, and words with several inflection types, each with line/column and a Sõnaveeb link |
| `check_commas(text, max_sentences=500, offset=0)` | **commas, over a whole text**: likely missing commas (subordinate clauses, „nii et”, „enne kui”, aga/kuid/vaid, kiil) and clearly superfluous ones, in two sections, „Kontrolli kindlasti” and „Kaalu”, each with line, place, reason and handbook section; it never rewrites. A longer text ends with `[jätk: offset=N]`: call again with that `offset` |
| `check_form(form, word=None)` | is this one form real, and is it in this word's paradigm („lähsin või läksin”) |
| `recommendation(word)` | does EKI advise against a word or prefer another |
| `lookup(word, dataset=None)` | meanings, value states and datasets (`eki`, `usu`, `ust`, `esterm`; codes from `datasets`) |
| `lemmatize(form)` | the base form of an unfamiliar form |
| `forms(word, form=None, all_forms=False)` | the key inflected forms (about ten by default), several paradigms side by side |
| `teatmik_search(query, kind="koik", chapter=None)` | rules in the EKI teatmik and the Eesti keele käsiraamat; `kind`: `teatmik` (rule articles), `keelenouvakk` (frequently asked questions), `kasiraamat` (the handbook: grammar, syntax, comma rules), `koik` (all three, mixed) |
| `teatmik_article(ref, offset=0)` | read the rule — a teatmik slug, or a handbook section code such as `SÜ 106`; long texts come in parts |
| `teatmik_chapters()` | teatmik chapters with slugs, handbook chapters with codes (`O`, `M`, `SM`, `SÜ`, `L`), for `chapter` |

**Make independent calls in parallel**: several `recommendation`, `check_form` or `teatmik_search` calls for different words or rules in one turn, not one by one.

## What each tool answer actually proves

This table exists because the natural reading of these outputs is wrong.

| Tool answer | Proves | Does NOT prove |
|---|---|---|
| `scan_text` does not list a word | Ekilex knows the form and has no warning for it | **Nothing about correctness.** It does not see commas (that is `check_commas`), kokku-lahku, capitals, wrong word choice or style. |
| `scan_text` → „tundmatu vorm” | Strong signal of a typo, a non-word or a name | — |
| `recommendation` → „soovitust pole” | Ekilex carries no warning flag for that word | **Nothing about correctness.** `hetkel`, `kompetents`, `läbi viima` all return this. Style and kantseliit live in the teatmik, not here. |
| `recommendation` → EKI soovitus text | EKI has written about the word | That it is an error. EKI often says the opposite („üldkeele sõnade tähendusi ei normita”). Read the text before reporting. |
| `recommendation` → väärtusolek „väldi” from **Esterm**, with an English definition „(inglise keeles)” | A term base marks the term as one to avoid *in that field* | EKI's general advice. The English text is Esterm's definition, not a reason. Report it as a terminology note, with the dataset, and check the preferred word (`Eelistatud vaste`) with `lookup`. |
| `lemmatize` → „ei leitud algvormi” | Strong signal of a typo or non-word | — |
| `lemmatize` → a lemma | **Nothing.** Ekilex happily lemmatises `tekkib` → `tekkima`. | That the form is correct. Use `check_form`. |
| `check_form` → „on … vorm” | The form is in the paradigm | That it is the main form, if several inflection types are flagged |
| `forms` / `check_form` / `scan_text` → several muuttüüpi | The paradigm is ambiguous in Ekilex (`tekkima` lists both `tekib` and `tekkib`) | Do **not** call a form wrong on this evidence. Report it as uncertain or find a teatmik rule. |
| `lookup` → väärtusolek `väldi` / `endine` / `mööndav` / `küsitav` | A real warning in that dataset | |
| `teatmik_search` hit list | That such an article exists | What the rule says. Read it with `teatmik_article` before you cite it. |
| `check_commas` → „Kontrolli kindlasti” | A rule check found a comma that is almost certainly missing or superfluous: fix it, citing the handbook section it names | — |
| `check_commas` → „Kaalu” | A comma that depends on the meaning or stress, or is free (lauselühendid appear only here) | An error. Decide by the sentence's meaning: report it as Soovitus or leave it. |
| `check_commas` finds nothing | No comma rule it knows was broken | **That the commas are right.** It does not see lists, järellisandid, direct speech, most lauselühendid or commas that depend on meaning, and some errors in long, complex sentences stay unfound (see its „Mida see kontroll ei leia” note). It does not replace your own reading of the commas. |

## Querying the teatmik

Query with **the name of the rule**, not with a question. An exact title match ranks first; question words (kas, või, ja) are dropped.

| Instead of | Query |
|---|---|
| „koma enne et” | `koma` (or `kind: "keelenouvakk"` for the Q&A on that exact case) |
| „kas suure või väikese tähega” | `algustäht` |
| „kas kokku või lahku” | `kokku- ja lahkukirjutamine` |
| „kuidas vältida poolt-lauseid” | `poolt tarind` or `kantseliit` |

Use `kind: "teatmik"` when you need the rule article, `kind: "keelenouvakk"` for question-shaped topics („Kuidas käänata tänavanimesid?”), `chapter` (from `teatmik_chapters`) to stay inside one area. **Scan the whole hit list**: the general rule article is not always first.

For commas and sentence structure, also query the handbook: `kind: "kasiraamat"` (or `chapter: "süntaks"`). Its sections are numbered — SÜ 106 (koma mitme määruse korral), SÜ 125 (järellisand), SÜ 127 (lisanditaolised määrused), O 57 (koma ülevaade) — and `teatmik_article` opens one by code.

## Reading articles: truncation and budget

- `teatmik_article` returns about 6000 characters per call. A longer article ends with **`[jätk: offset=N]`**. Never quote a rule as complete when that marker is there and the clause you need is not yet in view: call again with `offset: N`.
- **Read budget**: for one paragraph of text, open at most about three articles, and read further parts only when the deciding clause has not appeared. Prefer the specific article („Koma ja et-lause”) to the overview.
- Footnotes come with the article; they often hold the exception.

## The loop

1. **`scan_text` and `check_commas` on the whole text**, in the same turn (they are independent). `scan_text` checks at most `max_words` unique words and says what it skipped (use sections for long texts): take its list as the first set of candidates and verify each with `check_form`, `recommendation` or `lookup` before reporting. `check_commas` goes with every text you proofread and with every „kas siia käib koma” question (pass the sentence); fix its „Kontrolli kindlasti” items, decide each „Kaalu” by the meaning, and quote the handbook section it cites. If it ends with `[jätk: offset=N]`, call again with that `offset`.
2. Then work **sentence by sentence**. Number the paragraphs and sentences; do not read the text as a whole and report impressions. For each sentence, run down this trigger list. Only call a tool when a trigger fires.

| Trigger in the sentence | Tool |
|---|---|
| Foreign, modern or bureaucratic-sounding word | `recommendation`, then `lookup` if it returned nothing |
| A form you cannot place, or that looks off | `check_form` (with `word` when you know the base word) |
| Two words that could be one, or one that could be two | `teatmik_search` `kokku- ja lahkukirjutamine` |
| A capital on a common noun, or a lowercase name | `teatmik_search` `algustäht` |
| Comma near *et, mis, kui, ja, kuid*; a kiil; a lauselühend; a list | `check_commas` (step 1) covers most; for the rule behind a finding, or for what it does not see (lists, järellisandid, meaning-dependent commas), `teatmik_search` `koma` (`koik` already includes the handbook; `kind: "kasiraamat"` for syntax sections only) |
| Numbers, dates, percentages, abbreviations | `teatmik_search` `arvud` / `lühendid` |
| `poolt`-passive, `läbi viima`, `omab`, `antud`, `seoses`, `tulenevalt` | `teatmik_search` `kantseliit` |
| A term of the subject field | `lookup` with `dataset` (`usu`, `ust`, `esterm`) |

3. Read the article you found with `teatmik_article` and quote the sentence of the rule that decides the case.

**The article usually narrows the rule.** The `poolt`-tarind article permits *valla poolt makstav toetus* — an institution — and advises the personal construction only when the agent is a named person or pronoun. Flagging every `poolt` would misquote EKI. Find the clause that covers *this* sentence, not the topic.

## Output

The same shape as the Finnish proofreading skill. Headers in the answer's language (Estonian: `Koht · Algne → Parandus · Viga/soovitus · Allikas`; English: `Where · Original → Correction · Error/suggestion · Source`):

| Koht | Algne → Parandus | Viga/soovitus | Allikas |
|---|---|---|---|
| 1. lõik, 2. lause | „töö kogemus” → „töökogemus” | Viga · kokkukirjutamine: liitsõna, mille osad moodustavad ühe mõiste | <teatmiku artikli pealkiri> – <link> |
| 2. lõik, 1. lause | „lähsin” → „läksin” | Viga · vorm: „lähsin” pole sõna *minema* paradigmas | `check_form`, Sõnaveeb – <link> |
| 3. lõik, 3. lause | „Mari poolt kirjutatud kiri” → „Mari kirjutatud kiri” | Soovitus · poolt-tarind: tegija on nimega isik, teatmik soovitab siis tarindit ilma *poolt*-ita | <teatmiku artikli pealkiri> – <link> |

- **Koht**: paragraph and sentence („2. lõik, 1. lause”), or the line from `scan_text`.
- **Algne → Parandus**: only the faulty phrase and its correction, not the whole sentence.
- **Viga/soovitus**: start with **Viga** (a documented rule is broken) or **Soovitus** (EKI prefers another wording; style), then the topic and one short reason. Uncertain cases: „Ebaselge · … — Ekilexis vastuoluline, vajab inimotsust”.
- **Allikas is required**: the teatmik article title with the link; for the handbook, the source line and page link the tool returned (e.g. „Eesti keele käsiraamat (EKI 2020), SÜ 106, lk 469–470 – <link>”); or the Sõnaveeb link and dataset the tool returned. No source, no row — delete the finding instead.
- After the table, one line: which sentences you checked and found nothing in, and what `scan_text` left unchecked, if anything.
- **Do not return a rewritten text** unless the user asks for one. The translator decides; you supply evidence.

## Boundaries

- **Team terminology outranks EKI.** If the team's glossary and Ekilex disagree, the glossary wins and you say so — EKI's note on „Jehoova” is the standing example.
- **Style is not an error.** Report a wording preference only when a teatmik article calls it one, and mark it Soovitus. Otherwise leave the translator's voice alone.
- **Uncertain is a real verdict.** Write „Ekilexis vastuoluline, vajab inimotsust” rather than picking a side without evidence.

## Common mistakes

| Mistake | Fix |
|---|---|
| „`scan_text` ei leidnud midagi, tekst on korras” | It only checks word forms and warnings. Commas need `check_commas`; kokku-lahku, capitals and style need the loop. |
| „`check_commas` ei leidnud midagi, komad on korras” | It misses lists, järellisandid and commas that depend on meaning. Read the commas against the trigger list. |
| Reporting every „Kaalu” item as an error | „Kaalu” = decide by the sentence's meaning; „Kontrolli kindlasti” = fix, after reading the cited rule. |
| „`recommendation` ei leidnud midagi, sõna on korras” | It only checks warning flags. Kantseliit and style need a teatmik query. |
| „`lemmatize` leidis algvormi, vorm on õige” | It lemmatised `tekkib` too. Use `check_form`, and mind multiple paradigms. |
| Reporting an Esterm „väldi” as EKI's verdict | Name the dataset; it is a terminology note in that field. |
| Quoting a rule from the first part of a long article | Look for `[jätk: offset=N]` and read on when the clause is not there. |
| Citing a teatmik title without opening it | `teatmik_article` first, then quote. |
| Flagging a construction the article actually permits | The rule has conditions. Quote the clause that covers this sentence. |
| Calling tools one by one for ten words | Independent calls go in parallel. |
| Rewriting the paragraph | Findings table. The translator rewrites. |
| Skipping sentences that look clean | Run the trigger list on every sentence; say which ones came back clean. |
