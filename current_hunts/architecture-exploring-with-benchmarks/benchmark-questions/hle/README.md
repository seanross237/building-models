# HLE — Humanity's Last Exam

## What it is
2,500 expert-level questions crowdsourced from ~1,000 subject-matter experts across 100+ fields. 76% exact-match short answer, 24% multiple choice. Designed to be "Google-proof" — requires genuine reasoning, not retrieval.

## Current model scores (March 2026)
| Model | Score |
|-------|-------|
| Claude Opus 4.6 | 53.1% |
| Claude Sonnet 4.6 | 49.0% |
| Human experts | ~90% (in own domain) |

Best models still fail ~47% of questions. This is the best available benchmark for genuinely hard questions.

## Access
- **Main dataset:** `cais/hle` on Hugging Face — **gated** (requires login + terms agreement)
  - After agreeing to terms on the website, use: `load_dataset("cais/hle", split="test")`
- **Public subset (what we used):** `TalentZHOU/hle_material_science` — 106 questions, no gating
  - API: `https://datasets-server.huggingface.co/rows?dataset=TalentZHOU%2Fhle_material_science&config=default&split=test&offset=0&length=50`
- **Paper:** arxiv.org/abs/2501.14249
- **Leaderboard:** lastexam.ai

## Dataset fields
- `id` — unique question ID
- `question` — full question text
- `image` — image attachment (null for text-only)
- `answer` — exact expected answer
- `answer_type` — `exactMatch` or `multipleChoice`
- `rationale` — explanation of why the answer is correct
- `raw_subject` — subject area
- `category` — broader category

## How to run
Ask: `[question text]\n\nGive only your final answer, nothing else.`
Validate: exact string match (case-insensitive) against `answer` field.

## Questions loaded
See [questions.md](questions.md) — 14 text-only questions with answers and rationales.
