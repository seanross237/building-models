#!/usr/bin/env python3
"""Adversarial Logic Run 002 (Prose) Presentation Server"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PORT = 8881
SCRIPT_DIR = Path(__file__).parent.resolve()
HTML_PATH = SCRIPT_DIR / "presentation.html"
FEEDBACK_PATH = SCRIPT_DIR / "feedback.json"


def get_feedback():
    try:
        return json.loads(FEEDBACK_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = HTML_PATH.read_bytes()
            self._respond(200, "text/html", body)
        elif self.path == "/api/feedback":
            body = json.dumps(get_feedback()).encode()
            self._respond(200, "application/json", body)
        else:
            self._respond(404, "text/plain", b"Not found")

    def do_POST(self):
        if self.path == "/api/feedback":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw)
                FEEDBACK_PATH.write_text(json.dumps(data, indent=2))
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
    server = HTTPServer(("", PORT), Handler)
    print(f"Adversarial Logic Run 002 Presentation → http://localhost:{PORT}")
    server.serve_forever()
