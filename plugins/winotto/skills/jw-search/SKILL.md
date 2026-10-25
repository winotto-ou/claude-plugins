---
name: jw-search
description: "Use the jw.org tools to look up Bible verses (New World Translation), their study Bible notes and the publications that explain them, search jw.org content, read articles, get the daily text and the meeting workbook, and search video subtitles. TRIGGER when: user asks about Bible verses, scriptures, JW publications, Watchtower articles, jw.org content, JW videos, morning worship, the daily text, the meeting workbook, or anything related to Jehovah's Witnesses content. Also trigger when user mentions 'Bible', 'scripture', 'verse', 'jw.org', 'Watchtower', 'piibel', 'piiblisalm', 'kirjakoht', 'õppepiibel', 'õppemärkus', 'study notes', 'what does this verse mean', 'salmi selgitused', 'päevatekst', 'töövihik', 'koosolek', 'jw video', 'subtitle search', or wants to find what a speaker said in a talk. For a verse's meaning read the study notes (get_study_notes) first, then get_verse_references for where publications explain it; for the Hebrew or Greek word data use the piibli-algkeeled skill."
---

# jw.org search

You have the tools of the Winotto „jw.org otsing” connector: Bible verses and chapters (New World Translation), the study Bible notes, the publications that explain a verse, jw.org search, page reading, the daily text, the meeting workbook and video subtitle search.

## Tool names

The tools may carry a prefix depending on how they were added. In the one-connection „Winotto (kõik ühes)” setup every tool starts with its service prefix: `jw_` (jw.org otsing, e.g. `jw_search_jw`), `algkeeled_` (Piibli algkeeled), `keelenou_` (Eesti keelenõu), `suomi_` (Soome keelenõu), `postkast_` (Postkast), `ariregister_` (Äriregister). In Claude Code the name is longer and ends with `__search_jw`. Match a tool by the name it ends with.

## Ground rules

- **Bible text only from the tool.** Every verse you quote comes from `get_bible_verse` or `get_bible_chapter`, never from memory. If you only remember the wording, find the verse first (see „Scripture from a quoted text” below).
- **Study notes for every Bible question.** When the user asks what a verse means, about its background or wording, or about a Hebrew or Greek word, read the study Bible notes first: `get_study_notes` (in „Kõik ühes” `jw_get_study_notes`). They are jw.org's most current explanations, often comment on the original-language word, and outrank general knowledge. `get_bible_verse` already appends a short „Õppemärkused” section; call `get_study_notes` for the full text, and cite its jw.org link.
- **English notes when the language has none.** Estonian notes currently cover Matthew–Acts; the tool says when a verse has no Estonian notes and then returns the English study notes with a line saying so (the same for any other language without notes). Explain them in the user's language and say that they come from the English study Bible; the verse text itself still comes from `get_bible_verse` in the user's language. When neither language has notes, the tool says so plainly: tell the user there are no study notes on that verse and look further with `search_jw`.
- **Always cite the link.** Each result carries its wol.jw.org or jw.org link; put it next to what you quote. Never build or guess a link yourself.
- **Answer in the user's language.** Quote the Bible and publications in the language you fetched them in.
- **Default language is Estonian (`et`).** Pass another `language` only when the user writes in or asks for another language. Every language jw.org has works: give the language's code exactly as `list_languages` shows it (`fi`, `de`, `pt-PT`, `kun`; `list_languages` with `query` finds one among the more than thousand) or its name (`Finnish`, `suomi`). A jw.org WT code needs the prefix `wt:` (`wt:FI`, `wt:ST`), because many WT codes are also other languages' codes (`ST` is Estonian's WT code, but `st` is Sesotho). When a result ends with a line „Keel: …”, the tool is telling you which language it used: check that it is the one the user meant. If a source lacks the language (no wol library, no study Bible, no videos), the tool says so; pass that on instead of answering in English. When a result is marked as found in another language than you asked for, tell the user. Leaving an optional parameter empty gives its default.
- **Search with word stems.** Estonian has 14 cases: search `andesta`, not `andestamisest`; `piibliaru`, not `piibliaruteludest`. This matters most for subtitles.
- **Book names in Estonian work** in any common form: `Johannese`, `Joh`, `1. Moosese`, `1Mo`, `Õp`, `Mt`, also with a case ending (`Johannesest`), as well as English (`John`, `1 Cor`) and, with `language`, the names in that language (`Matteus`, `Matthäus`, `Матфея`). If a name is not recognised, the error suggests the form that works; `search_bible_books` resolves doubtful names.
- **Original-language questions** (what a Greek or Hebrew word means, Strong's numbers, interlinear) start with `get_study_notes`; the word data belongs to the piibli-algkeeled skill and its `algkeeled_` tools. Use this skill for the verse text and the study notes.

## Tools

| Tool | Use for | Main parameters |
|---|---|---|
| `get_bible_verse` | one verse or a range, with its link and a short study-notes section | `book`, `chapter`, `verse` (`"16"` or `"14-16"`), `language`, `study_notes` (default true) |
| `get_bible_chapter` | a whole chapter, with its link and a pointer to its study notes | `book`, `chapter`, `language` |
| `get_study_notes` | the study Bible notes on a verse, a range or a whole chapter: the word or phrase, the explanation (often on the Hebrew or Greek word), footnotes, cross-references and the jw.org link; English notes when the language has none | `book`, `chapter`, `verse` (empty = whole chapter), `language`, `max_chars`, `offset` |
| `get_verse_references` | where jw.org publications explain **one** verse (articles, books, Insight entries, for the Gospels video scenes), newest first, each with its reference and a link that opens the cited paragraph; English entries, with a line saying so, when the language has none („Salmi selgitused väljaannetes”) | `book`, `chapter`, `verse` (one number), `language`, `max_chars`, `offset` |
| `search_bible_books` | book names and numbers: Estonian/English, plus the names in `language` | `query`, `limit`, `language` |
| `search_jw` | articles, verses and videos on jw.org; index hits are collapsed to one line | `query`, `language`, `limit`, `sort` (`relevance`/`newest`), `type` (`all`/`article`/`video`/`index`) |
| `read_jw_page` | the text of a jw.org or wol.jw.org page, in parts | `url`, `max_chars` (default 12000), `offset` |
| `get_daily_text` | the daily text („Uuri pühakirja iga päev”) | `date` (`YYYY-MM-DD`, empty = today), `language` |
| `get_meeting_workbook` | the midweek meeting programme for the week of a date | `date` (empty = this week), `language` |
| `search_video_subtitles` | what was said in recent videos, with a link to the moment; `all` scans the newest videos of every category (`max_videos` of them) and answers in a few seconds | `query` (stem), `category` (name or key, several comma-separated, or `all`), `language`, `limit`, `max_videos` |
| `list_video_categories` | valid `category` values | `language` |
| `list_languages` | jw.org's languages with codes and names, filtered | `query` (part of a name or a code), `limit` |

## Workflows

### What a verse means
1. `get_bible_verse` for the wording and link; read its „Õppemärkused” section.
2. `get_study_notes` for the full notes (leave `verse` empty for a whole chapter; a long result ends with a continuation marker, call again with that `offset` only if you need the rest).
3. To show where the verse is explained, or for material for a study, talk or answer: `get_verse_references` (one verse per call; a range is refused) lists the publications that explain it. Read the cited paragraph with `read_jw_page` on the entry's link and cite that link. When the user's language has no entries the tool returns English ones with a line saying so: say so too and explain them in the user's language. A long list comes in parts: call again with the `offset` from the continuation marker.
4. Answer from the notes and the paragraphs you read, in the user's language, with the jw.org links. If the notes came in English, say so.
5. For a Hebrew or Greek word in more depth, continue with the piibli-algkeeled skill.

### Scripture from a quoted text
The user remembers words („tõde teeb teid vabaks”) but not the reference.
1. `search_jw` with the key words (`type: "article"` keeps out videos and index lines).
2. Take the reference from the hits, then `get_bible_verse` for the exact wording and link.
3. Quote from `get_bible_verse`, not from the search snippet or memory.

### Researching a topic
1. `search_jw` for articles and videos.
2. `read_jw_page` on the most relevant hits. A long page ends with a continuation marker: call again with that `offset` only if you need the rest.
3. `get_bible_verse` for the scriptures the article relies on.
4. Answer with the article titles and links.

### Daily text and meeting workbook
`get_daily_text` (today, or a `date`) and `get_meeting_workbook` (this week, or any date in the week). If the tool says the issue is not published yet, say so and offer another date.

### What a speaker said in a video
1. `search_video_subtitles` with a stem and a category (`Hommikused piibliarutelud`), or `all`: the newest videos across all categories (`max_videos` of them, default 50), which answers in a few seconds. A named category takes an equal share of each category's newest. Hits link to the moment in the video.
2. The tool scans recent videos and says how many of how many it scanned; when it stops early (after about 25 seconds) or some category lists could not be loaded, it says so. Tell the user the result is partial.
3. Nothing found? Try another stem or synonym, a wider category or `all`, a larger `max_videos`, and then `search_jw` with `type: "video"`, which also finds older videos by title and description.

### When a page fails
`read_jw_page` retries news pages on jw.org when the wol.jw.org copy is missing. If it still fails, give the user the link from the search result and say the page could not be read; do not summarise it from memory.
