# Research Radar Operations

## Canonical Config

- `config/topics-we-care-about.yaml`
- `config/what-we-care-about-right-now.md`
- `config/thresholds.yaml`

These files should be edited before changing live Supabase task definitions.

## Nightly Entry Point

- `pipelines/nightly-radar.sh`

The Railway task should call this script, not a long inline shell command.

## Data Layout

- `data/topics/<topic-slug>/youtube/overview.md` for topic-level YouTube summaries
- `data/topics/<topic-slug>/youtube/items/` for full per-video files
- `data/topics/<topic-slug>/papers/overview.md` for topic-level paper summaries
- `data/topics/<topic-slug>/papers/items/` for full per-paper files
- `data/topics/<topic-slug>/summaries/overview.md` for topic-level analyzed takeaways
- `data/topics/<topic-slug>/summaries/items/` for full per-item analysis files
- `data/queues/presentation-candidates/` for items with relevance at or above threshold
- `data/queues/published/` for items already turned into decks

## Presentations

Presentations must be written into `home-base/presentations/` and must follow:

- `/Users/seanross/kingdom_of_god/home-base/presentations/guide_presentations.md`

## Runner

The local copy of the Railway service lives under:

- `runner/agent-runner/`

Supabase task rows should stay thin. Repo config should remain canonical.
## Migration Note

Keep `home-base/current_hunts/youtube/` only as a temporary legacy source while Research Radar is being verified.
Once the new nightly path is running correctly and writing into `home-base/research-radar/`, remove the old `current_hunts/youtube/` folder so there is only one canonical YouTube collection location.

