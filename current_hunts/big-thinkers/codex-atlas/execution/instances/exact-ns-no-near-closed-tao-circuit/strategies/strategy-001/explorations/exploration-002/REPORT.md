# 1. Executive verdict

[VERIFIED] Decision target:

> Either there exists a concrete minimal support `(K,σ)` whose exact helical amplitude
> equations realize all Tao target monomials and can therefore be stress-tested in Phase 2,
> or even the static support/triad geometry already fails before any dynamical test.

[COMPUTED] Verdict on the singleton five-amplitude Phase 0 object: `already killed statically`.

[VERIFIED] The exact helical NS law used in the audit is

```text
(∂t + ν|k|^2) u_{s_k}(k)
  = -1/4 ∑_{p+q=k} ∑_{s_p,s_q}
      (s_p |p| - s_q |q|)
      overline{(h_{s_p}(p) × h_{s_q}(q)) · h_{s_k}(k)}
      u_{s_p}(p) u_{s_q}(q),
```

with `ik × h_s(k) = s|k| h_s(k)`. This is the Waleffe helical form of exact Leray-projected NS.

[COMPUTED] Three static obstructions already occur before any time evolution:

1. `a1^2 -> a2`, `a1^2 -> a3`, and `a4^2 -> a5` are impossible as singleton helical channels because the coefficient factor `(s_p|p| - s_q|q|)` vanishes when the same helical mode appears twice.
2. `a2 a3 -> a3` is impossible as an exact singleton monomial because `p+q=k3` with `q=±k3` forces either `p=0` or the conjugate channel `p=2k3, q=-k3`, i.e. `a2 \bar a3 -> a3`.
3. Once `a1 a3 -> a4` is enforced by `k4 = k1 + k3`, the return leg into `a1` is forced by mirror closure to be `\bar a3 a4 -> a1`, not `a3 a4 -> a1`.

[COMPUTED] The chosen best-case support also emits many nonzero off-support modes immediately; the audit script finds 96 ordered external helical emissions even before any outside mode feeds back.

# 2. Chosen minimal support and rationale

[CHECKED] I audited the smallest integer singleton support that preserves the only nondegenerate forward triad still compatible with the Tao-role template:

```text
k1 = (1,0,0),
k2 = (2,0,0) = 2k1,
k3 = (0,1,0),
k4 = (1,1,0) = k1 + k3,
k5 = (2,2,0) = 2k4.
```

[CHECKED] The sign-closed active support is

```text
S = {(k_j,σ_j), (-k_j,-σ_j) : j = 1,...,5}.
```

[COMPUTED] For the main audit I chose

```text
σ = (+,+,-,+,+).
```

[COMPUTED] This is the best helicity choice on this fixed wavevector support among all 32 sign patterns that keeps the only plausible desired channel `a1 a3 -> a4` nonzero. The script reports

```text
desired_abs_sum = 0.17677669529663684
internal_leak_abs_sum = 0.5303300858899106
external_leak_abs_sum = 15.749878978013312
```

for this `σ`.

[CHECKED] Rationale for this support:

- `k4 = k1 + k3` is mandatory if any exact `a1 a3 -> a4` term is to survive.
- `k2 = 2k1` and `k5 = 2k4` are the only singleton placements structurally aligned with the square targets, even though the exact helical coefficients later kill those channels.
- This is therefore the sharpest small-integer singleton test support for the Phase 0 object.

# 3. Exact helical interaction equations

[COMPUTED] Using `aj(t) = u_{σ_j}(k_j,t)` and the exact Waleffe coefficient formula, the internal contributions on the chosen support are:

```text
(∂t + ν)a1 = -0.176776695297 i · \bar a3 a4 + F1^ext,
(∂t + 4ν)a2 = F2^ext,
(∂t + ν)a3 = -0.176776695297 i · \bar a1 a4 + F3^ext,
(∂t + 2ν)a4 =  0.353553390593 i · a1 a3   + F4^ext,
(∂t + 8ν)a5 = F5^ext.
```

[COMPUTED] More explicitly, before combining the two orderings `(p,q)` and `(q,p)`, the nonzero internal ordered terms are:

```text
∂t a1:  (-0.088388347648 i) a4 \bar a3
         (-0.088388347648 i) \bar a3 a4

∂t a3:  (-0.088388347648 i) a4 \bar a1
         (-0.088388347648 i) \bar a1 a4

∂t a4:  (+0.176776695297 i) a1 a3
         (+0.176776695297 i) a3 a1
```

[COMPUTED] There are no nonzero internal terms at all in the `a2` or `a5` equations on this support. In particular, the structurally intended square channels `a1^2 -> a2`, `a1^2 -> a3`, and `a4^2 -> a5` are not merely small; they are exactly zero.

[COMPUTED] The first support-breaking external emissions are also exact and nonzero. The largest grouped target families are:

```text
target (2,1,0), helicity +:
  a2 a3, a1 a4, \bar a3 a5      total |coeff| sum = 1.495044591792

target (1,2,0), helicity +:
  \bar a1 a5, a3 a4             total |coeff| sum = 1.227543681390

target (0,2,0), helicity +:
  \bar a2 a5                    total |coeff| sum = 0.853553390593

target (2,3,0), helicity +:
  a3 a5                         total |coeff| sum = 0.721234726442
```

[CHECKED] The crucial point is structural: even the desired activation inputs `(a1,a3,a4)` already radiate into off-support targets such as `(1,2,0)` and `(2,1,0)`.

# 4. Desired-vs-leakage ledger

[COMPUTED] The exact ledger for the chosen support is:

| target equation | source monomial / triad | exact coefficient or structural form | status | tunable vs rigid | relevance to leakage |
| --- | --- | --- | --- | --- | --- |
| `∂t a2` | `a1,a1 -> k2=2k1` | `0` exactly because `(σ1|k1| - σ1|k1|)=0` | forbidden | rigid once singleton mode is fixed | kills the weak-pump channel at the coefficient level |
| `∂t a3` | `a1,a1 -> k3` | structurally absent on chosen support since `k3 != 2k1`; even if `k3=2k1`, same-mode helical square still gives coefficient `0` | forbidden | rigid | kills the seed channel |
| `∂t a3` | `a2,a3 -> a3` | no singleton solution to `±k2 ± k3 = k3` except zero mode or conjugate variant `2k3 + (-k3) = k3` | forbidden | rigid | kills the amplifier channel |
| `∂t a4` | `a1,a3 -> a4` with `k1+k3=k4` | `+0.353553390593 i` after summing the two orderings | desired | rigid after fixing `(K,σ)` | only surviving exact desired monomial |
| `∂t a1` | `\bar a3,a4 -> a1` with `-k3+k4=k1` | `-0.176776695297 i` | spectator / conjugate mismatch | rigid | mirror-forced return leg; not Tao’s exact `a3 a4 -> a1` |
| `∂t a3` | `\bar a1,a4 -> a3` with `-k1+k4=k3` | `-0.176776695297 i` | spectator | rigid | internal leakage inside the active support |
| `∂t a5` | `a4,a4 -> k5=2k4` | `0` exactly because `(σ4|k4| - σ4|k4|)=0` | forbidden | rigid | kills the handoff channel |
| `∂t u_+(2,1,0)` | `a2 a3`, `a1 a4`, `\bar a3 a5` | grouped total `1.495044591792` | spectator / external | rigid | immediate support-breaking emission |
| `∂t u_+(1,2,0)` | `a3 a4`, `\bar a1 a5` | grouped total `1.227543681390` | spectator / external | rigid | desired/support modes radiate off support |
| `∂t u_+(0,2,0)` | `\bar a2 a5` | grouped total `0.853553390593` | spectator / external | rigid | external leakage fed by roles intended to be passive |

[CHECKED] Every nonzero coefficient in the table is rigid after `(K,σ)` is fixed. The only tuning freedom is the pre-choice of geometry and helicity, and the scan over all 32 sign patterns on this wavevector support never restores the missing Tao channels.

# 5. Adversarial support check

[COMPUTED] I also checked the adversarial helicity assignment

```text
σ_alt = (+,+,+,-,+),
```

on the same wavevector support. This was chosen to suppress the activation channel.

[COMPUTED] The resulting internal equations are

```text
(∂t + ν)a1 = -0.073223304704 i · \bar a3 a4 + F1^ext,
(∂t + 4ν)a2 = F2^ext,
(∂t + ν)a3 =  0.073223304704 i · \bar a1 a4 + F3^ext,
(∂t + 2ν)a4 = F4^ext,
(∂t + 8ν)a5 = F5^ext.
```

[COMPUTED] So `σ_alt` does suppress the only surviving desired channel `a1 a3 -> a4`, but it does not rescue the singleton circuit:

- `desired_abs_sum = 0`,
- `internal_leak_abs_sum = 0.14644660940672624`,
- `external_leak_abs_sum = 17.943949298136992`,
- `external_term_count = 104`.

[CHECKED] This is the cheap counterexample screen: the sign choice that suppresses leakage also kills the only exact desired monomial, and the off-support emissions remain abundant.

# 6. Phase 2 recommendation

[COMPUTED] Recommendation: do not advance this singleton five-amplitude object to Phase 2. The correct verdict is `already killed statically`.

[CHECKED] Exact failure points:

- `coefficient/sign mismatch`: all singleton square channels vanish exactly.
- `triad geometry`: the amplifier `a2 a3 -> a3` has no exact singleton realization.
- `mirror-mode closure`: the return leg is forced to be `\bar a3 a4 -> a1`, not `a3 a4 -> a1`.
- `support explosion`: even the best-case support emits immediately into many outside modes such as `(2,1,0)`, `(1,2,0)`, `(0,2,0)`, and `(2,3,0)`.

[CHECKED] The only honest next move is to stop the singleton branch and, if the mission continues, reopen Phase 0 with genuinely multi-mode packets or a different exact role assignment.

## Sources

[VERIFIED] Primary sources used for the exact law and Tao target mechanism:

- Terence Tao, *Finite time blowup for an averaged three-dimensional Navier-Stokes equation*, JAMS 29 (2016), DOI `10.1090/jams/838`.
- Fabian Waleffe, *The nature of triad interactions in homogeneous turbulence*, Phys. Fluids A 4 (1992), DOI `10.1063/1.858309`, NASA NTRS entry: <https://ntrs.nasa.gov/citations/19920038608>.
- Fabian Waleffe, *Inertial transfers in the helical decomposition*, Phys. Fluids A 5 (1993), DOI `10.1063/1.858651`.

[CHECKED] Reproducible computations are in `code/helical_support_audit.py` and `code/audit-output.txt`.
