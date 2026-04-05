"""Contract-first orchestration kernel for the Open-Eywa rebuild."""

from .event_schema import EVENT_TYPES, EventRecord, EventSchemaError
from .event_writer import AppendOnlyJsonlWriter
from .node_contract import (
    NODE_STATUSES,
    TERMINAL_OUTCOMES,
    NodeLayout,
    create_node,
    node_layout,
)
from .node_controls import ResumeComputationResult, cancel_node, record_computation_result, resume_waiting_node_if_ready
from .node_recovery import (
    NodeRecoveryError,
    NodeRecoveryResult,
    prepare_node_for_fresh_attempt,
    prepare_node_for_retry,
)
from .node_preparation import PreparedNodeContextResult, prepare_node_context_packet
from .mission_contract import MissionLayout, create_mission, mission_layout
from .live_canary import (
    DEFAULT_LIVE_CANARY_GOAL,
    LiveCanaryConfig,
    build_default_live_canary_mission_path,
    run_live_canary,
)
from .mission_driver import MissionDriveResult, MissionDriver, MissionDriverError
from .orchestrator_core import NodeOrchestratorCore, NodeRunStepResult, OrchestratorCoreError
from .orchestrator_progression import (
    NodeProgressionEngine,
    NodeProgressionResult,
    OrchestratorProgressionError,
)
from .node_lifecycle import LEGAL_STATUS_TRANSITIONS, NodeTransitionError, transition_node
from .node_validator import NodeValidationIssue, NodeValidationReport, validate_node
from .role_contracts import ROLE_CONTRACTS, RoleContract, role_contract_for
from .summary_schema import MissionSummary, NodeSummary, RunSummary
from .usage_schema import CostRecord, UsageRecord, UsageSchemaError

__all__ = [
    "AppendOnlyJsonlWriter",
    "CostRecord",
    "EVENT_TYPES",
    "EventRecord",
    "EventSchemaError",
    "LEGAL_STATUS_TRANSITIONS",
    "MissionSummary",
    "MissionDriveResult",
    "MissionDriver",
    "MissionDriverError",
    "MissionLayout",
    "DEFAULT_LIVE_CANARY_GOAL",
    "LiveCanaryConfig",
    "NODE_STATUSES",
    "NodeOrchestratorCore",
    "NodeProgressionEngine",
    "NodeProgressionResult",
    "NodeRecoveryError",
    "NodeRecoveryResult",
    "NodeRunStepResult",
    "PreparedNodeContextResult",
    "NodeSummary",
    "TERMINAL_OUTCOMES",
    "NodeLayout",
    "NodeTransitionError",
    "NodeValidationIssue",
    "NodeValidationReport",
    "OrchestratorCoreError",
    "OrchestratorProgressionError",
    "ROLE_CONTRACTS",
    "RoleContract",
    "RunSummary",
    "UsageRecord",
    "UsageSchemaError",
    "ResumeComputationResult",
    "cancel_node",
    "create_node",
    "create_mission",
    "mission_layout",
    "node_layout",
    "prepare_node_context_packet",
    "record_computation_result",
    "prepare_node_for_fresh_attempt",
    "prepare_node_for_retry",
    "run_live_canary",
    "role_contract_for",
    "resume_waiting_node_if_ready",
    "transition_node",
    "validate_node",
    "build_default_live_canary_mission_path",
]
