---
topic: Per-plaquette Hessian inequality H_P ≤ (β/2N)|B_P|² is DEFINITIVELY FALSE for Q≠I
confidence: verified
date: 2026-03-28
source: "yang-mills strategy-003 exploration-004"
---

## Overview

The per-plaquette bound H_P(Q,v) ≤ (β/2N)|B_P(Q,v)|² — which was the first step in the two-step proof chain toward H_norm ≤ 1/12 — is **definitively false** for Q ≠ I. Both the per-plaquette and global-sum forms fail. The entire B_P proof chain is dead; any proof of H_norm ≤ 1/12 must use a different route.

## Results

### Per-Plaquette (L=4, d=4, SU(2), β=1.0)

At Q=I: H_P = (β/2N)|B_P|² exactly (ratio = 1.000000, machine precision). This is a **flat-vacuum coincidence**.

| Config | Max per-plaq ratio | \|B_P\|²<0 count | VIOLATED? |
|--------|-------------------|--------------|-----------|
| Q=I | 1.000000 | 0/1536 | NO |
| near-id ε=0.1 | **1.770** | 0/1536 | **YES** |
| near-id ε=0.5 | **158.3** | 117/1536 | **YES** |
| random Haar 1 | **8383** | 248/1536 | **YES** |
| random Haar 2 | **2496** | 234/1536 | **YES** |

### Global Sum Σ_P (at true v_max via full eigvalsh)

| Config | λ_max = Σ H_P | (β/2N)Σ\|B_P\|² | Ratio | Violated? |
|--------|--------------|----------------|-------|---------|
| Q=I | 4.0000 | 4.0000 | 1.000 | NO |
| near-id ε=0.5 | 3.2131 | 2.0875 | **1.539** | **YES** |
| random Haar 1 | 2.0611 | 1.0645 | **1.936** | **YES** |
| random Haar 2 | 2.0475 | 1.0745 | **1.906** | **YES** |

## Dead Proof Chain

The original two-step strategy was:
1. H_P ≤ (β/2N)|B_P|² per plaquette → **FALSE** for all Q ≠ I
2. Σ|B_P|² ≤ 4d|v|² → **TRUE** (confirmed at both L=2 and L=4)

Step 1 fails, and the global-sum relaxation (Step 1') also fails. H_norm ≤ 1/12 is still confirmed numerically but the proof **cannot** go through B_P.

## Why Q=I Is Special

At Q=I, the per-plaquette equality H_P = (β/2N)|B_P|² holds because both sides reduce to (β/2N) Σ_a (Σ_k s_k v_{k,a})². The nonlinear holonomy at Q ≠ I breaks this equality by introducing cross-terms that are positive in the Hessian but absent from |B_P|².

## Implication

Any rigorous proof of H_norm ≤ 1/12 must use a **direct spectral argument** (e.g., the B_□ inequality Σ|B_□(Q,v)|² ≤ 4d|v|²), gauge orbit convexity, or a completely different proof chain. See `b-square-inequality-proof-progress.md` for the status of alternative routes.
