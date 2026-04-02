# REPORT-SUMMARY

- Goal: decide whether the surviving harmonic far-field pressure loophole is Tao-compatible, Tao-incompatible, or still unclear by checking Tao's averaged Navier-Stokes equation at the equation level.
- What I tried:
  - read exploration 001 and the preloaded local Vasseur-context files to fix the exact loophole target;
  - searched the repository for Tao material;
  - attempted direct shell retrieval of Tao's paper, which failed because network/DNS was unavailable in the execution environment;
  - extracted Tao's primary-source formulas from AMS/JAMS and arXiv web snippets: the unaveraged `B`, the averaged operator `\tilde B`, and Tao's primitive-form `T(u,u)` remark.
- Outcome: succeeded.
- Verdict: `Tao-incompatible`.
- One key takeaway: the loophole needs the pressure source to be the local tensor-divergence `∂i∂j(u_i u_j)`, so that "far field" means genuinely distant fluid, but Tao replaces this with `-Δp = div T(u,u)` where `T(u,u)` is already a nonlocal averaged pseudodifferential bilinear operator.
- What replaces `-Δp = ∂i∂j(u_i u_j)` after averaging:

  ```text
  ∂_t u + T(u,u) = Δu - ∇p,   div u = 0,
  -Δp = div T(u,u).
  ```

- New bottleneck in the averaged setting: not a Vasseur-style local pressure term like `P_{k21}`, but the already-nonlocal averaged convection/pressure package `T(u,u)` or equivalently `\tilde B(u,u)`.
- Leads worth pursuing:
  - build a toy Tao-type averaged operator using explicit order-zero multipliers and measure how `S_avg := div T(u,u)` leaks into a local ball from distant velocity support;
  - formulate the sharper claim that the loophole requires source locality of `u ⊗ u`, which fails for any nontrivial Tao-type averaging.
- Unexpected findings:
  - Tao does preserve a formal harmonic far-field pressure remainder after any cutoff split of `div T`, so harmonicity alone is not the issue;
  - the decisive failure is pre-Poisson locality, not post-Poisson harmonicity.
- Computations worth doing later if outside scope:
  - numerically compare `S_NS := ∂i∂j(u_i u_j)` and `S_avg := div T(u,u)` for compactly supported divergence-free test fields and explicit multiplier choices;
  - test whether any restricted subclass of Tao averages that avoids nonlocal multipliers could preserve the loophole-relevant locality.
