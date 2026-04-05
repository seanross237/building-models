from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from runtime.config import load_config, repo_root


TERMINAL_STATUSES = {"complete", "escalated", "failed", "cancelled"}
SPAWNABLE_ROLES = {
    "librarian",
    "planner",
    "worker",
    "plan-reviewer",
    "plan-decider",
    "mid-plan-evaluator",
    "synthesizer",
}
ROLE_GUIDANCE = {
    "planner": [
        "stuff-for-agents/planning/planner/plan-design.md",
        "stuff-for-agents/planning/planner/execute-vs-plan.md",
    ],
    "mid-plan-evaluator": [
        "stuff-for-agents/planning/mid-plan-evaluator/continue-replan-escalate.md",
    ],
}


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def slugify_step_name(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {" ", "-", "_"} else " " for ch in name)
    parts = cleaned.replace("_", " ").split()
    return "-".join(parts) if parts else "step"


class Orchestrator:
    def __init__(self, mission_dir: Path) -> None:
        self.config = load_config()
        self.repo_root = repo_root()
        self.mission_dir = mission_dir.resolve()
        self.tree_root = self.mission_dir / "tree" / "root"
        self.log_file = self.mission_dir / "orchestrator.jsonl"

    def run(self) -> int:
        self._bootstrap_mission()
        print(f"Open-Eywa orchestrator: {self.mission_dir.name}")
        print(f"  dir={self.mission_dir}  log={self.log_file}")
        print("Entering main loop (Ctrl+C to stop)...")

        poll_interval = int(self.config["orchestrator"]["poll_interval_seconds"])
        chain_limit = int(self.config["orchestrator"]["max_status_chain"])

        while True:
            for node_path in self.find_all_nodes():
                for _ in range(chain_limit):
                    status = self.read_status(node_path)
                    if not status:
                        break
                    self.handle_status(node_path, status)
                    new_status = self.read_status(node_path)
                    if new_status == status:
                        break

            root_status = self.read_status(self.tree_root)
            if root_status == "complete":
                self.log_event(self.tree_root, "mission_complete")
                print("\nMission COMPLETE.")
                return 0
            if root_status == "failed":
                self.log_event(self.tree_root, "mission_failed")
                print("\nMission FAILED.")
                return 1
            if root_status == "escalated":
                self.log_event(self.tree_root, "mission_escalated")
                print("\nRoot ESCALATED.")
                return 1
            time.sleep(poll_interval)

    def _bootstrap_mission(self) -> None:
        if self.tree_root.exists():
            return
        goal_path = self.mission_dir / "mission-goal.md"
        if not goal_path.exists():
            raise RuntimeError(f"Mission goal not found: {goal_path}")
        for path in [
            self.tree_root / "input",
            self.tree_root / "output",
            self.tree_root / "for-orchestrator",
            self.tree_root / "system",
        ]:
            path.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(goal_path, self.tree_root / "input" / "goal.md")
        (self.tree_root / "for-orchestrator" / "agent-mode").write_text("planner", encoding="utf-8")
        (self.tree_root / "for-orchestrator" / "this-nodes-current-status").write_text(
            "pending", encoding="utf-8"
        )

    def log_event(
        self,
        node: Path,
        event: str,
        from_status: str = "",
        to_status: str = "",
        details: str = "",
    ) -> None:
        payload = {
            "ts": utc_now(),
            "node": str(node.resolve().relative_to(self.mission_dir.resolve())),
            "event": event,
            "from": from_status,
            "to": to_status,
            "details": details,
        }
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with self.log_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=True) + "\n")

    def read_status(self, node: Path) -> str:
        status_file = node / "for-orchestrator" / "this-nodes-current-status"
        return status_file.read_text(encoding="utf-8").strip() if status_file.exists() else ""

    def write_status(self, node: Path, expected: str, new: str) -> bool:
        status_file = node / "for-orchestrator" / "this-nodes-current-status"
        current = self.read_status(node)
        if current != expected:
            return False
        status_file.write_text(new, encoding="utf-8")
        self.log_event(node, "status_change", expected, new)
        return True

    def find_all_nodes(self) -> list[Path]:
        return sorted(
            path.parent.parent
            for path in self.mission_dir.rglob("this-nodes-current-status")
            if path.parent.name == "for-orchestrator"
        )

    def get_depth(self, node: Path) -> int:
        depth = 0
        rel = str(node.resolve().relative_to(self.tree_root.resolve()))
        for part in rel.split("/"):
            if part == "children":
                depth += 1
        return depth

    def spawn_role(self, node: Path, role: str) -> None:
        self.write_instructions(node, role)
        session_dir = node / "system"
        session_dir.mkdir(parents=True, exist_ok=True)
        stdout_path = session_dir / f"{role}-stdout.log"
        stderr_path = session_dir / f"{role}-stderr.log"
        stdout_handle = stdout_path.open("a", encoding="utf-8")
        stderr_handle = stderr_path.open("a", encoding="utf-8")
        process = subprocess.Popen(  # noqa: S603
            [
                sys.executable,
                str(self.repo_root / "system" / "scripts" / "run_agent.py"),
                role,
                str(node),
                str(self.mission_dir),
            ],
            cwd=str(self.repo_root),
            stdout=stdout_handle,
            stderr=stderr_handle,
            start_new_session=True,
        )
        stdout_handle.close()
        stderr_handle.close()
        metadata = {
            "pid": process.pid,
            "role": role,
            "started_at": utc_now(),
            "stdout": str(stdout_path),
            "stderr": str(stderr_path),
        }
        (node / "system" / "active-run.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        (node / "system" / "spawned-at.txt").write_text(str(time.time()), encoding="utf-8")
        self.log_event(node, "spawn", details=f"role={role} pid={process.pid}")

    def active_run(self, node: Path) -> dict[str, Any] | None:
        path = node / "system" / "active-run.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def process_alive(self, pid: int) -> bool:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        try:
            result = subprocess.run(  # noqa: S603
                ["ps", "-p", str(pid), "-o", "state="],
                capture_output=True,
                check=False,
                text=True,
            )
            if result.stdout.strip().startswith("Z"):
                return False
        except Exception:  # noqa: BLE001
            pass
        return True

    def stop_active_run(self, node: Path) -> None:
        metadata = self.active_run(node)
        if not metadata:
            return
        pid = int(metadata["pid"])
        try:
            os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

    def latest_activity_time(self, node: Path) -> float:
        latest = 0.0
        for directory in [node / "input", node / "output", node / "for-orchestrator", node / "system"]:
            if not directory.exists():
                continue
            for child in directory.rglob("*"):
                if child.is_file():
                    latest = max(latest, child.stat().st_mtime)
        return latest

    def check_zombie(self, node: Path) -> bool:
        run = self.active_run(node)
        if not run:
            return False
        pid = int(run["pid"])
        if not self.process_alive(pid):
            self.log_event(node, "process_dead", details=f"role={run['role']} pid={pid}")
            return False
        latest = self.latest_activity_time(node)
        timeout_seconds = int(self.config["orchestrator"]["zombie_timeout_seconds"])
        if latest and time.time() - latest < timeout_seconds:
            (node / "for-orchestrator" / ".zombie_state").write_text("0", encoding="utf-8")
            return True
        strike_path = node / "for-orchestrator" / ".zombie_state"
        strikes = int(strike_path.read_text(encoding="utf-8").strip()) if strike_path.exists() else 0
        strikes += 1
        strike_path.write_text(str(strikes), encoding="utf-8")
        if strikes == 1:
            self.log_event(node, "zombie_warning", details=f"role={run['role']} pid={pid}")
            return True
        if strikes == 2:
            self.log_event(node, "zombie_respawn", details=f"role={run['role']} pid={pid}")
            self.stop_active_run(node)
            time.sleep(1)
            self.spawn_role(node, run["role"])
            return True
        self.log_event(node, "zombie_failed", details=f"role={run['role']} pid={pid}")
        return False

    def role_prompt_paths(self, role: str) -> list[Path]:
        relative_paths = ROLE_GUIDANCE.get(role, [])
        return [self.repo_root / path for path in relative_paths]

    def child_output_paths(self, node: Path) -> list[Path]:
        return sorted(
            child / "output" / "final-output.md"
            for child in (node / "children").glob("step-*")
            if child.is_dir() and (child / "output" / "final-output.md").exists()
        )

    def write_instructions(self, node: Path, role: str) -> None:
        input_dir = node / "input"
        output_dir = node / "output"
        input_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        goal_path = input_dir / "parent-instructions.md"
        if not goal_path.exists():
            goal_path = input_dir / "goal.md"
        goal_content = goal_path.read_text(encoding="utf-8") if goal_path.exists() else ""
        knowledge_path = input_dir / "retrieved_relevant_knowledge_from_library.md"
        knowledge = knowledge_path.read_text(encoding="utf-8") if knowledge_path.exists() else ""
        state_path = output_dir / "state.md"
        state = state_path.read_text(encoding="utf-8") if state_path.exists() else ""
        latest_child = self.find_latest_terminal_child(node)
        latest_child_status = self.read_status(latest_child) if latest_child else ""
        latest_child_result = ""
        if latest_child:
            for candidate in [
                latest_child / "output" / "final-output.md",
                latest_child / "output" / "escalation.md",
                latest_child / "output" / "state.md",
            ]:
                if candidate.exists():
                    latest_child_result = candidate.read_text(encoding="utf-8")
                    break
        guidance = []
        for path in self.role_prompt_paths(role):
            if path.exists():
                guidance.append(path.read_text(encoding="utf-8"))
        guidance_text = "\n\n---\n\n".join(guidance)
        depth = self.get_depth(node)
        child_outputs = self.child_output_paths(node)
        child_output_list = "\n".join(f"- `{path}`" for path in child_outputs) or "- [No child outputs found yet]"
        instructions = {
            "librarian": (
                f"# Open-Eywa Instructions: librarian\n\n"
                f"Node: {node}\n\n"
                "Read `input/goal.md` or `input/parent-instructions.md`, navigate the library under "
                f"`{self.repo_root / 'stuff-for-agents/library'}`, and write "
                "`input/retrieved_relevant_knowledge_from_library.md`.\n"
            ),
            "planner": (
                "# Open-Eywa Instructions: planner\n\n"
                f"You are planning at depth {depth}.\n\n"
                "## Goal\n\n"
                f"{goal_content}\n\n"
                "## Library Knowledge\n\n"
                f"{knowledge}\n\n"
                "## Prior State\n\n"
                f"{state}\n\n"
                "## Guidance\n\n"
                f"{guidance_text}\n"
            ),
            "worker": (
                "# Open-Eywa Instructions: worker\n\n"
                f"You are executing at depth {depth}.\n\n"
                "## Goal\n\n"
                f"{goal_content}\n\n"
                "## Library Knowledge\n\n"
                f"{knowledge}\n\n"
                "Write `output/final-output.md` and `output/state.md`. If impossible, write `output/escalation.md`.\n"
            ),
            "plan-reviewer": (
                "# Open-Eywa Instructions: plan-reviewer\n\n"
                "Read the goal, `output/plan.md`, and retrieved knowledge, then write `output/review.md`.\n"
            ),
            "plan-decider": (
                "# Open-Eywa Instructions: plan-decider\n\n"
                "Read the goal, `output/plan.md`, `output/review.md`, and retrieved knowledge. "
                "Revise and approve the plan or write `output/escalation.md`. Always update `output/state.md`.\n"
            ),
            "mid-plan-evaluator": (
                "# Open-Eywa Instructions: mid-plan-evaluator\n\n"
                "Decide whether this node should `continue`, `replan`, or `escalate`.\n\n"
                "If prior state is missing, proceed using the plan and child result.\n\n"
                "## Current Plan\n\n"
                f"{(output_dir / 'plan.md').read_text(encoding='utf-8') if (output_dir / 'plan.md').exists() else ''}\n\n"
                "## Current State\n\n"
                f"{state or '[No state.md exists yet]'}\n\n"
                "## Latest Child Status\n\n"
                f"{latest_child_status or '[No terminal child found]'}\n\n"
                "## Latest Child Result\n\n"
                f"{latest_child_result or '[No child result file found]'}\n\n"
                "Write `for-orchestrator/eval-decision` with one of: `continue`, `replan`, or `escalate`.\n"
                "Also update `output/state.md`.\n\n"
                f"{guidance_text}\n"
            ),
            "synthesizer": (
                "# Open-Eywa Instructions: synthesizer\n\n"
                "Read these exact files before synthesizing:\n\n"
                f"- Goal: `{input_dir / 'goal.md'}` or `{input_dir / 'parent-instructions.md'}`\n"
                f"- Plan: `{output_dir / 'plan.md'}`\n"
                f"- State: `{output_dir / 'state.md'}`\n"
                "- Child final outputs:\n"
                f"{child_output_list}\n\n"
                "Then write:\n"
                "- `output/final-output.md`\n"
                "- `for-orchestrator/eval-decision` containing exactly `synthesize`\n"
                "- `output/state.md`\n\n"
                "Do not write a placeholder. If some inputs are missing, use the ones that exist and say exactly what was missing.\n"
            ),
        }[role]
        (input_dir / f"instructions-{role}.md").write_text(instructions, encoding="utf-8")

    def get_plan_review_tier(self, node: Path) -> str:
        plan = node / "output" / "plan.md"
        if not plan.exists():
            return "low"
        for line in plan.read_text(encoding="utf-8").splitlines():
            if line.startswith("Review:"):
                return line.split(":", 1)[1].strip() or "low"
        return "low"

    def plan_is_approved(self, node: Path) -> bool:
        plan = node / "output" / "plan.md"
        return plan.exists() and "Status: approved" in plan.read_text(encoding="utf-8")

    def parse_next_step(self, node: Path) -> tuple[str, str, str, int, int] | None:
        plan_path = node / "output" / "plan.md"
        if not plan_path.exists():
            return None
        cdir = node / "children"
        current_step: dict[str, Any] | None = None
        in_goal = False
        for raw_line in plan_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.rstrip()
            if line.startswith("### Step "):
                if current_step and current_step.get("goal"):
                    directory_name = (
                        f"step-{int(current_step['number']):02d}-"
                        f"{slugify_step_name(current_step['name'])}"
                    )
                    if not (cdir / directory_name).exists():
                        return (
                            current_step["number"],
                            current_step["name"],
                            current_step["goal"].strip(),
                            int(current_step.get("complexity", 5)),
                            int(current_step.get("importance", 5)),
                        )
                number_name = line.split("### Step ", 1)[1]
                number, name = number_name.split(":", 1)
                current_step = {"number": number.strip(), "name": name.strip()}
                in_goal = False
                continue
            if current_step is None:
                continue
            if line.startswith("Goal:"):
                current_step["goal"] = line.split(":", 1)[1].strip()
                in_goal = True
                continue
            if line.startswith("Complexity:"):
                current_step["complexity"] = line.split(":", 1)[1].strip()
                in_goal = False
                continue
            if line.startswith("Importance:"):
                current_step["importance"] = line.split(":", 1)[1].strip()
                in_goal = False
                continue
            if in_goal and not any(
                line.startswith(prefix)
                for prefix in ("Dependencies:", "Independent:", "Confidence:", "Verifiable:", "### Step ")
            ):
                current_step["goal"] += "\n" + line
            else:
                in_goal = False
        if current_step and current_step.get("goal"):
            directory_name = (
                f"step-{int(current_step['number']):02d}-"
                f"{slugify_step_name(current_step['name'])}"
            )
            if not (cdir / directory_name).exists():
                return (
                    current_step["number"],
                    current_step["name"],
                    current_step["goal"].strip(),
                    int(current_step.get("complexity", 5)),
                    int(current_step.get("importance", 5)),
                )
        return None

    def all_steps_terminal(self, node: Path) -> bool:
        plan_path = node / "output" / "plan.md"
        if not plan_path.exists():
            return False
        total = sum(1 for line in plan_path.read_text(encoding="utf-8").splitlines() if line.startswith("### Step "))
        if total == 0:
            return False
        terminal = 0
        for child in sorted((node / "children").glob("step-*")):
            if child.is_dir() and self.read_status(child) in TERMINAL_STATUSES:
                terminal += 1
        return terminal >= total

    def find_active_child(self, node: Path) -> Path | None:
        for child in sorted((node / "children").glob("step-*")):
            if child.is_dir() and self.read_status(child) not in TERMINAL_STATUSES:
                return child
        return None

    def find_latest_terminal_child(self, node: Path) -> Path | None:
        candidates = []
        for child in sorted((node / "children").glob("step-*")):
            if child.is_dir() and self.read_status(child) in {"complete", "escalated", "failed"}:
                candidates.append(child)
        if not candidates:
            return None
        return max(candidates, key=lambda path: (path / "for-orchestrator" / "this-nodes-current-status").stat().st_mtime)

    def cancel_pending_children(self, node: Path) -> None:
        for child in sorted((node / "children").glob("step-*")):
            if not child.is_dir():
                continue
            status = self.read_status(child)
            if status in {"complete", "cancelled", "failed"}:
                continue
            self.write_status(child, status, "cancelled")
            self.stop_active_run(child)

    def create_child(self, node: Path, step_number: str, short_name: str, goal: str, complexity: int, importance: int) -> None:
        child_name = f"step-{int(step_number):02d}-{slugify_step_name(short_name)}"
        child = node / "children" / child_name
        if child.exists():
            return
        for subdir in ["input", "output", "for-orchestrator", "system"]:
            (child / subdir).mkdir(parents=True, exist_ok=True)
        (child / "input" / "parent-instructions.md").write_text(goal, encoding="utf-8")
        depth = self.get_depth(child)
        adj_c = max(1, complexity - depth)
        adj_i = max(1, importance - depth)
        child_role = "planner" if adj_c * adj_i > int(self.config["orchestrator"]["plan_threshold"]) else "worker"
        if depth >= int(self.config["orchestrator"]["max_depth"]):
            child_role = "worker"
        (child / "for-orchestrator" / "agent-mode").write_text(child_role, encoding="utf-8")
        (child / "for-orchestrator" / "this-nodes-current-status").write_text("pending", encoding="utf-8")
        self.log_event(
            node,
            "child_created",
            details=f"child={child_name} C={complexity} I={importance} depth={depth} role={child_role}",
        )

    def handle_status(self, node: Path, status: str) -> None:
        handlers = {
            "pending": self.handle_pending,
            "retrieving": self.handle_retrieving,
            "running": self.handle_running,
            "needs_review": self.handle_needs_review,
            "reviewing": self.handle_reviewing,
            "needs_decision": self.handle_needs_decision,
            "deciding": self.handle_deciding,
            "approved": self.handle_approved,
            "executing": self.handle_executing,
            "evaluating": self.handle_evaluating,
            "waiting_comp": self.handle_waiting_comp,
            "cancelled": self.handle_cancelled,
        }
        handler = handlers.get(status)
        if handler:
            handler(node)

    def handle_pending(self, node: Path) -> None:
        if self.write_status(node, "pending", "retrieving"):
            self.spawn_role(node, "librarian")

    def handle_retrieving(self, node: Path) -> None:
        if (node / "input" / "retrieved_relevant_knowledge_from_library.md").exists():
            role = (node / "for-orchestrator" / "agent-mode").read_text(encoding="utf-8").strip()
            if self.write_status(node, "retrieving", "running"):
                self.spawn_role(node, role)
            return
        if not self.check_zombie(node):
            self.write_status(node, "retrieving", "failed")

    def handle_running(self, node: Path) -> None:
        if (node / "output" / "escalation.md").exists():
            self.write_status(node, "running", "escalated")
            return
        if (node / "output" / "final-output.md").exists():
            self.write_status(node, "running", "complete")
            return
        if (node / "output" / "plan.md").exists():
            if self.get_depth(node) >= int(self.config["orchestrator"]["max_depth"]):
                self.write_status(node, "running", "failed")
                return
            tier = self.get_plan_review_tier(node)
            if tier == "low":
                plan_path = node / "output" / "plan.md"
                content = plan_path.read_text(encoding="utf-8")
                if "Status: approved" not in content:
                    plan_path.write_text(content.replace("Status: draft", "Status: approved"), encoding="utf-8")
                self.write_status(node, "running", "approved")
            else:
                self.write_status(node, "running", "needs_review")
            return
        if (node / "for-orchestrator" / "WAITING_FOR_COMPUTATION").exists():
            self.stop_active_run(node)
            self.write_status(node, "running", "waiting_comp")
            return
        if not self.check_zombie(node):
            self.write_status(node, "running", "failed")

    def handle_needs_review(self, node: Path) -> None:
        if self.write_status(node, "needs_review", "reviewing"):
            self.spawn_role(node, "plan-reviewer")

    def handle_reviewing(self, node: Path) -> None:
        if (node / "output" / "review.md").exists():
            self.write_status(node, "reviewing", "needs_decision")
            return
        if not self.check_zombie(node):
            self.write_status(node, "reviewing", "failed")

    def handle_needs_decision(self, node: Path) -> None:
        if self.write_status(node, "needs_decision", "deciding"):
            self.spawn_role(node, "plan-decider")

    def handle_deciding(self, node: Path) -> None:
        if self.plan_is_approved(node):
            self.write_status(node, "deciding", "approved")
            return
        if (node / "output" / "escalation.md").exists():
            self.write_status(node, "deciding", "escalated")
            return
        if not self.check_zombie(node):
            self.write_status(node, "deciding", "failed")

    def handle_approved(self, node: Path) -> None:
        next_step = self.parse_next_step(node)
        if not next_step:
            self.write_status(node, "approved", "failed")
            return
        self.create_child(node, *next_step)
        self.write_status(node, "approved", "executing")

    def handle_executing(self, node: Path) -> None:
        if self.find_active_child(node):
            return
        child = self.find_latest_terminal_child(node)
        if not child:
            return
        child_status = self.read_status(child)
        if child_status == "complete":
            role = "synthesizer" if self.all_steps_terminal(node) else "mid-plan-evaluator"
            if self.write_status(node, "executing", "evaluating"):
                decision_file = node / "for-orchestrator" / "eval-decision"
                if decision_file.exists():
                    decision_file.unlink()
                self.spawn_role(node, role)
        elif child_status in {"escalated", "failed"}:
            if self.write_status(node, "executing", "evaluating"):
                decision_file = node / "for-orchestrator" / "eval-decision"
                if decision_file.exists():
                    decision_file.unlink()
                self.spawn_role(node, "mid-plan-evaluator")

    def handle_evaluating(self, node: Path) -> None:
        decision_file = node / "for-orchestrator" / "eval-decision"
        if (node / "output" / "final-output.md").exists() and not decision_file.exists():
            self.write_status(node, "evaluating", "complete")
            return
        if not decision_file.exists():
            if not self.check_zombie(node):
                self.write_status(node, "evaluating", "failed")
            return
        decision = decision_file.read_text(encoding="utf-8").strip()
        if decision == "continue":
            next_step = self.parse_next_step(node)
            if next_step:
                self.create_child(node, *next_step)
                context_file = node / "output" / "context-for-next-step.md"
                if context_file.exists():
                    child_name = f"step-{int(next_step[0]):02d}-{next_step[1]}"
                    child_name = f"step-{int(next_step[0]):02d}-{slugify_step_name(next_step[1])}"
                    pi = node / "children" / child_name / "input" / "parent-instructions.md"
                    pi.write_text(pi.read_text(encoding="utf-8") + "\n\n## Context From Prior Steps\n\n" + context_file.read_text(encoding="utf-8"), encoding="utf-8")
                    context_file.unlink()
            decision_file.unlink()
            self.write_status(node, "evaluating", "executing")
            return
        if decision == "replan":
            self.cancel_pending_children(node)
            decision_file.unlink()
            self.write_status(node, "evaluating", "approved")
            return
        if decision == "escalate":
            self.cancel_pending_children(node)
            decision_file.unlink()
            self.write_status(node, "evaluating", "escalated")
            return
        if decision == "synthesize":
            if (node / "output" / "final-output.md").exists():
                decision_file.unlink()
                self.write_status(node, "evaluating", "complete")
                return
            if not self.check_zombie(node):
                self.write_status(node, "evaluating", "failed")

    def handle_waiting_comp(self, node: Path) -> None:
        result_marker = node / "for-orchestrator" / "computation_result"
        waiting_marker = node / "for-orchestrator" / "WAITING_FOR_COMPUTATION"
        if result_marker.exists():
            if waiting_marker.exists():
                waiting_marker.unlink()
            role = (node / "for-orchestrator" / "agent-mode").read_text(encoding="utf-8").strip()
            if self.write_status(node, "waiting_comp", "running"):
                self.spawn_role(node, role)
            return
        if waiting_marker.exists():
            elapsed = time.time() - waiting_marker.stat().st_mtime
            limit = int(self.config["orchestrator"]["background_timeout_seconds"])
            if elapsed > limit:
                self.log_event(node, "background_timeout", details=f"elapsed={elapsed:.0f}s")
                self.write_status(node, "waiting_comp", "failed")

    def handle_cancelled(self, node: Path) -> None:
        self.stop_active_run(node)


def main(mission_directory: str) -> int:
    orchestrator = Orchestrator(Path(mission_directory))
    return orchestrator.run()
