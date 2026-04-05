from __future__ import annotations

import unittest
from pathlib import Path
import sys


THIS_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = THIS_DIR.parent
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from eywa_runtime.authored_response import (
    AuthoredResponseError,
    parse_authored_response_text,
    validate_authored_response,
)


class AuthoredResponseTests(unittest.TestCase):
    def test_parse_response_accepts_code_fences(self) -> None:
        payload = parse_authored_response_text(
            """```json
{"schema_name":"eywa_node_response","schema_version":"v1","orchestration_decision":"execute_locally","response":"ok"}
```"""
        )
        self.assertEqual(payload["orchestration_decision"], "execute_locally")

    def test_validate_delegate_requires_helpers(self) -> None:
        normalized = validate_authored_response(
            {
                "schema_name": "eywa_node_response",
                "schema_version": "v1",
                "orchestration_decision": "delegate",
                "helpers": [
                    {
                        "instructions": "do work",
                        "variable_overrides": {},
                    }
                ],
            },
            allowed_decisions=["execute_locally", "delegate", "report_problem"],
            max_helpers=3,
        )
        self.assertEqual(normalized["helpers"][0]["label"], "helper_01")

    def test_validate_rejects_unknown_decision(self) -> None:
        with self.assertRaises(AuthoredResponseError):
            validate_authored_response(
                {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "local_replan",
                },
                allowed_decisions=["execute_locally", "delegate", "report_problem"],
                max_helpers=3,
            )

    def test_validate_rejects_missing_orchestration_decision(self) -> None:
        with self.assertRaises(AuthoredResponseError):
            validate_authored_response(
                {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "response": "ok",
                },
                allowed_decisions=["execute_locally", "delegate", "report_problem"],
                max_helpers=3,
            )

    def test_validate_rejects_over_budget_helper_count(self) -> None:
        with self.assertRaises(AuthoredResponseError):
            validate_authored_response(
                {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "delegate",
                    "helpers": [
                        {"instructions": "one"},
                        {"instructions": "two"},
                    ],
                },
                allowed_decisions=["execute_locally", "delegate", "report_problem"],
                max_helpers=1,
            )

    def test_validate_rejects_disallowed_turn_decision(self) -> None:
        with self.assertRaises(AuthoredResponseError):
            validate_authored_response(
                {
                    "schema_name": "eywa_node_response",
                    "schema_version": "v1",
                    "orchestration_decision": "delegate",
                    "helpers": [{"instructions": "do work"}],
                },
                allowed_decisions=["execute_locally", "report_problem"],
                max_helpers=3,
            )


if __name__ == "__main__":
    unittest.main()
