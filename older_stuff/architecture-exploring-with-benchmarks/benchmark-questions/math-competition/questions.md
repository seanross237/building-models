# Math Competition Benchmark — 14 Hard Problems

Source: Publicly available competition problems from AIME (MAA), Putnam, and IMO.
Curated for AI benchmarking: all require multi-step reasoning, have exact verifiable answers,
and are drawn from the hardest tiers of their respective competitions.

**Purpose:** Problems where a naive "just solve it" approach fails. Structured reasoning
(planning, decomposition, critic loops, multi-agent) should outperform single-shot attempts.

**Format:** All AIME answers are integers 000-999. Other answers are exact values.

---

## MATH-01: Isoperimetric Tetrahedron Insphere
**Source:** 2024 AIME I, Problem 14
**Category:** Geometry (3D)
**Difficulty:** AIME-hard (#14)
**Answer type:** exactMatch (integer)
**Answer:** 104

Let $ABCD$ be a tetrahedron such that $AB = CD = \sqrt{41}$, $AC = BD = \sqrt{80}$, and $BC = AD = \sqrt{89}$. There exists a point $I$ inside the tetrahedron such that the distances from $I$ to each of the faces of the tetrahedron are all equal. This distance can be written in the form $\frac{m\sqrt{n}}{p}$, where $m$, $n$, and $p$ are positive integers, $m$ and $p$ are relatively prime, and $n$ is not divisible by the square of any prime. Find $m + n + p$.

---

## MATH-02: Sphere Containing All Boxes
**Source:** 2024 AIME I, Problem 15
**Category:** Algebra / Optimization
**Difficulty:** AIME-hard (#15)
**Answer type:** exactMatch (integer)
**Answer:** 721

Let $\mathcal{B}$ be the set of rectangular boxes with surface area $54$ and volume $23$. Let $r$ be the radius of the smallest sphere that can contain each of the rectangular boxes that are elements of $\mathcal{B}$. The value of $r^2$ can be written as $\frac{p}{q}$, where $p$ and $q$ are relatively prime positive integers. Find $p + q$.

---

## MATH-03: Fourth Power Divisibility
**Source:** 2024 AIME I, Problem 13
**Category:** Number Theory
**Difficulty:** AIME-hard (#13)
**Answer type:** exactMatch (integer)
**Answer:** 110

Let $p$ be the least prime number for which there exists a positive integer $n$ such that $n^4 + 1$ is divisible by $p^2$. Find the least positive integer $m$ such that $m^4 + 1$ is divisible by $p^2$.

---

## MATH-04: Octagon Rotation Probability
**Source:** 2024 AIME I, Problem 11
**Category:** Combinatorics / Probability
**Difficulty:** AIME-hard (#11)
**Answer type:** exactMatch (integer)
**Answer:** 371

Each vertex of a regular octagon is independently colored either red or blue with equal probability. The probability that the octagon can then be rotated so that all of the blue vertices end up at positions where there had been red vertices is $\frac{m}{n}$, where $m$ and $n$ are relatively prime positive integers. Find $m + n$.

---

## MATH-05: Nested Absolute Value Intersections
**Source:** 2024 AIME I, Problem 12
**Category:** Analysis / Algebra
**Difficulty:** AIME-hard (#12)
**Answer type:** exactMatch (integer)
**Answer:** 385

Define $f(x) = \left| |x| - \frac{1}{2} \right|$ and $g(x) = \left| |x| - \frac{1}{4} \right|$. Find the number of intersections of the graphs of $y = 4g(f(\sin(2\pi x)))$ and $x = 4g(f(\cos(3\pi y)))$.

---

## MATH-06: b-eautiful Numbers
**Source:** 2024 AIME II, Problem 14
**Category:** Number Theory / Algebra
**Difficulty:** AIME-hard (#14)
**Answer type:** exactMatch (integer)
**Answer:** 150

Let $b \ge 2$ be an integer. Call a positive integer $n$ *$b$-eautiful* if it has exactly two digits when expressed in base $b$ and these two digits sum to $\sqrt{n}$. For example, $81$ is $13$-eautiful because $81 = \underline{6} \cdot 13 + \underline{3}$ and $6 + 3 = \sqrt{81}$. Find the least integer $b \ge 2$ for which there are more than ten $b$-eautiful integers.

---

## MATH-07: Rectangles in a Dodecagon
**Source:** 2024 AIME II, Problem 15
**Category:** Combinatorics / Geometry
**Difficulty:** AIME-hard (#15)
**Answer type:** exactMatch (integer)
**Answer:** 315

Find the number of rectangles that can be formed inside a fixed regular dodecagon ($12$-gon) where each side of the rectangle lies on either a side or a diagonal of the dodecagon.

---

## MATH-08: Expected Regions from Random Chords
**Source:** 2025 AIME I, Problem 13
**Category:** Combinatorics / Probability
**Difficulty:** AIME-hard (#13)
**Answer type:** exactMatch (integer)
**Answer:** 204

Alex divides a disk into four quadrants with two perpendicular diameters intersecting at the center of the disk. He draws $25$ more line segments through the disk, drawing each segment by selecting two points at random on the perimeter of the disk in different quadrants and connecting these two points. Find the expected number of regions into which these $27$ line segments divide the disk.

---

## MATH-09: Fermat Point of a Pentagon
**Source:** 2025 AIME I, Problem 14
**Category:** Geometry / Optimization
**Difficulty:** AIME-hard (#14)
**Answer type:** exactMatch (integer)
**Answer:** 060

Let $ABCDE$ be a convex pentagon with $AB = 14$, $BC = 7$, $CD = 24$, $DE = 13$, $EA = 26$, and $\angle B = \angle E = 60°$. For each point $X$ in the plane, define $f(X) = AX + BX + CX + DX + EX$. The least possible value of $f(X)$ can be expressed as $m + n\sqrt{p}$, where $m$ and $n$ are positive integers and $p$ is not divisible by the square of any prime. Find $m + n + p$.

---

## MATH-10: Counting Triples Mod 3
**Source:** 2025 AIME I, Problem 15
**Category:** Number Theory / Combinatorics
**Difficulty:** AIME-hard (#15)
**Answer type:** exactMatch (integer)
**Answer:** 735

Let $N$ denote the number of ordered triples of positive integers $(a, b, c)$ such that $a, b, c \le 3^{333}$ and $a + b + c$ is a multiple of $3$. Find the remainder when $N$ is divided by $1000$.

---

## MATH-11: Surjective Clock Sequences
**Source:** 2023 AIME I, Problem 14
**Category:** Combinatorics
**Difficulty:** AIME-hard (#14)
**Answer type:** exactMatch (integer)
**Answer:** 608

An analog clock has two hands that can move independently of each other. Initially, both hands point to the number $12$. The clock performs a sequence of hand movements so that on each movement, one of the two hands moves clockwise to the next number on the clock face while the other hand does not move.

Let $N$ be the number of sequences of $144$ hand movements such that during the sequence, every possible positioning of the hands appears exactly once, and at the end of the $144$ movements, the hands have returned to their initial position. Find the remainder when $N$ is divided by $1000$.

---

## MATH-12: Complex Number Triangle
**Source:** 2023 AIME I, Problem 15
**Category:** Algebra / Number Theory / Geometry
**Difficulty:** AIME-hard (#15)
**Answer type:** exactMatch (integer)
**Answer:** 349

Find the largest prime number $p < 1000$ such that there exists a complex number $z$ satisfying:
- the real and imaginary parts of $z$ are both integers,
- $|z| = \sqrt{p}$, and
- there exists a triangle whose three side lengths are $p$, the real part of $z^3$, and the imaginary part of $z^3$.

---

## MATH-13: Binary Ones in a Product
**Source:** 2023 Putnam B2
**Category:** Number Theory
**Difficulty:** Putnam-easy (B2)
**Answer type:** exactMatch (integer)
**Answer:** 3

For each positive integer $n$, let $k(n)$ denote the number of ones in the binary representation of $2023 \cdot n$. What is the minimum value of $k(n)$?

---

## MATH-14: Diophantine Equation with Factorial
**Source:** IMO 2022, Problem 5
**Category:** Number Theory
**Difficulty:** IMO (Problem 5)
**Answer type:** exactMatch (enumerated pairs)
**Answer:** (2, 2, 2) and (3, 4, 3)

Find all triples $(a, b, p)$ of positive integers with $p$ prime and
$$a^p = b! + p.$$
