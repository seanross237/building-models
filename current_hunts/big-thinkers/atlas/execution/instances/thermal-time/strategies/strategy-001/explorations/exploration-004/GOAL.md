# Exploration 004 — TTH Interpretation Confirmed + KMS Temperature Analysis + Experimental Proposal

## Mission Context

The mission is close to its final result. Three prior explorations have found:
1. ΔK_A ≠ 0 for coupled thermal oscillators (O(λ²)), with squeezing structure
2. ‖C_full − C_local‖/‖C_full‖ = 82.7% at λ=0.3 — structural difference (beats vs. single freq)
3. The discrepancy is entirely between the LOCAL and GLOBAL modular flows (control check passed at machine zero)

**One question blocks the final result:** Does the Connes-Rovelli TTH prescribe the LOCAL or the GLOBAL modular flow for subsystem dynamics?

- If **local**: TTH predicts single-frequency oscillation for A (NO normal-mode beating). QM predicts beating. Difference is 9-83% depending on coupling. **This is a novel testable prediction.**
- If **global**: TTH = QM exactly (K_AB/β = H_AB for Gibbs states). No new prediction. **The mission's answer is "empirically indistinguishable."**

This exploration resolves that question, verifies the interpretation with a KMS check, and sketches an experimental test.

---

## Task A — Literature: Local vs. Global in Connes-Rovelli (30 minutes max)

**Specific question:** When Connes-Rovelli (1994) define thermal time for a physical system, do they use the modular automorphism group of the SUBSYSTEM state, or of the GLOBAL state?

**Context for your search:** In Tomita-Takesaki theory, for algebra M with state ω:
- The modular automorphism group σ_t^{ω} acts on M
- For a subalgebra M_A ⊂ M with restricted state ω_A = ω|_{M_A}, the induced modular automorphism σ_t^{ω_A} on M_A is the LOCAL flow
- The restriction of the global flow to M_A: σ_t^{ω}|_{M_A} is the GLOBAL flow restricted to A
- **Takesaki's theorem (1972):** σ_t^{ω_A} = σ_t^{ω}|_{M_A} IF AND ONLY IF the conditional expectation E: M → M_A satisfying E(σ_t^{ω}(a)) = σ_t^{ω_A}(E(a)) exists. For a Gibbs state of a coupled system, this condition fails when λ ≠ 0.

**Papers to check (in order of priority):**
1. **Connes & Rovelli (1994)**, *Class. Quant. Grav.* 11, 2899 — Section 3 "Applications" or anywhere they discuss observables in subsystems. Look for: "the state restricted to," "the modular group of the reduced state," or similar phrases.
2. **Rovelli (2014)**, "Why Gauge?" — a later essay where Rovelli re-examines TTH for operational observers; may be more explicit about the local/global distinction
3. **Martinetti & Rovelli (2003)**, *Class. Quant. Grav.* 20, 4919 — they explicitly compute TTH for bounded-trajectory observers. Do they use the local state of the observer?
4. **Haggard & Rovelli (2013)**, arXiv:1302.0724 — Section on "subsystems at different temperatures" — specifically relevant to the local question

**What to report:** Quote the exact sentence(s) from Connes-Rovelli (or the clearest available source) that establishes their intent. If ambiguous, report all interpretations.

---

## Task B — KMS Condition Analysis (Python computation)

The KMS condition states: a state ω satisfies KMS at inverse temperature β for dynamics α_t if ω(A · α_{t+iβ}(B)) = ω(B · A) for all observables A, B.

In terms of the two-point function: C(τ) = ⟨x_A(τ) x_A⟩ satisfies KMS at β if:
**C(τ + iβ) = C(-τ)** for all τ.

Equivalently (for real τ), checking the spectral function: C(ω) = [1 + 2n_B(ω)] × A(ω) where n_B(ω) = 1/(e^{βω}-1) is the Bose-Einstein distribution and A(ω) is the spectral density. If C satisfies KMS at β, then C(ω)/C(-ω) = e^{βω} (detailed balance).

**Compute for each correlator:**

1. **C_full_QM**: Tr[ρ_{AB} x_A(τ) x_A] with x_A(τ) under H_AB. Check the KMS condition at β=2:
   - Method: extend to complex time via the spectral representation C(τ) = ∫ dω A(ω) e^{-iωτ}, compute A(ω) by FFT of C_full (using the data from exploration-003's code), then check whether C(ω)/C(-ω) = e^{2ω} (KMS at β=2).
   - Also: compute the "KMS temperature" β_KMS such that C_full(ω)/C_full(-ω) = e^{β_KMS ω} best-fits the data. This gives the effective temperature at which A behaves thermally from QM's perspective.

2. **C_local_TTH**: Tr[ρ_A x_A_local(τ) x_A] with x_A under K_A/β. Same KMS check.
   - Expectation: C_local satisfies KMS at β by construction (ρ_A is a KMS state for K_A, and C_local uses the modular flow of K_A). So the KMS temperature for C_local should equal β = 2.0 exactly.
   - Verify this numerically.

3. **The key result:** If C_full satisfies KMS at β_KMS ≠ β=2, then standard QM places subsystem A at a DIFFERENT effective temperature from the global temperature. If C_local satisfies KMS at β=2 exactly, then local TTH correctly captures the thermal state of A. This would be a significant result.

**Implementation:** Load the computed correlators from exploration-003's `comparison_results.json`. The file has C_full[lambda][tau_idx] and C_local[lambda][tau_idx]. For each λ:
```python
import numpy as np
import json

with open('/path/to/exploration-003/code/comparison_results.json') as f:
    data = json.load(f)

# For lambda = 0.3
lam_key = '0.3'
tau = np.array(data['tau'])
C_full = np.array(data[lam_key]['C_full'])
C_local = np.array(data[lam_key]['C_local'])

# FFT to get spectral function
dt = tau[1] - tau[0]
freqs = np.fft.rfftfreq(len(tau), d=dt) * 2 * np.pi  # angular frequencies
A_full = np.abs(np.fft.rfft(C_full)) * dt
A_local = np.abs(np.fft.rfft(C_local)) * dt

# Check KMS: A_full(+omega) / A_full(-omega) should equal exp(beta * omega)
# (Use the two-sided FFT for this)
```

Note: computing C(τ+iβ) directly requires evaluating the correlator at complex time, which you can do using the spectral representation. Alternatively, use the ratio method: compute C(ω)/C(-ω) from the two-sided FFT and fit to e^{β_KMS ω}.

**Report:** For each λ ∈ {0.1, 0.3, 0.5}:
- β_KMS(C_full) — effective KMS temperature of full QM correlator for subsystem A
- β_KMS(C_local) — effective KMS temperature of local TTH correlator
- Do they agree? If not, what is Δβ_eff = β_KMS(C_full) − β?

---

## Task C — Experimental Proposal (Brief)

Given the 9.1% discrepancy at λ=0.1 (which might be measurable), sketch the minimum experimental setup to test TTH's prediction of single-frequency oscillation vs. QM's two-frequency beating.

**The observable:** C(τ) = ⟨x_A(τ) x_A(0)⟩ — position autocorrelation of oscillator A at thermal equilibrium.

**TTH predicts:** single frequency ω_eff ≈ ω_A(1 − 0.34λ²) (no beating)
**QM predicts:** two-frequency beating at ω_± = √(ω² ± λ), period T_beat = 2π/(ω_+ − ω_-)

**Physical systems where this setup is realizable (discuss each briefly):**
1. **Coupled microwave cavity modes** — Two coupled microwave resonators at dilution refrigerator temperature (T ≈ 20 mK). Coupling λ is tunable via an adjustable coupling element (e.g., a SQUID). Standard QFT-style experiments with superconducting qubits could probe this.
2. **Coupled phonon modes in trapped ions** — Two motional modes of a two-ion chain in a Paul trap. The coupling is mechanical, controlled by trap geometry. Position autocorrelation measurable via motional state tomography.
3. **Coupled optomechanical oscillators** — Two nano-mechanical oscillators coupled via an optical cavity. Ground-state cooling and position measurement are available.

For each, estimate:
- Typical ω_A (resonance frequency in Hz or GHz)
- Typical λ achievable (coupling fraction λ/ω)
- Decoherence time vs. beat period (can you observe the beat before decoherence?)
- Whether a 9% discrepancy in autocorrelation is detectable above noise

**Minimum requirement:** Identify the system with the best ratio (decoherence time) / (beat period). That is the best candidate for testing TTH.

---

## Prior Findings (Pre-Loaded Context)

**From exploration-001:**
- K_A = βH_A (product state, λ=0)
- TTH normalization: τ_physical = β × t_modular (confirmed)

**From exploration-002:**
- ΔK_A = O(λ²), structure: Δβ = -1.36λ² (temperature shift) + band-2 squeezing
- Sign: ω_eff < ω_A (entanglement red-shifts the TTH clock)

**From exploration-003:**
| λ   | ‖C_full − C_local‖/‖C_full‖ | C_full peak freqs    | C_local peak freq |
|-----|------------------------------|----------------------|-------------------|
| 0.1 | 0.0915                       | ω_+ ≈ 1.048, ω_- ≈ 0.949 | ≈ 0.98          |
| 0.3 | 0.827                        | ω_+ ≈ 1.14, ω_- ≈ 0.84  | ≈ 0.80           |
| 0.5 | 1.166                        | ω_+ ≈ 1.20, ω_- ≈ 0.70  | ≈ 0.80           |
- Control: C_global = C_full at machine zero ✓
- Stability: N=15 to N=25 change < 1 ppb ✓

**Code location:** `/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-003/code/`

---

## Failure Paths

1. **If Connes-Rovelli explicitly use the GLOBAL modular flow:** Report this clearly. The consequence is that TTH = QM for all equilibrium states (since K_AB = βH_AB for Gibbs). The mission's conclusion would be: "TTH is empirically equivalent to QM for equilibrium Gibbs states." This is itself a publishable result. Do NOT treat this as a failure — it's the alternative conclusion the mission accepted as valid.

2. **If the literature is ambiguous (both interpretations appear):** Report the two interpretations, compute both KMS temperatures, and note that the disambiguation experiment (detecting beats vs. no beats) could settle which interpretation is physically realized.

3. **If the KMS check shows β_KMS(C_full) = β exactly:** This would mean the full QM dynamics places A at the global temperature β, same as local TTH. This doesn't resolve the local/global question but shows the two correlators have the same effective temperature (only their shapes differ). Report and interpret.

4. **If the KMS computation fails** (e.g., spectral function has too much noise, or the two-sided FFT doesn't have enough frequency resolution): Fall back to the direct complex-time method. Replace τ with τ+iβ in the phase factors: C(τ+iβ) = ∑_mn ρ_mn ⟨m|x_A|n⟩ ⟨n|x_A|m⟩ e^{-iE_n(τ+iβ)} e^{iE_m(τ+iβ)} = ∑ ... e^{βE_n} ... . Implement this directly.

---

## Output

**Write to:** `/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-004/`

1. `REPORT.md` — sections: (1) Connes-Rovelli interpretation (with exact quotes), (2) KMS temperature analysis (table + plot), (3) Experimental proposal, (4) Synthesis — does TTH make a genuinely novel prediction?
2. `REPORT-SUMMARY.md` — written LAST as completion signal
3. `code/kms_analysis.py` — KMS temperature computation

---

## What a Successful Outcome Looks Like

Section 4 of REPORT.md contains either:

**Outcome A (Novel prediction confirmed):** "Connes-Rovelli use the local modular flow [cite exact passage]. The KMS analysis shows β_KMS(C_full) ≠ β while β_KMS(C_local) = β exactly. Therefore: for coupled thermal oscillators with λ ≥ 0.1, TTH (local interpretation) predicts single-frequency autocorrelation distinguishable from QM's two-frequency beating. The minimum testable setup is [system] with parameters [values]."

**Outcome B (Empirical equivalence):** "Connes-Rovelli use the global modular flow [cite exact passage]. Therefore K_AB/β = H_AB for Gibbs states and TTH = QM exactly in equilibrium. TTH would be distinguishable only for [non-equilibrium states / open systems / specific exotic conditions]."

Either outcome is a complete result.
