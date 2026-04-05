from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class PromptLoaderError(RuntimeError):
    """Raised when the runtime cannot load the prompt bundle for a role."""


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STUFF_FOR_AGENTS_DIR = PROJECT_ROOT / "stuff-for-agents"

ROLE_PROMPT_LAYOUT: dict[str, dict[str, object]] = {
    "planner": {
        "system_prompt": STUFF_FOR_AGENTS_DIR / "planning" / "planner" / "system-prompt.md",
        "support_docs": (
            STUFF_FOR_AGENTS_DIR / "planning" / "planner" / "plan-design.md",
            STUFF_FOR_AGENTS_DIR / "planning" / "planner" / "execute-vs-plan.md",
        ),
    },
    "worker": {
        "system_prompt": STUFF_FOR_AGENTS_DIR / "worker" / "system-prompt.md",
        "support_docs": (),
    },
    "mid-plan-evaluator": {
        "system_prompt": STUFF_FOR_AGENTS_DIR
        / "planning"
        / "mid-plan-evaluator"
        / "system-prompt.md",
        "support_docs": (
            STUFF_FOR_AGENTS_DIR / "planning" / "planner" / "plan-design.md",
            STUFF_FOR_AGENTS_DIR
            / "planning"
            / "mid-plan-evaluator"
            / "continue-replan-escalate.md",
        ),
    },
    "synthesizer": {
        "system_prompt": STUFF_FOR_AGENTS_DIR / "synthesizer" / "system-prompt.md",
        "support_docs": (),
    },
    "librarian": {
        "system_prompt": STUFF_FOR_AGENTS_DIR / "librarian" / "system-prompt.md",
        "support_docs": (),
    },
    "plan-reviewer": {
        "system_prompt": STUFF_FOR_AGENTS_DIR
        / "planning"
        / "plan-reviewer"
        / "system-prompt.md",
        "support_docs": (),
    },
    "plan-decider": {
        "system_prompt": STUFF_FOR_AGENTS_DIR
        / "planning"
        / "plan-decider"
        / "system-prompt.md",
        "support_docs": (),
    },
}


@dataclass(frozen=True)
class PromptBundle:
    role: str
    system_prompt: str
    support_documents: tuple[tuple[str, str], ...]
    source_paths: tuple[str, ...]


class PromptLoader:
    def __init__(self, *, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root).expanduser().resolve() if project_root else PROJECT_ROOT

    def load(self, role: str) -> PromptBundle:
        config = ROLE_PROMPT_LAYOUT.get(role)
        if config is None:
            raise PromptLoaderError(f"No prompt bundle is configured for role {role!r}.")

        system_prompt_path = Path(config["system_prompt"])
        support_doc_paths = tuple(Path(path) for path in config["support_docs"])  # type: ignore[arg-type]

        missing_paths = [
            str(path.relative_to(self.project_root))
            for path in (system_prompt_path, *support_doc_paths)
            if not path.exists()
        ]
        if missing_paths:
            raise PromptLoaderError(
                f"Prompt bundle for role {role!r} is missing files: {missing_paths!r}."
            )

        support_documents = tuple(
            (
                str(path.relative_to(self.project_root)),
                path.read_text(encoding="utf-8"),
            )
            for path in support_doc_paths
        )
        source_paths = (
            str(system_prompt_path.relative_to(self.project_root)),
            *(str(path.relative_to(self.project_root)) for path in support_doc_paths),
        )
        return PromptBundle(
            role=role,
            system_prompt=system_prompt_path.read_text(encoding="utf-8"),
            support_documents=support_documents,
            source_paths=tuple(source_paths),
        )
