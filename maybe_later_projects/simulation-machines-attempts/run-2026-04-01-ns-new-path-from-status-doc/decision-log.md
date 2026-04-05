# Decision Log

## Cycle 1

- Action set:
  - extract the residual live frontier from the status memo
  - generate four candidate route families
  - down-rank any route that merely renames a closed lane
- Chosen action:
  choose the route family that most directly resolves the memo's
  "object-definition problem"
- Decision:
  `critical-element packet leakage rigidity` becomes the leading branch
- Reason:
  the memo already says the Tao frontier is blocked at object definition; the
  critical-element anchor is the cleanest way to reduce modeling freedom before
  asking for a firewall theorem

## Cycle 2

- Candidate actions considered:
  1. check whether critical-element/profile decomposition gives a canonical bad object
  2. check whether recent microlocal work offers natural packet observables
  3. test whether "newly phrased" partial regularity is actually new
  4. keep a plain packet-model route as backup
- Chosen action:
  combine actions 1 and 2 in the scoring model and prune action 3
- Decision:
  retain the leading route and reinterpret the microlocal program as a support
  tool rather than the main route
- Reason:
  this makes the proposed path sharper: the theorem target becomes leakage
  rigidity for a canonical near-minimal packet graph, not a vague global
  geometric regularity program

## Cycle 3

- Candidate actions considered:
  1. state the exact theorem object
  2. choose the preferred ambient critical space
  3. decide whether the route is regularity-facing or blowup-exclusion-facing
  4. formulate the novelty caveat
- Chosen action:
  state the route as a blowup-exclusion theorem inside a critical-element setup
- Decision:
  final answer is the theorem program below
- Reason:
  this route best respects all observed closures while still turning the Tao
  mechanism into something exact-NS could plausibly forbid

## Final Theorem Program Chosen

1. Assume a minimal singular solution exists in a critical space such as `L^3`
   or a nearby critical Besov setting.
2. Use profile decomposition and compactness to obtain a canonical minimal bad
   object.
3. Define packet variables on that object by a fixed phase-space extraction rule
   rather than by ad hoc engineering choices.
4. Build the induced triadic transfer graph and identify whether any Tao-like
   five-role delayed-threshold near-circuit is present.
5. Prove exact NS forces either:
   - a positive lower bound on spectator leakage, or
   - a positive lower bound on angular spreading / entropy growth,
   at every scale where such a circuit would need to persist.
6. Conclude that the minimal singular object cannot realize the Tao-style
   isolated gate logic.
7. Use that exclusion as a firewall against the Tao-type blowup mechanism in
   exact NS.
