from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


class UsageSchemaError(ValueError):
    """Raised when usage or cost records violate the canonical schema."""


@dataclass(frozen=True)
class UsageRecord:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    reasoning_tokens: int = 0
    cached_prompt_tokens: int = 0
    total_tokens: int | None = None
    total_cost_usd: float = 0.0
    provider_details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in (
            "prompt_tokens",
            "completion_tokens",
            "reasoning_tokens",
            "cached_prompt_tokens",
        ):
            value = getattr(self, field_name)
            if value < 0:
                raise UsageSchemaError(f"{field_name} must be non-negative.")

        derived_total_tokens = self.prompt_tokens + self.completion_tokens
        if self.total_tokens is None:
            object.__setattr__(self, "total_tokens", derived_total_tokens)
        elif self.total_tokens < 0:
            raise UsageSchemaError("total_tokens must be non-negative.")

        if self.total_cost_usd < 0:
            raise UsageSchemaError("total_cost_usd must be non-negative.")
        if not isinstance(self.provider_details, dict):
            raise UsageSchemaError("provider_details must be a dictionary.")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CostRecord:
    direct_usd: float = 0.0
    children_usd: float = 0.0
    total_usd: float | None = None
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.direct_usd < 0:
            raise UsageSchemaError("direct_usd must be non-negative.")
        if self.children_usd < 0:
            raise UsageSchemaError("children_usd must be non-negative.")
        derived_total_usd = self.direct_usd + self.children_usd
        if self.total_usd is None:
            object.__setattr__(self, "total_usd", derived_total_usd)
        elif self.total_usd < 0:
            raise UsageSchemaError("total_usd must be non-negative.")
        if not isinstance(self.currency, str) or not self.currency.strip():
            raise UsageSchemaError("currency must be a non-empty string.")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
