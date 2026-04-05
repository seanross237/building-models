# Exploration 005: Close sum_S >= 0 via Polarization and Correction Bound

## Mission Context

We are one step from completing the Yang-Mills mass gap proof. The ENTIRE proof reduces to:

**sum_S(R, D, T) >= 0** for all R_mu, D_{mu,nu} in SO(3), T with sum T_mu = 0.

## What's Already Proved

### Master Identity [E004, VERIFIED to 7.1e-14]
sum_S(R, D, T) = baseline(R, T) + sum_{mu<nu} 2 u_{mu,nu}^T (I-D_{mu,nu}) v_{mu,nu}

where:
- **baseline = 6*sum_mu f(R_mu, T_mu) + |sum_mu R_mu^T T_mu|^2 >= 0** [PROVED, manifestly non-negative]
- **u_{mu,nu} = R_mu^T T_mu - T_nu**
- **v_{mu,nu} = T_mu - R_nu^T T_nu**
- **E = I - D_{mu,nu}** (note: E is PSD since D in SO(3) implies eigenvalues of D on unit circle, so eigenvalues of I-D >= 0)

Wait — is I-D PSD for D in SO(3)? For D a rotation by angle theta around axis n:
D = cos(theta) I + (1-cos(theta)) n n^T + sin(theta) [n]_x
I - D = (1-cos(theta))(I - n n^T) - sin(theta) [n]_x

The symmetric part of I-D is (1-cos(theta))(I - n n^T) which is PSD (eigenvalues 0, 1-cos(theta), 1-cos(theta) >= 0). So the SYMMETRIC part of E is PSD.

For any p: p^T E p = p^T (I-D) p = p^T [symmetric part of I-D] p >= 0. This is f(D,p) >= 0 which we already know.

But for the BILINEAR form u^T E v: this involves the full E (including antisymmetric part). So u^T E v can be negative even though u^T E u >= 0.

### Critical T Theorem [E004, PROVED]
For T_mu = c_mu * axis(R_mu) with sum c_mu axis(R_mu) = 0: u = v, so sum Delta = sum 2f(D,u) >= 0. Proof works perfectly.

### Numerical Evidence [E004, COMPUTED]
67K adversarial tests, min eigenvalue = 3.9e-13 ≈ 0 (tight at D = I). Zero violations.

## Your Task: Prove sum_S >= 0

### KEY APPROACH: Polarization Identity

The bilinear form u^T E v can be controlled via the polarization identity:

u^T E v = (1/2)[(u+v)^T E (u+v) - u^T E u - v^T E v]

Since f(D, p) = p^T(I-D)p = p^T E_sym p >= 0:
u^T E u = 2f(D, u) >= 0 (this is the quadratic form in u only — uses symmetric part)
v^T E v = 2f(D, v) >= 0

Wait — there's a subtlety. u^T E v = u^T (I-D) v. The quadratic form u^T(I-D)u = f(D,u) (NOT 2f(D,u) — check convention!). Actually f(D,p) = p^T(I-D)p. So yes, u^T E u = f(D,u).

Polarization: u^T E v = (1/2)[(u+v)^T E (u+v) - u^T E u - v^T E v] = (1/2)[f(D,u+v) - f(D,u) - f(D,v)]

Since f(D,p) >= 0 for all p:
u^T E v >= -(1/2)[f(D,u) + f(D,v)]

This gives a LOWER BOUND:
sum Delta = sum_{mu<nu} 2 u^T E v >= -sum_{mu<nu} [f(D,u) + f(D,v)]

Therefore:
sum_S >= baseline - sum_{mu<nu} [f(D_{mu,nu}, u_{mu,nu}) + f(D_{mu,nu}, v_{mu,nu})]

### Stage 1: Verify the Polarization Lower Bound

NUMERICALLY verify for 500+ (R, D, T) triples:
1. Compute sum_S directly
2. Compute baseline - sum [f(D,u) + f(D,v)]
3. Verify that sum_S >= baseline - sum [f(D,u) + f(D,v)] (should hold by construction)
4. Check: is baseline - sum [f(D,u) + f(D,v)] >= 0? (If yes, PROOF IS DONE!)

If step 4 fails, compute the RATIO: when does the lower bound go negative? How negative?

### Stage 2: Bound f(D,u) and f(D,v) in terms of baseline

f(D, u_{mu,nu}) = f(D, R_mu^T T_mu - T_nu). Since f(D,p) <= 2||p||^2 (max of 1-cos(theta) is 2):
f(D, u) <= 2||u||^2 = 2|R_mu^T T_mu - T_nu|^2 = 2(|T_mu|^2 + |T_nu|^2 - 2 T_mu^T R_mu T_nu)
= 2(|T_mu|^2 + |T_nu|^2 - 2T_mu^T R_mu T_nu)

Note: T_mu^T R_mu T_nu = T_mu^T T_nu + T_mu^T(R_mu - I)T_nu, and T_mu^T(R_mu - I)T_nu is bounded.

Also: ||u||^2 = |T_mu|^2 + |T_nu|^2 - 2 T_mu^T R_mu T_nu
= 2(|T_mu|^2 + |T_nu|^2)/2 - 2 T_mu^T R_mu T_nu
<= 2(|T_mu|^2 + |T_nu|^2) (since T_mu^T R_mu T_nu >= -|T_mu||T_nu|)

And sum_{mu<nu} ||u||^2 = sum_{mu<nu} [|T_mu|^2 + |T_nu|^2 - 2 T_mu^T R_mu T_nu]
= 3*sum|T_mu|^2 - 2 sum_{mu<nu} T_mu^T R_mu T_nu
= 3||T||^2 - 2 sum_{mu<nu} T_mu^T R_mu T_nu

The baseline has 6*sum f(R_mu, T_mu) = 6*sum(|T_mu|^2 - T_mu^T R_mu T_mu) = 6||T||^2 - 6 sum T_mu^T R_mu T_mu.

Can we show: 6*sum f(R_mu, T_mu) >= 2*sum_{mu<nu} ||u||^2? (factor 2 from the f(D,u) <= 2||u||^2 bound)

That would require: 6||T||^2 - 6 sum T_mu^T R_mu T_mu >= 2[6||T||^2 - 2 sum T_mu^T R_mu T_nu + additional]... this gets messy.

### Stage 3: Alternative — Tighter Bound via Cauchy-Schwarz

Instead of the crude f(D,u) <= 2||u||^2, use the actual D-dependent bound:

u^T E v = u^T E_sym v + u^T E_anti v

where E_sym = (I-D+I-D^T)/2 = I - (D+D^T)/2 (PSD) and E_anti = (D^T-D)/2 (antisymmetric).

The antisymmetric part: u^T E_anti v = -v^T E_anti u. For antisymmetric E_anti, |u^T E_anti v| <= ||E_anti|| * ||u|| * ||v||. And ||E_anti|| = |sin(theta)| <= 1.

The symmetric part: u^T E_sym v = (1/2)[f(D,u+v) - f(D,u) - f(D,v)] (from polarization, using symmetric part only).

Actually, since f(D,p) = p^T E_sym p (the antisymmetric part vanishes in quadratic form):
u^T E_sym v = (1/2)[f(D,u+v) - f(D,u) - f(D,v)] (standard polarization)

And by C-S for the PSD form: |u^T E_sym v| <= sqrt(f(D,u)) * sqrt(f(D,v))

So: |u^T E v| <= |u^T E_sym v| + |u^T E_anti v| <= sqrt(f(D,u)*f(D,v)) + |sin(theta)| * ||u|| * ||v||

This gives a TIGHTER bound. Check if the baseline absorbs this.

### Stage 4: Direct Writing as Sum of Squares

Try a completely different approach: write sum_S directly as a sum of squared norms.

sum_S = sum_{mu<nu} S_{mu,nu} where:
S_{mu,nu} = 2f(U,T_mu) + 2f(W,T_nu) - 2T_mu^T(2I - D^T - R_mu D R_nu^T)T_nu

Can we find vectors a_k(R, D, T) such that sum_S = sum_k ||a_k||^2?

At D=I, we found sum_S = 6*sum f(R,T) + |sum R^T T|^2 = sum of 4 squared norms (f(R,T) = ||(I-R^T)T_mu||^2/2 and |sum R^T T|^2). These squared norms vanish when T on axes.

For D != I, the Delta terms add 2f(D,u) per plaquette (on axes). Can we write sum_S as:
[sum of D=I squared norms] + [sum of D-dependent squared norms] + [cross terms that cancel]?

### Stage 5: Block Schur Complement

The 9x9 sum_S matrix M_S has a 3x3 block structure (3 blocks of 3, indexed by spatial constraint s_0, s_1, s_2 after eliminating s_3 = -s_0-s_1-s_2). Try:

M_S = [A B; B^T C] and show A >= 0, C >= 0, and A - B C^{-1} B^T >= 0 (Schur complement). Or equivalently, det(M_S) >= 0 by minors.

## Success Criteria

- **Full success**: Algebraic proof of sum_S >= 0. Completes the entire Yang-Mills mass gap proof.
- **Partial success**: Proof that baseline >= sum[f(D,u) + f(D,v)] (which implies sum_S >= 0 via polarization).
- **Failure with value**: Precise characterization of which bound is too loose and by how much.

## Dead Ends

- LEMMA_D, LEMMA_RDR individually: FALSE
- Per-plaquette bounds: FALSE
- Convexity in D: FAILS
- Per-plaquette VCBL: rank obstruction
- Eigenvalue perturbation: ratio too large
- Gershgorin: too loose

## Output

Write results to REPORT.md (max 250 lines) and REPORT-SUMMARY.md. Write incrementally after each stage.
