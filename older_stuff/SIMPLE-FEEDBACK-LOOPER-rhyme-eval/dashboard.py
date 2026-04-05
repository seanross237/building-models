#!/usr/bin/env python3
"""Rhyme-Eval Dashboard Server — reads state.json, serves dashboard.html"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PORT = 8877
SCRIPT_DIR = Path(__file__).parent.resolve()
STATE_PATH = SCRIPT_DIR / "state.json"
HTML_PATH = SCRIPT_DIR / "dashboard.html"

EMPTY_STATE = {
    "done": False,
    "total_generations": 5,
    "current_generation": 0,
    "generations": []
}


def get_state():
    try:
        return json.loads(STATE_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return EMPTY_STATE


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = HTML_PATH.read_bytes()
            self._respond(200, "text/html", body)
        elif self.path == "/api/state":
            body = json.dumps(get_state()).encode()
            self._respond(200, "application/json", body)
        else:
            self._respond(404, "text/plain", b"Not found")

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
    server = HTTPServer(("", PORT), Handler)
    print(f"Rhyme-Eval Dashboard → http://localhost:{PORT}")
    server.serve_forever()
