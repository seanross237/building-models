#!/usr/bin/env python3
"""Agent Loop Dashboard — real-time view of the research system.

Run:   python3 dashboard.py
Open:  http://localhost:8888
"""

import http.server
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse

PORT = 8888

SCRIPT_DIR = Path(__file__).parent.resolve()
EXECUTION_ROOT = SCRIPT_DIR.parent.parent / "execution"
INSTANCE_DIR = EXECUTION_ROOT / "instances" / "quantum-gravity"
AGENTS_DIR = EXECUTION_ROOT / "agents"
HTML_PATH = SCRIPT_DIR / (Path(__file__).stem + ".html")


def read_file(path):
    try:
        return Path(path).read_text()
    except (FileNotFoundError, PermissionError):
        return None


def parse_yaml_frontmatter(text):
    match = re.search(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).strip().split('\n'):
        if ':' not in line:
            continue
        key, _, value = line.partition(':')
        key = key.strip()
        value = value.strip().strip('"')
        if value.isdigit():
            value = int(value)
        elif value == 'true':
            value = True
        elif value == 'false':
            value = False
        result[key] = value
    return result


def get_mission_start_time():
    """Get mission start time from MISSION.md creation time."""
    mission_path = INSTANCE_DIR / "MISSION.md"
    if mission_path.exists():
        stat = os.stat(mission_path)
        # Use birthtime on macOS, fallback to mtime
        return getattr(stat, 'st_birthtime', stat.st_mtime)
    return time.time()


def get_state():
    # Mission
    mission_text = read_file(INSTANCE_DIR / "MISSION.md") or ""
    validation = read_file(INSTANCE_DIR / "MISSION-VALIDATION-GUIDE.md") or ""

    # Agent prompts
    agents = {}
    for name in ["missionary", "strategizer", "explorer"]:
        agents[name] = read_file(AGENTS_DIR / name / "system-prompt.md") or ""
    agents["curator"] = read_file(
        AGENTS_DIR / "library" / "curator" / "system-prompt.md") or ""

    # Strategies
    strategies = []
    strategies_dir = INSTANCE_DIR / "strategies"
    if strategies_dir.exists():
        for d in sorted(strategies_dir.iterdir()):
            if not d.is_dir() or d.name.startswith('.'):
                continue

            state_json_text = read_file(d / "state.json")
            state_data = {}
            if state_json_text:
                try:
                    state_data = json.loads(state_json_text)
                except json.JSONDecodeError:
                    pass

            loop_text = read_file(d / "LOOP-STATE.md") or ""
            loop_state = parse_yaml_frontmatter(loop_text) if loop_text else {}

            explorations = []
            exp_dir = d / "explorations"
            if exp_dir.exists():
                for ed in sorted(exp_dir.iterdir()):
                    if not ed.is_dir():
                        continue
                    explorations.append({
                        "id": ed.name,
                        "goal": read_file(ed / "GOAL.md"),
                        "report": read_file(ed / "REPORT.md"),
                        "report_summary": read_file(ed / "REPORT-SUMMARY.md"),
                    })

            done = state_data.get("done", False)
            active_loop = loop_state.get("active", False)
            status = "completed" if done else ("active" if active_loop else "idle")

            strategies.append({
                "id": d.name,
                "status": status,
                "strategy_md": read_file(d / "STRATEGY.md") or "",
                "state": state_data,
                "loop_state": loop_state,
                "history": read_file(d / "HISTORY.md") or "",
                "decisions": read_file(d / "DECISIONS.md") or "",
                "explorations": explorations,
            })

    # Library inbox
    inbox_dir = INSTANCE_DIR / "library-inbox"
    inbox_files = []
    if inbox_dir.exists():
        inbox_files = [f.name for f in inbox_dir.iterdir() if f.is_file()]

    # Stats
    completed_exps = []
    for s in strategies:
        completed_exps.extend(s["state"].get("explorations_completed", []))

    total_dirs = sum(len(s["explorations"]) for s in strategies)
    total = max(len(completed_exps), total_dirs)

    succeeded = sum(1 for e in completed_exps if e.get("outcome") == "succeeded")
    failed = sum(1 for e in completed_exps if e.get("outcome") == "failed")
    partial = sum(1 for e in completed_exps
                  if e.get("outcome") in ("partial", "inconclusive"))
    in_progress = sum(1 for s in strategies
                      if s["state"].get("current_exploration"))

    resets = sum(s.get("loop_state", {}).get("iteration", 0) for s in strategies)

    elapsed = time.time() - get_mission_start_time()
    hours, remainder = divmod(int(elapsed), 3600)
    minutes = remainder // 60

    return {
        "mission": {"text": mission_text, "validation_guide": validation},
        "agents": agents,
        "strategies": strategies,
        "library_inbox": {"count": len(inbox_files), "files": inbox_files},
        "stats": {
            "total_explorations": total,
            "succeeded": succeeded,
            "failed": failed,
            "partial": partial,
            "in_progress": in_progress,
            "success_rate": (f"{succeeded/total*100:.0f}%"
                            if total > 0 else "--"),
            "context_resets": resets,
            "time_running": f"{hours}h {minutes}m",
        },
    }


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            html = HTML_PATH.read_text()
            self._respond(200, "text/html", html)
        elif parsed.path == "/api/state":
            self._respond(200, "application/json", json.dumps(get_state()))
        else:
            self._respond(404, "text/plain", "Not found")

    def _respond(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode() if isinstance(body, str) else body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"Dashboard → http://localhost:{PORT}")
    print("Ctrl+C to stop\n")
    try:
        http.server.HTTPServer(("", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
