# Winotto Claude'i pluginad

Winotto OÜ Claude'i pluginate kogu (marketplace `winotto-ou`). Praegu on siin üks plugin, `winotto`: jw.org otsing, Piibli algkeeled, Eesti keelenõu ja Postkast ühendustena ning eesti ja soome keele toimetamise skillid. Ühendused töötavad serveris https://mcp.winotto.com.

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

Free-plaanil saab lisada ainult ühe ühenduse. Lisa pluginast skillid, aga ühendusi ära lisa pluginast. Võta ühendused portaali lehelt „Tasuta Claude? Lisa kõik ühe ühendusena →”.

## Ühenduste kasutamine

Ühenduste kasutamiseks on vaja kutset portaali: https://mcp.winotto.com.

## Märkus privaatse repo kohta

Kuni see repo on privaatne, vajab claude.ai selle lugemiseks Claude'i GitHubi rakendust ja Claude Code juurdepääsu GitHubile (näiteks sisselogitud `gh` või GitHubi tunnus).

## Kontroll

`python3 scripts/check.py` kontrollib manifeste, skille ja seda, et repos ei oleks saladusi. Testid: `python3 scripts/test_check.py`.

## Litsents

MIT, vt `LICENSE`. Soome skilli sisu kohta vt `plugins/winotto/README.md`.
