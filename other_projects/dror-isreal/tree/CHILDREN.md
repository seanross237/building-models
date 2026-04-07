# Children of the root

The root partition is **pre-committed**. A human (not an agent) decided
these 11 domains plus the `_countries/` cross-cut. Do not re-partition.

Every entry below corresponds to a folder at `tree/<name>/` with its own
`SCOPE.md` and `TYPE=branch`. Each domain branch will partition itself
further.

## Partition rationale

Domain-first, because the conversational product needs to ask "what do you
need to handle?" before it asks "where are you going?". Country-specific
information is cross-cut into `_countries/` and referenced from leaves that
need it, to prevent duplication.

Three Israel-specific domains are broken out (`01_exiting-israel`,
`02_money-and-tax` — which includes Israeli-side tax exit, and
`10_emotional-and-identity` — which includes the yerida framing) because
the audience is specifically Israeli, not generic expats.

## Children

- **00_eligibility-and-right-to-enter** — Every legal pathway by which an
  Israeli can obtain the right to live in another country.
- **01_exiting-israel** — All obligations, formalities, and practical
  wind-downs on the Israeli side of leaving.
- **02_money-and-tax** — Cross-border financial life, including Israeli
  tax exit, destination tax residency, double-taxation, pensions, and
  moving money.
- **03_logistics-of-the-move** — The physical move: movers, pets, vehicles,
  customs, shipping.
- **04_destination-landing** — The first 30 days in the destination:
  housing, ID, bank, phone, address registration.
- **05_healthcare** — Leaving Kupat Holim, bridging insurance, registering
  with destination healthcare, continuity of care.
- **06_work-and-income** — Work authorization, freelancing, remote work,
  startup visas, credential recognition.
- **07_family-and-education** — Moving with a partner or children: schools,
  family reunification, custody, bagrut recognition.
- **08_community-and-language** — Israeli communities abroad, language
  learning, social integration.
- **09_deciding-where-to-go** — Comparison frameworks for choosing a
  destination. Will seed the top 15 priority countries for `_countries/`.
- **10_emotional-and-identity** — The psychological, cultural, and
  identity dimensions of yerida.
- **_countries/** — Cross-cutting country-specific specializations.
  Initially empty. Populated as leaves across the other branches surface
  country-specific content that needs a single home.
