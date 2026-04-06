# Customer Support Machine

Autonomous customer support system — built on top of Serenade's reactive support pipeline as the first implementation, but designed to be generalizable.

## The Idea

Turn customer support into a system that handles 80%+ of emails autonomously, with human review only for edge cases. Not a chatbot — a full email response agent that knows your product, knows your voice, and knows the rules.

## Current Progress (Serenade as Test Case)

### What Exists Today

Serenade already has a reactive support pipeline in production:
- **Gmail → Apps Script → Edge Functions** — emails are ingested, classified by concern type, user context is enriched (songs count, unlocked songs, payment history), and draft responses are generated
- **Admin review UI** — Sean reviews and sends drafts (or edits them first)
- Pipeline: `reactive-ingest → reactive-update-state → reactive-draft → admin review → reactive-send`

### What We Built (April 2026)

**1. Knowledge Base (`docs/support-kb/`)**

Two research tracks ran in parallel to build product knowledge:
- **Playwright agents** — walked through the live site (homepage, creation form, sample songs, auth flow), took screenshots, documented every user-visible element
- **Code analysis agents** — read every component, extracted all user-facing content: 40+ error messages, every email users receive, FAQ answers, service facts

Output: `sources/` directory with raw research, designed to be distilled into clean `knowledge/` files.

**2. Rule Extraction from 457 Real Emails**

Pulled every first-contact support email from the database with full user context:
- `user_found`, `songs_count`, `unlocked_songs_count`, `amount_paid_cents`
- Structured `concerns` array (12 concern types)
- Sean's actual first response to each

Five parallel agents analyzed all emails by concern type and extracted **161 conditional response rules** in `WHEN → THEN` format:

| Concern Type | Rules | Top Confidence |
|---|---|---|
| Can't Access Song | 29 | 26 consistent |
| General FAQ | 22 | 16 consistent |
| Feature Request | 17 | 7 consistent |
| Other | 17 | 4 consistent |
| Download Issue | 16 | 9 consistent |
| Product Issues | 15 | 12 consistent |
| Edit Request | 13 | 10 consistent |
| Payment Issues | 11 | 10 consistent |
| Gratitude | 10 | 9 consistent |
| Money Hesitancy | 6 | 5 consistent |

**108 rules are "consistent"** (Sean always responds the same way), **12 are "uncertain"** (responses vary), **41 are "singletons"** (only 1 example).

**3. Review Interface**

Interactive HTML app where Sean can approve/reject/edit each rule, with:
- Grouping by concern type
- Confidence tags (consistent/uncertain/singleton)
- Example customer quotes + Sean's actual responses
- Inline editing of WHEN/THEN conditions
- Bulk approve for consistent rules
- Server-persisted state

### Planned Architecture

```
support-kb/
├── AGENT.md                    # Entry point: identity, tone, decision flow
├── rules/                      # Response logic (from approved rules)
│   ├── INDEX.md
│   ├── cant-access-song.md
│   ├── payment-issues.md
│   └── ...
├── knowledge/                  # Product facts (from Playwright + code analysis)
│   ├── pricing-and-payment.md
│   ├── song-creation-flow.md
│   └── ...
└── actions/                    # Capabilities (send login link, attach MP3, etc.)
```

Three-layer lookup:
1. **AGENT.md** — always loaded. Tone, personality, escalation rules.
2. **rules/{concern}.md** — loaded per detected concern. WHEN/THEN decision logic.
3. **knowledge/{topic}.md** — loaded when rules reference product facts.

### Automation Tiers (Proposed)

- **Auto-send** (~40% of emails) — Consistent rules with high confidence. Money hesitancy ("put $0"), simple access issues (send login link), gratitude replies.
- **Telegram approve** (~35%) — Draft 2-3 response variants, Sean taps to approve from his phone.
- **Human required** (~25%) — Unique situations, emotional complexity, multi-concern threads.

## Generalizing Beyond Serenade

The pattern is:
1. **Ingest** real support history (emails, tickets, chat logs)
2. **Enrich** with customer context from the product DB
3. **Extract rules** from the human's actual response patterns
4. **Human reviews** rules in an interactive UI → approve/reject/edit
5. **Build knowledge base** from product docs + automated site walkthroughs
6. **Wire into response agent** with the three-layer doc hierarchy
7. **Confidence-based routing** — auto-send vs. human-approve vs. escalate

Each step is repeatable for any product with email-based support.

## Key Insights from Serenade Data

- **"Put $0" is the universal answer** for money hesitancy AND payment issues — Sean never troubleshoots payment gateways, just bypasses them
- **Magic login links solve ~60% of access issues** — most "can't find my song" is just a login problem
- **Sean never says no to feature requests** — always validates, says it's on the list, offers manual workaround
- **Tone shifts for hardship stories** — cancer, terminal illness, disability get a more reverent response with no jokes
- **47% of money_hesitancy emails got no response** — strong automation candidate since the answer is always identical
- **Sean edits song titles on the backend but never edits audio** — for quality issues, he regenerates or refunds

## Next Steps

1. Sean reviews the 161 rules → approve/reject/edit
2. Generate `rules/` markdown files from approved rules
3. Distill `sources/` into clean `knowledge/` files
4. Write `AGENT.md` entry point
5. Wire into `reactive-draft` edge function
6. Test: replay past emails, compare agent drafts to Sean's real responses
7. Gradually enable auto-send tier, starting with highest-confidence rules

## Files & Locations

| What | Where |
|---|---|
| Reactive pipeline code | `supabase/functions/reactive-*` |
| Support KB sources | `docs/support-kb/sources/` |
| KB structure | `docs/support-kb/INDEX.md` |
| Playwright scripts | `scripts/kb-research/playwright/` |
| Code analysis prompts | `scripts/kb-research/code-analysis/` |
| Enriched email data | `/tmp/enriched-support-data.json` (457 emails) |
| Extracted rules | `/tmp/all-rules-merged.json` (161 rules) |
| Rule review app | `home-base/presentations/reactive-support-rules-2026-04-01/` |
| Rule review URL | http://localhost:8900/reactive-support-rules-2026-04-01/ |
