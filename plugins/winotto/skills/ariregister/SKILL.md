---
name: ariregister
description: "Use for questions about Estonian companies from the business register (äriregister): finding a company by name or registry code, board members (juhatuse liikmed), shareholders and their percentages (osanikud), commercial pledges (kommertspandid), VAT number (KMKR), address, contacts, field of activity (EMTAK), legal form, status, annual report figures (majandusaasta aruanne: revenue, profit, employees, auditor), the companies a named person is on the board of, and lists of companies by field of activity (EMTAK), location and revenue or its growth, such as IT companies in Tartu. TRIGGER on: 'müügitulu', 'käive', 'kasum', 'osanikud', 'ettevõtted valdkonnas', 'firmad Tartus', 'EMTAK', 'äriregister', 'registrikood', 'juhatuse liige', 'kes on juhatuses', 'mis firma', 'OÜ', 'AS', 'ettevõtte andmed', 'taustakontroll', 'KMKR', 'Estonian company', 'registry code', 'board member', 'company background check', or when the user gives an 8-digit Estonian registry code or a company name ending in OÜ, AS, TÜ, MTÜ or FIE."
---

# Estonian business register (Äriregister)

## Overview

The „Äriregister” connector gives read-only access to the open data of the Estonian commercial register (RIK). Use it for facts about a company (including its shareholders, commercial pledges and annual-report figures) or about a person's role in companies, and for lists of companies in a field of activity, a place or a revenue range. It does not rank companies by employees.

## Tool names

The tools may carry a prefix depending on how they were added. In the one-connection „Winotto (kõik ühes)” setup every tool starts with its service prefix: `ariregister_` (Äriregister, e.g. `ariregister_search_companies`), `jw_` (jw.org otsing), `algkeeled_` (Piibli algkeeled), `keelenou_` (Eesti keelenõu), `suomi_` (Soome keelenõu), `postkast_` (Postkast). In Claude Code the name is longer and ends with `__search_companies`. Match a tool by the name it ends with.

## Available tools

- `search_companies(query="", activity="", location="", include_deleted=False, limit=10, min_revenue=0, min_revenue_growth=0)`: find a company. A query of exactly 8 digits is a registry code lookup and finds a company of any status. Any other query is a name search (the name contains the text). With `activity` and/or `location` it searches all companies: `activity` is an EMTAK code prefix of 2–6 digits (`62` computer programming and IT consultancy, `6201` programming) or Estonian words from the activity name (`raamatupidamine`); `location` is a settlement, municipality or county in its base form (`Tartu`, `Harju maakond`, not `Tartus`); `query` then narrows by name. `min_revenue` (euros) and `min_revenue_growth` (percent against the year before, e.g. `20`) filter by each company's latest annual report of the last two fiscal years (0 = no filter); they work alone or with `activity`/`location`. Such a result gives the total number of matches, each with its main activity, location and latest revenue (with growth); ordered by name, or largest revenue first when a revenue filter is given. Set `include_deleted` only when the user asks about a dissolved or deleted company.
- `get_company(code)`: the full profile of one company by registry code: name, status, legal form, VAT number, registration date, address, contacts, share capital, activities (EMTAK, main activity first), annual report information (the latest 3 years, with the total count), representation rights (esindusõigus: how the board may represent the company, as recorded), the people on the registry card (board members, partners, liquidators, procurators, contact persons …, with role and dates), the shareholders of an OÜ (name, share size, percentage, ownership type, since when; the 20 largest; a legal person also with its registry code), the valid commercial pledges (amount, rank, since, holder) and earlier names.
- `company_finances(code, years=3)`: annual-report key figures year by year (1–7 years, from fiscal year 2019): revenue (non-profits: income), operating and net profit, assets, cash, equity, liabilities, share capital, employees and labour costs, each with its change % against the year before; the group's figures for a consolidated report; revenue by EMTAK activity; the audit (type, opinion, audit firm). A year filed only as PDF has no figures, and the answer says so.
- `find_person(name, role="", limit=20)`: the companies where a person is on the registry card. `name` is "First Last": the **last word** matches the start of the last name and the **rest** the start of the first name, so "Mari Tamm" also finds "Marika Tammik"; each row has `exact_name`. `role` is a role code (`JUHL` board member, `TOSAN`/`UOSAN` general or limited partner of a partnership (OÜ shareholders are not on the card), `LIKV` liquidator, `PROK` procurator …) or words of the role name (`juhatuse`).
- Past people: the open data has only the current people on the card. `include_past_people` (get_company) and `active_only=False` (find_person) add nothing, and the answer says so. For former board members or owners point to ariregister.rik.ee.

## Workflow

- Company by name: `search_companies` with the name, pick the right company from the hits (ask the user if several fit), then `get_company` with its registry code.
- Company by registry code: `get_company` directly, or `search_companies` with the 8 digits if you are unsure the code is valid.
- Companies in a field or place ("IT-ettevõtted Tartus"): `search_companies` with `activity` (prefer an EMTAK code when you know it; words match only the activity names the companies reported) and `location`. Give the total the tool reports. Without a revenue filter the list is a sample ordered by name, not the biggest or best companies; with `min_revenue` or `min_revenue_growth` it is ordered largest revenue first. Use `get_company` only for the companies the user wants to know more about. If the tool answers that the search data is being updated („otsinguandmed uuenevad”), say so and offer a search by name; it does not mean that no such company exists.
- Revenue or growth („IT-ettevõtted Tartus, mille müügitulu kasvas üle 20%”): `search_companies` with `activity`, `location` and `min_revenue_growth` (add `min_revenue`, e.g. 100000, when tiny companies would drown the list: growth from a few hundred euros means little). Say which fiscal year each figure is from (the tool shows it); a company's latest report may be a year older than another's. For one company's figures over the years use `company_finances`.
- Company's finances, owners or pledges: `company_finances` for revenue, profit, employees and the auditor; `get_company` for the shareholders and commercial pledges.
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

- No search by employees. Revenue filters work („companies with revenue over 1 M€”, largest first), but only on each company's latest annual report; companies that file only a PDF (mostly large ones, such as banks) have no figures and do not appear.
- Activity and location are what the company reported to the register: its reported activities (EMTAK) and its registered address, not where it actually works.
- The data comes from the open register data, so it has no personal identification codes and no addresses of private persons. Companies' own addresses are available.
- For legal persons in a role (a company that is a shareholder, for example) the registry code is shown, so you can continue with `get_company`.
- Annual-report figures come from the open data from fiscal year 2019 on, refreshed monthly; the source line of `company_finances` gives the cut-off date. Quote the figures with their year; do not compute ratios the user did not ask for, and do not present them as audited when the audit line says otherwise.
- Shareholders are in the data for private limited companies (OÜ) only; shareholders of an AS (kept in the Nasdaq CSD share register) are not, and the tool says so. Only the current shareholders are shown; a physical person by name only.
- Representation rights (esindusõigus) come with `get_company` as recorded on the card; quote them, do not interpret them as legal advice.

These questions cannot be answered from this data. Say so plainly and point to ariregister.rik.ee (the company link from the tool), where the full registry card and paid reports are:

- the beneficial owners (tegelikud kasusaajad), and the shareholders of an AS;
- full annual reports (notes, the auditor's report text): only the key figures are here;
- tax debts (point to the Tax and Customs Board's public query instead);
- share pledges and other encumbrances besides commercial pledges;
- former board members and owners;
- what a person owns: `find_person` searches the people on the registry card (board members and the like), not shareholdings, so "which companies does Mari Tamm own" cannot be answered; shareholders are shown only per company (`get_company`).

## Privacy

- **Companies:** combining sources is fine. You may add the company's own website, news or other public sources to the register data when the user asks for a background check, and say which facts come from where.
- **Private persons:** be restrained. Report the roles and dates the register shows and stop there. Do not compile a profile beyond what the user asked, do not guess private details, contact information or addresses, and do not combine register results with other sources to identify a person or to find out more about them.
