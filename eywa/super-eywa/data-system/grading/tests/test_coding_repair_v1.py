from __future__ import annotations

import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
GRADING_DIR = REPO_ROOT / "data-system" / "grading"
if str(GRADING_DIR) not in sys.path:
    sys.path.insert(0, str(GRADING_DIR))


class CodingRepairV1Tests(unittest.TestCase):
    def test_extract_python_code_handles_unclosed_fence(self) -> None:
        from coding_repair_v1 import _extract_python_code

        raw = "```python\nimport sys\nprint('hi')\n"
        self.assertEqual(_extract_python_code(raw), "import sys\nprint('hi')")

    def test_extract_python_code_handles_json_wrapped_main_py(self) -> None:
        from coding_repair_v1 import _extract_python_code

        raw = '{"main_py":"```python\\nimport sys\\nprint(1)\\n```","notes":"ok"}'
        self.assertEqual(_extract_python_code(raw), "import sys\nprint(1)")
