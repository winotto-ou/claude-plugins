---
name: piibli-algkeeled
description: "Use for questions about the original languages of the Bible (Hebrew, Aramaic, Greek) with the Piibli algkeeled tools: the original words of a verse word by word (interlinear), what a Hebrew or Greek word means, its Strong's number, where else it occurs and how it is rendered, which original word stands behind a translation word, and related passages. TRIGGER on: 'algkeel', 'algtekst', 'kreeka sõna', 'heebrea sõna', 'aramea', 'Strongi number', 'mida tähendab originaalis', 'mis sõna on originaalis', 'interlineaar', 'sõna-sõnalt', 'kus veel esineb', 'ristviited', 'original language', 'Greek word', 'Hebrew word', 'Strong's number', 'interlinear', 'what does it mean in the original', or a Hebrew or Greek word in the message (חֶסֶד, ἀγάπη)."
---

# Bible original languages (Piibli algkeeled)

The „Piibli algkeeled” connector gives the Hebrew, Aramaic and Greek text word by word (STEPBible data), the Brown-Driver-Briggs and Abbott-Smith dictionaries, occurrences and cross-references. It works together with the jw.org tools (jw-search skill), which give the verse in the New World Translation.

## Tool names

The tools may carry a prefix depending on how they were added. In the one-connection „Winotto (kõik ühes)” setup every tool starts with its service prefix: `algkeeled_` (Piibli algkeeled, e.g. `algkeeled_interlinear`), `jw_` (jw.org otsing, e.g. `jw_get_bible_verse`), `keelenou_` (Eesti keelenõu), `suomi_` (Soome keelenõu), `postkast_` (Postkast), `ariregister_` (Äriregister). In Claude Code the name is longer and ends with `__interlinear`. Match a tool by the name it ends with.

## Ground rules

- **The New World Translation text comes first, and only from the jw tool.** Show the verse with `get_bible_verse` (or `get_bible_chapter`) and its wol.jw.org link before the original words. If the jw tool is not available, give only the link the interlinear result contains and do not quote the verse from memory.
- **English glosses are helpers, not a translation.** The word-by-word English renderings and dictionary glosses show what a word can mean; they never replace or correct the New World Translation. Do not present a gloss as „the right translation” or prefer it over the NWT wording.
- **Dictionaries are the dictionary's view.** BDB and Abbott-Smith are 19th–20th century scholarly works in English. Explain them in the user's language and say that this is what the dictionary says, not what jw.org teaches. Draw no doctrinal conclusions from a lexicon entry; for what the Bible teaches, point to jw.org articles (jw-search).
- **Cite.** Give the jw.org link of each verse and the source line the tool returns (STEPBible, the dictionary, OpenBible.info).
- **Answer in the user's language.** Original words stay in their script, with the transliteration the tool gives.

## Tools

| Tool | Use for | Main parameters |
|---|---|---|
| `interlinear` | the original words of a verse or a short range (up to 10 verses) | `reference` („Johannese 1:1”, „Laul 83:18”, „John 1:1-3”, „Jhn.1.1”), `detail` (`compact` default, `full` adds parsing and variants, max 6 verses), `content_only` (true leaves out articles, pronouns and conjunctions), `edition` (Greek: `NA` default, `WH`, `TR`, `Byz`, `SBL`, …) |
| `lexicon` | the meaning of one word | `strongs` („G26”, „H2617”) or `lemma` („ἀγάπη”, „חֶסֶד”, „agapē”); `source` (`auto` default, cut to about 3000 characters; `full`; `brief`; `lsj` for Greek) |
| `occurrences` | where else the word occurs, with the form in each verse | `strongs` or `lemma`; `book` („Johannese”) or `testament` (`OT`/`NT`), not both; `limit`, `offset` |
| `find_word` | which original words stand behind a translation word | `english` (English only: translate Estonian first; „armastus”, „vaim”, „usk” are converted), `language` (`hebrew`/`aramaic`/`greek`) |
| `cross_references` | related passages | `reference`, `limit` |
| `sources_info` | where the data comes from, licences | — |

References can be given in Estonian, English or OSIS form. One call takes one verse or one range inside one book; for a list („Joh 3:16; Rm 5:8”) make separate calls, in parallel.

## Workflow

1. **Verse first.** `get_bible_verse` for the NWT wording and link.
2. **Original words.** `interlinear` on the verse. For a word study use `content_only: true`; keep `detail` compact unless the user asks about grammar (tense, case, voice).
3. **Meaning.** `lexicon` with the Strong's number from the interlinear (not the lemma, when you have the number). If you searched by lemma and the tool lists other candidates („Kas mõtlesid: …”), check that you have the right word. When the article is cut (`truncated`), call with `source: "full"` only if the user needs the rest.
4. **Other occurrences.** `occurrences` with the same number; narrow with `book` or `testament` for frequent words. The per-book counts come on the first page; page on with `offset` only if asked.
5. **Answer.** NWT verse with link → the relevant original words as a table → what the dictionary says (marked as the dictionary's view) → a few other occurrences with their NWT wording when they help.

Original words as a table:

| Eesti (UMT) | Algkeel | Translit. | Strong | Abivaste (ingl) |
|---|---|---|---|---|
| armastad | ἀγαπᾷς | agapas | G25 | love |

### Translation word → original word
„Mis kreeka sõna on armastus?” → `find_word` with `english: "love"` → choose the candidates by frequency → `lexicon` for the meaning → an example verse with `get_bible_verse`. Say that several original words can stand behind one translation word.

### Related passages
`cross_references` gives references only; fetch the text of the ones you quote with `get_bible_verse`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Quoting the verse from memory or from the English gloss | `get_bible_verse`, then the original words. |
| „Originaalis tähendab see tegelikult …” as a correction of the NWT | Glosses are helpers; show them next to the NWT text, do not rank them above it. |
| A teaching drawn from BDB or Abbott-Smith | Say what the dictionary says and point to jw.org for the teaching. |
| One call for „Joh 3:16; Rm 5:8” | Separate calls, one book each. |
| `detail: "full"` for a simple word question | Compact, with `content_only: true`. |
