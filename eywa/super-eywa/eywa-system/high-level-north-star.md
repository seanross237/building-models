# Eywa System — High-Level North Star

Eywa is the task-solving runtime inside Super-Eywa.

Its north star is a runtime where:

- the stable unit is the node
- every node is fundamentally the same kind of thing
- the main behavioral flexibility lives in explicit variables
- runs stay reconstructable and human-readable
- the runtime is graph-capable without becoming confusing

At the deepest level, Eywa should become a machine where:

- a task enters
- a root node starts
- same-DNA nodes work on the problem
- nodes emit results and structured follow-up outputs
- the system records enough truth that the run can later be understood and learned from

Eywa should be built so that the important run-to-run changes happen mainly through variables, not through hidden behavior spread across the runtime.

The goal is a strong, inspectable set of bones that can support later Bonsai learning.
