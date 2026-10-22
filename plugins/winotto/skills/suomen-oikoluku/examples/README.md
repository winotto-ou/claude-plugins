# Examples

Both texts are our own Finnish text, written for this skill (MIT, like the rest of the skill). `clean.txt` is the correct version; `with-errors.txt` is the same text with 7 errors:

1. missing comma before the relative clause: "palvelu, jonka …"
2. harjoitelaan → harjoitellaan (typo)
3. ennenkaikkea → ennen kaikkea (wrongly fused)
4. oikein kirjoitusta → oikeinkirjoitusta (wrongly split compound)
5. "jokaisesta jokaisesta" duplicated word
6. missing comma between two complete main clauses: "tekstejä, ja parhaat …"
7. Suomalaiset → suomalaiset (nationality lowercase)

Voikko catches 2, 3, 5, 7 and hints at 1 ("saattaa puuttua pilkku"); `clean.txt` gives no Voikko findings. Items 4 and 6 must be found by reading. Use this to sanity-check the skill after changes: the report should list all 7, each with an ohjepankki source, and nothing in `clean.txt`.
