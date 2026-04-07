# Scope: 09 — Deciding where to go

The "where?" branch. This is the comparative layer that helps an Israeli
decide which destination is worth pursuing before committing to a full
country-specific path. It compares countries against each other rather than
researching one country in isolation.

This branch should produce frameworks, matrices, and ranked shortlists,
not vague lifestyle prose. A user should come away with a narrower set of
countries to investigate and a clear reason those countries fit their
profile.

## What belongs here

- **Eligibility comparison** — which destinations are actually open to the
  user by ancestry, work route, passive-income route, student route,
  digital-nomad route, or partner/family route.
- **Cost-of-living comparison** — rent, childcare, groceries, transit,
  healthcare out-of-pocket costs, and the difference between nominal cost
  and what a newcomer without local history can really access.
- **Career-prospect comparison** — labor-market depth, language barriers,
  sector demand, salary levels, and how well Israeli experience travels.
- **Tax and money comparison** — headline tax burden, social contributions,
  treaty friendliness with Israel, banking friction, and whether the
  destination is simple or punishing for cross-border lives.
- **Healthcare comparison** — access quality, speed, coverage model,
  newcomer friction, and how friendly the system is to someone arriving
  with a chronic condition or family needs.
- **Family-fit comparison** — school quality, childcare availability,
  public-safety context, family reunification practicality, and whether
  daily life is manageable with children.
- **Community and identity fit** — Jewish / Israeli population density,
  Hebrew-speaking networks, antisemitism concerns, and whether the user is
  likely to find a social base quickly.
- **Climate, safety, distance, and travel friction** — weather, wildfire
  or heat patterns where relevant, flight availability, time-zone distance
  from Israel, and practical proximity to family.
- **Ease of arrival for Israelis specifically** — not just "is this a nice
  place to live?" but "how hard is this for an Israeli passport-holder or
  Israeli family to actually execute?"

## What does NOT belong here

- Full deep research on one country's visa rules
  → `00_eligibility-and-right-to-enter` and later `tree/_countries/`
- The administrative first-30-days landing sequence
  → `04_destination-landing`
- The user's inner moral or emotional struggle about leaving
  → `10_emotional-and-identity`
- Generic "best countries for expats" listicles with no Israel-specific
  filter

## Language note

English is often rich for comparative datasets, rankings, and broad policy
comparisons, but Hebrew matters for how Israelis discuss destinations and
where Israeli-specific friction appears. Destination-local sources matter
when a comparison turns on an official local rule rather than expat lore.

## Seeding responsibility

This branch is responsible for seeding `tree/_countries/`. A downstream
leaf in this branch should produce a `priority-15.md` artifact listing the
fifteen highest-priority destination countries for this project, with a
short rationale for each. That artifact is what determines which children
appear under `tree/_countries/`.

## Partition hint

- `01_eligibility-matrix-by-pathway`
- `02_cost-tax-and-money-comparison`
- `03_work-and-career-comparison`
- `04_healthcare-family-and-quality-of-life-comparison`
- `05_community-language-and-identity-fit`
- `06_climate-safety-distance-and-travel-friction`
- `07_priority-15-country-shortlist`

The branch agent can deviate.
