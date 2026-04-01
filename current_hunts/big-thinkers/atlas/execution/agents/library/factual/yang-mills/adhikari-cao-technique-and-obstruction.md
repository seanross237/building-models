---
topic: Adhikari-Cao swapping map technique and finite→continuous obstruction
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-001 exploration-006; Adhikari-Cao Ann. Prob. 53(1) 2025 arXiv:2202.10375; Borgs counterexample to Seiler claim"
---

## The Technique: Swapping Map Method

Adhikari-Cao prove exponential correlation decay (mass gap) for **all finite gauge groups** at weak coupling via a novel swapping map method — explicitly NOT a cluster expansion.

### Step-by-step framework:

1. **Homomorphism reformulation.** Reformulate the gauge theory in terms of ψ ∈ Hom(π₁(S₁(Λ), x₀), G), where S₁(Λ) is the 1-skeleton of the dual lattice. After gauge fixing on a spanning tree T, there is a bijection (Lemma 2.14) ψ_{x₀}: G^{Λ₁} → Ω preserving support structure.

2. **Defect decomposition.** Define defects as plaquettes where holonomy is nontrivial: supp(ψ) := {p ∈ Λ₂ : ψ(ξ_p) ≠ 1}. Key counting bound (Lemma 2.8): the number of ψ with supp(ψ) = P is at most |G|^{|P|}.

3. **Swapping map construction (Definition 3.1).** Construct a bijection T: E → E on pairs (ψ₁, ψ₂) of homomorphisms that is measure-preserving and swaps the dependence on two boxes.

4. **Covariance bound (Lemma 3.2).** |Cov(h₁, h₂)| ≤ 2‖h₁‖_∞‖h₂‖_∞ · P((Ψ₁,Ψ₂) ∉ E). The probability is bounded using Peierls-type estimates on defect configurations, leveraging the Boltzmann weight e^{-βΔ_G} per defect plaquette.

### Historical context: Borgs' counterexample

Seiler's monograph (1982) claimed cluster expansions extend "without difficulty" from finite abelian to general finite groups. **Borgs showed this is FALSE:** in non-abelian theories, defects can be topologically linked (even Borromean-ring-like, with multi-body interactions) preventing standard cluster decomposition into independent connected components. The swapping map approach circumvents this entirely.

### Quantitative result

For β ≥ (114 + 4 log|G|)/Δ_G (weak coupling), correlations between gauge-invariant observables at distance L decay as exp(-(β/2)Δ_G(L-1)). Correlation length ξ ~ 2/(βΔ_G).

## The Four-Layer Finite→Continuous Obstruction

The specific mathematical obstruction preventing extension of Adhikari-Cao to SU(2) has four structural layers — these are **fundamental, not technical**:

### Obstruction 1: Loss of discrete homomorphism space
The framework rests on Hom(π₁(S₁(Λ), x₀), G) being a finite set with |Hom| ≤ |G|^{rank(π₁)}. For G = SU(2), this becomes a continuous manifold. The "defect support" structure becomes ill-defined — for continuous groups, "generic" configurations have supp(ψ) = all plaquettes. The Peierls-type suppression of large defect regions breaks down.

### Obstruction 2: Counting bound failure
Lemma 2.8 gives "|G|^{|P|} configurations with support P." For SU(2), there are uncountably many configurations with any given support. The entropy vs. energy balance (|G|^{|P|} vs. e^{-βΔ_G|P|}) that underlies the Peierls argument completely fails.

### Obstruction 3: Swapping map requires discrete bijections
The swapping map T is constructed as a bijection on pairs of discrete homomorphisms. For continuous groups, one would need a measure-preserving map on pairs of elements of a continuous Lie group manifold. The combinatorial structure used to define T has no continuous analog.

### Obstruction 4: Spectral gap Δ_G → 0 in the continuum limit
For finite subgroups G_n ⊂ SU(2) with |G_n| → ∞, the spectral gap Δ_{G_n} → 0 (SU(2) is connected and χ is continuous). Consequences:
- Weak coupling threshold β₀ ~ log|G_n|/Δ_{G_n} → ∞
- Decay rate (β/2)Δ_{G_n} → 0 for any fixed β
- Mass gap estimate degenerates — no uniform bound

### Assessment
Obstructions 1-3 mean the entire framework has **no natural extension** to continuous groups. Obstruction 4 means even a hypothetical extension would produce degenerate estimates. A **fundamentally new approach** is needed — not refinements of this technique.

## Speculative Extension Directions

1. **Uniform finite-group bounds:** If mass gap bounds for G_n were independent of |G_n| and Δ_{G_n}, limit G_n → SU(2) might work. Requires completely different estimates exploiting Lie group structure.
2. **Continuous swapping via optimal transport:** Replace discrete bijection with measure-theoretic coupling — the spirit of Chatterjee's approach, but constructing such couplings for non-abelian gauge theories is open.
3. **Abandon homomorphism framework:** Work directly on G^{Λ₁} with analytical (not combinatorial) tools — essentially the Shen-Zhu-Zhu/Bakry-Émery direction, but currently limited to strong coupling.
