from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tjc-unicode-ui-as-code" / "scripts" / "audit_text_contract.py"
SPEC = importlib.util.spec_from_file_location("audit_text_contract", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class UnicodeTextContractAuditTests(unittest.TestCase):
    def test_valid_utf8_contract_passes_and_recommends_byte_headroom(self) -> None:
        spec = {
            "encoding": "utf-8",
            "objects": [
                {
                    "name": "t_status",
                    "texts": ["正常", "传感器异常", "V0.9.1"],
                    "txt_maxl": 18,
                }
            ],
        }
        report = MODULE.audit(spec, set("正常传感器异常"), headroom=4)
        self.assertTrue(report["passed"])
        self.assertEqual(report["objects"][0]["max_utf8_bytes"], 15)
        self.assertEqual(report["objects"][0]["recommended_txt_maxl"], 19)

    def test_invalid_contract_reports_identifier_capacity_and_glyphs(self) -> None:
        spec = {
            "encoding": "utf-8",
            "object_name_limit_bytes": 8,
            "objects": [
                {"name": "状态对象名称过长", "texts": ["传感器异常"], "txt_maxl": 4}
            ],
        }
        report = MODULE.audit(spec, set("传感器异"), headroom=4)
        kinds = {error["kind"] for error in report["errors"]}
        self.assertFalse(report["passed"])
        self.assertIn("non_ascii_object_name", kinds)
        self.assertIn("txt_maxl_too_small", kinds)
        self.assertIn("missing_font_glyphs", kinds)
        self.assertEqual(report["missing_non_ascii_characters"], "常")

    def test_ascii_object_name_limit_is_configurable(self) -> None:
        report = MODULE.audit(
            {
                "encoding": "utf-8",
                "object_name_limit_bytes": 8,
                "objects": [{"name": "t_status9", "texts": ["OK"], "txt_maxl": 4}],
            },
            set(),
            headroom=2,
        )
        self.assertFalse(report["passed"])
        self.assertIn("object_name_over_limit", {e["kind"] for e in report["errors"]})

    def test_non_utf8_contract_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "UTF-8"):
            MODULE.audit({"encoding": "gbk", "objects": []}, set(), headroom=4)

    def test_invalid_object_name_limit_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "object_name_limit_bytes"):
            MODULE.audit(
                {"encoding": "utf-8", "object_name_limit_bytes": 0, "objects": []},
                set(),
                headroom=4,
            )


if __name__ == "__main__":
    unittest.main()

