# Presentation Guide

Learnings and principles for what makes a good science briefing presentation. This will be refined over time.

## Purpose

Presentations are built on request to context-load Sean back into the project. They are visual, click-through slide decks focused on methodology performance — how the autonomous research system is doing, not just the science results.

## Learnings

### Visual Style
- **Dark theme by default.** Presentations should be dark themed unless Sean explicitly asks for something else.
- **Keep slides distinct from the page.** Even in a dark theme, slides should still read as clear cards/panels with separation, depth, and strong contrast. Avoid muddy dark-on-dark layouts.
- **60-word hard limit.** Visible text on any slide must not exceed 60 words. Content beyond that must go inside a collapsed `<details>` section. No exceptions.
- **Less text.** Keep slides sparse. Visuals and short labels over paragraphs. If it feels like reading, there's too much.
- **Make it fun.** Slides should feel visually engaging, not like a document. Use color, layout variety, and whitespace generously. Avoid walls of text even if the content is interesting.
- **Short chunks, not walls.** When you land on a slide, the first impression should be clean and scannable — headlines, labels, small cards. Never hit the reader with a block of text. If detail is needed, put it behind a collapsible section (collapsed by default). Use `<details><summary>` or a click-to-expand pattern so the reader can drill in when they want to and skip when they don't. The slide should feel light on arrival and rich on demand.
- **Lively and visual.** Use color-coded tags, stat boxes, visual hierarchies, icons, and layout variety to keep energy up. Each slide should feel different from the last. Monotonous card grids are boring — mix up the layout.

### Structure
- **Table of contents first.** Every presentation starts with a slide showing what's coming — the topics/sections at a glance. Lets Sean orient before diving in. The TOC should look good — chunk items into logical sections with clear visual grouping, not just a flat list.
- **TL;DR slide right after the TOC.** The second slide should be a quick summary of what happened and what the takeaway is. Hit the reader with the punchline up front so they have context for everything that follows. Keep it to a few short bullets — no detail, just the story arc and conclusion.
- **One message per slide.** Each slide should focus on one major takeaway and very little text. If a slide is making two or three points, split it up. Combining the pipeline diagram, stats, parameters, AND information flow into one slide is too much — those are separate messages. Prefer visuals, diagrams, and short labels over sentences. If you're reading more than a few words per element, there's too much text.
- **Title every slide with the question it answers.** Each slide's title should be the question that slide is answering. This forces clarity about what the slide is for and helps the reader know exactly what they're about to learn (e.g., "How did the agents coordinate?" instead of "Agent Coordination").

### Project Emojis

Every presentation should include its project emoji in the title slide and meta.json title. These help Sean context-switch quickly between projects.

| Project | Emoji | Character |
|---------|-------|-----------|
| Adversarial Logic | ⚔️ | crossed swords |
| Atlas | 🌍 | globe |
| Rhyme-Eval / Feedback Looper | 🔄 | cycle |
| BBEH Benchmark | 📊 | bar chart |

Use the emoji at the start of the presentation title (e.g., `"title": "⚔️ Adversarial Logic — Run 004"`). Also include it visually on the title slide itself.

### Content
- **Light on history.** The presentation catches you up on where things are *now*. Historical context is for the timeline stage — don't repeat it heavily in the presentation. A brief "how we got here" is fine, but it shouldn't dominate.
- **Don't extrapolate.** Stick to Sean's stated goals and actual results. Don't invent priorities, suggest directions, or editorialize about what should happen next unless Sean has said it. Present what is, not what could be.
- **Methodology over science.** The focus is on how the system performed, not the physics details. Science results are context, not the story. Gear content toward a non-physicist audience.
- **Conclusions over raw data.** Don't dump all the information — focus on what was learned and what the takeaways are. Data supports the conclusion, it doesn't replace it.
- **Show how information flowed.** When presenting results from a multi-agent system, highlight what was passed between agents, how knowledge accumulated, and where the system self-corrected. The structure's performance is the story.
- **Make agents visible.** When a system uses agents, make it immediately clear how many agents are involved and what each one's job is. You should be able to glance at a slide and instantly know the agent architecture.
- **No quotes.** Don't put quotes in presentations. Present insights directly.

## Feedback System (Required)

Every presentation must include a per-slide feedback mechanism so Sean can leave notes while reviewing. These notes get saved to `feedback.json` in the presentation folder for later use (editing the presentation, extracting learnings, etc.).

### How it works
- Each slide gets a collapsible "Leave feedback on this slide" section at the bottom
- Clicking it reveals a textarea + Save button (Cmd+Enter shortcut)
- Each feedback entry records: the text, a timestamp, and the slide title
- Feedback is saved to both localStorage (immediate) and `feedback.json` on disk (via the server)
- Existing feedback entries show below the input with timestamps and a delete button

### Implementation
- **CSS:** Add `.feedback-section`, `.feedback-toggle`, `.feedback-textarea`, `.feedback-save`, `.feedback-entry` styles
- **JS:** On page load, inject a feedback section into every `.slide` element. Use localStorage key `{presentation-name}-feedback` for client-side persistence. On save, POST to `/api/feedback` to persist to disk.
- **Server:** The `serve.py` must handle:
  - `GET /api/feedback` — return `feedback.json` contents (or `{}` if missing)
  - `POST /api/feedback` — write request body to `feedback.json`
  - CORS headers on all responses + OPTIONS preflight handler
- **Merge on load:** On startup, fetch from `/api/feedback` and merge with localStorage so feedback survives across browsers/devices

### Reference implementation
See `home-base/presentation_hub/getting-caught-up-on-old-attempts-2026-03-25/` for a working example with all the CSS, JS, and server code.

## Unified Server & Index Page

All presentations are served from a single server at `presentations/serve.py` (port 8900). It auto-discovers any subdirectory containing `presentation.html` and serves them all at `/{folder-name}/`. The index page at `/` lists all presentations.

### meta.json (Required)

Every presentation folder must include a `meta.json` with a human-readable display title. The index page uses this — do NOT rely on the folder name for the display title.

```json
{"title": "Your Nice Title Here"}
```

- The folder name is for filesystem organization (kebab-case, with date suffix like `my-presentation-2026-03-25`)
- The `meta.json` title is what the user sees in the index — make it readable
- Optionally override the date: `{"title": "...", "date": "Mar 25"}`
- The server auto-extracts the date from the folder name suffix, so you only need the `date` field if you want to override it

### Viewed / New tracking

The index page tracks which presentations have been viewed. Unviewed presentations show a blue "New" badge and are full opacity; viewed ones are dimmed. This is tracked in `viewed.json` at the presentations root and synced to localStorage.

- The index page has two sections: **New** at the top and **Reviewed** below, separated by a divider. Unviewed presentations appear in New with a blue badge; viewed ones are moved to the Reviewed section and dimmed.
- Clicking a presentation card automatically marks it as viewed
- New presentations appear with a "New" badge by default — no action needed from the creating agent
- Both sections are always visible, even when empty
- The `viewed.json` is the source of truth; localStorage merges on load

### Feedback API paths

When served via the unified server, feedback API paths are automatically rewritten from `/api/feedback` to `/{folder-name}/api/feedback`. No changes needed in presentation HTML — the server handles the rewrite. Individual `serve.py` files per presentation are no longer needed but can be kept as standalone fallbacks.
