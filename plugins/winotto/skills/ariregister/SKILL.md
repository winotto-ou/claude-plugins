---
name: ariregister
description: "Use for questions about Estonian companies from the business register (äriregister): finding a company by name or registry code, board members (juhatuse liikmed), shareholders, VAT number (KMKR), address, contacts, field of activity (EMTAK), legal form, status and annual report (majandusaasta aruanne) information, for finding which companies a named person sits on the board of, and for listing companies by field of activity (EMTAK) and location, such as IT companies in Tartu. TRIGGER on: 'ettevõtted valdkonnas', 'firmad Tartus', 'EMTAK', 'äriregister', 'registrikood', 'juhatuse liige', 'kes on juhatuses', 'mis firma', 'OÜ', 'AS', 'ettevõtte andmed', 'taustakontroll', 'KMKR', 'Estonian company', 'registry code', 'board member', 'company background check', or when the user gives an 8-digit Estonian registry code or a company name ending in OÜ, AS, TÜ, MTÜ or FIE."
---

# Estonian business register (Äriregister)

## Overview

The „Äriregister” connector gives read-only access to the open data of the Estonian commercial register (RIK). Use it for facts about a company or about a person's role in companies, and for lists of companies in a field of activity or a place. It does not rank companies by size or financial figures.

## Tool names

The tools may carry a prefix depending on how they were added. In the one-connection „Winotto (kõik ühes)” setup every tool starts with its service prefix: `ariregister_` (Äriregister, e.g. `ariregister_search_companies`), `jw_` (jw.org otsing), `algkeeled_` (Piibli algkeeled), `keelenou_` (Eesti keelenõu), `suomi_` (Soome keelenõu), `postkast_` (Postkast). In Claude Code the name is longer and ends with `__search_companies`. Match a tool by the name it ends with.

## Available tools

- `search_companies(query="", activity="", location="", include_deleted=False, limit=10)`: find a company. A query of exactly 8 digits is a registry code lookup and finds a company of any status. Any other query is a name search (the name contains the text). With `activity` and/or `location` it searches all companies: `activity` is an EMTAK code prefix of 2–6 digits (`62` computer programming and IT consultancy, `6201` programming) or Estonian words from the activity name (`raamatupidamine`); `location` is a settlement, municipality or county in its base form (`Tartu`, `Harju maakond`, not `Tartus`); `query` then narrows by name. Such a result gives the total number of matches, ordered by name, each with its main activity and location. Set `include_deleted` only when the user asks about a dissolved or deleted company.
- `get_company(code)`: the full profile of one company by registry code: name, status, legal form, VAT number, registration date, address, contacts, share capital, activities (EMTAK, main activity first), annual report information (the latest 3 years, with the total count), representation rights (esindusõigus: how the board may represent the company, as recorded), the people on the registry card (board members, partners, liquidators, procurators, contact persons …, with role and dates) and earlier names.
- `find_person(name, role="", limit=20)`: the companies where a person is on the registry card. `name` is "First Last": the **last word** matches the start of the last name and the **rest** the start of the first name, so "Mari Tamm" also finds "Marika Tammik"; each row has `exact_name`. `role` is a role code (`JUHL` board member, `OSAN` shareholder or partner, `LIKV` liquidator, `PROK` procurator …) or words of the role name (`juhatuse`).
- Past people: the open data has only the current people on the card. `include_past_people` (get_company) and `active_only=False` (find_person) add nothing, and the answer says so. For former board members or owners point to ariregister.rik.ee.

## Workflow

- Company by name: `search_companies` with the name, pick the right company from the hits (ask the user if several fit), then `get_company` with its registry code.
- Company by registry code: `get_company` directly, or `search_companies` with the 8 digits if you are unsure the code is valid.
- Companies in a field or place ("IT-ettevõtted Tartus"): `search_companies` with `activity` (prefer an EMTAK code when you know it; words match only the activity names the companies reported) and `location`. Give the total the tool reports; the list is a sample ordered by name, not the biggest or best companies. Use `get_company` only for the companies the user wants to know more about. If the tool answers that the search data is being updated („otsinguandmed uuenevad”), say so and offer a search by name; it does not mean that no such company exists.
- Person: `find_person` with the full name in the order first name, last name (add `role` when the user asks only for board membership or ownership), then `get_company` for the companies the user wants to know more about.
  - Names given last name first („Tamm Mari”) do not match: if nothing fits, retry with the words swapped.
  - One word matches only the start of a **last name** or a company name. A first name alone („Mari”) finds people whose last name starts with it, which is misleading: ask for the last name instead.
  - No row with `exact_name` true: the register may hold the name with a middle name or in another form („Mari-Liis Tamm”, „Mari Anna Tamm”), which never matches exactly. Show the partial matches, say plainly that none matched the name exactly, and let the user choose.
- Several searches in one answer are fine, but do not walk the register: answer what was asked.

## Answering

- Answer in the user's language, whatever language the data is in.
- Give the source line and the company link exactly as the tool returns them (the source line once per tool result, not per fact; `Allikas: äriregistri avaandmed (RIK), seisuga <date>` and `https://ariregister.rik.ee/est/company/<code>`). The date shows how fresh the data is; do not present it as live.
- Take only what the tool returned. Do not fill gaps from memory, and say so when a field is empty.
- Report only rows whose name equals the asked name (`exact_name` true), unless the user gave a partial name; mention that rows marked as a name prefix only („ainult nime algus”) were left out. If there are no exact rows, show the partial ones and say so (see Workflow).
- Several people may share one name. A name match does not prove it is the same person, and the register data shown here has no personal identification code to tell them apart. Say this when a name returns hits in unrelated companies, and let the user confirm which one they mean (for example by the company).

## What the data does not cover

- No search or ranking by size, employees or financial figures (for example "the biggest companies in Estonia"). Say so plainly and offer what works: a list by field of activity and location, a search by name or registry code, or a lookup of a person's roles.
- Activity and location are what the company reported to the register: its reported activities (EMTAK) and its registered address, not where it actually works.
- The data comes from the open register data, so it has no personal identification codes and no addresses of private persons. Companies' own addresses are available.
- For legal persons in a role (a company that is a shareholder, for example) the registry code is shown, so you can continue with `get_company`.
- Annual report data shows which fiscal years have report data (period, employees, activity) — no financial figures and no filing dates.
- Representation rights (esindusõigus) come with `get_company` as recorded on the card; quote them, do not interpret them as legal advice.

These questions cannot be answered from this data. Say so plainly and point to ariregister.rik.ee (the company link from the tool), where the full registry card and paid reports are:

- shareholdings and percentages, and the beneficial owners (tegelikud kasusaajad);
- revenue, profit and other financial figures;
- tax debts (point to the Tax and Customs Board's public query instead);
- pledges (kommertspandid) and other encumbrances;
- former board members and owners.

## Privacy

- **Companies:** combining sources is fine. You may add the company's own website, news or other public sources to the register data when the user asks for a background check, and say which facts come from where.
- **Private persons:** be restrained. Report the roles and dates the register shows and stop there. Do not compile a profile beyond what the user asked, do not guess private details, contact information or addresses, and do not combine register results with other sources to identify a person or to find out more about them.
