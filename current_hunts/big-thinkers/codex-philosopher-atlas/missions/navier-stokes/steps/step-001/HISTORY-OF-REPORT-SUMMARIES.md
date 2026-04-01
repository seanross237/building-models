# History of Report Summaries — Step 1

## Exploration 001: CKN (1982) Proof Architecture
**Explorer type:** Standard | **Outcome:** Succeeded

All 5 structural features extracted. CKN's ε-regularity uses A(r)+E(r)+C(r)+D(r) < ε₀ with all four scale-invariant. Localization via explicit cutoff functions φ with |∇φ|~1/r. Four Young/absorption steps identified (Y1-Y4), with Y2 (Ladyzhenskaya absorption) being the dominant lossy step. The dimension-1 bound is forced by E(r) = (1/r)∫∫|∇u|² being scale-invariant: singular points require ∫∫|∇u|² ≥ ε₀·r, so Vitali covering gives Σ rᵢ ≤ (1/ε₀)∫∫|∇u|² < ∞ → P¹(Σ)=0. Parabolic Sobolev exponent 10/3 = 2·5/(5-2). The bottleneck is scale-invariance + global energy bound, not proof technique.

## Exploration 002: Lin (1998) Proof Architecture
**Explorer type:** Standard | **Outcome:** Succeeded

All 5 features extracted. Lin simplifies the ε-criterion to C(r)+D(r) < ε₀ (drops A,E). Localization via blow-up/compactness/contradiction instead of cutoff functions — same Young steps are present but hidden in compactness infrastructure. Same covering argument, same scaling exponents, same P¹(Σ)=0 conclusion. Key insight: C(r) alone gives only dim ≤ 2; dim ≤ 1 specifically requires reintroducing E(r) from the dissipation integral. Lin's proof is a streamlining, not a structural departure. It hides lossiness rather than eliminating it.

## Exploration 003: Vasseur (2007) Proof Architecture
**Explorer type:** Standard | **Outcome:** Succeeded

All 5 features extracted. Vasseur uses De Giorgi iteration for localization — level sets of |u| on shrinking cylinders with master inequality U_k ≤ C^k · U_{k-1}^{β_p}. Same covering argument and ε-regularity → P¹(Σ)=0 route as CKN. De Giorgi gives better velocity exponent (5/3 vs CKN's 3/2) but worse pressure exponent (4/3). Vasseur identifies β = 3/2 as the precise threshold for full regularity — local pressure term at 4/3 < 3/2 is the structural obstruction. Weaker pressure assumption (L^p(L¹) vs L^{3/2}) at cost of harder internal obstruction. Parabolic Sobolev 10/3 universal.
