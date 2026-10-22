# winotto

Plugin `winotto@winotto-ou`: neli ühendust ja eesti ning soome keele skillid.

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

Ühendus „Kõik ühes” (`/mcp`) ei kuulu pluginasse, see lisatakse portaalist.

## Skillid

Skillid asuvad kaustas `skills/`; loend lisatakse siia, kui skillid on olemas.

## Litsents

Skillifailid on MIT-litsentsiga (vt repo `LICENSE`). Soome skilli sisu sisaldab Kotimaisten kielten keskuse (Kotus) materjali litsentsi CC BY-NC-ND 4.0 all; see sisu ei kuulu MIT-litsentsi alla.
