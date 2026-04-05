# Refined Chain: CKN Structural Limitation Analysis

**Mission:** Find the loosest estimate in NS regularity theory — identify which structural feature of the proof architecture is the binding constraint on regularity results.

**Planning loop verdict:** Modified. Original Chain A (bound-by-bound audit of CKN constants) was restructured after adversarial review. The attacker demonstrated that individual constant sharpness is irrelevant to CKN's qualitative conclusion — the limitation comes from the covering/scaling argument, not from suboptimal constants. The refined chain targets the structural constraint directly.

**Probability of presentable result:** 65-70% (Judge's assessment)

---

## Step 1: Comparative proof architecture analysis

**Type:** Standard Explorer (literature)

**Objective:** Compare three independent proofs of CKN partial regularity — CKN (1982), Lin (1998), Vasseur (2007) — at the structural level. For each, extract:

1. The epsilon-regularity criterion used (what scaled quantity must be small?)
2. The covering argument (how is the singular set estimated?)
3. The localization mechanism (cutoff functions / compactness / De Giorgi iteration?)
4. The scaling exponents (what powers of r appear in key estimates?)
5. Which estimates are free-parameter (absorption) vs. fixed-constant?

**Output:** Comparative table showing where the three strategies agree (constraint is fundamental) and where they differ (constraint is proof-specific). Identify whether all three arrive at dimension <= 1 through the same scaling route or different routes.

**Kill condition:** If all three strategies reduce to the same covering argument with the same scaling exponents, the constraint is likely fundamental. Report that as the finding — valid negative result.

**Feeds into:** Step 2 needs the scaling exponents and regularity-relevant quantities to measure in DNS.

---

## Step 2: Scaling measurement in resolved DNS

**Type:** Math Explorer (computation)

**Objective:** Measure how regularity-relevant quantities scale in turbulent DNS. Compare observed scaling to the scaling assumed by each proof strategy from Step 1.

**Resolution matched to Re (actual DNS, not under-resolved):**
- Re = 100: 64^3
- Re = 400: 128^3
- Re = 1600: 256^3 (verify via energy spectrum falloff)

**Quantities to measure:**
1. CKN scaled energy: r^{-1} integral of |u|^3 + |p|^{3/2} over parabolic cylinders at multiple scales r
2. Prodi-Serrin norms: ||u||_{L^p_t L^q_x} for (p,q) on/near critical line 2/p + 3/q = 1
3. Enstrophy and vortex stretching: ||omega||_{L^2}^2 and omega . nabla u . omega
4. Pressure Hessian alignment statistics

**Output:** Table of scaling exponents — observed vs. assumed by CKN, Lin, Vasseur. Identify where the gap is largest.

**Kill condition:** If DNS can't be validated (no clean inertial range + dissipation in energy spectrum), reduce Re. If Re < 100, turbulence too weak — report null result.

**Feeds into:** Step 3 synthesizes the scaling gaps.

---

## Step 3: Identify the binding structural constraint

**Type:** Standard Explorer + Math Explorer (analysis/synthesis)

**Objective:** Synthesize Steps 1 and 2:
- Which proof-assumed scaling exponents are closest to DNS-observed scaling? (tight — not where improvement is possible)
- Which are farthest? (loose — either improvable or conservative-by-necessity)
- Cross-reference with comparative proof table: same gap in all strategies = fundamental. Gap in only one = that strategy can be improved.

**Key question:** Is the dimension-1 bound forced by parabolic scaling, or could a proof with different scaling (anisotropic covering, frequency-localized estimates) do better?

**Output:** Identification of the binding constraint with evidence classification (fundamental vs. proof-specific), supported by analytical comparison and numerical scaling data.

**Kill condition:** If evidence is ambiguous, report top 2-3 candidates with evidence for and against each.

---

## Step 4: Targeted investigation of the binding constraint

**Type:** Math Explorer or Standard Explorer (depends on Step 3 outcome)

**If proof-specific** (one strategy avoids it):
- Investigate whether the avoiding strategy can be pushed further.
- Test: Can Vasseur's De Giorgi approach + anisotropic covering improve the dimension bound?

**If fundamental** (all strategies share it):
- Characterize precisely what makes it fundamental.
- Investigate whether Scheffer examples (dimension 1 singular sets) represent true worst case, or whether Leray-Hopf/energy inequality constraints exclude them.
- Produce: "Here is why no proof of CKN type can do better than dimension 1."

**Kill condition:** If investigation exceeds single exploration scope, produce concrete conjecture with supporting evidence rather than incomplete proof.

---

## Key Refinements from Adversarial Review

| Issue Identified | Resolution |
|---|---|
| Individual constant sharpness is irrelevant to qualitative CKN conclusion | Reframed to structural constraint identification |
| 128^3 at Re=5000 is not DNS | Resolution matched to Re (64^3/128^3/256^3 for Re=100/400/1600) |
| Smooth solutions trivially satisfy CKN bounds with huge slack | Focus on scaling exponents, not absolute slack values |
| CKN proof is iterative, not linear chain | Comparative analysis across three proof architectures |
| Absorption estimates (Young's inequality) are trivially loose | Classification distinguishes free-parameter from fixed-constant estimates |
| "Tightening one inequality" doesn't change qualitative conclusion | Goal is identifying the binding structural constraint, not tightening a constant |
