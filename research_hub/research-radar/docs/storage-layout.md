# Storage Layout

Research Radar stores material in two layers.

## 1. Topic Overviews

Each topic has compact overview docs so the running knowledge base stays browsable.

Paths:

- `data/topics/<topic-slug>/overview.md`
- `data/topics/<topic-slug>/youtube/overview.md`
- `data/topics/<topic-slug>/papers/overview.md`
- `data/topics/<topic-slug>/summaries/overview.md`

## 2. Full Per-Item Files

Every collected or analyzed item gets its own full-detail file.

Paths:

- `data/topics/<topic-slug>/youtube/items/<item-id>.md`
- `data/topics/<topic-slug>/papers/items/<item-id>.md`
- `data/topics/<topic-slug>/summaries/items/<item-id>.md`

The intended contents are:

- YouTube item files: title, URL, channel, publish date, metadata, transcript status, full transcript text when available, notes
- Paper item files: title, URL, authors, abstract, publication info, PDF link when available, full text status, extracted text when available, notes
- Summary item files: concise summary, relevance score, why it matters now, presentation decision
