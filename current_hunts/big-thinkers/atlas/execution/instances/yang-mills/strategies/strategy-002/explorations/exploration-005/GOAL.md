# Exploration 005: Hessian Sharpness Check for SU(2) Bakry-Émery Bound

## Mission Context
This is a YANG-MILLS mission. Do not confuse with other missions.

## Background

The Shen-Zhu-Zhu (SZZ) proof of mass gap for SU(N) lattice Yang-Mills uses the Bakry-Émery condition:
```
K_S = N/2 - (Hessian contribution) > 0
```

For the edge formulation (SZZ): **Lemma 4.1** bounds the Hessian as:
```
|HessS(v,v)| ≤ 8(d-1)N|β| · |v|²
```
This gives threshold β < 1/(16(d-1)) = 1/48 in d=4, N=2 (SU(2)):
- N = 2, d = 4
- K_S = N/2 - 8N(d-1)β = 1 - 48β
- K_S > 0 iff β < 1/48 ≈ 0.0208

For the vertex σ-model (CNS Sept 2025): Hessian ≤ 4(d-1)Nβ, giving threshold 1/24.

**The key question:** Is the Lemma 4.1 bound **tight** (i.e., the actual Hessian is close to 48β for configurations drawn from the Gibbs measure), or is it **loose** (actual Hessian ≪ 48β)?

If the bound is loose by a factor k, then the actual threshold might be k/48 instead of 1/48.
If the bound is loose by a factor 2, this would recover the CNS vertex bound 1/24 even using the edge formulation.

## Your Task

Numerically measure the Hessian of the Wilson action for SU(2) lattice gauge theory.

**IMPORTANT: Write code immediately. Start coding in the first 5 minutes.**

### Step 1: Set up the Hessian measurement

For the Wilson action S = -β Σ_plaq Re Tr(U_plaq):
- The Hessian of S at a gauge field configuration Q ∈ SU(2)^E is a quadratic form on the tangent space T_Q SU(2)^E
- A tangent vector v ∈ T_Q SU(2)^E is a collection of vectors v_e ∈ su(2) (one per edge e)
- HessS(v,v) = Σ_{e,f} v_e^T [∂²S/∂U_e ∂U_f] v_f

For a single edge e:
```
HessS_e(v_e, v_e) = Re Tr(v_e [∂S/∂U_e]) + Re Tr(v_e² [∂S/∂U_e]) + ...
```

More practically, use the **finite-difference Hessian**: approximate
```
HessS(v,v) ≈ [S(Q exp(ε v)) - 2S(Q) + S(Q exp(-ε v))] / ε²
```
where v is a random unit tangent vector (v_e = random unit su(2) element for each edge e).

### Step 2: Measure the normalized Hessian

For n_samples random configurations Q drawn from the Gibbs measure μ_β and n_tangent random unit tangent vectors v per configuration:

```
H_normalized(Q, v) = |HessS(v,v)| / (|v|² · 8(d-1)N|β|)
```

If Lemma 4.1 is tight: H_normalized ≈ 1
If Lemma 4.1 has slack: H_normalized ≪ 1

### Step 3: Scan β values

Measure H_normalized at β = 0.02, 0.1, 0.5, 1.0, 2.0 on a 4³ lattice (3D is fine for this measurement).

For each β:
- Draw 20 random configurations Q from the Gibbs measure (use 500 thermalization + 100 measurement sweeps, discard autocorrelation)
- For each configuration, measure H_normalized for 10 random tangent vectors v
- Report: mean(H_normalized), std(H_normalized), max(H_normalized)

**The bound says:** H_normalized ≤ 1 always. Check this.
**The question is:** what is max(H_normalized) across configurations?

### Step 4: Interpret

If max(H_normalized) ≈ 1.0 at β = 0.02 (near SZZ threshold): Lemma 4.1 is tight; no slack
If max(H_normalized) ≈ 0.5: The actual threshold may be 2× better (1/24 instead of 1/48)
If max(H_normalized) ≈ 0.25: The threshold may be 4× better (1/12 instead of 1/48)

Compare with CNS vertex formulation prediction: vertex Hessian = 4(d-1)Nβ, while edge Hessian bound = 8(d-1)Nβ. If the edge Hessian is actually ~4(d-1)Nβ, the ratio would be 0.5.

## Technical Setup

- Use the SU(2) simulation code from: `../../strategy-001/explorations/exploration-003/code/su2_lattice.py`
- SU(2) tangent space su(2): basis {iσ₁, iσ₂, iσ₃} / √2 (or use random unit quaternions with zero real part)
- Finite-difference step: ε = 1e-4
- |v|² = Σ_e |v_e|²_su(2) = Σ_e Re Tr(v_e† v_e)/2

Use a 4³ lattice for speed (smaller than 4⁴ but same physics for Hessian measurement).

## Success Criteria

**Success:**
1. H_normalized table for 5 β values with mean, std, max
2. Clear comparison to Lemma 4.1 bound (=1 if tight)
3. Estimate of how much the threshold could improve if the actual Hessian is used

**Failure:** If SU(2) Hessian measurement is too noisy or the finite-difference approximation fails. Report: what noise level you measured and why.

## Output Format

1. **code/** directory with:
   - `hessian_sharpness.py` — main measurement script
   - `results.json` — structured results

2. **REPORT.md** covering:
   - Results table
   - Comparison to Lemma 4.1 bound
   - Slack estimate and implication for threshold improvement

3. **REPORT-SUMMARY.md** (1 page):
   - Main result: is Lemma 4.1 tight or loose?
   - Estimated threshold improvement if actual Hessian is used
   - Whether this motivates a sharper analytic proof

## Important Notes
- Save code to files immediately before running
- Print results as you get them for each β
- If a computation fails, note it and move to the next β value
- Cross-check: at β = 0.02, the actual max H should ≤ 1.0 (Lemma 4.1 is an UPPER BOUND, not equality)
- Write report section by section, not as one large block
