# Migration Plan

## Goal

Retire `home-base/current_hunts/youtube/` and leave Research Radar as the only active path.

## Phases

1. Point the runner at `home-base/research-radar/pipelines/nightly-radar.sh`.
2. Verify that new runs write into `home-base/research-radar/data/topics/...`.
3. Verify transcripts, paper links, and summaries are landing in the new per-topic layout.
4. Delete `home-base/current_hunts/youtube/`.
5. Keep Research Radar as the only active YouTube collection path.

## Rule

There is now only one canonical YouTube collection location: `home-base/research-radar/`.
