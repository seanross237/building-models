# Migration Plan

## Goal

Retire `[RETIRED] home-base/current_hunts/youtube/ (no longer exists)` and leave Research Radar as the only active path.

## Phases

1. Point the runner at `home-base/research_hub/research-radar/pipelines/nightly-radar.sh`.
2. Verify that new runs write into `home-base/research_hub/research-radar/data/topics/...`.
3. Verify transcripts, paper links, and summaries are landing in the new per-topic layout.
4. Delete `[RETIRED] home-base/current_hunts/youtube/ (no longer exists)`.
5. Keep Research Radar as the only active YouTube collection path.

## Rule

There is now only one canonical YouTube collection location: `home-base/research_hub/research-radar/`.
