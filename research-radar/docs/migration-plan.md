# Migration Plan

## Goal

Retire `home-base/current_hunts/youtube/` once Research Radar is actually handling the flow.

## Phases

1. Keep the old YouTube folder as a temporary legacy source while the new structure is being wired.
2. Point the runner at `home-base/research-radar/pipelines/nightly-radar.sh`.
3. Verify that new runs write into `home-base/research-radar/data/topics/...`.
4. Verify transcripts, paper links, and summaries are landing in the new per-topic layout.
5. After the new path is trusted, delete `home-base/current_hunts/youtube/`.

## Rule

There should only be one canonical YouTube collection location once the new system is working.
