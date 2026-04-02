# Quick Check

Five yes/no questions. Takes 2 minutes. Run this whenever you propose a new theory or major revision.

---

## The Questions

### 1. Does your theory have a partition function Z?

**Why it matters:** A partition function (or action, or Hamiltonian) is what separates a *theory* from an *idea*. Without one, you can't compute anything, and you can't make predictions.

- **YES** -> Good. Write it down explicitly: Z = ...
- **NO** -> You have a framework, not a theory. That's fine at early stages — but your next step should be formalizing it into a concrete Z or S.

---

### 2. Does it produce a massless spin-2 particle?

**Why it matters:** The Weinberg-Witten theorem and decades of evidence tell us that the graviton is a massless spin-2 particle. Any theory of gravity must contain one (or explain very carefully why it doesn't while still reproducing all gravitational phenomena).

- **YES** -> Good. This is gravity.
- **MASSIVE SPIN-2** -> Acceptable if the mass is below 1.2 x 10^-22 eV (LIGO bound). But you must show the theory is ghost-free (see Boulware-Deser ghost).
- **NO** -> Your theory doesn't describe gravity. Either add a mechanism to produce a spin-2 mode, or reconsider what your theory actually describes.

---

### 3. Can it reproduce Newton's F = GMm/r^2 in some limit?

**Why it matters:** Newton's law is verified from solar system scales down to ~50 micrometers. Any theory of gravity must reproduce it in the appropriate limit.

- **YES** -> Good. Show the calculation or identify the limit where it appears.
- **NOT YET COMPUTED** -> This should be a priority. It's usually the easiest quantitative check.
- **NO** -> Your theory doesn't match reality at the most basic level. This needs to be fixed before anything else.

---

### 4. Does it violate any known experimental bound?

**Why it matters:** If a theory predicts something that's already been ruled out, it's dead (unless you can show the prediction is an artifact of an approximation).

Check these critical bounds:

| Bound | Value | Source |
|-------|-------|--------|
| Graviton mass | m_g < 1.2 x 10^-22 eV | LIGO O3 |
| GW speed | \|c_gw/c - 1\| < 5 x 10^-16 | GW170817 |
| Equivalence principle | eta < 1.3 x 10^-14 | MICROSCOPE |
| Lorentz violation (photon) | delta_c/c < 10^-33 | Fermi-LAT |
| Lorentz violation (gravity) | delta_c/c < 10^-15 | GW170817 |
| Newton's law | Verified to ~50 um | Eot-Wash |

Full data: [EXPERIMENTAL-DATA.md](EXPERIMENTAL-DATA.md)

- **NO VIOLATIONS** -> Good. Proceed.
- **POSSIBLE VIOLATION** -> Identify which bound and compute the exact value. Maybe your approximation overestimates the effect.
- **YES, VIOLATED** -> Fix it or the theory is ruled out. Common fixes: add a screening mechanism, show the violation is above the theory's cutoff, or find an error in your calculation.

---

### 5. Does it predict at least one thing that standard GR doesn't?

**Why it matters:** If your theory reproduces GR exactly with no new predictions, it's just GR in a different language. That can still be useful (new computational techniques, new conceptual insights), but it's not a new theory.

- **YES** -> Excellent. Write down the prediction explicitly. Is it a number? Is it testable?
- **NOT YET** -> That's okay if the theory is young. But keep this in mind — the goal is predictions.
- **NO, AND THE THEORY IS MATURE** -> Consider: is this a reformulation of GR? That's valuable, but be honest about what it is.

---

## Scorecard

| # | Question | Result | Notes |
|---|----------|--------|-------|
| 1 | Has partition function Z? | | |
| 2 | Massless spin-2 particle? | | |
| 3 | Reproduces Newton's law? | | |
| 4 | Within experimental bounds? | | |
| 5 | Novel prediction? | | |

**Interpretation:**
- **5/5** -> Theory is in good shape. Proceed to VALIDATION-TESTS.md Tier 1.
- **3-4/5** -> Viable but incomplete. Address the gaps.
- **1-2/5** -> Significant foundational work needed. Focus on the failures before proceeding.
- **Fails #4** -> Immediate action needed. Either find the error or pivot.
