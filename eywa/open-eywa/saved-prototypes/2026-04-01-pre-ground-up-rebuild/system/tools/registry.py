from __future__ import annotations

import glob as globlib
import json
import os
import re
import shlex
import subprocess
import time
from pathlib import Path
from typing import Any
from uuid import uuid4


class ToolError(RuntimeError):
    pass


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class ToolRegistry:
    def __init__(
        self,
        *,
        repo_root: Path,
        mission_dir: Path,
        node_path: Path,
        role: str,
        tool_names: list[str],
        preview_chars: int,
    ) -> None:
        self.repo_root = repo_root
        self.mission_dir = mission_dir
        self.node_path = node_path
        self.role = role
        self.tool_names = tool_names
        self.preview_chars = preview_chars
        self.node_system_dir = self.node_path / "system"
        self.jobs_dir = self.node_system_dir / "jobs"
        self.artifacts_dir = self.node_system_dir / "artifacts"
        self.tool_log_path = self.node_system_dir / "tool-log.jsonl"
        self.mission_tool_log_path = self.mission_dir / "tools.jsonl"
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def schemas(self) -> list[dict[str, Any]]:
        return [self._schema(name) for name in self.tool_names]

    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        if name not in self.tool_names:
            raise ToolError(f"Tool '{name}' is not enabled for role '{self.role}'.")
        method = getattr(self, f"_tool_{name}", None)
        if method is None:
            raise ToolError(f"Unknown tool '{name}'.")
        start = time.time()
        try:
            result = method(arguments)
            self._log_tool_call(name, arguments, result, "ok", time.time() - start)
            return result
        except Exception as exc:  # noqa: BLE001
            payload = {"error": str(exc), "type": type(exc).__name__}
            self._log_tool_call(name, arguments, payload, "error", time.time() - start)
            raise

    def _schema(self, name: str) -> dict[str, Any]:
        schemas: dict[str, dict[str, Any]] = {
            "read_file": {
                "description": "Read a UTF-8 text file from the repo.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            },
            "write_file": {
                "description": "Write UTF-8 text to a file under the current node directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["path", "content"],
                },
            },
            "edit_file": {
                "description": "Replace text inside a file under the current node directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "find_text": {"type": "string"},
                        "replace_text": {"type": "string"},
                        "replace_all": {"type": "boolean"},
                    },
                    "required": ["path", "find_text", "replace_text"],
                },
            },
            "glob": {
                "description": "Glob for files relative to the current node directory or an absolute repo path.",
                "parameters": {
                    "type": "object",
                    "properties": {"pattern": {"type": "string"}},
                    "required": ["pattern"],
                },
            },
            "grep": {
                "description": "Search text within files under a directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string"},
                        "path": {"type": "string"},
                    },
                    "required": ["pattern", "path"],
                },
            },
            "run_shell": {
                "description": "Run a shell command from the node directory or a child directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"},
                        "cwd": {"type": "string"},
                        "timeout_seconds": {"type": "integer"},
                    },
                    "required": ["command"],
                },
            },
            "run_python": {
                "description": "Run Python code or a Python script and capture the result.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "script_path": {"type": "string"},
                        "args": {"type": "array", "items": {"type": "string"}},
                        "timeout_seconds": {"type": "integer"},
                    },
                },
            },
            "run_sage": {
                "description": "Run Sage code or a Sage script and capture the result.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "script_path": {"type": "string"},
                        "args": {"type": "array", "items": {"type": "string"}},
                        "timeout_seconds": {"type": "integer"},
                    },
                },
            },
            "run_lean": {
                "description": "Run Lean on a generated or existing .lean file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "script_path": {"type": "string"},
                        "timeout_seconds": {"type": "integer"},
                    },
                },
            },
            "start_background_job": {
                "description": "Start a long-running shell command as a background job.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"},
                        "cwd": {"type": "string"},
                        "label": {"type": "string"},
                    },
                    "required": ["command"],
                },
            },
            "check_background_job": {
                "description": "Check the status of a background job by job id.",
                "parameters": {
                    "type": "object",
                    "properties": {"job_id": {"type": "string"}},
                    "required": ["job_id"],
                },
            },
            "cancel_background_job": {
                "description": "Cancel a background job by job id.",
                "parameters": {
                    "type": "object",
                    "properties": {"job_id": {"type": "string"}},
                    "required": ["job_id"],
                },
            },
        }
        entry = schemas[name]
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": entry["description"],
                "parameters": entry["parameters"],
            },
        }

    def _resolve_read_path(self, raw_path: str) -> Path:
        path = Path(raw_path)
        resolved = (self.node_path / path).resolve() if not path.is_absolute() else path.resolve()
        if self.repo_root not in resolved.parents and resolved != self.repo_root:
            raise ToolError(f"Path '{resolved}' is outside the Open-Eywa repo.")
        return resolved

    def _resolve_write_path(self, raw_path: str) -> Path:
        path = Path(raw_path)
        resolved = (self.node_path / path).resolve() if not path.is_absolute() else path.resolve()
        if self.node_path not in resolved.parents and resolved != self.node_path:
            raise ToolError(f"Writable path '{resolved}' must stay inside the current node.")
        resolved.parent.mkdir(parents=True, exist_ok=True)
        return resolved

    def _resolve_cwd(self, raw_cwd: str | None) -> Path:
        if not raw_cwd:
            return self.node_path
        return self._resolve_read_path(raw_cwd)

    def _preview_text(self, text: str) -> str:
        return text[: self.preview_chars]

    def _run_sync(self, command: list[str], cwd: Path, timeout_seconds: int) -> dict[str, Any]:
        try:
            completed = subprocess.run(
                command,
                cwd=str(cwd),
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
            return {
                "command": command,
                "cwd": str(cwd),
                "returncode": completed.returncode,
                "stdout": self._preview_text(completed.stdout),
                "stderr": self._preview_text(completed.stderr),
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "command": command,
                "cwd": str(cwd),
                "returncode": 124,
                "stdout": self._preview_text(exc.stdout or ""),
                "stderr": self._preview_text((exc.stderr or "") + f"\nTimed out after {timeout_seconds}s"),
            }

    def _tool_read_file(self, arguments: dict[str, Any]) -> Any:
        path = self._resolve_read_path(arguments["path"])
        return {"path": str(path), "content": path.read_text(encoding="utf-8")}

    def _tool_write_file(self, arguments: dict[str, Any]) -> Any:
        path = self._resolve_write_path(arguments["path"])
        path.write_text(arguments["content"], encoding="utf-8")
        return {"path": str(path), "bytes_written": len(arguments["content"].encode("utf-8"))}

    def _tool_edit_file(self, arguments: dict[str, Any]) -> Any:
        path = self._resolve_write_path(arguments["path"])
        original = path.read_text(encoding="utf-8")
        find_text = arguments["find_text"]
        replace_text = arguments["replace_text"]
        replace_all = bool(arguments.get("replace_all", False))
        if find_text not in original:
            raise ToolError("find_text was not found in the file.")
        if replace_all:
            updated = original.replace(find_text, replace_text)
            replacements = original.count(find_text)
        else:
            updated = original.replace(find_text, replace_text, 1)
            replacements = 1
        path.write_text(updated, encoding="utf-8")
        return {"path": str(path), "replacements": replacements}

    def _tool_glob(self, arguments: dict[str, Any]) -> Any:
        pattern = arguments["pattern"]
        if pattern.startswith("/"):
            files = globlib.glob(pattern, recursive=True)
        else:
            files = globlib.glob(str(self.node_path / pattern), recursive=True)
        return {"matches": sorted(files)[:500]}

    def _tool_grep(self, arguments: dict[str, Any]) -> Any:
        regex = re.compile(arguments["pattern"])
        base = self._resolve_read_path(arguments["path"])
        if base.is_file():
            files = [base]
        else:
            files = [path for path in base.rglob("*") if path.is_file()]
        matches: list[dict[str, Any]] = []
        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for index, line in enumerate(content.splitlines(), start=1):
                if regex.search(line):
                    matches.append(
                        {"path": str(file_path), "line": index, "text": self._preview_text(line)}
                    )
                    if len(matches) >= 200:
                        return {"matches": matches}
        return {"matches": matches}

    def _tool_run_shell(self, arguments: dict[str, Any]) -> Any:
        command = arguments["command"]
        cwd = self._resolve_cwd(arguments.get("cwd"))
        timeout_seconds = int(arguments.get("timeout_seconds", 60))
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        return {
            "command": command,
            "cwd": str(cwd),
            "returncode": completed.returncode,
            "stdout": self._preview_text(completed.stdout),
            "stderr": self._preview_text(completed.stderr),
        }

    def _write_generated_script(self, kind: str, suffix: str, content: str) -> Path:
        target_dir = self.artifacts_dir / kind
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{kind}-{uuid4().hex}{suffix}"
        path.write_text(content, encoding="utf-8")
        return path

    def _tool_run_python(self, arguments: dict[str, Any]) -> Any:
        timeout_seconds = int(arguments.get("timeout_seconds", 120))
        args = list(arguments.get("args", []))
        if arguments.get("code"):
            script = self._write_generated_script("python", ".py", arguments["code"])
        elif arguments.get("script_path"):
            script = self._resolve_read_path(arguments["script_path"])
        else:
            raise ToolError("run_python requires either code or script_path.")
        return self._run_sync(["python3", str(script), *args], self.node_path, timeout_seconds)

    def _tool_run_sage(self, arguments: dict[str, Any]) -> Any:
        timeout_seconds = int(arguments.get("timeout_seconds", 120))
        args = list(arguments.get("args", []))
        if arguments.get("code"):
            script = self._write_generated_script("sage", ".sage", arguments["code"])
        elif arguments.get("script_path"):
            script = self._resolve_read_path(arguments["script_path"])
        else:
            raise ToolError("run_sage requires either code or script_path.")
        return self._run_sync(["sage", str(script), *args], self.node_path, timeout_seconds)

    def _tool_run_lean(self, arguments: dict[str, Any]) -> Any:
        timeout_seconds = int(arguments.get("timeout_seconds", 120))
        if arguments.get("code"):
            script = self._write_generated_script("lean", ".lean", arguments["code"])
        elif arguments.get("script_path"):
            script = self._resolve_read_path(arguments["script_path"])
        else:
            raise ToolError("run_lean requires either code or script_path.")
        return self._run_sync(["lean", str(script)], self.node_path, timeout_seconds)

    def _job_dir(self, job_id: str) -> Path:
        return self.jobs_dir / job_id

    def _job_status(self, job_dir: Path) -> dict[str, Any]:
        stdout_path = job_dir / "stdout.txt"
        stderr_path = job_dir / "stderr.txt"
        status_path = job_dir / "status.txt"
        pid_path = job_dir / "pid.txt"
        result = {
            "job_id": job_dir.name,
            "status": status_path.read_text(encoding="utf-8").strip() if status_path.exists() else "unknown",
            "stdout": self._preview_text(stdout_path.read_text(encoding="utf-8")) if stdout_path.exists() else "",
            "stderr": self._preview_text(stderr_path.read_text(encoding="utf-8")) if stderr_path.exists() else "",
        }
        if pid_path.exists():
            result["pid"] = int(pid_path.read_text(encoding="utf-8").strip())
        return result

    def _tool_start_background_job(self, arguments: dict[str, Any]) -> Any:
        job_id = arguments.get("label") or f"job-{uuid4().hex[:10]}"
        job_dir = self._job_dir(job_id)
        if job_dir.exists():
            raise ToolError(f"Background job '{job_id}' already exists.")
        job_dir.mkdir(parents=True, exist_ok=True)
        command = arguments["command"]
        cwd = self._resolve_cwd(arguments.get("cwd"))
        (job_dir / "command.txt").write_text(command, encoding="utf-8")
        (job_dir / "cwd.txt").write_text(str(cwd), encoding="utf-8")
        (job_dir / "status.txt").write_text("running", encoding="utf-8")
        (job_dir / "started_at.txt").write_text(_now(), encoding="utf-8")
        stdout_path = job_dir / "stdout.txt"
        stderr_path = job_dir / "stderr.txt"
        script_path = job_dir / "run.sh"
        wait_marker = self.node_path / "for-orchestrator" / "WAITING_FOR_COMPUTATION"
        result_marker = self.node_path / "for-orchestrator" / "computation_result"
        wait_marker.parent.mkdir(parents=True, exist_ok=True)
        wait_marker.write_text(job_id, encoding="utf-8")
        script = f"""#!/bin/sh
cd {shlex.quote(str(cwd))} || exit 99
/bin/sh -lc {shlex.quote(command)} > {shlex.quote(str(stdout_path))} 2> {shlex.quote(str(stderr_path))}
status=$?
printf '%s' "$status" > {shlex.quote(str(job_dir / "returncode.txt"))}
date -u +%Y-%m-%dT%H:%M:%SZ > {shlex.quote(str(job_dir / "finished_at.txt"))}
if [ "$status" -eq 0 ]; then
  printf '%s' "completed" > {shlex.quote(str(job_dir / "status.txt"))}
else
  printf '%s' "failed" > {shlex.quote(str(job_dir / "status.txt"))}
fi
printf '%s' {shlex.quote(str(job_dir))} > {shlex.quote(str(result_marker))}
"""
        script_path.write_text(script, encoding="utf-8")
        os.chmod(script_path, 0o755)
        process = subprocess.Popen(  # noqa: S603
            ["/bin/sh", str(script_path)],
            cwd=str(self.node_path),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        (job_dir / "pid.txt").write_text(str(process.pid), encoding="utf-8")
        return {"job_id": job_id, "pid": process.pid, "job_dir": str(job_dir)}

    def _tool_check_background_job(self, arguments: dict[str, Any]) -> Any:
        job_dir = self._job_dir(arguments["job_id"])
        if not job_dir.exists():
            raise ToolError(f"Background job '{arguments['job_id']}' does not exist.")
        return self._job_status(job_dir)

    def _tool_cancel_background_job(self, arguments: dict[str, Any]) -> Any:
        job_dir = self._job_dir(arguments["job_id"])
        if not job_dir.exists():
            raise ToolError(f"Background job '{arguments['job_id']}' does not exist.")
        pid_path = job_dir / "pid.txt"
        if not pid_path.exists():
            raise ToolError("Job pid is missing.")
        pid = int(pid_path.read_text(encoding="utf-8").strip())
        try:
            os.killpg(pid, 15)
        except ProcessLookupError:
            pass
        (job_dir / "status.txt").write_text("cancelled", encoding="utf-8")
        (job_dir / "finished_at.txt").write_text(_now(), encoding="utf-8")
        wait_marker = self.node_path / "for-orchestrator" / "WAITING_FOR_COMPUTATION"
        if wait_marker.exists() and wait_marker.read_text(encoding="utf-8").strip() == arguments["job_id"]:
            wait_marker.unlink()
        return {"job_id": arguments["job_id"], "status": "cancelled"}

    def _log_tool_call(
        self,
        name: str,
        arguments: dict[str, Any],
        result: Any,
        status: str,
        duration_seconds: float,
    ) -> None:
        entry = {
            "ts": _now(),
            "role": self.role,
            "node": str(self.node_path.relative_to(self.mission_dir)),
            "tool": name,
            "status": status,
            "duration_seconds": round(duration_seconds, 3),
            "arguments": arguments,
            "result_preview": self._preview_text(json.dumps(result, ensure_ascii=True)),
        }
        for path in (self.tool_log_path, self.mission_tool_log_path):
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=True) + "\n")
