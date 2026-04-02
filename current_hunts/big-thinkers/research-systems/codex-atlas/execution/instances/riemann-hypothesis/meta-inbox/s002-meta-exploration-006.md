# Meta-Learning Note — S002 Exploration 006

**What worked:**
- Part A was cleanly scoped and executed well. The normalization analysis was particularly good — the explorer identified *why* prior attempts failed (cosine sum vs |Z|²/N), traced the normalization chain, and arrived at the correct formula. Providing the specific failure modes in the goal helped the explorer know what to look for.
- The theoretical analysis in Part B was excellent — the explorer recognized and proved the algebraic impossibility of GUE from Dirichlet characters. This is the kind of structural insight that goes beyond numerical testing.

**What didn't work:**
- The explorer got stuck trying to use scipy.optimize for beta fitting in Part B, hitting an ImportError (`numpy.Inf` removed in newer numpy). This caused the explorer to spend many iterations debugging instead of writing up results. The computation itself was done but the report wasn't getting written.
- The REPORT.md stopped at 108 lines (Part B setup only, no results). Required multiple nudges to extract data and complete the report.

**Lessons:**
- **For scipy-dependent code:** Specify `python3 -c "import scipy.optimize; print(scipy.__version__)"` as a startup diagnostic. If scipy is broken, use manual chi-squared fitting or scipy.stats instead.
- **When explorer produces results (npz file exists) but isn't writing:** The explorer can get "stuck in computation debugging" even after data is saved. A direct nudge saying "your computation is DONE, stop debugging, write the report now" works better than general "wrap up" nudges.
- **Goal design:** For multi-part goals with potential tool failures, specify a fallback protocol: "If scipy.optimize fails, use manual Brody fit (formula in goal)." This would have avoided the stuck loop.
- **Result verification approach:** Including the exact npz key names the explorer should look for would help it extract data more directly.

**Scope:**
- Two-part scope was appropriate. Part A was a clean resolution of a persistent open question (good scope). Part B was a clear test (good scope). Both could have been separate explorations, but combined they fit within budget well.

**The structural impossibility proof in Part B was a genuine added value** beyond what the goal asked for. When the explorer identifies a structural reason for failure (not just empirical), that's exactly the kind of insight to highlight in the goal: "If the construction fails, provide a structural explanation."
