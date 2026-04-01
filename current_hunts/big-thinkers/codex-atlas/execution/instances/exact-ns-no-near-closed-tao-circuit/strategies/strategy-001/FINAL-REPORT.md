# Final Report: Strategy 001

## Executive Verdict

```text
definition-level negative
```

[CHECKED] A testable exact object was found at Phase 0, but it did not survive the first exact-support audit.

[COMPUTED] The sharp singleton-support version of a near-closed Tao circuit is already false: the two desired `a1^2` channels force roles 2 and 3 onto the same conjugate wavevector pair, after which the amplifier `a2 a3 -> a3` cannot satisfy exact triad closure for any sign choice.

[CHECKED] The only surviving replacement is a packetized backup, but that object is not canonical enough to count as one theorem-facing exact-NS target. It depends on packet support choice, projection choice, leakage scalarization, and exact-network restoration conventions.

So the mission ends at outcome 3 from the strategy brief:

```text
the near-closed Tao circuit idea does not survive as one precise exact-NS object
```

## Directions Tried

### 1. Phase 0 definition gate

[CHECKED] Exploration 001 succeeded. It sharpened the mission object into a five-role helical-mode directed hypergraph with a coefficient-weighted leakage functional and delayed-trigger windows. This showed that the idea does not fail immediately as a slogan.

### 2. Exact interaction audit on the preferred exact object

[COMPUTED] Exploration 002 killed the preferred singleton-support version before coefficient or leakage analysis. The exact triad-closure constraints imply:

- `a1^2 -> a2` forces `k2 = ± 2k1`,
- `a1^2 -> a3` forces `k3 = ± 2k1`,
- hence roles 2 and 3 occupy the same conjugate wavevector pair,
- and then `a2 a3 -> a3` has no exact triad realization for any conjugate-sign choice.

[CHECKED] This is a stronger obstruction than the original spectator-coupling story. The cleanest failure is non-embeddability of the target monomial pattern on singleton exact supports.

### 3. Refine-or-stop test on the packetized backup

[CHECKED] Exploration 003 asked whether the packetized backup could replace the failed singleton object as one canonical exact-channel table.

[CHECKED] It could not. Once packetization is introduced, the object depends on extra choices not fixed by exact NS:

- which exact modes belong to each packet,
- how packet roles are projected or coordinatized,
- how desired channels are separated from internal packet cross-terms,
- how leakage is measured after restoring the full exact network.

That means the backup is not one exact object but a family of engineering choices.

## Strongest Findings

1. [VERIFIED] Tao's mechanism remains the right reference object: a five-role delayed-trigger circuit is the load-bearing structure to compare against exact NS.
2. [COMPUTED] The most precise exact singleton-mode version of that circuit is statically impossible.
3. [CHECKED] The remaining packetized versions are too underconstrained to serve as one mission object without a new canonical packet model.

## Negative Results and Dead Ends

- [COMPUTED] The preferred singleton-support object dies before any coefficient-ratio or leakage lower-bound computation.
- [CHECKED] Helicity/sign adversarial checks do not rescue the singleton object, because they do not change triad-closure geometry.
- [CHECKED] The packetized backup does not rescue the mission in its current form; it moves the ambiguity into packet support, projection, and leakage bookkeeping.

## Recommended Next Move For The Missionary

[CHECKED] Stop this line as currently posed.

[CHECKED] Only reopen it under a differently framed mission whose primary job is:

```text
invent and defend a canonical exact packet model for Tao-like circuit roles
before asking any obstruction/construction question
```

[CHECKED] Without that, further work would not be testing one object. It would be designing the object ad hoc while simultaneously trying to prove things about it.

## Claims Worth Carrying Forward

- [COMPUTED] The singleton exact-mode Tao-circuit object is false for structural wavevector reasons, not merely because leakage looks large.
- [CHECKED] Any future "near-closed Tao circuit" mission must start by fixing a canonical packet model, not by treating packetization as a fallback after singleton failure.
- [CHECKED] The original firewall slogan sharpens into a stronger negative: the crisp exact version dies, and the flexible replacement loses object-level precision.
