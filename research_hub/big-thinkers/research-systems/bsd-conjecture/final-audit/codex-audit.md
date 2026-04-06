# Audit of the p-adic BSD Proof Chain

**Date of audit:** 2026-04-06

## Files Read
1. [`proof-outline.md`](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md)
2. [`findings.md`](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md)
3. [`findings.md`](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/normalization-check/findings.md)
4. [`findings.md`](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/determine-unit-u/findings.md)
5. [`findings.md`](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/verify-mcs-hypotheses/findings.md)
6. [`findings.md`](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-gaps-are-one/findings.md)
7. [`codex-review.md`](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-bf-formalize/codex-review.md)

**Scope note:** This audit is grounded only in the seven files above. I did not independently inspect the external papers they cite. When I call a published step `[SOUND]` or `[QUESTIONABLE]`, that judgment is about how the claim is supported inside these files, including citation specificity and whether the needed hypotheses are stated.

## Step 1. Park-Park BF = TQFT
- **Claim being audited:** Park-Park arithmetic BF theory is a genuine arithmetic TQFT.
- **Label:** [QUESTIONABLE]
- **Justification:**
  - [`proof-outline.md` #L115-L125](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L115) states: "`Theorem 2.1 (Park-Park)`" and says the theory satisfies the Atiyah-Segal axioms, with "`Partition function = arithmetic torsion`" and "`Gluing formula ... via the Poitou-Tate exact sequence`."
  - [`proof-outline.md` #L451-L453](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L451) treats this as "`Status: [KNOWN] Park-Park 2026.`"
  - But [`route-bf-kolyvagin-system/findings.md` #L772-L774](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L772) says the Park-Park paper "`is from February 2026 and unreviewed.`" So the chain description "`[published]`" is overstated inside the dossier itself.
  - Citation specificity is only moderate: author + arXiv identifier are given, but no theorem number from the Park-Park paper itself appears in these files.
- **Hidden assumptions:**
  - The dossier assumes Park-Park's TQFT formalism extends cleanly from the partition function to inserted observables. But [`proof-outline.md` #L527-L539](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L527) says this formalization is exactly Gap 1.
- **Connection to next step:**
  - The gluing bridge is explicit at the level of partition functions and Selmer complexes; it is not explicit at the level needed for BF correlators with insertions. The next-step bridge is therefore only partial.

## Step 2. MCS: det(Selmer complex) ≅ Stark systems
- **Claim being audited:** The Macias Castillo-Sano theorem supplies `det(SC) ≅ SS_1`, and its hypotheses have been verified.
- **Label:** [QUESTIONABLE]
- **Justification:**
  - [`verify-mcs-hypotheses/findings.md` #L53-L63](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/verify-mcs-hypotheses/findings.md#L53) gives a specific citation: "`Theorem 3.4 (MCS). Under Hypotheses 2.11 and 2.17, there is a canonical isomorphism ... det ... ≅ SS_{chi(F)}.`"
  - [`verify-mcs-hypotheses/findings.md` #L466-L473](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/verify-mcs-hypotheses/findings.md#L466) narrows the verified application to "`GOOD ORDINARY REDUCTION at p`" under three explicit conditions: good ordinary reduction, `p ∤ #E(Q)_tors * Tam(E/Q) * #\tilde E(F_p)`, and irreducible `E[p]`.
  - [`route-bf-kolyvagin-system/findings.md` #L768-L770](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L768) adds that the MCS paper "`was posted to arXiv only 10 days ago`" and "`has not been peer-reviewed.`" So "`[published March 2026]`" is again overstated.
  - The hypothesis verification is not universal even inside the campaign: [`verify-mcs-hypotheses/findings.md` #L239-L257](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/verify-mcs-hypotheses/findings.md#L239) says for `681b1 at p = 3` that "`HYPOTHESIS 2.11(iii) PARTIALLY FAILS`" and "`MCS Theorem 3.4 does not directly apply to this case.`"
- **Hidden assumptions:**
  - Good ordinary reduction, non-anomalous prime, `p ∤` torsion/Tamagawa/local point count, irreducible residual representation, and the correctness of an unreviewed March 2026 preprint.
- **Connection to next step:**
  - The MCS theorem only lands in Stark systems. The next step additionally needs Burns-Sano's derivative and a proof that the BF observable/restriction maps are compatible with Poitou-Tate in the precise way required for Kolyvagin recursion.

## Step 3. TQFT structure + Poitou-Tate → Kolyvagin system
- **Claim being audited:** The campaign's new theorem rigorously constructs `κ^BF` and proves the Kolyvagin recursion from TQFT gluing.
- **Label:** [GAP]
- **Justification:**
  - [`route-bf-kolyvagin-system/findings.md` #L356-L377](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L356) states "`Theorem A`" and claims the BF theory "`canonically produces`" classes `κ^BF_n`, satisfying the recursion and hence lying in `KS_1`.
  - But the same file later gives the controlling caveat: [`route-bf-kolyvagin-system/findings.md` #L787-L804](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L787) says "`The vulnerability: The argument in Section IV.3 ... is more schematic than fully rigorous`" and its status table records "`TQFT gluing → recursion | New (this work) | Schematic proof given, needs full write-up.`"
  - The older master outline was never updated to say this gap is closed: [`proof-outline.md` #L527-L539](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L527) still says the needed statement is to "`formalize the definition of the k-point correlation function`" and that "`no one has written down the precise definition of BF correlators with insertions at Kolyvagin primes and verified that the resulting quantity matches the Kurihara number.`"
- **Hidden assumptions:**
  - Identification of the Poitou-Tate connecting map with the Kolyvagin derivative operator.
  - Full compatibility of BF observable insertion with the Selmer-localization map.
  - Compatibility of Cassels-Tate/global duality with the local Tate duality used in the recursion.
- **Connection to next step:**
  - Explicit but incomplete. The normalization file addresses only the sign/local-duality subissue, not the full BF-to-Kolyvagin construction.

## Step 4. Signs `epsilon = +1`
- **Claim being audited:** The sign in the local-global pairing comparison is `+1`.
- **Label:** [SOUND]
- **Justification:**
  - [`normalization-check/findings.md` #L12-L16](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/normalization-check/findings.md#L12) states: "`The signs are correct. The compatibility is essentially tautological`" because Cassels-Tate is defined as a sum of local Tate pairings.
  - [`normalization-check/findings.md` #L94-L111](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/normalization-check/findings.md#L94) explicitly says the connecting map satisfies "`delta(c_ell)(b) = inv_ell(c_ell cup b_ell) = <c_ell, b_ell>_ell`" and concludes "`The sign epsilon(ell) = +1 for all Kolyvagin primes ell.`"
  - [`normalization-check/findings.md` #L229-L245](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/normalization-check/findings.md#L229) records `22/22` pair checks and `60/60` distribution checks, i.e. `82/82`.
  - [`normalization-check/findings.md` #L382-L387](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/normalization-check/findings.md#L382) restates the formal theorem: the connecting homomorphism equals local Tate duality and "`epsilon(ell) = +1`."
- **Hidden assumptions:**
  - Standard convention choices for the Weil pairing and local invariant map are used consistently.
  - This step does not by itself prove the whole Kolyvagin recursion; it only resolves the sign/compatibility subissue.
- **Connection to next step:**
  - Explicit. [`normalization-check/findings.md` #L326-L339](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/normalization-check/findings.md#L326) inserts the sign result directly into the chain leading to the comparison `κ^BF = u * κ^Kato`.

## Step 5. Mazur-Rubin freeness: `κ^BF = u · κ^Kato`
- **Claim being audited:** Mazur-Rubin freeness is correctly cited and actually yields the comparison `κ^BF = u · κ^Kato`.
- **Label:** [GAP]
- **Justification:**
  - The published input itself is cited specifically and correctly: [`route-bf-kolyvagin-system/findings.md` #L393-L397](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L393) quotes "`Theorem 5.2.10`" and the conclusion that `KS_1(T,F_can)` is "`free of rank 1 over Λ.`"
  - The application to `κ^BF` is only valid if Step 3 has already produced an honest element of `KS_1`. The same file admits that the step immediately before this is still schematic: [`route-bf-kolyvagin-system/findings.md` #L804-L806](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L804) says "`TQFT gluing → recursion ... Schematic proof given, needs full write-up`" and only then lists "`κ^BF = u · κ^Kato | Immediate | From freeness + the above.`"
  - So the freeness theorem is sound, but the chain step that uses it is not yet fully established in these files.
- **Hidden assumptions:**
  - A fully rigorous construction of `κ^BF ∈ KS_1`.
  - Verified hypotheses for the Mazur-Rubin/Buyukboduk/Bullach-Burns setup in the exact BF setting.
  - Good ordinary and non-anomalous hypotheses where needed.
- **Connection to next step:**
  - Explicit but conditional. The `u`-analysis only starts after this comparison is accepted.

## Step 6. `u = 1` for optimal semistable curves
- **Claim being audited:** The unit is exactly `u = 1`, proved by the stated density + completeness argument.
- **Label:** [GAP]
- **Justification:**
  - [`determine-unit-u/findings.md` #L17-L24](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/determine-unit-u/findings.md#L17) states the strategy: trivial character, finite-order characters, then Chebotarev + completeness.
  - [`determine-unit-u/findings.md` #L173-L201](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/determine-unit-u/findings.md#L173) gives the crucial Step A-D argument, but its core assertions are only asserted, not proved in the listed files: "`The same Kim identity holds at each layer`", "`the density argument ... gives u(zeta_{p^n}-1) ≡ 1 mod p^k for all k`", and then Weierstrass is invoked to conclude `u=1`.
  - The file itself concedes dependence on earlier unresolved work: [`determine-unit-u/findings.md` #L301-L310](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/determine-unit-u/findings.md#L301) says "`The density argument is rigorous (assuming the proof chain MCS + Burns-Sano + TQFT gluing)`" and also notes that the Chebotarev/Iwasawa part "`requires care`."
  - There is an internal consistency problem in its main worked example. [`determine-unit-u/findings.md` #L349-L352](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/determine-unit-u/findings.md#L349) says for `11a1 at p=5` that "`mu = 1, lambda = 0`", while the broader chain repeatedly assumes `mu = 0`.
  - Worse, the hypothesis-verification file explicitly excludes that same example from the MCS route: [`verify-mcs-hypotheses/findings.md` #L268-L273](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/verify-mcs-hypotheses/findings.md#L268) says "`11a1 at p = 5`" is anomalous and has reducible `rho_bar`, a "`Double failure.`"
- **Hidden assumptions:**
  - Step 3 must already be fully rigorous.
  - The BF/Kim comparison must hold at all cyclotomic characters, not just at the base layer.
  - For every `k` and every relevant specialization, there must exist Kolyvagin primes of the required depth with unit Kurihara value.
- **Connection to next step:**
  - Explicit but unstable. The file upgrades "`up to a unit`" to exact element equality, but that upgrade is not secure enough to support later assembly.

## Step 7. Kim: Kurihara numbers → higher Fitting ideals → Selmer structure
- **Claim being audited:** Kim's published results determine the higher Fitting ideals and the Selmer structure from Kurihara numbers.
- **Label:** [QUESTIONABLE]
- **Justification:**
  - [`proof-outline.md` #L275-L289](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L275) gives a fairly specific statement of "`Theorem 4.3 (Kim Structure Theorem)`" and spells out the corank and elementary-divisor consequences.
  - [`endgame-gaps-are-one/findings.md` #L109-L122](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-gaps-are-one/findings.md#L109) again cites "`Kim ... Theorem 1.1`" and states the consequence `Sel(Q,W_f) = (Q_p/Z_p)^r` under `partial^(r)=0`.
  - However, both files also state the crucial hidden hypothesis: [`proof-outline.md` #L275-L279](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L275) begins "`Assume Kato's Kolyvagin system ... is non-trivial`", and [`endgame-gaps-are-one/findings.md` #L135-L142](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-gaps-are-one/findings.md#L135) says rank `>= 2` nontriviality "`is expected to hold but not yet proved unconditionally.`"
  - So the published Kim step is cited specifically enough to audit, but the chain statement as written suppresses a nontrivial hypothesis.
- **Hidden assumptions:**
  - Kato nontriviality.
  - The BF-Kurihara comparison must already identify the relevant Kurihara data with the BF side.
  - The needed `partial^(r)=0` condition or equivalent unit/nonvanishing input must be available.
- **Connection to next step:**
  - Explicit. The dossier uses Kim's structure theorem to pass to `char(X) = (T^r)` and then invokes Schneider-Perrin-Riou.

## Step 8. Schneider-Perrin-Riou: Selmer structure → height nondegeneracy + Sha finite
- **Claim being audited:** Published Schneider/Perrin-Riou results turn the algebraic `char(X)` information into height nondegeneracy and Sha finiteness.
- **Label:** [QUESTIONABLE]
- **Justification:**
  - The best citation appears in [`endgame-gaps-are-one/findings.md` #L118-L122](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-gaps-are-one/findings.md#L118): "`Theorem 6.2 (Perrin-Riou [PR93]; stated as Theorem 1.7 in Balakrishnan-Mueller-Stein [BMS13]; see also Schneider [Sch85, Theorem 2'])`" with the precise "`iff`" statement.
  - The master outline, however, still describes Gap 2 as open in general: [`proof-outline.md` #L400-L414](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L400) labels Schneider's conjecture "`[GAP 2: Open in general]`."
  - The later collapse argument therefore does not eliminate Gap 2 unconditionally; it replaces it with the need to prove the hypotheses leading to `ord_T(char(X)) = r`. [`endgame-gaps-are-one/findings.md` #L129-L142](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-gaps-are-one/findings.md#L129) is explicit: Gap 2 follows only "`If the BF-Kurihara correspondence is established, AND Kato's Kolyvagin system is nontrivial.`"
- **Hidden assumptions:**
  - Upstream proof of the BF-Kurihara step.
  - Kato nontriviality.
  - Control-theorem passage from Selmer structure to `char(X) = (T^r)` without omitted exceptional behavior.
- **Connection to next step:**
  - Explicit. Once the algebraic characteristic power series has exact order `r`, the dossier uses this together with Perrin-Riou's p-adic BSD formula to assemble p-adic BSD.

## Step 9. Assembly → p-adic BSD
- **Claim being audited:** The preceding steps assemble into a complete p-adic BSD proof.
- **Label:** [GAP]
- **Justification:**
  - The master outline itself is still framed as conditional: [`proof-outline.md` #L3-L5](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L3) says "`Status: CONDITIONAL PROOF OUTLINE -- Two precisely identified gaps remain`", and [`proof-outline.md` #L15-L23](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L15) states the conditional theorem with Gap 1 and Gap 2 as assumptions.
  - The later "gap collapse" file still keeps a remaining assumption: [`endgame-gaps-are-one/findings.md` #L251-L288](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-gaps-are-one/findings.md#L251) makes the conclusion conditional on `(H1) Kato nontriviality` and `(H2) BF-Kurihara correspondence`.
  - The strongest "complete" claim appears in the `u = 1` file, but it is downstream of the unresolved Step 3 and Step 6 issues: [`determine-unit-u/findings.md` #L274-L289](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/determine-unit-u/findings.md#L274) says "`The complete proof chain is now`" and "`Every step is an EQUALITY of elements`", which is not supported by the caveats elsewhere.
- **Hidden assumptions:**
  - Full closure of Step 3.
  - A valid comparison `κ^BF = u·κ^Kato`.
  - Either a rigorous `u=1` theorem or a proof that only the unit class matters for the claimed p-adic BSD conclusion.
  - Kato nontriviality in the higher-rank cases targeted by the overall campaign.
- **Connection to next step:**
  - Terminal step; no next step.

## Status of the 5 Gaps from the Earlier Codex Review

### Gap 1. Derived-category definition → concrete localization map
- **Status:** Partially resolved
- **Why:** [`route-bf-kolyvagin-system/findings.md` #L474-L475](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L474) claims MCS resolves the passage `det(SC) → SS_1 → KS_1`. But [`proof-outline.md` #L527-L539](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/endgame-unified-attack/proof-outline.md#L527) still says the inserted correlator itself has not been formally defined in the needed way, and [`route-bf-kolyvagin-system/findings.md` #L787-L804](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L787) says the new comparison theorem remains schematic.

### Gap 2. Mazur-Rubin 5.2.12 used too strongly
- **Status:** Resolved
- **Why:** [`route-bf-kolyvagin-system/findings.md` #L476-L476](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L476) explicitly corrects the citation and says the new argument uses "`5.2.10 (freeness)`" rather than overloading `5.2.12`.

### Gap 3. Coefficient-level mismatch: finite level vs `Λ`
- **Status:** Partially resolved
- **Why:** [`route-bf-kolyvagin-system/findings.md` #L478-L478](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L478) and [`route-bf-kolyvagin-system/findings.md` #L499-L519](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L499) invoke Buyukboduk and Bullach-Burns as the fix, but the files do not supply a full BF-specific hypothesis check for those `Λ`-adic tools. The later audit sections still treat MCS/BF compatibility as a nontrivial prerequisite.

### Gap 4. The composite equality was a type-changing assertion
- **Status:** Partially resolved
- **Why:** [`route-bf-kolyvagin-system/findings.md` #L480-L482](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L480) gives a typed chain `det(SC) → SS_1 → KS_1 → H^1 ... → exp*`. But the crucial BF-to-Kolyvagin and localization-to-reciprocity identifications are still not fully proved: [`route-bf-kolyvagin-system/findings.md` #L463-L468](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L463) simply asserts "`<O...>_BF = loc^s(κ^BF_n) = exp*(κ^BF_n)`", while [`route-bf-kolyvagin-system/findings.md` #L787-L804](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L787) says the needed comparison remains schematic.

### Gap 5. Dependency loop between Proposition 1 and the comparison
- **Status:** Resolved
- **Why:** [`route-bf-kolyvagin-system/findings.md` #L483-L483](/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/bsd-conjecture/route-bf-kolyvagin-system/findings.md#L483) explicitly says: "`We no longer use Proposition 1 to prove the comparison.`" The circular dependency identified in the earlier review is removed. The replacement argument has other weaknesses, but the specific loop is gone.

## Final Verdict

**Overall chain status:** [GAP]

The dossier does not yet give a gap-free end-to-end proof of p-adic BSD. The strongest positive findings are:
- the sign normalization issue is genuinely settled inside the listed files;
- the use of Mazur-Rubin is cleaner than in the earlier draft;
- Kim and Schneider/BMS are cited with enough precision to support a conditional algebraic-to-height bridge.

The blocking problems are:
- the core new theorem "`TQFT gluing = Kolyvagin recursion`" is explicitly described by its own file as "`schematic ... needs full write-up`";
- the comparison `κ^BF = u·κ^Kato` therefore remains downstream of an unresolved construction step;
- the `u = 1` file relies on assertions at all cyclotomic layers that are not proved in the listed files and uses `11a1/p=5` as a main example even though the MCS-verification file flags that pair as a double failure of the stated hypotheses;
- the Gap 1 ⇒ Gap 2 collapse remains conditional on Kato nontriviality, which the same files say is open for rank `>= 2`.

So the chain is not circular in the same way as the earlier draft, but it is still incomplete.

## Recommendations
1. Prove the BF-to-Kolyvagin theorem in full detail: formal definition of inserted BF correlators, exact relation to Poitou-Tate localization, and exact identification of the connecting map with the Burns-Sano derivative modulo `I_n`.
2. State the theorem only in the good ordinary, non-anomalous, irreducible setting unless the multiplicative/anomalous/reducible cases are separately proved. In particular, stop using `11a1/p=5` and `681b1/p=3` as support for the general theorem without a distinct argument.
3. Give a complete `Λ`-adic hypothesis check for the Buyukboduk/Bullach-Burns tools in the BF setting, not just a citation-level fix.
4. Rework the `u = 1` proof so that every step at finite-order characters and all cyclotomic layers is explicitly justified from the listed hypotheses, and reconcile the `mu = 1` computation for `11a1/p=5` with the chain's repeated `mu = 0` assumptions.
5. Rewrite the final assembly theorem with exact remaining assumptions. As the files stand, "`BF formalization + Kato nontriviality`" is the honest status, not "`proof complete`."
