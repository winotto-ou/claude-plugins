---
name: jw-search
description: "Use the JW Bible MCP tools to look up Bible verses, search jw.org content, read articles, and search video subtitles. TRIGGER when: user asks about Bible verses, scriptures, JW publications, Watchtower articles, jw.org content, JW videos, morning worship, meeting workbook, or anything related to Jehovah's Witnesses content. Also trigger when user mentions 'Bible', 'scripture', 'verse', 'jw.org', 'Watchtower', 'piibel', 'piiblisalm', 'jw video', 'subtitle search', or wants to find what a speaker said in a talk."
---

# JW Bible MCP Tools

You have access to the jw.org tools of the Winotto „jw.org otsing” connector. Use them to look up Bible verses, search articles, read pages, and search video subtitles.

## Tool names

The tools may carry a prefix depending on how they were added: `jw_search_jw` in the one-connection „Winotto (kõik ühes)” setup; in Claude Code the name is longer and ends with `__search_jw`. Match a tool by the name it ends with.

## Language Handling

- The default language is **Estonian (et)**. When the user writes in Estonian, use `language: "et"`. When they write in English, use `language: "en"`.
- Detect the user's language from their message and set the `language` parameter accordingly.
- For subtitle/content searches in Estonian: use **word stems** rather than full declined forms, since Estonian has 14 grammatical cases. For example, search "piibliaru" instead of "piibliaruteludest" to match all forms.

## Available Tools

### 1. Bible Verse Lookup — `get_bible_verse`

Look up specific verses. Supports ranges.

```
book: "John"          # Book name or abbreviation (Gen, 1 Cor, Rev, etc.)
chapter: 3            # Chapter number
verse: "16"           # Verse or range like "14-16"
language: "et"        # Optional, defaults to "et"
```

### 2. Bible Chapter — `get_bible_chapter`

Fetch an entire chapter.

```
book: "Genesis"
chapter: 1
language: "et"
```

### 3. Bible Book Search — `search_bible_books`

Resolve ambiguous book names. Pure local lookup, no network.

```
query: "john"         # Partial name, abbreviation, or number
limit: 5              # Max results
```

### 4. Bible Verse URL — `get_bible_verse_url`

Get a direct wol.jw.org link to a verse without fetching content.

```
book: "Romans"
chapter: 8
verse: "28"
language: "et"
```

### 5. Search jw.org — `search_jw`

Search articles, Bible verses, and videos on jw.org.

```
query: "resurrection hope"
language: "et"
limit: 10
sort: "relevance"     # or "newest"
```

### 6. Read jw.org Page — `read_jw_page`

Fetch and read the full content of any jw.org or wol.jw.org page. Use with URLs from search results.

```
url: "https://wol.jw.org/et/wol/d/r37/lp-st/..."
```

### 7. Search Video Subtitles — `search_video_subtitles`

Search for text within video subtitles. Returns matching timestamps with context. Accepts category names in any language.

```
query: "usk"                              # Use word stems for Estonian
category: "Hommikused piibliarutelud"     # Display name or key
language: "et"
limit: 5                                  # Max matching videos
max_videos: 50                            # How many videos to scan
```

### 8. List Video Categories — `list_video_categories`

List all available video categories with display names and API keys.

```
language: "et"
```

### 9. List Languages — `list_languages`

List known language codes. No parameters.

## Workflow Patterns

### Finding what a speaker said in a talk
1. Use `search_video_subtitles` with a keyword and category (e.g., "Hommikused piibliarutelud")
2. Results include timestamps — the user can jump to the exact moment

### Researching a Bible topic
1. Use `search_jw` to find relevant articles and videos
2. Use `read_jw_page` to read the full article content
3. Use `get_bible_verse` to look up referenced scriptures

### Looking up a scripture
1. If the book name is ambiguous, use `search_bible_books` first
2. Use `get_bible_verse` for specific verses or `get_bible_chapter` for full chapters
3. Use `get_bible_verse_url` to provide a shareable link
