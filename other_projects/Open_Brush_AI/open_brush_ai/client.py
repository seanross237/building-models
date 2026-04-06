"""Open Brush HTTP API client."""

from __future__ import annotations

import json
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from .config import COMMAND_DELAY, OPEN_BRUSH_URL, RECORDINGS_DIR, ExecutionMode
from .models import PaintCommand, PaintingPlan, Recording


class OpenBrushClient:
    """Wrapper around the Open Brush HTTP API (localhost:40074)."""

    def __init__(
        self,
        base_url: str = OPEN_BRUSH_URL,
        mode: ExecutionMode = ExecutionMode.MOCK,
        delay: float = COMMAND_DELAY,
    ):
        self.base_url = base_url
        self.mode = mode
        self.delay = delay
        self._command_log: list[dict[str, Any]] = []
        self._command_count = 0

    # ── Dispatch ──────────────────────────────────────────────

    # Maps action names to functions that convert params → API query dict
    DISPATCH: dict[str, Any] = {
        "set_brush": lambda p: {"brush.type": p["type"]},
        "set_color_rgb": lambda p: {
            "color.set.rgb": f"{p['r']},{p['g']},{p['b']}"
        },
        "set_color_html": lambda p: {"color.set.html": p["color"]},
        "set_size": lambda p: {"brush.size.set": str(p["size"])},
        "move_to": lambda p: {
            "brush.move.to": f"{p['x']},{p['y']},{p['z']}"
        },
        "move_by": lambda p: {
            "brush.move.by": f"{p['dx']},{p['dy']},{p['dz']}"
        },
        "draw_path": lambda p: {
            "draw.path": ",".join(
                f"[{pt[0]},{pt[1]},{pt[2]}]" for pt in p["points"]
            )
        },
        "draw_stroke": lambda p: {
            "draw.stroke": ",".join(
                f"[{s[0]},{s[1]},{s[2]},{s[3]},{s[4]},{s[5]},{s[6]}]"
                for s in p["strokes"]
            )
        },
        "draw_svg_path": lambda p: {"draw.svg.path": p["path"]},
        "look_at": lambda p: {
            "brush.look.at": f"{p['x']},{p['y']},{p['z']}"
        },
        "turn_y": lambda p: {"brush.turn.y": str(p["degrees"])},
        "turn_x": lambda p: {"brush.turn.x": str(p["degrees"])},
        "turn_z": lambda p: {"brush.turn.z": str(p["degrees"])},
        "draw_forward": lambda p: {"brush.draw": str(p["length"])},
    }

    def execute(self, command: PaintCommand) -> dict[str, Any]:
        """Execute a single PaintCommand."""
        self._command_count += 1

        if command.action == "pause":
            pause_time = command.params.get("seconds", 0.5)
            self._log_command(command, {"_pause": pause_time})
            if self.mode == ExecutionMode.LIVE:
                time.sleep(pause_time)
            return {"status": "paused", "seconds": pause_time}

        dispatch_fn = self.DISPATCH.get(command.action)
        if not dispatch_fn:
            print(f"  ⚠ Unknown action: {command.action}")
            return {"status": "error", "message": f"Unknown action: {command.action}"}

        api_params = dispatch_fn(command.params)
        self._log_command(command, api_params)
        return self._send(api_params)

    def execute_plan(self, plan: PaintingPlan) -> None:
        """Execute all commands in a painting plan."""
        total = len(plan.commands)
        print(f"\n{'='*60}")
        print(f"  Painting: {plan.title}")
        print(f"  {plan.description}")
        print(f"  {total} commands")
        print(f"{'='*60}\n")

        for i, cmd in enumerate(plan.commands):
            label = cmd.comment or self._summarize_params(cmd)
            print(f"  [{i+1}/{total}] {cmd.action}: {label}")
            self.execute(cmd)
            if self.delay > 0 and self.mode != ExecutionMode.MOCK:
                time.sleep(self.delay)

        print(f"\n  ✓ Painting complete! ({total} commands executed)\n")

    @staticmethod
    def _summarize_params(cmd: PaintCommand) -> str:
        """Create a readable summary of command params."""
        p = cmd.params
        if cmd.action == "set_brush":
            return p.get("type", "?")
        if cmd.action in ("set_color_html", "set_color_rgb"):
            return p.get("color", f"rgb({p.get('r')},{p.get('g')},{p.get('b')})")
        if cmd.action == "set_size":
            return f"size={p.get('size', 0):.2f}"
        if cmd.action in ("move_to", "look_at"):
            return f"({p.get('x')}, {p.get('y')}, {p.get('z')})"
        if cmd.action == "draw_path":
            pts = p.get("points", [])
            return f"{len(pts)} points"
        if cmd.action == "draw_stroke":
            s = p.get("strokes", [])
            return f"{len(s)} stroke points"
        if cmd.action == "pause":
            return f"{p.get('seconds', 0.5)}s"
        return str(p)

    # ── HTTP layer ────────────────────────────────────────────

    def _send(self, params: dict[str, str]) -> dict[str, Any]:
        """Send params to the Open Brush API."""
        if self.mode == ExecutionMode.MOCK:
            return {"status": "mock", "params": params}

        if self.mode == ExecutionMode.RECORD:
            return {"status": "recorded", "params": params}

        # LIVE mode
        try:
            encoded = urllib.parse.urlencode(params)
            if len(encoded) > 1000:
                resp = requests.post(self.base_url, data=params, timeout=10)
            else:
                resp = requests.get(self.base_url, params=params, timeout=10)
            return {"status": resp.status_code, "body": resp.text}
        except requests.ConnectionError:
            print(
                "  ✗ Cannot connect to Open Brush. "
                "Is it running with the API enabled?"
            )
            return {"status": "connection_error"}

    # ── Logging / Recording ───────────────────────────────────

    def _log_command(self, command: PaintCommand, api_params: dict) -> None:
        """Log command for recording purposes."""
        self._command_log.append({
            "index": self._command_count,
            "action": command.action,
            "params": command.params,
            "api_params": api_params,
            "comment": command.comment,
        })

    def save_recording(
        self,
        prompt: str,
        plan: PaintingPlan,
        style: str | None = None,
    ) -> Path:
        """Save the executed plan as a recording JSON file."""
        now = datetime.now(timezone.utc)
        recording = Recording(
            created_at=now.isoformat(),
            prompt=prompt,
            style=style,
            plan=plan,
        )
        slug = now.strftime("%Y%m%d_%H%M%S")
        title_slug = plan.title.lower().replace(" ", "_")[:30]
        filename = f"{slug}_{title_slug}.json"
        path = RECORDINGS_DIR / filename
        path.write_text(json.dumps(recording.model_dump(), indent=2))
        print(f"  💾 Saved recording: {path}")
        return path

    @staticmethod
    def load_recording(path: str | Path) -> Recording:
        """Load a recording from a JSON file."""
        data = json.loads(Path(path).read_text())
        return Recording.model_validate(data)

    # ── Connection check ──────────────────────────────────────

    def check_connection(self) -> bool:
        """Check if Open Brush is reachable."""
        try:
            resp = requests.get(
                self.base_url.replace("/api/v1", "/help/commands"),
                timeout=3,
            )
            return resp.status_code == 200
        except requests.ConnectionError:
            return False

    def get_camera_view(self) -> bytes | None:
        """Get a PNG screenshot from Open Brush's camera."""
        try:
            resp = requests.get(
                self.base_url.replace("/api/v1", "/cameraview"),
                timeout=5,
            )
            if resp.status_code == 200:
                return resp.content
            return None
        except requests.ConnectionError:
            return None

    # ── Convenience methods ───────────────────────────────────

    def set_brush(self, brush_type: str) -> dict:
        return self.execute(PaintCommand(
            action="set_brush", params={"type": brush_type}
        ))

    def set_color(self, color: str) -> dict:
        return self.execute(PaintCommand(
            action="set_color_html", params={"color": color}
        ))

    def set_size(self, size: float) -> dict:
        return self.execute(PaintCommand(
            action="set_size", params={"size": size}
        ))

    def move_to(self, x: float, y: float, z: float) -> dict:
        return self.execute(PaintCommand(
            action="move_to", params={"x": x, "y": y, "z": z}
        ))

    def draw_path(self, points: list[list[float]]) -> dict:
        return self.execute(PaintCommand(
            action="draw_path", params={"points": points}
        ))
