#!/usr/bin/env python3
"""Eywa Mission Visualizer — serves tree state as JSON + static HTML."""

import http.server
import json
import os
import sys
import urllib.parse
from pathlib import Path

EYWA_ROOT = Path(__file__).resolve().parent.parent
MISSIONS_DIR = EYWA_ROOT / "missions"

STATUS_PATHS = [
    "status",
    "for-orchestrator/this-nodes-current-status",
]

AGENT_MODE_PATHS = [
    "for-orchestrator/agent-mode",
]

FILE_CANDIDATES = {
    "goal.md": [
        "goal.md",
        "input/goal.md",
    ],
    "plan.md": [
        "plan.md",
        "output/plan.md",
    ],
    "result.md": [
        "result.md",
        "output/final-output.md",
    ],
    "review.md": [
        "review.md",
        "output/review.md",
    ],
    "decision-log.md": [
        "decision-log.md",
    ],
    "state.md": [
        "state.md",
        "output/state.md",
    ],
    "knowledge.md": [
        "knowledge.md",
        "retrieved_relevant_knowledge_from_library.md",
        "input/retrieved_relevant_knowledge_from_library.md",
    ],
    "TASK.md": [
        "TASK.md",
        "TASK-node.md",
    ],
    "TASK-retrieval.md": [
        "TASK-retrieval.md",
    ],
    "TASK-evaluation.md": [
        "TASK-evaluation.md",
    ],
    "TASK-synthesis.md": [
        "TASK-synthesis.md",
    ],
    "escalation.md": [
        "escalation.md",
        "output/escalation.md",
    ],
    "eval-decision": [
        "eval-decision",
        "for-orchestrator/eval-decision",
    ],
    "instructions-executor.md": [
        "input/instructions-executor.md",
    ],
    "instructions-planner.md": [
        "input/instructions-planner.md",
    ],
    "instructions-retrieval.md": [
        "input/instructions-retrieval.md",
    ],
    "instructions-reviewer.md": [
        "input/instructions-reviewer.md",
    ],
    "instructions-decider.md": [
        "input/instructions-decider.md",
    ],
    "instructions-evaluation.md": [
        "input/instructions-evaluation.md",
    ],
    "instructions-synthesis.md": [
        "input/instructions-synthesis.md",
    ],
}

LEGACY_ARTIFACT_CATEGORIES = {
    "goal.md": "input",
    "retrieved_relevant_knowledge_from_library.md": "input",
    "TASK.md": "input",
    "TASK-node.md": "input",
    "TASK-retrieval.md": "input",
    "TASK-evaluation.md": "input",
    "TASK-synthesis.md": "input",
    "plan.md": "output",
    "review.md": "output",
    "result.md": "output",
    "decision-log.md": "output",
    "state.md": "output",
    "escalation.md": "output",
    "eval-decision": "control",
    "status": "control",
}


def read_first_existing(base_path, candidates):
    """Return the contents of the first readable file from a candidate list."""
    for rel_path in candidates:
        path = base_path / rel_path
        if not path.exists():
            continue
        try:
            return path.read_text(errors="replace")
        except Exception:
            return "(could not read)"
    return None


def compute_parent_path(node_path, tree_root):
    """Return parent node path relative to the tree root, if any."""
    if node_path == tree_root or node_path == tree_root / "root":
        return None
    parent = node_path.parent
    if parent.name == "children":
        parent = parent.parent
    if parent == node_path:
        return None
    rel = str(parent.relative_to(tree_root))
    return "root" if rel == "." else rel


def classify_artifact(rel_path):
    """Classify an artifact by where it lives in the node directory."""
    if rel_path.startswith("input/"):
        return "input"
    if rel_path.startswith("output/"):
        return "output"
    if rel_path.startswith("for-orchestrator/"):
        return "control"
    return LEGACY_ARTIFACT_CATEGORIES.get(Path(rel_path).name, "other")


def collect_artifacts(node_path):
    """Collect visible artifacts from current and legacy layouts."""
    artifacts = []
    category_order = {"input": 0, "output": 1, "control": 2, "other": 3}

    def append_artifact(path):
        rel_path = str(path.relative_to(node_path))
        if any(part.startswith(".") for part in Path(rel_path).parts):
            return
        try:
            content = path.read_text(errors="replace")
        except Exception:
            content = "(could not read)"
        artifacts.append({
            "path": rel_path,
            "name": path.name,
            "category": classify_artifact(rel_path),
            "content": content,
        })

    for child in sorted(node_path.iterdir()):
        if child.name.startswith(".") or child.name == "children":
            continue
        if child.is_file():
            append_artifact(child)
            continue
        if child.is_dir() and child.name in {"input", "output", "for-orchestrator"}:
            for nested in sorted(child.rglob("*")):
                if nested.is_file():
                    append_artifact(nested)

    artifacts.sort(key=lambda artifact: (category_order.get(artifact["category"], 99), artifact["path"]))
    return artifacts


def build_flow_summary(rel_path, parent_path, files):
    """Explain where key inputs came from and where outputs go next."""
    flow = []
    is_root = rel_path == "root"

    if files.get("goal.md"):
        source = "mission goal" if is_root else f"parent node {parent_path} plan"
        flow.append({
            "direction": "in",
            "artifact": "goal.md",
            "summary": f"Goal arrives from {source}.",
        })

    if files.get("knowledge.md"):
        flow.append({
            "direction": "in",
            "artifact": "knowledge.md",
            "summary": "Knowledge is produced by this node's retrieval pass and fed into the worker/planner prompt.",
        })

    instruction_files = [name for name in files if name.startswith("instructions-")]
    if instruction_files:
        flow.append({
            "direction": "in",
            "artifact": ", ".join(sorted(instruction_files)),
            "summary": "Instructions are generated by the orchestrator to define the node's current mode.",
        })

    if files.get("state.md"):
        flow.append({
            "direction": "out",
            "artifact": "state.md",
            "summary": "State is preserved so this node can be re-spawned with its prior reasoning intact.",
        })

    if files.get("plan.md"):
        flow.append({
            "direction": "out",
            "artifact": "plan.md",
            "summary": f"Plan is read by the orchestrator to create children under {rel_path}/children/...",
        })

    if files.get("review.md"):
        flow.append({
            "direction": "out",
            "artifact": "review.md",
            "summary": "Review is handed to the decider for this same node.",
        })

    if files.get("result.md"):
        destination = "mission result" if is_root else f"parent node {parent_path} for evaluation or synthesis"
        flow.append({
            "direction": "out",
            "artifact": "result.md",
            "summary": f"Final output flows to {destination}.",
        })

    if files.get("escalation.md"):
        destination = "mission-level failure handling" if is_root else f"parent node {parent_path}"
        flow.append({
            "direction": "out",
            "artifact": "escalation.md",
            "summary": f"Escalation is surfaced to {destination}.",
        })

    if files.get("eval-decision"):
        flow.append({
            "direction": "out",
            "artifact": "eval-decision",
            "summary": "Evaluation decision is consumed by the orchestrator to continue, replan, escalate, or synthesize.",
        })

    return flow


def resolve_root_node(mission_path):
    """Return (tree_root, root_node) for either current or legacy mission layouts."""
    current_root = mission_path / "tree" / "root"
    if current_root.exists():
        return mission_path / "tree", current_root

    legacy_signals = [
        mission_path / "goal.md",
        mission_path / "status",
        mission_path / "plan.md",
        mission_path / "children",
    ]
    if any(path.exists() for path in legacy_signals):
        return mission_path, mission_path

    return None, None


def scan_node(node_path, tree_root, depth=0):
    """Recursively scan a node directory into a dict."""
    rel = str(node_path.relative_to(tree_root))
    if rel == ".":
        rel = "root"
    name = node_path.name
    parent_path = compute_parent_path(node_path, tree_root)

    status = "unknown"
    status_text = read_first_existing(node_path, STATUS_PATHS)
    if status_text:
        status = status_text.strip() or "unknown"

    agent_mode = None
    agent_mode_text = read_first_existing(node_path, AGENT_MODE_PATHS)
    if agent_mode_text:
        agent_mode = agent_mode_text.strip() or None

    # Collect available files, normalized across legacy + current layouts.
    files = {}
    for label, candidates in FILE_CANDIDATES.items():
        contents = read_first_existing(node_path, candidates)
        if contents is not None:
            files[label] = contents

    artifacts = collect_artifacts(node_path)
    flow = build_flow_summary(rel, parent_path, files)

    # Scan children
    children = []
    children_dir = node_path / "children"
    if children_dir.is_dir():
        for child in sorted(children_dir.iterdir()):
            if child.is_dir() and not child.name.startswith("."):
                children.append(scan_node(child, tree_root, depth + 1))

    return {
        "name": name,
        "path": rel,
        "parent_path": parent_path,
        "status": status,
        "depth": depth,
        "agent_mode": agent_mode,
        "files": files,
        "artifacts": artifacts,
        "flow": flow,
        "children": children,
    }


def scan_events(mission_path):
    """Read orchestrator.jsonl into a list of event dicts."""
    jsonl = mission_path / "orchestrator.jsonl"
    events = []
    if jsonl.exists():
        for line in jsonl.read_text(errors="replace").strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return events


def scan_mission(mission_name):
    """Scan entire mission into JSON-serializable dict."""
    mission_path = MISSIONS_DIR / mission_name
    tree_root, root_node = resolve_root_node(mission_path)

    if not tree_root or not root_node or not root_node.exists():
        return {"error": f"No root node found in {mission_name}"}

    tree = scan_node(root_node, tree_root)
    events = scan_events(mission_path)

    return {
        "mission": mission_name,
        "tree": tree,
        "events": events,
    }


def list_missions():
    """List available missions."""
    missions = []
    if MISSIONS_DIR.is_dir():
        for d in sorted(MISSIONS_DIR.iterdir()):
            if d.name.startswith(".") or not d.is_dir():
                continue
            tree_root, root_node = resolve_root_node(d)
            if tree_root and root_node:
                missions.append(d.name)
    return missions


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self._handle_request(send_body=True)

    def do_HEAD(self):
        self._handle_request(send_body=False)

    def _handle_request(self, send_body):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/missions":
            self._json_response(list_missions(), send_body=send_body)
        elif path.startswith("/api/mission/"):
            name = path[len("/api/mission/"):]
            self._json_response(scan_mission(name), send_body=send_body)
        elif path == "/" or path == "/index.html":
            self._serve_file("index.html", "text/html", send_body=send_body)
        else:
            if send_body:
                super().do_GET()
            else:
                super().do_HEAD()

    def _json_response(self, data, send_body=True):
        body = json.dumps(data, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def _serve_file(self, filename, content_type, send_body=True):
        filepath = Path(__file__).parent / filename
        if not filepath.exists():
            self.send_error(404)
            return
        body = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def log_message(self, format, *args):
        # Quiet logging — only errors
        if args and "404" in str(args[0]):
            super().log_message(format, *args)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8777
    os.chdir(Path(__file__).parent)
    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    print(f"Eywa Visualizer running at http://localhost:{port}")
    print(f"Scanning missions from: {MISSIONS_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()
