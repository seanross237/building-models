# Mission

## The product this serves

A conversational AI product that walks an Israeli through the process of
leaving Israel to live in another country. The AI asks a small number of
questions up-front, then walks the user stage by stage through the actions
they need to take — surfacing country-specific details as the user's
destination narrows, and returning them to earlier stages when they need
to fill a gap.

Example flow:
> User: "I want to leave Israel."
> AI: "Do you already know where you're going?"
> User: "Probably Portugal."
> AI: "Portugal requires three things for a long-stay residence permit:
>      a D7 visa, proof of sufficient funds, and Portuguese tax registration.
>      Do you have a D7 visa application in progress?"
> User: "No."
> AI: "OK — here is exactly what the D7 visa requires, how to assemble the
>      application, and what to do in what order. Where are you now in the
>      timeline?"

## Who it's for

Israelis (not generic "people moving abroad"). This audience matters because:

- **Israel-specific exit obligations** — bituach leumi (national insurance)
  transition, Kupat Holim (health fund) exit, reserve duty (miluim) status,
  tax-residency exit rules, foreign-currency controls, and bank closures are
  not covered by generic "moving abroad" content.
- **Ancestry-based EU citizenship** — a large fraction of Israelis are
  eligible for German, Polish, Romanian, Hungarian, or other EU passports
  via grandparents or great-grandparents. This is the single highest-leverage
  legal path for many users and is nearly absent from generic content.
- **Hebrew-language sources** — Israeli government documents, Israeli lawyer
  blogs, and Israeli expat communities publish in Hebrew. A knowledge base
  that only reads English sources will miss material that matters.
- **Yerida context** — the cultural framing of leaving Israel is distinct.
  The product must respect the emotional and identity dimensions, not treat
  the user as a generic expat.

## Non-negotiable constraints

1. **Every factual claim is verifiable.** No claim appears in the knowledge
   base without a source URL, fetch date, trust tier, and a short verbatim
   quote from the source.
2. **Trust tiers matter.** Government websites > consulates/embassies >
   established law firms or banks > expat blogs > forums. At least one
   tier-1 or tier-2 source is required per major claim.
3. **Three language surfaces.** Every leaf attempts English, Hebrew, and
   the destination country's local language. When a language is unavailable,
   that is recorded in `sources.md`, not hidden.
4. **Staleness is a first-class concept.** Every leaf records a
   `last_verified` date. Visa rules, tax thresholds, and consulate fees
   change. The verifier (future work) re-fetches and diffs; the product
   surfaces anything older than a per-domain cadence.
5. **Real users, real stakes.** This knowledge drives decisions about
   someone's citizenship, taxes, pension, and family. Hedging is better
   than confident-but-wrong. A leaf that reports "this is unclear and
   here are the three conflicting sources" is more valuable than a leaf
   that picks one and sounds certain.

## What this knowledge base is NOT

- Not legal or tax advice. Leaves must include a standard disclaimer and
  direct users to licensed professionals for their specific situation.
- Not a real-time feed. It's a snapshot that the verifier keeps fresh on
  a cadence. Users needing same-day accuracy on, say, a visa fee must be
  told to verify with the consulate.
- Not opinionated about the user's decision to leave. It informs, it does
  not persuade, it does not moralize.

## Out of scope for this build

- The conversational product itself — this repo produces the data it reads.
- The verifier loop — written after the initial tree is populated.
- Country-specific detail in `_countries/` — seeded organically by
  `09_deciding-where-to-go` picking the top 15 destinations first, then
  specializations appear.
