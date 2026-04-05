# FrontierMath

## What it is
Research-level mathematics problems created by 60+ professional mathematicians. Tiers 1–4 (~350 problems) range from hard undergraduate to multi-day research problems. Also has ~14 genuinely unsolved open problems. Answers are exact numbers or SymPy expressions, verified programmatically.

## Current model scores (March 2026)
| Model | Score (Tiers 1–3) |
|-------|-------------------|
| GPT-5.4 | 47.6% |
| Claude Opus 4.6 | ~35% (estimated) |
| Launch scores (late 2024) | <2% |
| Tier 4 specifically | ~38% (best) |

**Note:** Scores are self-reported by model providers. Epoch AI's independent verification found actual scores ~10-15pp lower than self-reported.

## Access situation
- **Main dataset (Tiers 1–4):** GATED. Owned by OpenAI; Epoch AI cannot share with third parties without written permission. Contact: math_evals@epochai.org
- **Public sample problems:** ~12 problems publicly posted at epoch.ai/frontiermath/tiers-1-4/benchmark-problems
- **Open Problems:** ~14 unsolved problems with full public statements at epoch.ai/frontiermath/open-problems (ZIP available)
- **Paper:** arxiv.org/abs/2411.04872

## Answer format
Models submit a Python `answer()` function returning an integer or SymPy expression. For our purposes, exact numeric/symbolic answers work fine.

## Alternative open datasets
If FrontierMath access remains blocked, these are publicly available and similarly hard:
| Dataset | Level | Access |
|---------|-------|--------|
| HARDMath | Graduate applied math | github.com/sarahmart/HARDMath |
| OlympiadBench | Olympiad math + physics | github.com/OpenBMB/OlympiadBench |
| HMMT Feb 2025 | Harvard-MIT competition | huggingface.co/datasets/MathArena/hmmt_feb_2025 |

## Questions loaded
See [questions.md](questions.md) — 5 public sample problems from the Epoch AI website.
