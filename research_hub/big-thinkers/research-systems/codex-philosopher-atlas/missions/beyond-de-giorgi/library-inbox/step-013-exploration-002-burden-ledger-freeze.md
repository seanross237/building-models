# Exploration 002 Report

## Goal

Freeze one theorem-facing baseline burden, one admissible gain notion, the
typed burden ledger, the same-currency comparability rule, and the mandatory
transfer-lemma rule for cross-currency claims.

## Method

- Read the inherited exact-rewrite architecture and the obstruction-screening
  notes already tied to the LEI audit.
- Use those sources to freeze one theorem-facing burden instead of inventing a
  new surrogate.
- Translate the required Step-013 currencies into an explicit ledger format.

## Evidence Read

- [VERIFIED] `missions/beyond-de-giorgi/steps/step-013/GOAL.md`
- [VERIFIED] `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-009/winning-chain.md`
- [VERIFIED] `library/factual/exact-rewrite-architecture-screening/local-energy-flux-localization-is-the-right-inherited-architecture-for-the-exact-rewrite-audit.md`
- [VERIFIED] `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- [VERIFIED] `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- [VERIFIED] `library/factual/exact-rewrite-obstruction-audit/freeze-one-ckn-style-parabolic-cutoff-protocol-for-the-rewrite-audit.md`
- [VERIFIED] `library/factual/exact-rewrite-obstruction-audit/every-rewrite-must-stay-inside-the-same-localized-lei-package.md`
- [VERIFIED] `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- [VERIFIED] `library/meta/obstruction-screening/a-scope-lock-is-not-real-until-baseline-cash-out-and-threshold-are-frozen-in-the-same-burden-currency.md`
- [VERIFIED] `missions/beyond-de-giorgi/library-inbox/step-006-exploration-003-unified-tao-verdict.md`
- [VERIFIED] `missions/beyond-de-giorgi/library-inbox/step-008-exploration-002-one-ledger-coherence.md`

## Findings

### 1. Baseline burden

- [VERIFIED] The inherited exact-rewrite architecture already fixes one
  theorem-facing bad term:
  `I_flux[phi] = ∬_{Q_r} (|u|^2 + 2p) u · ∇phi`
  inside the localized LEI balance.
- [VERIFIED] This is the right baseline burden for Step-013 because it is the
  exact place where nonlinear transport and pressure transport are charged
  together inside the inherited theorem ledger.
- [INFERRED] The baseline burden should therefore be frozen as:
  `the full localized LEI cutoff-flux bundle under the shared CKN-style cutoff protocol`.

### 2. Admissible gain notion

- [VERIFIED] The exact-rewrite screening packet already fixes the branch's gain
  currency:
  `coefficient shrinkage in the fixed localized LEI balance`.
- [VERIFIED] A reformulation only counts if, after projection, CZ,
  commutator, pressure-recovery, and reconstruction costs are repaid, the same
  `I_flux[phi]` bundle carries a smaller effective coefficient.
- [INFERRED] The admissible gain notion for Step-013 is therefore:
  `net positive-margin shrinkage of the effective coefficient on the full I_flux[phi] bundle in the same protocol`.

### 3. Typed burden ledger

| currency | frozen meaning | how later steps must record it |
| --- | --- | --- |
| derivative count | `[INFERRED]` whether a candidate truly reduces derivative demand on the live estimate rather than only in a pre-localized identity | record the claimed derivative reduction and the exact step where it returns to the LEI bundle; if it never returns, mark as non-cashable |
| locality | `[VERIFIED]` whether a gain acts on the full cutoff-flux bundle under the shared cutoff rather than on a surrogate local piece | record whether the gain survives on the full localized `I_flux[phi]` bundle or dies when exterior/nonlocal pieces are restored |
| cancellation | `[INFERRED]` exact sign, null structure, or commutator cancellation that lowers the same full-bundle coefficient | record the cancelled term, where the cancellation appears, and whether the full-bundle coefficient is smaller after all debt |
| integrability | `[INFERRED]` any exponent or space improvement offered by the candidate | record the improved space and whether an explicit transfer carries it back to smaller `I_flux[phi]` cost |
| pressure recoverability | `[VERIFIED]` debt from pressure reconstruction, Helmholtz projection, CZ recovery, or nonlocal pressure re-entry | record every pressure-recovery step as debt charged against the candidate before any gain is counted |
| admissibility | `[VERIFIED]` debt from leaving suitable-weak / Leray-Hopf plus LEI or from requiring extra regularity | record any stronger host-class assumption as negative burden unless an explicit admission bridge is provided |
| compactness input | `[INFERRED]` debt from relying on extraction, compactness, or rigidity machinery outside the frozen endpoint argument | record any extra compactness package as a distinct debt that cannot be silently counted as endpoint progress |
| scaling compatibility | `[VERIFIED]` whether the claimed gain respects the inherited LEI / CKN scaling and shared cutoff protocol | record whether the gain is scale-compatible on the same normalized LEI ledger or only in a differently scaled surrogate |

### 4. Same-currency comparability rule

- [INFERRED] Same-currency comparison is sufficient only when two claims act on
  the same frozen endpoint object:
  the full localized `I_flux[phi]` bundle,
  in the same solution class,
  under the same CKN-style cutoff protocol,
  and after the same pressure/admissibility debt is charged.
- [VERIFIED] In that setting, later steps may compare net coefficient changes
  directly without extra translation.

### 5. Transfer-lemma rule

- [VERIFIED] Cross-currency optimism is disallowed by the chain scope-lock.
- [INFERRED] A transfer lemma is mandatory whenever the claimed gain is stated
  in a different currency from the baseline burden, for example:
  derivative reduction,
  integrability improvement,
  partial cancellation on a surrogate quantity,
  or compactness-side leverage.
- [INFERRED] The transfer lemma must name the exact implication:
  how the surrogate gain yields a positive-margin smaller effective coefficient
  on the full `I_flux[phi]` bundle, under the same solution class and cutoff
  protocol, after all new debts are charged.
- [VERIFIED] If no explicit transfer is named, the claim stays unresolved and
  does not count as progress.

### 6. Burden-ledger memo

- [VERIFIED] The baseline cash-out and the admissible gain notion are frozen in
  the same burden currency, which is what makes this scope lock real rather
  than rhetorical.
- [VERIFIED] Decorative improvements to identities, variables, exponents, or
  derivative placements do not count unless they cash out on the same `I_flux`
  coefficient.
- [INFERRED] This ledger is mechanical enough to govern Step 2 candidate
  comparison because every future candidate must either post a same-currency
  coefficient change or supply a named transfer lemma.

## Dead Ends / Failed Attempts

- [VERIFIED] I found no better-supported theorem-facing burden than the shared
  localized LEI cutoff-flux bundle.
- [VERIFIED] I found no source support for letting exponent or derivative-count
  language count on its own before it returns to the frozen LEI burden.

## Conclusion

- [VERIFIED] Baseline burden:
  the full localized LEI cutoff-flux bundle `I_flux[phi]` under the shared
  CKN-style cutoff protocol.
- [VERIFIED] Admissible gain notion:
  coefficient shrinkage in that same localized LEI balance.
- [INFERRED] Same-currency rule:
  direct comparison is allowed only on the same full `I_flux[phi]` object,
  same solution class, same localization regime, and same charged debt.
- [INFERRED] Transfer-lemma rule:
  every cross-currency claim must explicitly map back to a smaller full-bundle
  coefficient after debt.

## Source Map

### Inherited architecture evidence

- [VERIFIED] `library/factual/exact-rewrite-architecture-screening/local-energy-flux-localization-is-the-right-inherited-architecture-for-the-exact-rewrite-audit.md`
- [VERIFIED] `library/factual/exact-rewrite-architecture-screening/the-localized-lei-cutoff-flux-bundle-is-the-fixed-bad-term-for-the-audit.md`
- [VERIFIED] `library/factual/exact-rewrite-architecture-screening/success-requires-a-smaller-effective-lei-cutoff-flux-cost-in-the-same-protocol.md`
- [VERIFIED] `library/factual/exact-rewrite-obstruction-audit/freeze-one-ckn-style-parabolic-cutoff-protocol-for-the-rewrite-audit.md`
- [VERIFIED] `library/factual/exact-rewrite-obstruction-audit/every-rewrite-must-stay-inside-the-same-localized-lei-package.md`

### Obstruction-screening evidence

- [VERIFIED] `library/meta/obstruction-screening/demand-estimate-level-action-on-the-live-obstruction.md`
- [VERIFIED] `library/meta/obstruction-screening/a-scope-lock-is-not-real-until-baseline-cash-out-and-threshold-are-frozen-in-the-same-burden-currency.md`
- [VERIFIED] `missions/beyond-de-giorgi/library-inbox/step-006-exploration-003-unified-tao-verdict.md`
- [VERIFIED] `missions/beyond-de-giorgi/library-inbox/step-008-exploration-002-one-ledger-coherence.md`

### Planning-run evidence

- [VERIFIED] `missions/beyond-de-giorgi/steps/step-013/GOAL.md`
- [VERIFIED] `missions/beyond-de-giorgi/CHAIN.md`
- [VERIFIED] `missions/beyond-de-giorgi/planning-runs/run-009/winning-chain.md`
