Execute the full Strategizer role for Atlas mission "anatomy-of-averaged-ns-blowup-firewall", strategy "strategy-001".

Operational workdir:
- /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/anatomy-of-averaged-ns-blowup-firewall/strategies/strategy-001

Primary inputs:
- Strategy: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/anatomy-of-averaged-ns-blowup-firewall/strategies/strategy-001/STRATEGY.md
- Mission: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/anatomy-of-averaged-ns-blowup-firewall/MISSION.md
- Validation guide: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/anatomy-of-averaged-ns-blowup-firewall/MISSION-VALIDATION-GUIDE.md
- Prior strategies: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/anatomy-of-averaged-ns-blowup-firewall/strategies
- Computation registry: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/instances/anatomy-of-averaged-ns-blowup-firewall/COMPUTATIONS-FOR-LATER.md
- Shared library: /Users/seanross/kingdom_of_god/building_models/current_hunts/big-thinkers/codex-atlas/execution/agents/library

Required behavior:
- Run the strategizer loop until you produce FINAL-REPORT.md or hit a clear blocker.
- Keep state.json, LOOP-STATE.md, REASONING.md, and HISTORY-OF-REPORT-SUMMARIES.md synchronized with the work.
- Use $CODEX_ATLAS_ROOT/bin/run-role.sh for synchronous receptionist queries.
- Use $CODEX_ATLAS_ROOT/bin/launch-role.sh to launch explorers and curator runs.
- Use session names beginning with codex-atlas.
- For each explorer, set the sentinel file to REPORT-SUMMARY.md in that exploration directory.
- For curator runs, use a receipt file as the sentinel output.
- Stay entirely inside this repository.
