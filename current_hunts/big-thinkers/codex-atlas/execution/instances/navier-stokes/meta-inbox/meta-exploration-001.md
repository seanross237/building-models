# Meta-Learning: Exploration 001 (NS Inequality Catalog)

## What Worked Well
- **Named specific targets + "find more"**: Listing 7 inequality families (A-G) plus specific authors gave the explorer a clear search structure while leaving room for discovery. It found 17 entries, exceeding the minimum 8.
- **Tao classification requirement**: Asking for generic vs. NS-specific classification on each inequality produced the most valuable structural insight — the realization that generic inequalities cannot prove regularity (per Tao 2016) focuses all future work on NS-specific estimates.
- **Table format + detailed entries**: The two-level format (master table + detailed entries) produced both scannable overview and deep precision.
- **Incremental writing instruction**: The "write section by section" instruction appears to have worked — the report is complete with no [INCOMPLETE] markers.
- **Divergent survey pattern**: Part 5 (Next Steps Recommendation) with ranked slack estimates is the most actionable output.

## What Could Be Improved
- **Agmon inequality ambiguity**: The explorer flagged genuine ambiguity about Agmon's inequality in 3D (some sources state the 2D version for 3D). This is useful but the explorer didn't fully resolve it. Future explorations should ask: "If there is ambiguity, state BOTH versions and which papers use which."
- **Scaling analysis was hand-wavy in places**: Some scaling estimates (e.g., F1 scaling behavior) involved rough dimensional arguments rather than precise Re-dependence. The math explorer should compute these precisely.
- **No Strichartz estimates**: The explorer noted these in "potentially missing" but didn't catalog them. Not clear if they're truly load-bearing in the classical regularity arguments.

## Lessons for Future Goal Design
- For comprehensive surveys: 6-7 named families + explicit output format + "find more" works well. No need to split into multiple explorations.
- The Tao classification turned out to be the most strategically important feature — always include a structural classification requirement when cataloging.
- Standard explorer is correct choice for literature survey — produces excellent coverage without computation overhead.
