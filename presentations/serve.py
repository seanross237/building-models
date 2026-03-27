#!/usr/bin/env python3
"""Unified presentation server — serves index + all presentations from one port."""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote

PORT = 8900
PRESENTATIONS_DIR = Path(__file__).parent.resolve()
VIEWED_PATH = PRESENTATIONS_DIR / "viewed.json"


def discover_presentations():
    """Find all subdirectories containing a presentation.html, newest first."""
    import re
    presentations = []
    for d in PRESENTATIONS_DIR.iterdir():
        if d.is_dir() and (d / "presentation.html").exists():
            presentations.append(d.name)

    def sort_key(name):
        m = re.search(r'(\d{4}-\d{2}-\d{2})$', name)
        return m.group(1) if m else '0000-00-00'

    presentations.sort(key=sort_key, reverse=True)
    return presentations


def get_feedback(pres_name):
    path = PRESENTATIONS_DIR / pres_name / "feedback.json"
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_feedback(pres_name, data):
    path = PRESENTATIONS_DIR / pres_name / "feedback.json"
    path.write_text(json.dumps(data, indent=2))


def get_viewed():
    try:
        return json.loads(VIEWED_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_viewed(data):
    VIEWED_PATH.write_text(json.dumps(data, indent=2))


def build_index(presentations):
    """Generate the index page HTML."""
    import re
    from datetime import datetime as _dt

    cards = ""
    for name in presentations:
        # Check for meta.json with custom title
        meta_path = PRESENTATIONS_DIR / name / "meta.json"
        meta = {}
        try:
            meta = json.loads(meta_path.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # Extract YYYY-MM-DD date from end of folder name
        title = name
        short_date = ""
        m = re.search(r'-(\d{4}-\d{2}-\d{2})$', name)
        if m:
            date_str = m.group(1)
            title = name[:m.start()]
            try:
                short_date = _dt.strptime(date_str, "%Y-%m-%d").strftime("%b %d")
            except ValueError:
                short_date = date_str

        # meta.json overrides: {"title": "...", "date": "Mar 25"}
        display_title = meta.get("title", title.replace("-", " ").title())
        if meta.get("date"):
            short_date = meta["date"]

        cards += f"""
    <a href="/{name}/" class="pres-card" data-name="{name}" onclick="markViewed('{name}')">
      <div class="pres-date">{short_date}</div>
      <div class="pres-title">{display_title}</div>
      <div class="pres-new" id="new-{name}">New</div>
    </a>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Presentations</title>
<style>
:root {{
  --bg: #0d1117;
  --slide-bg: #f8f9fa;
  --slide-border: #e1e4e8;
  --text: #1f2937;
  --muted: #6b7280;
  --accent: #4f46e5;
  --accent-light: #eef2ff;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: var(--bg);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  display: flex; flex-direction: column; align-items: center;
  min-height: 100vh; padding: 60px 20px;
}}
.container {{
  width: 100%; max-width: 720px;
  background: var(--slide-bg); border: 1px solid var(--slide-border);
  border-radius: 16px; padding: 48px 56px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.3);
}}
h1 {{ font-size: 28px; font-weight: 700; color: var(--text); margin-bottom: 4px; }}
.subtitle {{ font-size: 14px; color: var(--muted); margin-bottom: 32px; }}
.count {{ font-size: 13px; color: var(--muted); margin-bottom: 16px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
.pres-card {{
  display: flex; align-items: center; gap: 16px;
  padding: 16px 20px; border: 1px solid var(--slide-border);
  border-radius: 10px; margin-bottom: 10px; background: white;
  text-decoration: none; transition: all 0.15s; cursor: pointer;
}}
.pres-card:hover {{ border-color: var(--accent); background: var(--accent-light); }}
.pres-date {{
  font-size: 13px; color: #7c3aed; font-weight: 600; white-space: nowrap;
  flex-shrink: 0; min-width: 52px;
  padding: 4px 10px; background: #f5f3ff; border-radius: 6px;
}}
.pres-title {{ font-size: 15px; font-weight: 600; color: var(--text); flex: 1; }}
.pres-new {{
  font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
  padding: 3px 8px; border-radius: 6px; flex-shrink: 0;
  background: #dbeafe; color: #2563eb;
}}
.pres-new.hidden {{ display: none; }}
.pres-card.viewed {{ opacity: 0.55; }}
.pres-card.viewed:hover {{ opacity: 1; }}
.section-heading {{
  font-size: 13px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.6px; color: #2563eb; margin-bottom: 12px;
}}
.section-heading-reviewed {{
  color: var(--muted);
}}
.section-reviewed {{
  margin-top: 32px; padding-top: 28px;
  border-top: 1px solid var(--slide-border);
}}
#section-new.empty .section-heading, #section-reviewed.empty .section-heading {{
  opacity: 0.4;
}}
</style>
</head>
<body>
<div class="container">
  <h1>Presentations</h1>
  <p class="subtitle">Building Models &mdash; all presentations</p>
  <p class="count">{len(presentations)} presentation{"s" if len(presentations) != 1 else ""}</p>

  <div id="section-new">
    <h2 class="section-heading">New</h2>
    <div id="cards-new">{cards}</div>
  </div>

  <div id="section-reviewed" class="section-reviewed">
    <h2 class="section-heading section-heading-reviewed">Reviewed</h2>
    <div id="cards-reviewed"></div>
  </div>
</div>
<script>
const VIEWED_KEY = 'presentations-viewed';

function loadViewed() {{
  try {{ return JSON.parse(localStorage.getItem(VIEWED_KEY) || '[]'); }}
  catch {{ return []; }}
}}

function saveViewed(list) {{
  localStorage.setItem(VIEWED_KEY, JSON.stringify(list));
  fetch('/api/viewed', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify(list)
  }}).catch(() => {{}});
}}

function markViewed(name) {{
  const viewed = loadViewed();
  if (!viewed.includes(name)) {{
    viewed.push(name);
    saveViewed(viewed);
  }}
}}

function applyViewed() {{
  const viewed = loadViewed();
  const reviewedContainer = document.getElementById('cards-reviewed');
  document.querySelectorAll('.pres-card').forEach(card => {{
    const name = card.dataset.name;
    if (viewed.includes(name)) {{
      card.classList.add('viewed');
      const badge = document.getElementById('new-' + name);
      if (badge) badge.classList.add('hidden');
      reviewedContainer.appendChild(card);
    }}
  }});
  // Hide empty sections
  const newSection = document.getElementById('section-new');
  const revSection = document.getElementById('section-reviewed');
  if (!document.getElementById('cards-new').children.length) newSection.classList.add('empty');
  else newSection.classList.remove('empty');
  if (!reviewedContainer.children.length) revSection.classList.add('empty');
  else revSection.classList.remove('empty');
}}

// Load server-side viewed list and merge
(async function() {{
  try {{
    const resp = await fetch('/api/viewed');
    const serverViewed = await resp.json();
    const localViewed = loadViewed();
    const merged = [...new Set([...localViewed, ...serverViewed])];
    if (merged.length > localViewed.length) {{
      localStorage.setItem(VIEWED_KEY, JSON.stringify(merged));
    }}
  }} catch {{}}
  applyViewed();
}})();
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(self.path)

        # Index
        if path in ("/", "/index.html"):
            presentations = discover_presentations()
            body = build_index(presentations).encode()
            self._respond(200, "text/html", body)
            return

        # Viewed API
        if path == "/api/viewed":
            body = json.dumps(get_viewed()).encode()
            self._respond(200, "application/json", body)
            return

        # Presentation routes: /{name}/ or /{name}
        parts = path.strip("/").split("/")
        pres_name = parts[0] if parts else ""
        pres_dir = PRESENTATIONS_DIR / pres_name

        if not pres_dir.is_dir() or not (pres_dir / "presentation.html").exists():
            self._respond(404, "text/plain", b"Not found")
            return

        # /{name}/api/feedback
        if len(parts) >= 3 and parts[1] == "api" and parts[2] == "feedback":
            body = json.dumps(get_feedback(pres_name)).encode()
            self._respond(200, "application/json", body)
            return

        # /{name}/ or /{name} — serve the presentation HTML
        # Rewrite internal API paths so feedback works
        html = (pres_dir / "presentation.html").read_text()
        html = html.replace("'/api/feedback'", f"'/{pres_name}/api/feedback'")
        html = html.replace("\"/api/feedback\"", f"\"/{pres_name}/api/feedback\"")
        # Also handle /api/state if present
        html = html.replace("'/api/state'", f"'/{pres_name}/api/state'")
        html = html.replace("\"/api/state\"", f"\"/{pres_name}/api/state\"")
        self._respond(200, "text/html", html.encode())

    def do_POST(self):
        path = unquote(self.path)
        parts = path.strip("/").split("/")

        # Viewed API
        if path == "/api/viewed":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw)
                # Merge with existing
                existing = get_viewed()
                merged = list(set(existing + data))
                save_viewed(merged)
                self._respond(200, "application/json", b'{"ok":true}')
            except (json.JSONDecodeError, Exception) as e:
                self._respond(400, "application/json", json.dumps({"error": str(e)}).encode())
            return

        if len(parts) >= 3 and parts[1] == "api" and parts[2] == "feedback":
            pres_name = parts[0]
            pres_dir = PRESENTATIONS_DIR / pres_name
            if not pres_dir.is_dir():
                self._respond(404, "text/plain", b"Not found")
                return

            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw)
                save_feedback(pres_name, data)
                self._respond(200, "application/json", b'{"ok":true}')
            except (json.JSONDecodeError, Exception) as e:
                self._respond(400, "application/json", json.dumps({"error": str(e)}).encode())
        else:
            self._respond(404, "text/plain", b"Not found")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _respond(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # silent


if __name__ == "__main__":
    print(f"Presentations index → http://localhost:{PORT}")
    print(f"Serving from: {PRESENTATIONS_DIR}")
    print(f"Found: {', '.join(discover_presentations())}")
    server = HTTPServer(("", PORT), Handler)
    server.serve_forever()
