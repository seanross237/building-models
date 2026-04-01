---
topic: BCFW triangulation of the amplituhedron — rigorous proof (Inventiones 2025)
confidence: verified
date: 2026-03-27
source: "amplituhedron strategy-001 exploration-004; Even-Zohar, Lakrec, Tessler arXiv:2112.02703 Inventiones Mathematicae 239(2025)1009-1138"
---

## The Result

The conjecture that BCFW recursion gives exactly a triangulation of the amplituhedron was rigorously proved by Even-Zohar, Lakrec, and Tessler, published in Inventiones Mathematicae (arXiv:2112.02703, Inventiones Math. 239(2025)1009–1138). The original conjecture was stated in 2013 (Arkani-Hamed & Trnka, arXiv:1312.2007). Proof required 12 years.

## What Was Proved

1. **Injectivity**: BCFW cells map injectively into the amplituhedron. Proved from combinatorics using chord diagrams and domino matrices.
2. **Surjectivity**: BCFW cells tile the amplituhedron without gaps. Proved via a topological argument.
3. **Topology**: The interior of the amplituhedron is homeomorphic to an open ball.

## Why Spurious Poles Cancel (Geometric Argument)

The BCFW decomposition breaks the amplituhedron into cells. Each cell has poles at ALL its boundaries:
- **Outer boundaries** (boundaries of the full amplituhedron) — correspond to physical singularities
- **Internal boundaries** (shared between adjacent BCFW cells) — correspond to spurious poles

When two adjacent BCFW cells share an internal boundary, they induce **opposite orientations** on that boundary. Their contributions to the sum appear with opposite signs, so they cancel identically.

When a boundary is the outer boundary of the full amplituhedron, all cells agree on the orientation — contributions add.

This is the geometric explanation for why BCFW decompositions produce amplitudes with only physical poles, despite each individual cell having non-physical poles.

## Significance

This proof formally completes the central geometric claim for locality emergence in the amplituhedron: spurious poles cancel **because they are internal to the triangulation**, not because of any ad hoc cancellation. The result closes a logical gap that existed for 12 years between the original conjecture and rigorous proof.

The complexity of the proof methods (chord diagrams, domino matrices, topological arguments) suggests the geometric structure is genuinely non-trivial — not a trivially obvious fact. The homeomorphism to an open ball was a key technical input for the surjectivity argument.
