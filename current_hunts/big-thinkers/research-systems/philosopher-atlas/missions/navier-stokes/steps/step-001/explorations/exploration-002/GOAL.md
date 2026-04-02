# Exploration 002: Lin (1998) Proof Architecture

## Objective

Analyze Fanghua Lin's simplified proof (1998) of the Caffarelli-Kohn-Nirenberg partial regularity theorem for Navier-Stokes. Extract the structural features that determine the dimension bound on the singular set, with particular attention to how Lin's approach differs from the original CKN (1982) proof.

**Paper:** Fanghua Lin, "A new proof of the Caffarelli-Kohn-Nirenberg theorem," *Communications on Pure and Applied Mathematics*, 51(3):241-257, 1998.

Also consider Ladyzhenskaya and Seregin (1999) as a closely related simplification that appeared around the same time.

## What to Extract

For each item below, provide the **precise mathematical statement** from the paper, not just a verbal description. Include equation numbers or theorem numbers where possible.

### 1. Epsilon-Regularity Criterion
What scaled quantity must be small for regularity to follow? Write the precise inequality. Compare with the CKN (1982) criterion:
- CKN uses a scaled energy-type quantity involving ∫|∇u|² and ∫|u|³ + |p|^{3/2} over parabolic cylinders.
- Does Lin use the same criterion, a different one, or reformulate it?
- What is the scaling of Lin's criterion under parabolic rescaling?

### 2. Covering Argument
How does Lin estimate the size of the singular set? Key questions:
- Does Lin use the same Vitali-type covering as CKN?
- Are the covering objects the same (parabolic cylinders)?
- Is the step from covering to dimension bound ≤ 1 identical to CKN, or does it differ?
- Does the compactness argument in Lin's approach change the covering step?

### 3. Localization Mechanism
Lin's proof is famous for its simplification of the localization step. Specifically:
- Does Lin use cutoff functions like CKN, or does compactness replace explicit localization?
- What is the compactness argument (blow-up / contradiction)?
- What information is lost in the compactness step that was explicit in CKN?
- Is Lin's approach more or less lossy than CKN's explicit cutoff approach?

### 4. Critical Scaling Exponents
What powers of the radius r appear in Lin's key estimates? Specifically:
- What scaling exponents appear in the epsilon-regularity criterion?
- Are these the same as CKN's scaling exponents?
- Does the compactness approach change the relationship between scaling and the dimension bound?
- If Lin uses a blow-up argument, what is the scaling of the blow-up sequence?

### 5. Free-Parameter vs. Fixed-Constant Estimates
- Does Lin's compactness approach eliminate the need for explicit Young/absorption steps?
- Which estimates still require free parameters?
- Does the indirect (compactness/contradiction) nature of the proof obscure where lossiness enters?

## Success Criteria

A structured report containing:
- All five items above with precise mathematical content
- Clear identification of what Lin's compactness argument simplifies vs. what it preserves from CKN
- An explicit comparison: does Lin's proof arrive at dimension ≤ 1 through the same scaling route as CKN, or through a different mechanism?
- A clear statement of whether Lin's simplification changes the structural bottleneck or merely streamlines the path to the same bottleneck

## Failure Criteria

- Treating Lin's proof as just "CKN but simpler" without identifying precisely what is different
- Failing to extract the scaling exponents that determine the dimension bound
- Not comparing with the CKN approach on each of the five items

## Context

This is one of three parallel explorations. The other two analyze CKN (1982) and Vasseur (2007). The results will be compared to determine whether all three proof strategies converge on the same structural bottleneck or offer different routes. Your extraction must use the same 5-item template so results are directly comparable.

The key insight Lin's proof is known for: replacing CKN's explicit energy estimates with a compactness/contradiction argument. The question is whether this changes the structural constraint or just repackages it. Lin's proof is shorter and more elegant — but does it open a door CKN's approach doesn't?
