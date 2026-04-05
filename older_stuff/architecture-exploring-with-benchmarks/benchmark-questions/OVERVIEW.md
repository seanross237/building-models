# Benchmark Questions

This folder is the canonical store of all test questions used to evaluate model/architecture performance.

## Sources

| Source | Questions | Auto-validate? | Difficulty | Location |
|--------|-----------|----------------|------------|----------|
| [BBEH](bbeh/) | 23 tasks (subset used) | Yes — exact match | Hard reasoning | `bbeh/` |
| [HLE](hle/) | 14 loaded, 2500+ available | Yes — exact match | Expert-level (frontier models ~53%) | `hle/` |
| [ARC-AGI-2](arc-agi/) | 4 loaded, 1000+ available | Yes — grid match | Hard abstraction (frontier models ~77%) | `arc-agi/` |
| [FrontierMath](frontiermath/) | ~5 public examples | Yes — numeric | Research-level math (frontier models ~48%) | `frontiermath/` |
| [Math Competition](math-competition/) | 14 problems | Yes — exact match | AIME #11-15 / Putnam B / IMO (frontier models ~30-50%) | `math-competition/` |
| [Code Reasoning](code-reasoning/) | 10 problems | Yes — exact match | Medium-hard algorithmic reasoning with adversarial traps | `code-reasoning/` |

## How to Add New Questions

Each source folder has a `README.md` with access instructions. New questions go in `questions.md` for that source.

Format for each question entry:
```
## Q[N]: [short title]
**Source:** [dataset + ID if available]
**Subject:** [topic]
**Answer type:** exactMatch | multipleChoice | manual
**Answer:** [exact expected answer]
**Validation:** auto | Sean-manual
**Model results:** [leave blank until tested]

[Full question text here]
```

## Running Questions

Use the T5 Triple Fusion system prompt (Experiment 7 winner) as the baseline:
> "Default to EXCLUSION -- better to select too few. Ground every claim in specific cited evidence. Before committing, consider the OPPOSITE of your initial reading. Check if surface patterns are misleading you. Only include what survives all three checks."

Ask for answers in format: `Final answer: [answer]`
