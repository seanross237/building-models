# Scope: _countries

The cross-cutting country-specialization branch. This folder is where the
project eventually keeps one branch per destination country, so that
country-specific rules have a single canonical home instead of being
duplicated across the domain branches.

Examples of future children: `portugal/`, `germany/`, `canada/`,
`united-kingdom/`, `spain/`, `netherlands/`. Each such child is itself a
branch whose job is to organize that country's material across visas, tax,
healthcare, housing, work, community, and destination-specific quirks.

## What belongs here

- **Country-specific consolidations** — anything that is fundamentally
  about one destination country and would otherwise be repeated across
  multiple domain branches.
- **Per-country sub-branches** — each destination gets its own subtree,
  with children such as visa pathways, tax and money, healthcare, housing
  and arrival, work and credential recognition, community and language,
  and "country quirks" that do not fit neatly elsewhere.
- **Cross-references from the domain branches** — leaves elsewhere in the
  tree may summarize a country-specific rule locally and point here for the
  full country page.
- **Canonical country pages** — if five branches need Portugal-specific
  detail, `_countries/portugal/` should become the single deeper home.

## What does NOT belong here

- The decision of which countries deserve deep country branches
  → `09_deciding-where-to-go`
- Generic domain knowledge that applies across many destinations
  → the numbered domain branches
- A self-generated partition on first spawn. This parent branch does not
  get to invent country children before `09_deciding-where-to-go` seeds
  them.

## Language note

Country children should expect destination-local language to matter
heavily. English and Hebrew still matter, but the official rule set for a
country usually lives in that country's own language first.

## Partition hint

On first spawn, do NOT partition this branch into country children. Instead:

- write `WAITING-FOR-SEEDING`
- exit

This branch is populated only AFTER `09_deciding-where-to-go` identifies
the top 15 destination countries and deposits child scopes here. Once
children exist, each country child should itself be a branch and may later
partition into topics such as:

- `01_visa-and-entry-paths`
- `02_tax-and-money`
- `03_healthcare`
- `04_housing-and-arrival`
- `05_work-and-credentials`
- `06_community-language-and-school`
- `07_country-quirks-and-pitfalls`

But that partition happens inside each country child, not here at the
parent `_countries/` level.
