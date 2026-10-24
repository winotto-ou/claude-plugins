# winotto

Plugin `winotto@winotto-ou`: kuus ühendust ja kuus skilli (jw.org otsing, Piibli algkeeled, Postkast, Äriregistri andmed, eesti ja soome keele toimetamine).

## Paigaldus

Terminalis:

```
claude plugin install winotto --marketplace winotto-ou/claude-plugins
```

Või kahes sammus: `/plugin marketplace add winotto-ou/claude-plugins` ja `/plugin install winotto@winotto-ou`.

## Ühendused

- `jw`: jw.org otsing, Piibli salmid ja õppepiibli märkused, artiklid ja videote subtiitrid (https://mcp.winotto.com/jw/mcp).
- `bible-lex`: Piibli algkeeled (heebrea, aramea, kreeka) sõna kaupa (https://mcp.winotto.com/bible-lex/mcp).
- `et-proof`: Eesti keelenõu, EKI andmed ja Ekilex (https://mcp.winotto.com/et-proof/mcp).
- `fi-proof`: Soome keelenõu, Voikko õigekirjakontroll ja Kielitoimiston ohjepankki (https://mcp.winotto.com/fi-proof/mcp).
- `email`: Postkast (https://mcp.winotto.com/email/mcp).
- `arireg`: Äriregister, ettevõtted, juhatuse liikmed ja majandusaasta aruanded äriregistri avaandmetest (https://mcp.winotto.com/arireg/mcp).

Ühendus „Kõik ühes” (`/mcp`) ei kuulu pluginasse, see lisatakse portaalist.

## Skillid

- `jw-search`: Piibli salmid ja õppepiibli märkused, jw.org sisu, artiklid, päevatekst, koosoleku töövihik ja videote subtiitrite otsing `jw` ühenduse tööriistadega.
- `piibli-algkeeled`: salmi heebrea, aramea ja kreeka sõnad, sõnaraamatu artiklid ja esinemised `bible-lex` ühenduse tööriistadega, koos Uue maailma tõlke tekstiga `jw` ühendusest.
- `estonian-proofreading`: eesti teksti korrektuur ja keelenõu `et-proof` ühenduse (EKI andmed, Ekilex) tööriistadega.
- `suomen-oikoluku`: soome keele oikoluku Kotuse allikate järgi, `fi-proof` ühenduse tööriistadega (Voikko, Kielitoimiston ohjepankki) või ilma nendeta.
- `postkast`: oma kirjade lugemine, kokkuvõtted, vastused, mustandid, tõstmine ja kustutamine `email` ühenduse tööriistadega; saadab ja kustutab ainult sinu selge loa järel.
- `ariregister`: Eesti ettevõtete, registrikoodide, juhatuse liikmete ning valdkonna ja asukoha järgi päringud `arireg` ühenduse tööriistadega.

## Litsents

Skillifailid on MIT-litsentsiga (vt repo `LICENSE`). Järgmised failid sisaldavad Kotimaisten kielten keskuse (Kotus, https://www.kotus.fi/) materjali ja on litsentsi [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) all; need ei kuulu MIT-litsentsi alla:

- `skills/suomen-oikoluku/references/ohjepankki-index.md`
- tsiteeritud näited failis `skills/suomen-oikoluku/references/pikaohje.md`

Kaust `skills/suomen-oikoluku/examples/` sisaldab meie endi kirjutatud soomekeelset teksti (MIT).
