# Winotto Claude'i pluginad

Winotto OÜ Claude'i pluginate kogu (marketplace `winotto-ou`). Praegu on siin üks plugin, `winotto`: kuus ühendust (jw.org otsing, Piibli algkeeled, Eesti keelenõu, Soome keelenõu, Postkast ja Äriregister) ja kuus skilli (`jw-search`, `piibli-algkeeled`, `estonian-proofreading`, `suomen-oikoluku`, `postkast`, `ariregister`). Ühendused töötavad serveris https://mcp.winotto.com.

## Paigaldus claude.ai-s

1. Ava Customize → Plugins → Add → Add marketplace ja sisesta `winotto-ou/claude-plugins`.
2. Vali plugin `winotto` ja vajuta Install.
3. Ava plugina Connectors-vahekaart ja vajuta vajalike ühenduste juures Connect.

## Paigaldus Claude Code'is

```
/plugin marketplace add winotto-ou/claude-plugins
/plugin install winotto@winotto-ou
```

## Free-plaan

Kui kasutad Free-plaani (seal saab lisada ainult ühe ühenduse), lisa plugin skillide jaoks, aga ära vajuta pluginas ühenduste juures „Connect”; lisa tööriistad portaalist reaga „Tasuta Claude? Lisa kõik ühe ühendusena →”.

## Ühenduste kasutamine

Ühenduste kasutamiseks on vaja kutset portaali: https://mcp.winotto.com.

## Märkus privaatse repo kohta

Kuni see repo on privaatne, vajab claude.ai selle lugemiseks Claude'i GitHubi rakendust ja Claude Code juurdepääsu GitHubile (näiteks sisselogitud `gh` või GitHubi tunnus). Kuni repo on privaatne, saavad marketplace'i lisada ainult inimesed, kellel on repole juurdepääs.

## Kontroll

`python3 scripts/check.py` kontrollib manifeste, skille ja seda, et repos ei oleks saladusi. Testid: `python3 scripts/test_check.py`. Kohalik paigalduskontroll ajutise seadistuskaustaga (ei puuduta sinu `~/.claude`): `bash scripts/try_install.sh`.

## Litsents

MIT, vt `LICENSE`. MIT katab repo enda failid; Kotuse materjalist tuletatud failid, mis on loetletud failis `plugins/winotto/README.md`, on litsentsi CC BY-NC-ND 4.0 all.
