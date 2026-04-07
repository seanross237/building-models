# Trust tiers

Every source cited by a leaf gets a trust tier. Each major factual claim in
a leaf must be supported by at least one **tier-1** or **tier-2** source.
Tiers 3–5 provide texture and lived-experience context but never stand alone
on a factual claim.

## Tier 1 — Government official

- Israeli ministries (`.gov.il`): `btl.gov.il` (Bituach Leumi), `taxes.gov.il`,
  `piba.gov.il` (Population and Immigration Authority), `idf.il`, etc.
- Destination-country ministries (`.gov.pt`, `.bund.de`, `.gov.uk`,
  `.canada.ca`, `.usa.gov`, etc.)
- Official gazettes and legislative portals.

Use for: visa rules, tax rules, reserve duty obligations, national insurance
rules, official fees, processing timelines (when published), statutory
requirements.

## Tier 2 — Consulate / embassy / official service provider

- Consulates and embassies (usually on the destination-country ministry of
  foreign affairs website or a dedicated subdomain).
- Official service providers like VFS Global, TLScontact, BLS — when they
  are the designated visa application partner for a given consulate.
- Major international bodies (EU official portals, UN, OECD) when they
  document a treaty or directive that drives policy.

Use for: in-person appointment procedures, required document lists,
translation/apostille requirements, fees at a specific consulate.

## Tier 3 — Established law firm, major bank, recognized relocation service

- Law firms with a published practice area for the specific topic (e.g.
  a Portuguese immigration law firm's D7 guide).
- Major Israeli banks (Hapoalim, Leumi, Discount, Mizrahi) on the topic of
  closing accounts, transferring funds, foreign-currency reporting.
- Major destination-country banks on opening accounts as a non-resident.
- Relocation services with a track record (Sixt, AGS, Crown, etc.) on
  moving logistics, pet transport, and customs.
- Big-four accounting firms (PwC, EY, Deloitte, KPMG) on tax residency
  and exit-tax questions.

Use for: interpreting the rules (not the rules themselves), procedural
nuance, cost estimates, timelines in practice.

## Tier 4 — Expat blog, community site, journalistic coverage

- Established expat-focused sites (Nomad List, Expatica, Portugal News,
  The Local, etc.).
- Israeli expat Facebook groups, Telegram communities (cited for the
  existence of community resources, not for facts).
- Mainstream journalism covering relocation topics (Haaretz, Calcalist,
  Ynet, Times of Israel, and destination-country papers).

Use for: what the lived experience is like, timelines real people report,
common pitfalls, community contacts. Never as the sole support for a rule.

## Tier 5 — Forum posts, anecdotes, individual stories

- Reddit threads, individual forum posts, personal blogs.
- YouTube vlogs from expats.

Use for: atmospheric color, warnings about specific pitfalls that haven't
been covered elsewhere. Flag explicitly in `sources.md` that these are
anecdotal. Never drive a factual claim.

## What "major claim" means

A claim is "major" (requires tier-1 or tier-2 backing) if it would change
a reader's action. Examples:

- "You must file Form X within 90 days of leaving" — major, needs tier-1.
- "Most people find the process takes around 4 months" — minor, tier-3
  or tier-4 is fine.
- "You can apply for a D7 visa at the Portuguese consulate in Tel Aviv" —
  major, needs tier-1 or tier-2.
- "Bring patience — the waiting room is slow" — minor, tier-5 OK.

## When the rule is unclear

If a leaf can't find a tier-1 or tier-2 source for a major claim, it must:

1. Record the claim as `status: unverified` in `facts.md`.
2. Note in `sources.md` what queries were tried and in what languages.
3. Point the user toward a licensed professional in the checklist.

Never fabricate tier-1 backing. "Unverified" is a valid and useful state.
