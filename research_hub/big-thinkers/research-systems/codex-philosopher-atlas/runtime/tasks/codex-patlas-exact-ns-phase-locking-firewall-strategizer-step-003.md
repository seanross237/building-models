Execute the Strategizer role for the copied mission step below.

- Mission: exact-ns-phase-locking-firewall
- Step: step-003
- Operational workdir: /Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-003
- Primary input: /Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/steps/step-003/GOAL.md
- Mission chain context: /Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/CHAIN.md
- Chain history: /Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/missions/exact-ns-phase-locking-firewall/CHAIN-HISTORY.md
- Local library root: /Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/codex-philosopher-atlas/library

Required behavior:
- Run the full strategizer loop for this step until you either complete the step or hit a clear blocker.
- Write or update RESULTS.md in the step directory before finishing.
- Keep state.json, REASONING.md, and HISTORY-OF-REPORT-SUMMARIES.md in sync with the work you do.
- Use $CODEX_PATLAS_ROOT/bin/run-role.sh for synchronous receptionist queries.
- Use $CODEX_PATLAS_ROOT/bin/launch-role.sh to launch explorers and curator sessions.
- Use session names beginning with codex-patlas.
- For each explorer, set the sentinel file to that exploration's REPORT-SUMMARY.md.
- For curator runs, set the sentinel file to the expected library/meta output you just created or updated.
- Do not read or write anything outside this repository.
