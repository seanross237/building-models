# Presentation Guide

Learnings and principles for what makes a good science briefing presentation. This will be refined over time.

## Purpose

Presentations are built on request to context-load Sean back into the project. They are visual, click-through slide decks focused on methodology performance — how the autonomous research system is doing, not just the science results.

## Learnings

### Visual Style
- **Lighter backgrounds.** Slides should render inside a distinct square/card with a lighter background, clearly separated from the dark page behind it. Not dark-on-dark.
- **Less text.** Keep slides sparse. Visuals and short labels over paragraphs. If it feels like reading, there's too much.

### Structure
- **Table of contents first.** Every presentation starts with a slide showing what's coming — the topics/sections at a glance. Lets Sean orient before diving in.
- **Keep it short.** ~6-8 slides max unless Sean asks for more. 12 is too many. Each slide should earn its spot.

### Content
- **Light on history.** The presentation catches you up on where things are *now*. Historical context is for the timeline stage — don't repeat it heavily in the presentation. A brief "how we got here" is fine, but it shouldn't dominate.
- **Don't extrapolate.** Stick to Sean's stated goals and actual results. Don't invent priorities, suggest directions, or editorialize about what should happen next unless Sean has said it. Present what is, not what could be.
- **Methodology over science.** The focus is on how the system performed, not the physics details. Science results are context, not the story.
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
See `building_models/presentations/getting-caught-up-on-old-attempts-2026-03-25/` for a working example with all the CSS, JS, and server code.
