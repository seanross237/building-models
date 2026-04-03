"""Build a provider-neutral runtime task file from prompt bundle + prepared context.

The task file is a markdown document that any CLI runtime can consume.
It packages the system prompt, support documents, prepared context packets,
and artifact requirements into one inspectable file on disk.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from system.orchestrator.role_contracts import role_contract_for

from .prompt_loader import PromptBundle
from .runtime_interface import RuntimeRequest


class RuntimeTaskBuildError(ValueError):
    """Raised when the task file cannot be assembled."""


def load_prepared_packet(path: str) -> dict[str, Any]:
    """Load and validate a single prepared context packet from disk."""
    packet_path = Path(path).expanduser().resolve()
    if not packet_path.exists():
        raise RuntimeTaskBuildError(
            f"Prepared input packet does not exist: {packet_path!s}."
        )
    try:
        return json.loads(packet_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeTaskBuildError(
            f"Prepared input packet is not valid JSON: {packet_path!s}."
        ) from exc


def build_runtime_task_content(
    request: RuntimeRequest,
    prompt_bundle: PromptBundle,
    prepared_packets: list[dict[str, Any]],
    *,
    provider_name: str,
) -> str:
    """Assemble the full runtime task markdown content.

    Returns a markdown string ready to be written to disk.
    """
    sections: list[str] = []

    # Header
    sections.append(
        f"# Runtime Task\n\n"
        f"- **Role:** {request.role}\n"
        f"- **Node root:** {request.node_path}\n"
        f"- **Run ID:** {request.run_id}\n"
        f"- **Provider:** {provider_name}\n"
        f"- **Model:** {request.model or '(default)'}\n"
    )

    # System prompt
    sections.append(
        f"## System Prompt\n\n{prompt_bundle.system_prompt.strip()}\n"
    )

    # Support documents
    if prompt_bundle.support_documents:
        doc_parts: list[str] = []
        for relative_path, content in prompt_bundle.support_documents:
            doc_parts.append(f"### {relative_path}\n\n{content.strip()}")
        sections.append(
            f"## Supporting Documents\n\n" + "\n\n".join(doc_parts) + "\n"
        )

    # Runtime note
    sections.append(
        "## Runtime Note\n\n"
        "You are running as an Open-Eywa node via CLI. "
        "Use the file tools available in your environment to read and write files. "
        "All work must stay within the current node directory. "
        "Do not assume any tools beyond file operations are available.\n"
    )

    # Prepared context
    if prepared_packets:
        packet_json = json.dumps(prepared_packets, indent=2, sort_keys=True)
        sections.append(
            f"## Prepared Context\n\n```json\n{packet_json}\n```\n"
        )

    # Required artifacts
    contract = role_contract_for(request.role)
    required_artifacts = ", ".join(f"`{a}`" for a in contract.required_artifacts) or "none"
    sections.append(
        f"## Required Artifacts\n\n"
        f"Your role contract requires these exact artifact paths: {required_artifacts}\n\n"
        f"These paths are enforced by code after the run completes. "
        f"If the task or context mentions a different output filename, "
        f"still write the required artifact path for your role. "
        f"You may write additional files if they help, but they do not replace the required artifacts.\n"
    )

    # Instructions
    sections.append(
        "## Instructions\n\n"
        "1. Read and understand the system prompt and prepared context above.\n"
        "2. Execute the role's task using the available file tools.\n"
        "3. Write all required output artifacts listed above.\n"
        "4. If the task is impossible under the node's assumptions, write `output/escalation.md`.\n"
        "5. Do not write files outside the node boundary.\n"
    )

    return "\n".join(sections)
