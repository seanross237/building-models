# Riemann Hypothesis Investigation — Model Learnings

**Date:** 2026-04-04 to 2026-04-06

## What the investigation was

~30 AI agents across 8+ waves exploring unconventional approaches to the Riemann Hypothesis, starting from a YouTube video about the primon gas and ending at the frontier of arithmetic geometry (Connes' program, the arithmetic site, tropical intersection theory).

## Key learnings about how models investigate hard problems

### 1. Every reformulation of a hard problem tends to be equivalent in difficulty

We reformulated RH as: thermodynamic stability, Fisher information minimization, PF kernel positivity, Möbius martingale bound, entropy maximization, and more. EVERY reformulation turned out to be equivalent to RH. This is probably a general feature of Millennium Prize problems — they've been studied so thoroughly that most "new angles" are known to be equivalent.

**Implication for future investigations:** When a reformulation seems promising, immediately check: is the hard step in the new formulation equivalent to the original problem? Our agents were good at identifying this but only after doing significant work.

### 2. Errors compound and self-correct across waves

The Polya kernel agent (Wave 2) claimed "Φ is NOT globally log-concave." This error propagated to the Fisher information and truncated primon agents. The Goldilocks agent (Wave 3) corrected it by distinguishing PF₂ from PF_∞. Later, the Euler repulsion agent (Wave 4) said "the gamma factor is the bottleneck" — corrected by the gamma bypass agent (Wave 5) which found it's the complex multiplication.

**Implication:** Multi-wave investigations naturally self-correct, but errors in early waves can waste later agents' time. A "review agent" between waves would help.

### 3. Negative results are the most valuable outputs

The single most useful finding was "PF_∞ is structurally impossible for functions with zeros" (Schoenberg 1951) — a negative result that closed an entire framework. Similarly, "the Euler product and functional equation live in complementary half-planes" was a negative observation that redirected the entire investigation toward geometry.

**Implication:** Agents should be encouraged to prove IMPOSSIBILITY results, not just attempt proofs. "Why CAN'T this work?" is often more productive than "how might this work?"

### 4. The "breakthrough question" technique works

Asking "what is the best question to ask me?" produced genuinely different thinking. The first time yielded "RH = Möbius random walk" (which led to the martingale approach — known but illuminating). The second time yielded "what bridges the two half-planes in Weil's proof?" (which led to the geometric core — the deepest level we reached).

**Implication:** Meta-questions that force reframing are more productive than direct "try harder" prompts.

### 5. Cross-disciplinary approaches are great for mapping, not for proving

We tried physics (primon gas, black holes), information theory (Fisher info, entropy), computer science (cellular automata, evolutionary search), probability (martingales, concentration), and dynamics (almost-periodicity). Each produced genuine insights about the STRUCTURE of the problem but none produced a proof path. The actual proof technology (exponential sums, arithmetic geometry) is domain-specific.

**Implication:** Use cross-disciplinary exploration to MAP a problem space, then redirect to domain-specific tools for actual progress. Don't expect physics to prove a math theorem.

### 6. The "additive not multiplicative" insight came from failure

We only discovered that globalization should be additive (intersection theory) rather than multiplicative (product of norms) AFTER watching the multiplicative approach fail repeatedly (Bohr-Jessen divergence, Euler product fluctuations). The correct approach was invisible from the starting point.

**Implication:** Failure paths carry information. Document WHY each approach fails, not just THAT it fails. The failure mode often points to the correct approach.

### 7. Codex agents are good at careful literature review and error-checking

The Codex agents (Weil positivity bridge, arithmetic intersection) were the most careful about distinguishing KNOWN from PROPOSED from CONJECTURE. They also caught errors and overclaims from earlier agents. The non-Codex agents were more creative but less rigorous.

**Implication:** Use creative agents for exploration, then Codex for verification and synthesis.

## Mathematical learnings worth preserving

1. PF_∞ controls zero EXISTENCE (zero-free), not zero LOCATION. The right framework for RH must handle functions that HAVE zeros.
2. The finite variance property V(σ) = Σ_p p^{-2σ}/2 is the correct convolution invariant replacing PF_∞. It transitions at σ = 1/2.
3. The "modular boost" (theta-function terms constructively interfering to raise PF order) is an analytic shadow of geometric positivity.
4. Connes' exact obstruction: semilocal Sonin spaces stabilize (vector spaces), but S-dependent inner products don't (partial Euler product weights). The limit can be harmonic-measure-smoothed.
5. The arithmetic Hodge-Siegel-Weil principle (our conjecture) is the most concrete proposal for the missing object.
6. **Additive globalization requires COUPLING.** Independent per-prime weights have zero optimization content (decoupling lemma): the minimax LP depends only on the total envelope mass. Coupled additive methods (mollifiers, intersection pairings, theta lifts) work because they share frequency structure with ζ's Dirichlet series. Pure envelopes can't dominate -log|ζ| because it has logarithmic singularities at every zero while bounded envelopes are O(1).
