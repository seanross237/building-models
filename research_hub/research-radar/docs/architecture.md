# Research Radar Architecture

## Goal

Research Radar is the continuous intake and triage layer for home-base.

It should:

1. Collect fresh YouTube videos for the topics we care about.
2. Collect transcripts for those videos.
3. Collect new research papers for those topics.
4. Analyze each item against `config/what-we-care-about-right-now.md`.
5. Queue only the highest-relevance items for presentation generation.

## Source Of Truth

`research-radar/` is the source of truth for:

- config
- runner code
- collection pipelines
- analysis prompts
- operational docs
- collected data and queues

`home-base/presentation_hub/` remains the publish target for decks.

## High-Level Flow

1. Railway task runs `pipelines/nightly-radar.sh`
2. Nightly pipeline runs collectors
3. Collectors write normalized items into `data/items/`
4. Analyzers write summaries and scores into `data/analyses/`
5. Relevance `>= 9` goes into `data/queues/presentation-candidates/`
6. Presentation generator writes compliant folders into `home-base/presentation_hub/`

## System Boundaries

- Collection is broad and topic-driven.
- Scoring is narrower and driven by the current Eywa focus.
- Atlas-style research systems are included because they are highly informative for Eywa.
