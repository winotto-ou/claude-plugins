---
name: jw-search
description: "Use the jw.org tools to look up Bible verses (New World Translation), search jw.org content, read articles, get the daily text and the meeting workbook, and search video subtitles. TRIGGER when: user asks about Bible verses, scriptures, JW publications, Watchtower articles, jw.org content, JW videos, morning worship, the daily text, the meeting workbook, or anything related to Jehovah's Witnesses content. Also trigger when user mentions 'Bible', 'scripture', 'verse', 'jw.org', 'Watchtower', 'piibel', 'piiblisalm', 'kirjakoht', 'päevatekst', 'töövihik', 'koosolek', 'jw video', 'subtitle search', or wants to find what a speaker said in a talk. For the Hebrew or Greek words behind a verse use the piibli-algkeeled skill."
---

# jw.org search

You have the tools of the Winotto „jw.org otsing” connector: Bible verses and chapters (New World Translation), jw.org search, page reading, the daily text, the meeting workbook and video subtitle search.

## Tool names

The tools may carry a prefix depending on how they were added. In the one-connection „Winotto (kõik ühes)” setup every tool starts with its service prefix: `jw_` (jw.org otsing, e.g. `jw_search_jw`), `algkeeled_` (Piibli algkeeled), `keelenou_` (Eesti keelenõu), `suomi_` (Soome keelenõu), `postkast_` (Postkast), `ariregister_` (Äriregister). In Claude Code the name is longer and ends with `__search_jw`. Match a tool by the name it ends with.

## Ground rules

- **Bible text only from the tool.** Every verse you quote comes from `get_bible_verse` or `get_bible_chapter`, never from memory. If you only remember the wording, find the verse first (see „Scripture from a quoted text” below).
- **Always cite the link.** Each result carries its wol.jw.org or jw.org link; put it next to what you quote. Never build or guess a link yourself.
- **Answer in the user's language.** Quote the Bible and publications in the language you fetched them in.
- **Default language is Estonian (`et`).** Pass another `language` code only when the user writes in or asks for another language (`en`, `fi`, …; `list_languages` lists the codes). When a result is marked as found in another language than you asked for, tell the user. Leaving an optional parameter empty gives its default.
- **Search with word stems.** Estonian has 14 cases: search `andesta`, not `andestamisest`; `piibliaru`, not `piibliaruteludest`. This matters most for subtitles.
- **Book names in Estonian work** in any common form: `Johannese`, `Joh`, `1. Moosese`, `1Mo`, `Õp`, `Mt`, also with a case ending (`Johannesest`), as well as English (`John`, `1 Cor`). If a name is not recognised, the error suggests the form that works; `search_bible_books` resolves doubtful names.
- **Original-language questions** (what a Greek or Hebrew word means, Strong's numbers, interlinear) belong to the piibli-algkeeled skill and its `algkeeled_` tools. Use this skill for the verse text itself.

## Tools

| Tool | Use for | Main parameters |
|---|---|---|
| `get_bible_verse` | one verse or a range, with its link | `book`, `chapter`, `verse` (`"16"` or `"14-16"`), `language` |
| `get_bible_chapter` | a whole chapter, with its link | `book`, `chapter`, `language` |
| `search_bible_books` | Estonian/English book names and numbers (local, no network) | `query`, `limit` |
| `search_jw` | articles, verses and videos on jw.org; index hits are collapsed to one line | `query`, `language`, `limit`, `sort` (`relevance`/`newest`), `type` (`all`/`article`/`video`/`index`) |
| `read_jw_page` | the text of a jw.org or wol.jw.org page, in parts | `url`, `max_chars` (default 12000), `offset` |
| `get_daily_text` | the daily text („Uuri pühakirja iga päev”) | `date` (`YYYY-MM-DD`, empty = today), `language` |
| `get_meeting_workbook` | the midweek meeting programme for the week of a date | `date` (empty = this week), `language` |
| `search_video_subtitles` | what was said in recent videos, with a link to the moment | `query` (stem), `category` (name or key, several comma-separated, or `all`), `language`, `limit`, `max_videos` |
| `list_video_categories` | valid `category` values | `language` |
| `list_languages` | valid `language` codes | — |

## Workflows

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
1. `search_video_subtitles` with a stem and a category (`Hommikused piibliarutelud`, or `all`). Hits link to the moment in the video.
2. The tool scans recent videos and says how many of how many it scanned; it may stop early with partial results. Say so if it did.
3. Nothing found? Try another stem or synonym, a wider category or `all`, a larger `max_videos`, and then `search_jw` with `type: "video"`, which also finds older videos by title and description.

### When a page fails
`read_jw_page` retries news pages on jw.org when the wol.jw.org copy is missing. If it still fails, give the user the link from the search result and say the page could not be read; do not summarise it from memory.
