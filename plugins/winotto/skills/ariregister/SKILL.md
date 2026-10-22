---
name: ariregister
description: "Use for questions about Estonian companies from the business register (äriregister): finding a company by name or registry code, board members (juhatuse liikmed), shareholders, VAT number (KMKR), address, contacts, field of activity (EMTAK), legal form, status and annual report (majandusaasta aruanne) information, and for finding which companies a named person sits on the board of. TRIGGER on: 'äriregister', 'registrikood', 'juhatuse liige', 'kes on juhatuses', 'mis firma', 'OÜ', 'AS', 'ettevõtte andmed', 'taustakontroll', 'KMKR', 'Estonian company', 'registry code', 'board member', 'company background check', or when the user gives an 8-digit Estonian registry code or a company name ending in OÜ, AS, TÜ, MTÜ or FIE."
---

# Estonian business register (Äriregister)

## Overview

The „Äriregister” connector gives read-only access to the open data of the Estonian commercial register (RIK). Use it for facts about a company or about a person's role in companies. It does not browse or rank companies.

## Tool names

The tools may carry a prefix depending on how they were added: `ariregister_search_companies` in the one-connection „Winotto (kõik ühes)” setup; in Claude Code the name is longer and ends with `__search_companies`. Match a tool by the name it ends with.

## Available tools

- `search_companies(query, include_deleted=False, limit=10)`: find a company. A query of exactly 8 digits is a registry code lookup and finds a company of any status. Any other query is a name search (the name contains the text). Set `include_deleted` only when the user asks about a dissolved or deleted company.
- `get_company(code, include_past_people=False)`: the full profile of one company by registry code: name, status, legal form, VAT number, addresses, contacts, share capital, activities (EMTAK), annual report information, current people (board members, shareholders) and name history. Set `include_past_people` only when the user asks about former board members or owners.
- `find_person(name, role="", active_only=True, limit=20)`: find the roles a person holds in companies. Matching is by name prefix: "First Last" matches names that start with those words (so "Mari Tamm" also finds "Marika Tammik"); each row has `exact_name`. One word also finds a company holding a role, by one word of its name (for example `find_person("Raamatupidaja")`). `role` is a role code (for example `JUHL` for board member, `OSAN` for shareholder) or role text. Set `active_only=False` only when the user asks about past roles.

## Workflow

- Company by name: `search_companies` with the name, pick the right company from the hits (ask the user if several fit), then `get_company` with its registry code.
- Company by registry code: `get_company` directly, or `search_companies` with the 8 digits if you are unsure the code is valid.
- Person: `find_person` with the full name (add `role` when the user asks only for board membership or ownership), then `get_company` for the companies the user wants to know more about.
- Several searches in one answer are fine, but do not walk the register: answer what was asked.

## Answering

- Answer in the user's language, whatever language the data is in.
- Give the source line and the company link exactly as the tool returns them (the source line once per tool result, not per fact; `Allikas: äriregistri avaandmed (RIK), seisuga <date>` and `https://ariregister.rik.ee/est/company/<code>`). The date shows how fresh the data is; do not present it as live.
- Take only what the tool returned. Do not fill gaps from memory, and say so when a field is empty.
- Report only rows whose name equals the asked name (`exact_name` true), unless the user gave a partial name; mention that rows marked as a name prefix only were left out.
- Several people may share one name. A name match does not prove it is the same person, and the register data shown here has no personal identification code to tell them apart. Say this when a name returns hits in unrelated companies, and let the user confirm which one they mean (for example by the company).

## What the data does not cover

- No search by field of activity, location, size or financial figures across all companies (for example "all IT companies in Tartu" or "the biggest companies in Estonia"). Say so plainly and offer what works: a search by name or registry code, or a lookup of a person's roles.
- The data comes from the open register data, so it has no personal identification codes and no addresses of private persons. Companies' own addresses are available.
- For legal persons in a role (a company that is a shareholder, for example) the registry code is shown, so you can continue with `get_company`.
- Annual report data shows which fiscal years have report data (period, employees, activity) — no financial figures and no filing dates.

## Privacy

Do not compile a profile of a private person beyond what the user asked. Report the roles and dates the register shows and stop there. Do not guess private details, contact information or addresses, and do not combine register results with other sources to identify a person.
