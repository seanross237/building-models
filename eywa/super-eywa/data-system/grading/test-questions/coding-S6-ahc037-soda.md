# S6. AHC037 / Soda

- Type: Coding
- Subtype: Score-gradient task
- Source: https://atcoder.jp/contests/ahc037/tasks/ahc037_a

## Task

Starting from beverage (0, 0), build a target set of 1000 beverages with desired sweetness and carbonation pairs using a sequence of monotone derivation operations with minimum total cost.

## Grading

round(10^6 * NL / (1 + C)), where C is total cost and L is the max coordinate scale.
Higher is better.

## Why It Discriminates

This is a hard constructive optimization / DAG design problem.
It rewards reuse, abstraction, and discovering shared intermediate states.

## Notes

- 
