# Atlas Morning Briefing — Presentation Generator Prompt

You are generating a single-file HTML presentation for an Atlas mission briefing. This is a morning summary of what a multi-agent research system (codex-atlas) investigated overnight and what it found.

This is NOT a radar presentation about what was detected — this is about what Atlas **investigated and concluded**.

## Your task

Generate a complete, self-contained `presentation.html` file. Output ONLY the raw HTML — no markdown fences, no commentary, no explanation. The entire response must be valid HTML that can be saved directly as a file and opened in a browser.

## Visual style (MANDATORY)

- Dark page background: `--bg: #0d1117`
- Light slide cards with strong contrast and separation (white/off-white cards on dark background)
- Sparse text, visually engaging, color-coded tags, stat boxes
- Each slide should feel different from the last — mix up layout, use cards, stat boxes, tags, flow diagrams
- Never hit the reader with a wall of text. Keep slides scannable with headlines, labels, small cards
- If detail is needed, put it behind a `<details><summary>` collapsed by default

## CSS variables (use these exact values)

```css
:root {
  --bg: #0d1117;
  --slide-bg: #f8f9fa;
  --slide-border: #e1e4e8;
  --text: #1f2937;
  --muted: #6b7280;
  --accent: #4f46e5;
  --accent-light: #eef2ff;
  --green: #059669;
  --green-light: #ecfdf5;
  --red: #dc2626;
  --red-light: #fef2f2;
  --amber: #d97706;
  --amber-light: #fffbeb;
  --blue: #2563eb;
  --blue-light: #eff6ff;
  --teal: #0d9488;
  --teal-light: #f0fdfa;
  --purple: #7c3aed;
  --purple-light: #f5f3ff;
}
```

## Required CSS classes

Use these exact class names (they are the design system):

- `.slide`, `.slide.active` — slide containers; only `.active` is visible
- `.nav`, `.nav-btn`, `.nav-counter` — fixed bottom navigation bar
- `.card`, `.card-header`, `.card-num`, `.card-title`, `.card-desc` — content cards
- `.stats`, `.stats-2`, `.stats-3` — stat box grids (2-col, 3-col)
- `.stat`, `.stat-value`, `.stat-label` — individual stat boxes
- `.tag` with variants: `.tag-green`, `.tag-red`, `.tag-amber`, `.tag-blue`, `.tag-accent`, `.tag-teal`, `.tag-purple`
- `.toc-item`, `.toc-num`, `.toc-text` — table of contents items (clickable, with onclick="goTo(N)")
- `.divider` — horizontal rule
- `.feedback-section`, `.feedback-toggle`, `.feedback-textarea`, `.feedback-save`, `.feedback-entry` — feedback system

## Slide structure (MANDATORY, in this order)

1. **Title slide** — Show the globe emoji and satellite antenna emoji in the title. Include: mission name, date, topic, breakthrough score as a colored tag. Include a TOC below the title info showing what slides are coming.
2. **TL;DR slide** — 2-3 bullet punchline of what the mission investigated, what it found, and the bottom-line verdict. Short, punchy, no paragraphs.
3. **"What was the breakthrough claim?" slide** — What the radar detected that triggered this mission. What was the original claim, paper, or discovery? Present it clearly with source info and why it was flagged.
4. **"What did Atlas find?" slide(s)** — The investigation results. This is the core of the briefing. What did the agents actually discover? Present key findings, validation results, novel claims. Use stat boxes for quantitative results. Use tags for claim status (confirmed/debunked/mixed/novel). If there are multiple strategies or many explorations, show the breadth. 1-3 slides depending on content richness.
5. **"How did the agents coordinate?" slide** — Agent architecture performance. How many strategies were run? How many explorations? Show the mission structure visually: missionary -> strategizer -> explorer pipeline. Highlight any interesting coordination patterns, self-corrections, or knowledge accumulation.
6. **"What's the verdict?" slide** — Final assessment. Was the breakthrough claim confirmed, debunked, or mixed? Use a large colored tag (green for confirmed, red for debunked, amber for mixed). Summarize the strength of evidence. Note any novel claims that emerged from the investigation.
7. **"What does this mean for Eywa?" slide** — Connect findings to the Eywa project: a self-evolving AI agent orchestration system focused on durable improvement loops, eval/feedback, and hard science problems. Be specific about which aspect of Eywa this relates to. Do NOT make up priorities or editorialize — stick to what the mission data shows.

## Title format

The title should be: `GLOBE_EMOJI SATELLITE_EMOJI TITLE_TEXT — Atlas Briefing`

where GLOBE_EMOJI is the globe emoji and SATELLITE_EMOJI is the satellite antenna emoji.

## Navigation (include inline in HTML)

Fixed bottom nav bar with prev/next buttons, slide counter, arrow key support. Use this exact HTML at the end of `<body>`:

```html
<div class="nav">
  <button class="nav-btn" id="prevBtn" onclick="prev()">&larr;</button>
  <div class="nav-counter" id="navCounter">1 / N</div>
  <button class="nav-btn" id="nextBtn" onclick="next()">&rarr;</button>
</div>
```

## Feedback system (include inline in HTML)

Each slide gets a collapsible feedback section injected via JS. Include this complete feedback system in a `<script>` tag:

- localStorage key: `{folder-name}-feedback` (the folder name will be provided)
- On save: POST to `/api/feedback` to persist to disk
- On load: fetch GET `/api/feedback` and merge with localStorage
- Each entry records: text, timestamp, slideTitle
- Cmd+Enter shortcut to save
- Delete button per entry
- Blue dot indicator when feedback exists

The JS must:
1. Define `FEEDBACK_KEY` using the folder name provided
2. Implement: `loadFeedback()`, `saveFeedbackStore()`, `addFeedback()`, `deleteFeedback()`, `getSlideName()`, `renderFeedbackForSlide()`, `escapeHtml()`, `submitFeedback()`, `toggleFeedback()`
3. Inject feedback UI into every `.slide` on load
4. Fetch and merge server feedback on startup
5. Implement navigation: `show(n)`, `next()`, `prev()`, `goTo(n)`, arrow key listener (skip when textarea focused)

## Content guidelines

- **Verdicts over data.** Lead with the conclusion, support with evidence. Don't dump all findings — synthesize them.
- **Make agents visible.** Show how many agents ran, what each did, and how information flowed between them. The multi-agent coordination story is as important as the science results.
- **Methodology over raw science.** The focus is on how the atlas system performed. Science results are context, not the story. Gear content toward a non-physicist audience.
- **Validation tiers.** If the mission includes validation tier achievements, show them prominently with colored tags (green for achieved, amber for partial, muted for not reached).
- **Novel claims.** If the mission produced novel claims, highlight them with purple tags. Note their strength and whether they survived adversarial review.
- **No quotes.** Present insights directly.
- **Don't extrapolate or invent priorities.** Present what the mission data shows.
- **Keep it fun and visual.** Stat boxes, tags, flow diagrams where appropriate.

## What you will receive

You will be given:
1. Mission metadata (name, topic, breakthrough score, reasons)
2. MISSION-COMPLETE.md — the final summary of what was found
3. MISSION.md — the original mission description
4. Strategy-level FINAL-REPORT.md files — detailed strategy results
5. Exploration-level REPORT.md files — individual exploration findings

Not all files will be present for every mission. Use whatever is available. Focus on MISSION-COMPLETE.md as the primary source, with strategy and exploration reports as supporting detail.

Generate a complete presentation from this material. Make it visually engaging and informative. The audience is a technical founder building AI agent systems who wants to know: what did my agents find overnight?
