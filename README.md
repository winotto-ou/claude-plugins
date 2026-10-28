# Winotto Claude'i pluginad

Winotto OÜ Claude'i pluginate kogu (marketplace `winotto-ou`). Praegu on siin üks plugin, `winotto`: kuus ühendust (jw.org otsing, Piibli algkeeled, Eesti keelenõu, Soome keelenõu, Postkast ja Äriregister) ja kuus skilli (`jw-search`, `piibli-algkeeled`, `estonian-proofreading`, `suomen-oikoluku`, `postkast`, `ariregister`). Ühendused töötavad serveris https://mcp.winotto.com.

## Paigaldus claude.ai-s

Töötab igas Claude'i plaanis, ka tasuta.

1. Ava Customize → Plugins (https://claude.ai/customize/plugins).
2. Vajuta Add → Add marketplace, sisesta `winotto-ou/claude-plugins` ja kinnita.
3. Vali pluginate seast `winotto` ja vajuta Add.
4. Ava plugina Connectors-vahekaart ja vajuta iga ühenduse juures Connect (kui seal on Add, siis enne seda); portaali lehel vajuta „Luba ühendus”.

## Paigaldus Claude Code'is

```
/plugin marketplace add winotto-ou/claude-plugins
/plugin install winotto@winotto-ou
```

## Ühenduste kasutamine

Ühenduste kasutamiseks on vaja kutset portaali: https://mcp.winotto.com.

## Kontroll

`python3 scripts/check.py` kontrollib manifeste, skille ja seda, et repos ei oleks saladusi. Testid: `python3 scripts/test_check.py`. Kohalik paigalduskontroll ajutise seadistuskaustaga (ei puuduta sinu `~/.claude`): `bash scripts/try_install.sh`.

## Litsents

MIT, vt `LICENSE`. MIT katab repo enda failid; Kotuse materjalist tuletatud failid, mis on loetletud failis `plugins/winotto/README.md`, on litsentsi CC BY-NC-ND 4.0 all.
