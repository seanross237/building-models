# Research Radar — Presentation Generator Prompt

You are generating a single-file HTML presentation for a Research Radar briefing.

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

1. **Title slide** — Include the radar emoji at the start of the title. Show: title, date, source type (YouTube / arXiv), source URL as a link, relevance score as a colored tag. Include a TOC below the title info showing what slides are coming.
2. **TL;DR slide** — 2-3 bullet punchline of what this is and why it matters. Short, punchy, no paragraphs.
3. **Main content slides (3-5 slides)** — One message per slide. Title each slide with the question it answers (e.g., "What did they find?" not "Findings"). Use cards, stat boxes, tags, and visual variety. Draw from the summary and source material.
4. **"What does this mean for Eywa?" slide** — Connect the content to the Eywa project: a self-evolving AI agent orchestration system focused on durable improvement loops, eval/feedback, and hard science problems. Be specific about which aspect of Eywa this relates to. Do NOT make up priorities or editorialize — stick to the connection.

## Title format

The title should be: `RADAR_EMOJI TITLE_TEXT — Research Radar`

where RADAR_EMOJI is the satellite antenna emoji.

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

- Focus on what matters NOW, not full history
- Methodology over raw science — how does the system/approach work?
- Conclusions over raw data — what was learned?
- No quotes. Present insights directly.
- Don't extrapolate or invent priorities. Present what the source material says.
- Keep it fun and visual. Stat boxes, tags, diagrams where appropriate.

## What you will receive

You will be given:
1. A summary markdown file with: title, topic, source URL, relevance score, summary paragraph, "why it matters now" paragraph, and key takeaways
2. The source item markdown with the full content (transcript, abstract, etc.)
3. A folder name for the feedback localStorage key

Generate a complete presentation from this material. Make it visually engaging and informative. The audience is a technical founder building AI agent systems.
