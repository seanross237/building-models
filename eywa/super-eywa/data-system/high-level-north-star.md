# Data System — High-Level North Star

The data-system is the truth-preserving and evaluation layer around Eywa.

Its north star is a system that:

- preserves enough truth from every run that the run can later be understood and reconstructed
- keeps grading separate from correctness
- organizes questions, runs, scores, and replay artifacts cleanly
- makes later Bonsai learning possible without redesigning the storage foundation

The data-system should not just be a pile of logs.

It should preserve canonical truth first, then support simpler and richer derived views on top of that truth.

In the long run, it should make it easy to answer questions like:

- what task was attempted?
- what variables were used?
- what happened at each node?
- how well did the run do?
- what similar runs already exist?
