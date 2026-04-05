# ARC-AGI-2

## What it is
Grid transformation puzzles testing fluid intelligence / abstract reasoning. Each task shows 3-5 input/output grid pairs as demonstrations; the model must infer the transformation rule and apply it to a new input. Tasks are designed so any human can solve them in minutes but resist pattern-matching shortcuts.

## Current model scores (March 2026)
| Model | Score (unlimited compute) | Score (resource-constrained) |
|-------|--------------------------|------------------------------|
| Gemini 3.1 Pro | 77.1% | — |
| Claude Opus 4.6 | 68.8% | — |
| Kaggle competition winner | — | ~24% |
| Human | ~98% | ~98% |

ARC-AGI-1 is largely solved (90%+). ARC-AGI-2 remains hard, especially under compute constraints.

## Access
All training and public evaluation tasks are fully open:
- **ARC-AGI-2 training (1,000 tasks):** `https://github.com/arcprize/ARC-AGI-2/tree/main/data/training`
- **ARC-AGI-2 public eval (120 tasks):** `https://github.com/arcprize/ARC-AGI-2/tree/main/data/evaluation`
- **ARC-AGI-1 (400 training + 400 eval):** `https://github.com/fchollet/ARC-AGI/tree/master/data`
- Fetch any task: `https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/data/training/<task_id>.json`
- Interactive explorer: arcprize.org

## Grid format
- Grids are 2D arrays of integers 0–9
- Color mapping: 0=black, 1=blue, 2=red, 3=green, 4=yellow, 5=grey, 6=magenta, 7=orange, 8=light-blue, 9=maroon
- Grid sizes: 1×1 to 30×30

## How to run as text
Represent grids as raw JSON arrays (no conversion needed — LLMs parse this natively):
```
Here are training examples showing an input→output transformation.
Figure out the rule and apply it to the test input.

Training Example 1:
Input: [[7,9],[4,3]]
Output: [[7,9,7,9,7,9],[4,3,4,3,4,3],[9,7,9,7,9,7],[3,4,3,4,3,4],[7,9,7,9,7,9],[4,3,4,3,4,3]]

[... more examples ...]

Test Input: [[3,2],[7,8]]
Output:
```
Validate: exact grid match (compare arrays element-by-element).

## Questions loaded
See [questions.md](questions.md) — 4 tasks with full JSON, transformation rule, and text-prompt format.
