from __future__ import annotations

from dataclasses import dataclass, field
import re
from pathlib import Path
from typing import Any


class ToolExecutionError(RuntimeError):
    """Raised when a tool call violates the file-tool contract."""


@dataclass(frozen=True)
class ToolCallResult:
    tool_name: str
    output: dict[str, Any] = field(default_factory=dict)
    artifact_paths: tuple[str, ...] = ()


class FileToolExecutor:
    """Small node-bounded file tool executor for the rebuild runtime seam."""

    TOOL_NAMES: tuple[str, ...] = (
        "read_file",
        "write_file",
        "edit_file",
        "glob",
        "grep",
    )

    def execute(
        self,
        node_root: str | Path,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ) -> ToolCallResult:
        root = Path(node_root).expanduser().resolve()
        args = dict(arguments or {})
        if tool_name not in self.TOOL_NAMES:
            raise ToolExecutionError(f"Unsupported tool name: {tool_name!r}.")

        if tool_name == "read_file":
            return self._read_file(root, args)
        if tool_name == "write_file":
            return self._write_file(root, args)
        if tool_name == "edit_file":
            return self._edit_file(root, args)
        if tool_name == "glob":
            return self._glob(root, args)
        return self._grep(root, args)

    def _read_file(self, root: Path, arguments: dict[str, Any]) -> ToolCallResult:
        path = self._resolve_node_relative_path(root, self._required_string(arguments, "path"))
        if not path.exists():
            raise ToolExecutionError(f"read_file target does not exist: {path!s}.")
        if not path.is_file():
            raise ToolExecutionError(f"read_file target is not a file: {path!s}.")
        return ToolCallResult(
            tool_name="read_file",
            output={
                "path": str(path.relative_to(root)),
                "content": path.read_text(encoding="utf-8"),
            },
        )

    def _write_file(self, root: Path, arguments: dict[str, Any]) -> ToolCallResult:
        path = self._resolve_node_relative_path(root, self._required_string(arguments, "path"))
        content = self._required_string(arguments, "content", allow_empty=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        relative_path = str(path.relative_to(root))
        return ToolCallResult(
            tool_name="write_file",
            output={"path": relative_path, "bytes_written": len(content.encode("utf-8"))},
            artifact_paths=(relative_path,),
        )

    def _edit_file(self, root: Path, arguments: dict[str, Any]) -> ToolCallResult:
        path = self._resolve_node_relative_path(root, self._required_string(arguments, "path"))
        find_text = self._required_string(arguments, "find_text", allow_empty=False)
        replace_text = self._required_string(arguments, "replace_text", allow_empty=True)
        replace_all = bool(arguments.get("replace_all", False))

        if not path.exists():
            raise ToolExecutionError(f"edit_file target does not exist: {path!s}.")
        original = path.read_text(encoding="utf-8")
        if find_text not in original:
            raise ToolExecutionError("edit_file could not find the requested text.")

        if replace_all:
            updated = original.replace(find_text, replace_text)
            replacement_count = original.count(find_text)
        else:
            updated = original.replace(find_text, replace_text, 1)
            replacement_count = 1

        path.write_text(updated, encoding="utf-8")
        relative_path = str(path.relative_to(root))
        return ToolCallResult(
            tool_name="edit_file",
            output={"path": relative_path, "replacement_count": replacement_count},
            artifact_paths=(relative_path,),
        )

    def _glob(self, root: Path, arguments: dict[str, Any]) -> ToolCallResult:
        pattern = self._required_string(arguments, "pattern")
        include_directories = bool(arguments.get("include_directories", False))
        matches = [
            str(path.relative_to(root))
            for path in sorted(root.glob(pattern))
            if include_directories or path.is_file()
        ]
        return ToolCallResult(
            tool_name="glob",
            output={"pattern": pattern, "matches": matches, "match_count": len(matches)},
        )

    def _grep(self, root: Path, arguments: dict[str, Any]) -> ToolCallResult:
        pattern = self._required_string(arguments, "pattern")
        start_path = arguments.get("start_path", ".")
        case_sensitive = bool(arguments.get("case_sensitive", True))
        regex = re.compile(pattern, 0 if case_sensitive else re.IGNORECASE)

        search_root = self._resolve_node_relative_path(root, str(start_path))
        if not search_root.exists():
            raise ToolExecutionError(f"grep start_path does not exist: {search_root!s}.")
        if search_root.is_file():
            candidate_files = [search_root]
        else:
            candidate_files = [path for path in sorted(search_root.rglob("*")) if path.is_file()]

        matches: list[dict[str, Any]] = []
        for file_path in candidate_files:
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for line_number, line in enumerate(content.splitlines(), start=1):
                if regex.search(line):
                    matches.append(
                        {
                            "path": str(file_path.relative_to(root)),
                            "line_number": line_number,
                            "line": line,
                        }
                    )

        return ToolCallResult(
            tool_name="grep",
            output={"pattern": pattern, "matches": matches, "match_count": len(matches)},
        )

    def _resolve_node_relative_path(self, node_root: Path, relative_path: str) -> Path:
        candidate = (node_root / relative_path).expanduser().resolve()
        try:
            candidate.relative_to(node_root)
        except ValueError as exc:
            raise ToolExecutionError(
                f"Path escapes the node boundary: {relative_path!r}."
            ) from exc
        return candidate

    def _required_string(
        self,
        arguments: dict[str, Any],
        field_name: str,
        *,
        allow_empty: bool = False,
    ) -> str:
        value = arguments.get(field_name)
        if not isinstance(value, str):
            raise ToolExecutionError(f"{field_name} must be a string.")
        if not allow_empty and not value:
            raise ToolExecutionError(f"{field_name} must be non-empty.")
        return value
