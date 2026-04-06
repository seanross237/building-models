# Research Memo: Smith Transfer Route to Density Zero for Rank >= 2

Date: 2026-04-05

## Executive Summary

Alexander Smith's March 22, 2025 preprint proves that for every fixed elliptic curve \(E/\mathbf{Q}\), the quadratic twists \(E_d\) have \(2^\infty\)-Selmer corank \(0\) and \(1\) with density \(1/2\) each, and density \(0\) for corank \(\ge 2\). [ESTABLISHED] The underlying mechanism comes from the Klagsbrun-Mazur-Rubin Markov model for Selmer-rank evolution under adding twisting primes, together with Smith's 2022 "higher Selmer / fixed-point Selmer" machinery and, in the 2025 paper, new isogeny arguments for the balanced-isogeny cases. [ESTABLISHED] The abstract Markov kernel is essentially universal; the curve-dependence enters when one proves that an actual twist family shadows that kernel with quantitative error. [ESTABLISHED]

The main conclusion of this memo is negative for the literal transfer strategy. [SPECULATIVE, but based on a straightforward counting analysis] Even a uniform spectral-gap statement for the abstract Markov chain would not by itself imply density zero for rank \(\ge 2\) among all elliptic curves ordered by naive height, because a positive-density share of height-bounded curves seem to lie in twist classes that contribute only \(O(1)\) twists below that height. A successful "Smith transfer" would therefore need more than uniform mixing in each fixed twist family: it would need either uniform control of the very first few twists in most twist classes, or a second global-height input not contained in Smith's fixed-family theorem.

## 1. Smith's Markov-Chain / Random-Matrix Technique

### 1.1 The Klagsbrun-Mazur-Rubin model

- [ESTABLISHED] In Zev Klagsbrun, Barry Mazur, and Karl Rubin, *A Markov model for Selmer ranks in families of twists* (Compositio Mathematica 150 (2014), 1077-1106), the state space is the set of nonnegative integers \(r\), interpreted as \(p\)-Selmer rank.
- [ESTABLISHED] The one-step transition is the "mod-\(p\) Lagrangian operator": from state \(r\), one moves to \(r-1\) with probability \(1-p^{-r}\) and to \(r+1\) with probability \(p^{-r}\). For \(p=2\), this is \(r \mapsto r-1\) with probability \(1-2^{-r}\) and \(r \mapsto r+1\) with probability \(2^{-r}\).
- [ESTABLISHED] The chain comes from linear algebra on maximal isotropic subspaces: when a new twisting prime is imposed, one local Selmer condition is replaced by another, and the global Selmer group changes as the dimension of an intersection of Lagrangians changes by \(\pm 1\).
- [ESTABLISHED] KMR prove that, in suitable twist orderings ("fan structures"), the limiting distribution exists and is given by an equilibrium distribution of this Markov process. Their abstract explicitly states that the Markov process itself is independent of \(E\) and \(K\), up to a single parity-bias parameter called the disparity.

### 1.2 How Smith upgrades this to \(2^\infty\)-Selmer

- [ESTABLISHED] In Alexander Smith, *The distribution of \(\ell^\infty\)-Selmer groups in degree \(\ell\) twist families I* (arXiv:2207.05674, first posted July 12, 2022), the key new object is the fixed-point Selmer group, which acts as the base layer of the higher Selmer filtration.
- [ESTABLISHED] Smith's 2022 program is not just "one Markov chain on ranks." It is a layered statement: once the fixed-point layer is stable on a grid class, the higher Selmer data are controlled by successive Cassels-Tate pairings, and the resulting rank evolution is described by random alternating-matrix models closely related to the KMR chain.
- [ESTABLISHED] The actual randomness is arithmetic, not probabilistic: one proves that the relevant local symbols and local conditions at newly introduced twisting primes become equidistributed on well-chosen boxes or grids of twists. The Markov model is the limiting linear-algebra law for that arithmetic equidistribution.
- [ESTABLISHED] Smith's March 22, 2025 preprint *The Birch and Swinnerton-Dyer conjecture implies Goldfeld's conjecture* (arXiv:2503.17619) extends the fixed-family result to all \(E/\mathbf{Q}\), including the balanced-isogeny cases that were excluded in the generic 2022 theorem.
- [ESTABLISHED] In the 2025 paper, Smith shows that the \(2\)-Selmer-rank distribution itself can differ from the Poonen-Rains distribution in balanced-isogeny cases, but the final \(2^\infty\)-Selmer corank statement still comes out \(50\%\) corank \(0\), \(50\%\) corank \(1\), \(0\%\) corank \(\ge 2\).

### 1.3 Where the convergence comes from

- [ESTABLISHED] There are two distinct convergence mechanisms.
- [ESTABLISHED] First, there is convergence inside the abstract linear-algebra model: iterating the Lagrangian Markov operator pushes any initial rank distribution toward its equilibrium law.
- [ESTABLISHED] Second, there is convergence of the arithmetic family to that abstract model: one uses effective equidistribution of Frobenius classes and local symbols over carefully constructed grids of twisting primes.
- [ESTABLISHED] In Smith's framework, the slow quantitative loss comes from the arithmetic comparison, especially from passing from grid orderings to the natural ordering by \(|d|\). It does not primarily come from any difficult spectral analysis of the universal Markov operator itself.
- [HYPOTHESIS] A project-local note records that Smith 2022, Remark 1.3, gives an explicit natural-order upper bound of shape
  \[
  \Pr_{|d|\le D}\big(r_{2^\infty}(E_d)\ge 2\big)\ \ll_E\ \exp\!\big(-c_E\sqrt{\log\log\log D}\big).
  \]
  I was not able to verify the exact wording directly from the accessible web text of the paper, so I am treating this precise formula as plausible but not fully checked here.

### 1.4 What is established versus what is not

- [ESTABLISHED] The limiting \(2^\infty\)-Selmer corank distribution for fixed \(E/\mathbf{Q}\) is a theorem of Smith 2025.
- [ESTABLISHED] The Markov/random-matrix explanation of the limiting law is solidly grounded in KMR 2014 and Smith 2022.
- [ESTABLISHED] The 2025 proof is not merely "run the same Markov chain for all curves." It also uses balanced-isogeny casework and an isogeny contradiction argument.
- [SPECULATIVE] It is conceptually convenient to speak of a "spectral gap bottleneck," but the published arguments are not phrased as a uniform spectral-gap theorem plus a perturbation bound. The real arithmetic bottleneck is the quantitative approximation of twist families by the universal kernel.

## 2. Uniformity of the Spectral Gap

### 2.1 The abstract chain versus the arithmetic theorem

- [ESTABLISHED] For the generic KMR transition kernel, the Markov operator itself does not depend on the base curve \(E\). Therefore any intrinsic spectral gap of that abstract operator would also be independent of \(E\).
- [ESTABLISHED] I did not find a published theorem in the accessible sources that states an explicit spectral-gap constant for the KMR operator or for Smith's higher-Selmer operators.
- [ESTABLISHED] The curve-dependence in Smith's arithmetic theorem comes from the comparison of actual twist statistics to the model, not from a visibly curve-dependent Markov kernel.

### 2.2 Where \(E\)-dependence plausibly enters

- [ESTABLISHED] The local bad places depend on \(E\), and Smith's grids are built to avoid or control them.
- [ESTABLISHED] The Chebotarev fields governing the local symbols depend on the Galois data of \(E[2]\), the relevant isogenies, and the fixed-point Selmer layer.
- [ESTABLISHED] Effective Chebotarev error terms depend on the degree and discriminant of these auxiliary fields, hence on arithmetic invariants of \(E\).
- [ESTABLISHED] In the balanced-isogeny cases of Smith 2025, extra parameters enter the random-matrix model, so even the exact stationary law for \(2\)-Selmer rank is not literally the same as in the generic case.

### 2.3 What can and cannot be claimed today

- [ESTABLISHED] There is no theorem in the sources I checked that gives a uniform lower bound, over all \(E/\mathbf{Q}\) of bounded height or bounded conductor, for the arithmetic rate at which the twist family approaches the limiting corank law.
- [ESTABLISHED] There is no theorem in the accessible sources that converts Smith's fixed-family limit into a bound uniform in \(E\) and \(D\).
- [SPECULATIVE] It is plausible that the arithmetic approximation constants should degrade only polylogarithmically or at worst polynomially in natural invariants such as the conductor or discriminant of the relevant auxiliary fields, because the governing Galois extensions all have bounded degree in the \(2\)-primary setting. I have not found a proof of this.
- [SPECULATIVE] If one rewrote Smith's proof as "universal Markov operator + arithmetic perturbation," the likely uniformity problem would be to control the perturbation uniformly, not to prove a new spectral-gap theorem.

### 2.4 Bottom line for angle 2

- [ESTABLISHED] The abstract gap is the easy part conceptually and appears universal.
- [ESTABLISHED] The hard missing theorem is a uniform quantitative comparison between actual quadratic-twist statistics and the abstract model.
- [SPECULATIVE] Even that uniform comparison may still be insufficient for a transfer to height order; see Section 3.

## 3. The Twist-to-Height Counting Argument

### 3.1 The formal decomposition

- [ESTABLISHED] If \(E\) is given by a short integral Weierstrass equation \(y^2=x^3+Ax+B\), then the quadratic twist by squarefree \(d\) can be written \(y^2=x^3+d^2Ax+d^3B\). On this equation, the naive height scales exactly by \(|d|^6\).
- [ESTABLISHED] After passing to minimal models, one should still have \(H(E_d)\asymp_E |d|^6 H(E)\); for transfer purposes the exact constants are not the main issue.
- [ESTABLISHED] Choosing one representative \(E_0\) per quadratic-twist class, one can formally write
  \[
  \#\{E: H(E)\le H,\ \mathrm{rank}(E)\ge 2\}
  \le
  \sum_{E_0} \#\left\{d:\ H(E_0^d)\le H,\ \mathrm{rank}(E_0^d)\ge 2\right\}.
  \]

### 3.2 The optimistic transfer that people first imagine

- [CONJECTURE / desired input] Suppose one had a uniform bound
  \[
  \sup_{E/\mathbf{Q}}\ \Pr_{|d|\le D}\big(r_{2^\infty}(E_d)\ge 2\big)\le \eta(D),
  \qquad \eta(D)\to 0.
  \]
- [SPECULATIVE] Then one might hope to insert \(D\sim (H/H(E_0))^{1/6}\) into the sum over twist classes and conclude that the weighted average of \(\eta(D)\) goes to \(0\).
- [SPECULATIVE] This is the transfer picture usually suggested informally.

### 3.3 Why the direct transfer appears to fail

- [SPECULATIVE, but the counting point is elementary] The problem is that most height-bounded curves appear to live in twist classes with only very few representatives below the same height bound.
- [SPECULATIVE, but strongly supported] Random integral pairs \((A,B)\) are usually not simultaneously divisible by \(d^2\) and \(d^3\) for any large squarefree \(d\). So most curves are already "twist-primitive."
- [SPECULATIVE, but easy to justify heuristically] Because of this, the average number of curves of height \(\le H\) in a twist class with representative height \(\le H\) should be \(O(1)\), not growing with \(H\).
- [SPECULATIVE] If that heuristic is right, then per-family asymptotics as \(D\to\infty\) are too weak to control the height family: for a large fraction of twist classes, the available twist range \(D\) is only \(1,2,3,\dots\), where asymptotic mixing says nothing.

### 3.4 A concrete lower-bound heuristic for the number of twist classes

- [SPECULATIVE, but very plausible] Consider short Weierstrass models \(y^2=x^3+Ax+B\) with \(A\) squarefree. Such a curve cannot be a nontrivial quadratic twist of another integral short Weierstrass model, because a nontrivial twist factor \(d\) would force \(d^2\mid A\).
- [SPECULATIVE] The number of squarefree \(A\) with \(|A|\ll H^{1/3}\) is a positive proportion of all such \(A\), and for each such \(A\) there are \(\gg H^{1/2}\) admissible \(B\)'s. This suggests \(\gg H^{5/6}\) twist-primitive curves up to height \(H\).
- [SPECULATIVE] Since the total number of elliptic curves up to naive height \(H\) is itself \(\asymp H^{5/6}\), twist classes are already as numerous as curves to first order. That makes a fixed-family transfer intrinsically weak.

### 3.5 What uniformity would actually have to look like

- [ESTABLISHED as a logical point] A mere bound of the form \(\eta(D)\to 0\) for large \(D\) is not enough.
- [SPECULATIVE] To get a true transfer, one would need one of the following much stronger inputs.
- [SPECULATIVE] A bound uniform in \(E\) that is already nontrivial for the first \(O(1)\) twists in almost every twist class.
- [SPECULATIVE] A second global theorem controlling twist-primitive classes directly in height order.
- [SPECULATIVE] A family-averaged Smith theorem over both \(E\) and \(d\), rather than a separate asymptotic for each fixed \(E\).

### 3.6 Bottom line for angle 3

- [ESTABLISHED] The formal twist decomposition is easy.
- [SPECULATIVE] The naive transfer from "0% in each twist family" to "0% in the whole height family" seems blocked for structural reasons, not only for lack of a uniform spectral gap.
- [SPECULATIVE] This is the strongest reason to doubt that Smith's theorem alone can be transferred into a \(100\%\)-BSD theorem for all curves ordered by height.

## 4. Related Work of Klagsbrun-Mazur-Rubin

### 4.1 What KMR prove

- [ESTABLISHED] Zev Klagsbrun, *Selmer ranks of quadratic twists of elliptic curves with partial rational two-torsion* (Transactions of the AMS 369 (2017), originally circulated in 2011) proves explicit parity results for \(2\)-Selmer ranks in quadratic-twist families and gives a formula for the density of even \(2\)-Selmer rank as a product of local factors.
- [ESTABLISHED] Zev Klagsbrun, Barry Mazur, and Karl Rubin, *A Markov model for Selmer ranks in families of twists* (2014), identify the universal Markov operator and the equilibrium distributions governing \(p\)-Selmer-rank statistics in suitably ordered twist families.
- [ESTABLISHED] The KMR abstract explicitly says that the equilibrium law depends only on the disparity, while the Markov process itself is independent of \(E\) and \(K\).

### 4.2 How close KMR get to the needed uniformity

- [ESTABLISHED] KMR give a conceptual mechanism that is already uniform at the model level.
- [ESTABLISHED] Their ordering is not the natural ordering by \(|d|\); it is built from fan structures and products of prime sets chosen to expose independence.
- [ESTABLISHED] Because of that, KMR do not by themselves provide the natural-order, all-\(E\), quantitative statement one would need for a height transfer.
- [ESTABLISHED] Smith's 2022 work can be viewed as a major upgrade here: it is precisely about converting the grid/fan technology into a theorem robust enough to handle higher Selmer layers and natural twist orderings.

### 4.3 Do KMR methods give effective rates?

- [ESTABLISHED] They are effective in principle at the level of the arithmetic inputs: the whole story is built from explicit local conditions plus effective counting/equidistribution over twisting primes.
- [ESTABLISHED] I did not locate in the accessible sources an explicit KMR theorem of the form "for every \(E\), the natural-order error term is at most \(F_E(D)\)."
- [ESTABLISHED] Therefore KMR do not currently supply the missing uniformity theorem for the Smith-transfer program.
- [SPECULATIVE] What KMR do supply is a roadmap: if one can make the arithmetic local equidistribution uniform over \(E\), the universal operator is already there.

### 4.4 A cautionary point from later work

- [ESTABLISHED] Smith 2025 shows that in balanced-isogeny cases the \(2\)-Selmer-rank distribution is not always the naive Poonen-Rains distribution.
- [ESTABLISHED] More recent work in the partial-two-torsion direction, such as Klagsbrun-Lemke Oliver on the distribution of \(2\)-Selmer ranks with partial two-torsion, also shows that \(2\)-Selmer-rank behavior can vary sharply with the base curve.
- [ESTABLISHED] So the right universal object is subtler than "the same \(2\)-Selmer rank law for every \(E\)." Smith's 2025 theorem succeeds by moving to \(2^\infty\)-Selmer corank and by using isogeny structure.

## 5. The Alternative Iwaniec-Sarnak Analytic Route

### 5.1 What the analytic route aims to prove

- [ESTABLISHED] The analytic route tries to show directly that for most curves, the central \(L\)-value or its first derivative does not vanish. Together with Gross-Zagier, Kolyvagin, and later \(p\)-converse results, this would force algebraic rank \(0\) or \(1\).
- [ESTABLISHED] Henryk Iwaniec and Peter Sarnak, *The non-vanishing of central values of automorphic \(L\)-functions and Landau-Siegel zeros* (announced 1998; widely cited through later expositions), prove a \(50\%\) nonvanishing result for central values in level-aspect families of holomorphic newforms with even functional equation.
- [ESTABLISHED] Their abstract also states that improving the \(50\%\) threshold in that setting is intimately connected to the Landau-Siegel-zero problem.

### 5.2 What is known closer to elliptic curves

- [ESTABLISHED] Friedberg-Hoffstein and Bump-Friedberg-Hoffstein prove positive-proportion nonvanishing theorems for twists and for derivatives of automorphic \(L\)-functions on \(\mathrm{GL}_2\).
- [ESTABLISHED] These results show that mollifier/amplification methods can force nonvanishing for a positive proportion of twists of a fixed modular form, hence of a fixed elliptic curve.
- [ESTABLISHED] They do not get anywhere close to "all but \(o(1)\)" in a height-ordered family of elliptic curves over \(\mathbf{Q}\).

### 5.3 Comparison with the Smith route

- [ESTABLISHED] Smith's route is algebraic and family-specific: fix \(E\), vary \(d\), and exploit local-global structure in Selmer groups.
- [ESTABLISHED] The analytic route is global and value-specific: it attacks \(L(E,1)\) or \(L'(E,1)\) directly.
- [ESTABLISHED] Smith's theorem is dramatically stronger than current analytic methods inside a single quadratic-twist family: it gives density \(0\) for rank \(\ge 2\) for every fixed base curve.
- [ESTABLISHED] Analytic methods, however, are better suited to handling curves that do not come from long twist orbits below a height cutoff, because they can in principle work directly in the global family ordered by conductor or height.

### 5.4 Could a hybrid be stronger?

- [SPECULATIVE] A hybrid is plausible in philosophy: use Smith to control long twist orbits, and use mollified first-moment or second-moment technology to control twist-primitive curves or the first few twists in each class.
- [SPECULATIVE] I do not know of any paper that turns this philosophy into a concrete theorem or even a sharply formulated program.
- [SPECULATIVE] The main obstacle is that the analytic route still struggles to move from "positive proportion" to "density \(1\)," especially for odd functional equation where one needs control of \(L'(E,1)\), not just \(L(E,1)\).
- [SPECULATIVE] So at present the hybrid route looks more like a long-term research direction than a near-term proof strategy.

## Assessment

### Feasibility rating

- [ESTABLISHED] Smith's fixed-family theorem is a major breakthrough and is exactly the right kind of algebraic input one would want for Goldfeld-type questions.
- [SPECULATIVE] As a direct route to "rank \(\ge 2\) has density \(0\) among all elliptic curves ordered by naive height," I rate the Smith-transfer program as **low feasibility in its current form**.
- [SPECULATIVE] As a component of a broader hybrid program combining fixed-family Selmer technology with genuinely height-global inputs, I rate it as **medium feasibility**.

### Why the direct transfer currently looks too weak

- [ESTABLISHED] No uniform natural-order convergence theorem over all \(E/\mathbf{Q}\) is presently available.
- [SPECULATIVE] Even if such a theorem were proved, a direct transfer still seems obstructed because many height-bounded curves belong to twist classes with only \(O(1)\) members below the same height bound.
- [SPECULATIVE] Therefore the slogan "uniform spectral gap implies \(100\%\) BSD" is too optimistic.

### What would materially change the picture

- [CONJECTURE / desired theorem] A theorem averaging Smith-type Selmer equidistribution simultaneously over the base curve \(E\) and the twisting parameter \(d\).
- [CONJECTURE / desired theorem] A direct global-height bound showing that twist-primitive curves with rank \(\ge 2\) already have density \(0\).
- [CONJECTURE / desired theorem] A much stronger analytic nonvanishing theorem for \(L(E,1)\) and \(L'(E,1)\) in the full height family.

## References

- Alexander Smith, *The Birch and Swinnerton-Dyer conjecture implies Goldfeld's conjecture*, arXiv:2503.17619, submitted March 22, 2025. https://arxiv.org/abs/2503.17619
- Alexander Smith, *The distribution of \(\ell^\infty\)-Selmer groups in degree \(\ell\) twist families I*, arXiv:2207.05674, first posted July 12, 2022. https://arxiv.org/abs/2207.05674
- Alexander Smith, papers page, listing the 2022 two-part Selmer project and the 2025 Goldfeld/BSD preprint. https://www.asmith-math.org/papers.html
- Zev Klagsbrun, Barry Mazur, and Karl Rubin, *A Markov model for Selmer ranks in families of twists*, Compositio Mathematica 150 (2014), 1077-1106. Cambridge abstract page: https://www.cambridge.org/core/journals/compositio-mathematica/article/a-markov-model-for-selmer-ranks-in-families-of-twists/S0010437X13007896
- Zev Klagsbrun, *Selmer ranks of quadratic twists of elliptic curves with partial rational two-torsion*, Transactions of the American Mathematical Society 369 (2017), 3355-3385.
- Henryk Iwaniec and Peter Sarnak, *The non-vanishing of central values of automorphic \(L\)-functions and Landau-Siegel zeros*. Rutgers summary page with abstract: https://www.researchwithrutgers.com/en/publications/the-non-vanishing-of-central-values-of-automorphic-l-functions-an
- Daniel Bump, Solomon Friedberg, and Jeffrey Hoffstein, *Nonvanishing theorems for \(L\)-functions of modular forms and their derivatives*, Inventiones Mathematicae 102 (1990), 543-618.
- Solomon Friedberg and Jeffrey Hoffstein, *Nonvanishing theorems for automorphic \(L\)-functions on \(\mathrm{GL}(2)\)*, Annals of Mathematics 142 (1995), 385-423.
