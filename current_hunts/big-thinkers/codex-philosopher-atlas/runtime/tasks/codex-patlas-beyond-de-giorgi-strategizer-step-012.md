Execute the Strategizer role for the copied mission step below.

- Mission: beyond-de-giorgi
- Step: step-012
- Operational workdir: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-012
- Primary input: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/steps/step-012/GOAL.md
- Mission chain context: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/CHAIN.md
- Chain history: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/missions/beyond-de-giorgi/CHAIN-HISTORY.md
- Local library root: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-philosopher-atlas/library

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
