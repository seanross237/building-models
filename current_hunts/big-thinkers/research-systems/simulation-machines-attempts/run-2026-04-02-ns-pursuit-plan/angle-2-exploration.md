# Angle 2 Exploration: Convex Integration Rigidity --- Proving Blowup Solutions Cannot Be Wild

**Date:** 2026-04-02
**Role:** Adversarial research mathematician
**Verdict:** `weakly promising` (but closer to `unclear` than to `promising`)

---

## 1. Concise Statement of the Route

Assume for contradiction that a smooth NS solution `u` on `[0,T)` blows up at time `T`. The rescaled solutions `u_lambda(x,t) = lambda u(lambda x, lambda^2 t + T)` near the singularity must (by standard compactness arguments) accumulate on a limiting profile --- typically self-similar (SS) or discretely self-similar (DSS). The route then invokes convex integration technology in a novel way:

- **Step A (Rigidity):** Prove that any blowup profile arising from smooth data must live in a regularity class strictly above the Onsager threshold `C^{1/3}`. Concretely, show `||U||_{C^{1/3+epsilon}} >= C_0 > 0` for some universal `epsilon, C_0`.

- **Step B (Flexibility):** Use convex integration (Buckmaster-Vicol and successors) to show that in any `C^{1/3+epsilon}`-neighborhood of such a profile `U`, there exist weak solutions with arbitrarily prescribed energy dissipation rates, violating the energy equality that the smooth approximating solutions satisfy.

- **Step C (Incompatibility):** Argue that the blowup solution, as it approaches the singularity, must traverse a regularity corridor where its behavior is simultaneously forced to be rigid (by Step A) and surrounded by flexible competitors (by Step B). Extract a topological or measure-theoretic contradiction from this coexistence.

The first theorem-object is a **blowup profile rigidity lemma**: rescaled solutions converge to a self-similar profile `U` with `||U||_{C^{1/3+}} >= C_0 > 0`, a quantitative stiffness bound incompatible with convex integration flexibility.

---

## 2. Check Against Known Obstructions

The status document records these relevant closed or capped routes:

| Obstruction | Relevance to Angle 2 |
|---|---|
| **Enstrophy/BKM circularity** (Finding 2) | Angle 2 does not attempt to bound `\|\|omega\|\|_{L^infty}` directly; it works by contradiction from a blowup assumption. **Not directly triggered.** |
| **De Giorgi `beta = 4/3` cap** (Findings 3, 4) | Angle 2 does not use De Giorgi iteration or epsilon-regularity at all. **Not triggered.** |
| **Epsilon-regularity family** (Finding 5) | Same: the route is not a bootstrap. **Not triggered.** |
| **Exact reformulation no-gain** (Finding 9) | The route is not a reformulation of the equation. It introduces an external object (convex integration solutions) to create a contradiction. **Not triggered in the standard sense**, though see Section 4 below. |
| **Standard compactness-rigidity host-space retries** (Finding 9, "What Is Closed") | **Potentially triggered.** The route does invoke compactness-rigidity reasoning (blowup => rescaled limits => profile). The status document lists "standard compactness-rigidity host-space retries" as closed. The question is whether Angle 2's use of compactness-rigidity is standard or genuinely novel. See Section 4. |
| **Tao-adjacent lines** (Findings 8, 10--18) | Angle 2 does not target the Tao mechanism directly. It instead targets blowup profiles, which is upstream of the Tao construction. **Not directly triggered**, but Tao's averaged-NS construction must be examined as a stress test: does Tao's blowup produce a profile that the rigidity/flexibility argument can see? |

**Summary:** Angle 2 does not fall into any of the explicitly closed routes. The closest contact point is with standard compactness-rigidity, but the specific use of convex integration flexibility as the contradiction source is genuinely new. No previous route in the status document tried this.

---

## 3. Strongest Argument For: Why the Route Might Work

**The rigidity/flexibility dichotomy is a real structural phenomenon in fluid mechanics, and it has never been pointed at the regularity problem.**

Here is the honest case:

**(a) The dichotomy is not speculative; it exists in nearby problems.** Convex integration has produced a sharp Onsager-type dichotomy for the Euler equations: below `C^{1/3}`, energy dissipation is unconstrained (flexibility); above `C^{1/3}`, energy is conserved (rigidity). For Navier-Stokes, the Buckmaster-Vicol non-uniqueness results for Leray-Hopf solutions similarly show flexibility below a regularity threshold. This is a proven structural feature of the equations, not a hypothesis.

**(b) A blowup profile would have to sit in a very specific regularity band.** Any self-similar or DSS blowup profile `U` for NS would satisfy the self-similar NS equations, which impose elliptic-type regularity constraints. The profile cannot be arbitrary: it must solve a specific nonlinear elliptic PDE. This forces it into a narrow regularity class that is potentially in tension with the flexibility results. Known results (Tsai, Jia-Sverak, Bradshaw-Tsai) already show that self-similar profiles, if they exist, must satisfy strong regularity and decay conditions. This is non-trivial existing content.

**(c) The argument targets a genuine gap in the literature.** The interaction between convex integration flexibility and classical blowup analysis has barely been explored. The question "can a blowup profile coexist with the wild solutions that convex integration places nearby?" has not been asked in a rigorous setting, let alone answered. There is real room for a new theorem here, even if it falls short of resolving the full regularity question.

**(d) It naturally separates into modular subproblems.** Steps A, B, and C are independent enough that partial progress on any one of them would be a publishable result. A rigidity theorem for blowup profiles (Step A) is valuable independently of the contradiction argument. A convex integration result producing competitors near SS/DSS profiles (Step B) would be a major contribution to the convex integration program. This modularity is a practical advantage.

---

## 4. Strongest Argument Against: Why It Probably Fails

**The route has at least four serious structural problems, one of which may be fatal.**

### Problem 1: The compactness-to-profile step is non-trivial and may not produce the required convergence

The assertion that rescaled blowup solutions converge to a self-similar or DSS profile is not a theorem for 3D NS. The best available results are:

- **Leray (1934):** If blowup occurs, there exists a subsequence of rescalings that converges weakly to a self-similar solution (a "backward self-similar solution"). But Necas-Ruzicka-Sverak (1996) and Tsai (2009) showed that such backward self-similar solutions must be zero under mild integrability assumptions.
- **For forward self-similar solutions:** Jia-Sverak (2014) proved existence of forward self-similar solutions for certain data, but these are global-in-time objects with specific structure, not blowup profiles.
- **For DSS solutions:** Bradshaw-Tsai (2019), Chae-Wolf (2019), and others have studied DSS solutions and obtained conditional exclusion results.

The key problem: **there is no theorem guaranteeing that a blowup for smooth data must produce a non-trivial limiting profile.** The blowup could be of Type II (with the rescalings not having a clean limit), or the convergence could be too weak to carry the quantitative stiffness bound through to the limit. This is the most fragile link in the chain.

### Problem 2: The Onsager threshold and the NS blowup regularity band may not overlap

The convex integration flexibility results (Buckmaster-Vicol and successors) work below `C^{1/3}` Holder regularity (or in suitable Besov spaces `B^{1/3}_{3,infty}` etc). A blowup profile, if it exists, would plausibly have much higher regularity away from the singular set --- it satisfies an elliptic PDE and would be smooth except possibly at the origin. The stiffness bound `||U||_{C^{1/3+}} >= C_0` is meant to say the profile has regularity *strictly above* the Onsager threshold.

But this is exactly the wrong direction for the contradiction: **if the profile has regularity above `C^{1/3}`, then it is in the rigidity regime where convex integration does NOT produce nearby wild solutions.** The energy conservation/dissipation dichotomy says:
- Below `C^{1/3}`: wild solutions exist (flexibility).
- Above `C^{1/3}`: energy is conserved (rigidity) --- but this is a *good* property, not a contradictory one.

So the proposed contradiction has a fundamental orientation issue. For the contradiction to work, you would need the blowup approach to force the solution *below* `C^{1/3}` at some point, where wild competitors exist. But if the solution is smooth until the blowup time, its Holder regularity only degrades *at the blowup time*, not before. The regularity corridor traversal happens only in the limit, and in the limit the profile is already a distributional solution where the convex integration / Onsager framework does not directly produce the needed contradiction.

This is the single most serious concern. The proposed theorem-object states `||U||_{C^{1/3+}} >= C_0 > 0` and calls this "incompatible with convex integration flexibility." But if `C^{1/3+}` is *above* the Onsager threshold, the profile is in the rigidity regime, and convex integration does not say anything contradictory about solutions with that regularity. The incompatibility claim needs much more careful formulation.

### Problem 3: Convex integration for NS (not Euler) is far less developed

The sharp Onsager dichotomy is for the Euler equations. For Navier-Stokes:
- Buckmaster-Vicol proved non-uniqueness of weak solutions, but not at the sharp Onsager regularity.
- The non-uniqueness results for NS are in much weaker regularity classes and involve solutions that are not Leray-Hopf.
- There is no result saying that near a given NS profile, one can produce NS weak solutions with arbitrarily prescribed energy dissipation.

The gap between what convex integration currently delivers for NS and what Step B requires is substantial. Step B would itself be a breakthrough-level result.

### Problem 4: Topological/measure-theoretic contradiction mechanism is underspecified

Step C says to extract a "topological obstruction to blowup" from the coexistence of rigidity and flexibility. But the proposed mechanism for this contradiction is vague. In what sense does the existence of wild solutions *near* a profile contradict the profile being a blowup limit? The wild solutions are not the actual solution --- they are other solutions that convex integration produces. The actual solution is a specific smooth function that approaches the profile. The existence of other, non-smooth solutions nearby does not obviously obstruct this convergence.

For a genuine contradiction, you would need something like: "the set of solutions with property P is topologically trivial (contractible, connected, etc.), and removing the blowup profile disconnects it." But no such topological structure theorem exists for the space of NS solutions, and proving one would be at least as hard as the original problem.

---

## 5. First 2--5 Concrete Subproblems

### Subproblem 1: Profile existence and regularity for Type I blowup

**Statement:** Prove that if a smooth NS solution on `R^3` (or `T^3`) undergoes a Type I blowup at `(x_0, T)` (meaning `||u(t)||_{L^infty} <= C / sqrt{T-t}`), then the rescaled solutions converge in `C^k_{loc}(R^3)` for all `k` to a non-trivial self-similar profile `U` satisfying the self-similar NS equations.

**Status in the literature:** Partially known. Seregin, Escauriaza-Seregin-Sverak, and others have results in this direction, but the convergence is typically in weaker topologies and the non-triviality of the limit is conditional. This subproblem is serious but not unprecedented.

**Difficulty:** High but tractable. This would be a strong standalone result.

### Subproblem 2: Regularity band identification for SS/DSS profiles

**Statement:** Determine the exact Holder/Besov regularity of any non-trivial self-similar or DSS solution to the NS self-similar equations. Specifically, prove that such a profile `U` must belong to `C^alpha` for some explicit `alpha > 1/3` (or prove that `alpha <= 1/3` is possible).

**Status:** For self-similar solutions with finite `L^3` norm, Jia-Sverak and Korobkov-Tsai have regularity results. But the sharp Holder exponent relative to the Onsager threshold `1/3` has not been determined. This is the critical subproblem: if SS/DSS profiles can have regularity at or below `1/3`, the route's orientation problem (Problem 2 above) becomes fatal.

**Difficulty:** Very high. This is essentially a new regularity theory for the self-similar NS equations.

### Subproblem 3: Convex integration near SS/DSS profiles for NS

**Statement:** Prove that for any non-trivial self-similar NS profile `U` in some Besov space `B^s_{p,q}` with `s < 1/3` (Onsager-subcritical), there exist infinitely many weak NS solutions in a ball around `U` with arbitrarily prescribed energy dissipation.

**Status:** No such result exists. The existing convex integration results for NS (Buckmaster-Vicol) do not produce solutions near a prescribed profile with controlled closeness. This is a major open problem in convex integration.

**Difficulty:** Extremely high. This would itself be a landmark result.

### Subproblem 4: Formalize the contradiction mechanism

**Statement:** Assuming Subproblems 1--3 are solved, give a precise logical argument for why the coexistence of a rigid blowup profile (from Subproblem 1--2) and flexible nearby weak solutions (from Subproblem 3) yields a contradiction with the blowup.

**Status:** No existing framework. The proposed "topological obstruction" needs to be made precise. The most natural formalization would be through uniqueness: if the blowup profile is the unique limit of the rescaled solutions, and convex integration produces other limit points, then the rescaled sequence cannot converge --- contradicting Subproblem 1. But this requires the convex integration solutions to be *limits of the same rescaling sequence*, which is not what convex integration gives.

**Difficulty:** This may be the subproblem where the route collapses entirely. The logical gap between "wild solutions exist near the profile" and "the actual smooth solution cannot approach the profile" has no known bridge.

---

## 6. Classification: Theorem-Facing, Mechanism-Facing, or Speculative

**Mostly speculative, with mechanism-facing components.**

The individual subproblems (profile regularity, convex integration near profiles) are honest mathematical questions with potential for standalone theorems. In that sense, the route has mechanism-facing value: progress on Subproblems 1--3 would teach us real things about NS structure regardless of whether the full contradiction argument works.

However, the route as a proof of regularity is speculative for two reasons:

1. The contradiction mechanism (Subproblem 4) does not have even a candidate formalization. The "topological obstruction" is a metaphor, not a mathematical object. Until it can be stated as a precise claim, the route is not theorem-facing.

2. The orientation of the rigidity/flexibility dichotomy (Problem 2 in Section 4) may be fundamentally wrong: the profile having *high* regularity means it is in the regime where convex integration is *silent*, not contradictory.

The route would upgrade to mechanism-facing if the orientation problem were resolved (i.e., if there were a precise reason why blowup forces the solution through a sub-`C^{1/3}` regularity band during the approach to singularity) and the contradiction mechanism were formalized.

It would upgrade to theorem-facing only after Subproblems 1--3 each had honest proof strategies.

---

## 7. Final Verdict: `weakly promising`

**Reasoning:**

- **Not dead:** The route does not fall into any explicitly closed class in the status document. The idea of using convex integration flexibility as a regularity tool is genuinely novel and has not been tested. The individual subproblems are real mathematics.

- **Not promising:** The route has a potential orientation-level flaw (Problem 2): the rigidity/flexibility dichotomy may point in the wrong direction for the contradiction. The contradiction mechanism (Subproblem 4) is completely unformalized. The convex integration technology for NS is far from what Step B needs. Each subproblem is individually at least "very hard," and they compound multiplicatively.

- **Weakly promising because:** (a) The rigidity/flexibility theme is a genuine structural feature of these equations that has not been explored for regularity. (b) Even partial progress (profile regularity relative to Onsager threshold, convex integration near specific profiles) would be valuable. (c) The orientation problem (Problem 2) might be resolvable --- it is conceivable that the blowup approach forces a loss of regularity in specific norms or at specific scales that does cross the Onsager threshold, even if the solution remains smooth until the blowup time. This is speculative but not obviously impossible.

- **The critical near-term test is Subproblem 2:** Determine whether self-similar NS profiles have Holder regularity above or below `1/3`. If above (which is the expected answer based on elliptic regularity of the self-similar equations), the route needs a fundamentally different formulation of the contradiction. If below, the route becomes significantly more interesting.

**Recommended disposition:** Worth a focused 2--3 day investigation of Subproblem 2 (profile regularity relative to Onsager threshold). If the answer is "profiles are smooth away from the origin and thus trivially above `C^{1/3}`," the route needs radical surgery or should be parked. If there is any mechanism by which the blowup approach forces passage through the sub-`C^{1/3}` band (perhaps in a spatial average or a Besov norm with specific integrability), the route would merit a longer investigation.
