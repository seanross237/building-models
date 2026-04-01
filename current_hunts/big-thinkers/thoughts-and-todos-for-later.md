# Thoughts and TODOs for Later

## Multi-model support via OpenRouter

Run alternative models (Kimi K2.5, Grok 4.1, etc.) as Atlas explorers through OpenRouter while keeping the strategizer and missionary on Opus. Claude Code stays the same app — only the remote model brain is swapped. No Atlas code changes needed; just swap which binary launches explorer sessions in operator.sh.

Full setup guide: `docs_and_guides/openrouter-multi-model-guide.md`

Key considerations:
- Data sent to the model goes to that provider's servers (e.g., Moonshot for Kimi = China-based)
- Tool use compatibility varies by model — must test before real missions
- Best use case: cheap models for literature survey explorations, keep Opus for math
- `clauo` wrapper script already created at `~/.local/bin/clauo` (needs OpenRouter API key in env)

## System to review new claims and findings and mark them as verified

The Vasseur pressure mission revealed that a hallucinated citation ("Tran-Yu 2014 AIHP") was embedded in a mission document written by a previous agent. It was plausible enough to survive into the next mission's planning. The patlas Step 0 orientation caught it, but only because the wide funnel plan specifically included a verification task.

**Need:** A systematic process where new claims, citations, and findings produced by any agent are independently verified before they become trusted inputs to future work. Claims should be tagged with verification status (e.g., VERIFIED, UNVERIFIED, HALLUCINATION-RISK) so downstream agents know what to trust.

Things to think about:
- When should verification happen? (At report time? At library curation? At mission doc creation?)
- Who verifies? (A dedicated verifier agent? The curator? A separate pass?)
- What gets verified? (All citations? Only novel claims? Only things that feed into future missions?)
- How do we handle the cost? (Verifying everything is expensive; verifying nothing lets hallucinations propagate)
