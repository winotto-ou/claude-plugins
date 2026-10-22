---
name: estonian-proofreading
description: "Use when proofreading, editing or checking Estonian text — jw.org translations, articles, subtitles — or when answering a question about Estonian spelling, compound words, capitalisation, punctuation, case forms, abbreviations or word choice. TRIGGER on: 'toimeta', 'korrektuur', 'keeletoimetus', 'kas see on õige', 'kas nii võib öelda', 'proofread', 'check my Estonian', or when the user pastes Estonian prose and asks what is wrong with it."
---

# Estonian proofreading with the et-proof tools

## Overview

The „Eesti keelenõu” connector (et-proof) exposes EKI's own data: Ekilex (ÕS, EKI ühendsõnastik 2026, term bases) and the EKI teatmik + keelenõuvakk. Your job is to find errors **that EKI documents** and hand the translator a decision, not a rewrite.

**Core principle: the tools prove errors. They never clear text.** A tool that returns nothing means you have no evidence — not that the sentence is fine.

## Tool names

The tools may carry a prefix depending on how they were added: `keelenou_lookup` in the one-connection „Winotto (kõik ühes)” setup; in Claude Code the name is longer and ends with `__lookup`. Match a tool by the name it ends with.

## What each tool answer actually proves

This table exists because the natural reading of these outputs is wrong.

| Tool answer | Proves | Does NOT prove |
|---|---|---|
| `recommendation` → „soovitust pole” | Ekilex carries no warning flag for that word | **Nothing about correctness.** `hetkel`, `kompetents`, `läbi viima` all return this. Style and kantseliit live in the teatmik, not here. |
| `recommendation` → EKI soovitus text | EKI has written about the word | That it is an error. EKI often says the opposite („üldkeele sõnade tähendusi ei normita”). Read the text before reporting. |
| `lemmatize` → „ei leitud algvormi” | Strong signal of a typo or non-word | — |
| `lemmatize` → a lemma | **Nothing.** Ekilex happily lemmatises `tekkib` → `tekkima`. | That the form is correct. `lemmatize` is not a spellchecker. |
| `forms` → one muuttüüp table | Those are the standard forms | |
| `forms` → two or more muuttüüp tables | The paradigm is ambiguous in Ekilex (`tekkima` lists both `tekib` and `tekkib`) | Do **not** call a form wrong on this evidence. Report it as uncertain or find a teatmik rule. |
| `lookup` → väärtusolek `väldi` / `endine` / `mööndav` / `küsitav` | A real EKI warning | |
| `teatmik_search` hit list | That such an article exists | What the rule says. Read it with `teatmik_article` before you cite it. |

## Querying the teatmik

Query with **the name of the rule**, not with a question. The index scores titles; function words dilute it into alphabetical noise.

| Instead of | Query |
|---|---|
| „koma enne et” → Amhara tähetabel, Araabia tähetabel … | `koma` |
| „kas suure või väikese tähega” | `algustäht` |
| „kas kokku või lahku” | `kokku- ja lahkukirjutamine` |
| „kuidas vältida poolt-lauseid” | `poolt tarind` or `kantseliit` |

Question-shaped wording belongs in `keelenouvakk_search`, which indexes real questions („Kuidas käänata tänavanimesid?”).

**Scan the whole hit list.** The general rule article is often not first — searching `koma` puts four keelenõuvakk Q&As above the „Koma” article itself.

## The loop

Work **sentence by sentence**. Number the sentences; do not read the text as a whole and report impressions.

For each sentence, run down this trigger list. Only call a tool when a trigger fires — do not look up every word.

| Trigger in the sentence | Tool |
|---|---|
| Foreign, modern or bureaucratic-sounding word | `recommendation`, then `lookup` if it returned nothing |
| A form you cannot place, or that looks off | `lemmatize`; if a lemma comes back, check `forms` |
| Two words that could be one, or one that could be two | `teatmik_search` `kokku- ja lahkukirjutamine` |
| A capital on a common noun, or a lowercase name | `teatmik_search` `algustäht` |
| Comma near *et, mis, kui, ja, kuid*; a kiil; a lauselühend | `teatmik_search` `koma` |
| Numbers, dates, percentages, abbreviations | `teatmik_search` `arvud` / `lühendid` |
| `poolt`-passive, `läbi viima`, `omab`, `antud`, `seoses`, `tulenevalt` | `teatmik_search` `kantseliit` |
| A term of the subject field | `lookup` with `dataset` (`usu`, `ust`, `esterm`) |

Then read the article you found with `teatmik_article` and quote the sentence of the rule that decides the case.

**The article usually narrows the rule.** The `poolt`-tarind article permits *valla poolt makstav toetus* — an institution — and advises the personal construction only when the agent is a named person or pronoun. Flagging every `poolt` would misquote EKI. Find the clause that covers *this* sentence, not the topic.

## Output

Return a findings table, in Estonian:

| Lause | Koht | Probleem | Ettepanek | Allikas |
|---|---|---|---|---|

- **Allikas is required.** No source, no row — delete the finding instead.
- Quote the rule, and give the teatmik link the tool returned.
- After the table, one line: which sentences you checked and found nothing in.
- **Do not return a rewritten text** unless the user asks for one. The translator decides; you supply evidence.

## Boundaries

- **Team terminology outranks EKI.** If the team's glossary and Ekilex disagree, the glossary wins and you say so — EKI's note on „Jehoova” is the standing example.
- **Style is not an error.** Report a wording preference only when a teatmik article calls it one. Otherwise leave the translator's voice alone.
- **Uncertain is a real verdict.** Write „Ekilexis vastuoluline, vajab inimotsust” rather than picking a side without evidence.

## Common mistakes

| Mistake | Fix |
|---|---|
| „`recommendation` ei leidnud midagi, sõna on korras” | It only checks warning flags. Kantseliit and style need a teatmik query. |
| „`lemmatize` leidis algvormi, vorm on õige” | It lemmatised `tekkib` too. Check `forms`, and mind multiple paradigms. |
| Citing a teatmik title without opening it | `teatmik_article` first, then quote. |
| Flagging a construction the article actually permits | The rule has conditions. Quote the clause that covers this sentence. |
| Rewriting the paragraph | Findings table. The translator rewrites. |
| Skipping sentences that look clean | Run the trigger list on every sentence; say which ones came back clean. |
