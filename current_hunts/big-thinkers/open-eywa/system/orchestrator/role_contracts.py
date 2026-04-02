from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .node_contract import NodeLayout
from .node_record import node_next_action_after_child_report

RoleSuccessMode = Literal["nonterminal", "terminal"]


@dataclass(frozen=True)
class RoleContract:
    role: str
    required_artifacts: tuple[str, ...]
    success_mode: RoleSuccessMode
    allowed_escalation: bool = True
    allowed_waiting: bool = False
    required_decision_values: tuple[str, ...] = ()

    def missing_required_artifacts(self, layout: NodeLayout) -> tuple[str, ...]:
        missing: list[str] = []
        for relative_path in self.required_artifacts:
            if not (layout.root / relative_path).exists():
                missing.append(relative_path)
        return tuple(missing)

    def invalid_decision_value(self, layout: NodeLayout) -> str | None:
        if not self.required_decision_values:
            return None
        decision = node_next_action_after_child_report(layout)
        if decision not in self.required_decision_values:
            return decision
        return None


ROLE_CONTRACTS: dict[str, RoleContract] = {
    "librarian": RoleContract(
        role="librarian",
        required_artifacts=("input/retrieved_relevant_knowledge_from_library.md",),
        success_mode="nonterminal",
    ),
    "planner": RoleContract(
        role="planner",
        required_artifacts=("output/plan.md",),
        success_mode="nonterminal",
    ),
    "plan-reviewer": RoleContract(
        role="plan-reviewer",
        required_artifacts=("output/review.md",),
        success_mode="nonterminal",
    ),
    "plan-decider": RoleContract(
        role="plan-decider",
        required_artifacts=("output/plan.md",),
        success_mode="nonterminal",
    ),
    "worker": RoleContract(
        role="worker",
        required_artifacts=("output/final-output.md",),
        success_mode="terminal",
        allowed_waiting=True,
    ),
    "mid-plan-evaluator": RoleContract(
        role="mid-plan-evaluator",
        required_artifacts=(),
        success_mode="nonterminal",
        required_decision_values=("continue", "replan", "escalate"),
    ),
    "synthesizer": RoleContract(
        role="synthesizer",
        required_artifacts=("output/final-output.md",),
        success_mode="terminal",
    ),
}


def role_contract_for(role: str) -> RoleContract:
    try:
        return ROLE_CONTRACTS[role]
    except KeyError as exc:
        raise ValueError(f"Unknown role contract: {role!r}.") from exc
