# winotto

Plugin `winotto@winotto-ou`: viis ühendust ja neli skilli (jw.org otsing, Äriregistri andmed, eesti ja soome keele toimetamine).

## Paigaldus

Terminalis:

```
claude plugin install winotto --marketplace winotto-ou/claude-plugins
```

Või kahes sammus: `/plugin marketplace add winotto-ou/claude-plugins` ja `/plugin install winotto@winotto-ou`.

## Ühendused

- `jw`: jw.org otsing, Piibli salmid, artiklid ja videote subtiitrid (https://mcp.winotto.com/jw/mcp).
- `bible-lex`: Piibli algkeeled (heebrea, aramea, kreeka) sõna kaupa (https://mcp.winotto.com/bible-lex/mcp).
- `et-proof`: Eesti keelenõu, EKI andmed ja Ekilex (https://mcp.winotto.com/et-proof/mcp).
- `email`: Postkast (https://mcp.winotto.com/email/mcp).
- `arireg`: Äriregister, ettevõtted, juhatuse liikmed ja majandusaasta aruanded äriregistri avaandmetest (https://mcp.winotto.com/arireg/mcp).

Ühendus „Kõik ühes” (`/mcp`) ei kuulu pluginasse, see lisatakse portaalist.

## Skillid

- `jw-search`: Piibli salmide, jw.org sisu, artiklite ja videote subtiitrite otsing `jw` ühenduse tööriistadega.
- `estonian-proofreading`: eesti teksti korrektuur ja keelenõu `et-proof` ühenduse (EKI andmed, Ekilex) tööriistadega.
- `ariregister`: Eesti ettevõtete, registrikoodide ja juhatuse liikmete päringud `arireg` ühenduse tööriistadega.
- `suomen-oikoluku`: soome keele oikoluku Kotuse allikate ja valikulise Voikko kontrolliga.

## Litsents

Skillifailid on MIT-litsentsiga (vt repo `LICENSE`). Järgmised failid sisaldavad Kotimaisten kielten keskuse (Kotus, https://www.kotus.fi/) materjali ja on litsentsi [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) all; need ei kuulu MIT-litsentsi alla:

- `skills/suomen-oikoluku/references/ohjepankki-index.md`
- tsiteeritud näited failis `skills/suomen-oikoluku/references/pikaohje.md`
- `skills/suomen-oikoluku/examples/*.txt`
