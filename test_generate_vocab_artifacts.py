#!/usr/bin/env python3
"""
test_generate_vocab_artifacts.py — unit tests for generate-vocab-artifacts.py.

Run from the wiki repository root:

    python3 -m unittest test_generate_vocab_artifacts -v

Covers: render function output, vocabulary.json validation rejections (bad
id, embedded quote, duplicate id), marker fault handling (missing pair,
duplicated pair, out-of-order pair), and the --check CLI exit-code contract
(0 in sync, 1 drifted, 2 fatal) — per BL-W-01 spec Section 5 Step 2 gate.
"""

import importlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

# generate-vocab-artifacts.py is not import-safe by module name (hyphens), so
# load it explicitly. This mirrors the spec's rationale for the hyphenated
# filename: the CLI/--check contract is the interface, not a Python import.
_spec = importlib.util.spec_from_file_location(
    "generate_vocab_artifacts",
    os.path.join(os.path.dirname(__file__), "generate-vocab-artifacts.py"),
)
gva = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gva)

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(REPO_ROOT, "generate-vocab-artifacts.py")


def sample_vocab():
    return {
        "schema_version": 1,
        "competency_domains": [
            {
                "id": "tool-evaluation-and-selection",
                "label": "Tool Evaluation and Selection",
                "covers": "Assessing and choosing AI tools",
            },
            {
                "id": "capability-horizon-awareness",
                "label": "Capability Horizon Awareness",
                "covers": "Tracking emerging capabilities",
            },
        ],
        "professional_contexts": [
            {"id": "legal-practice", "label": "Legal Practice"},
            {"id": "journalism-and-media", "label": "Journalism and Media"},
        ],
    }


class RenderFunctionTests(unittest.TestCase):
    def test_render_tagging_skill_block_structure(self):
        block = gva.render_tagging_skill_block(sample_vocab())
        self.assertIn("### 1.1 Professional Competency Domains", block)
        self.assertIn("| Value (use exactly as shown) | Covers |", block)
        self.assertIn(
            "| `tool-evaluation-and-selection` | Assessing and choosing AI tools |",
            block,
        )
        self.assertIn("### 1.2 Professional Context Terms", block)
        self.assertIn("| `legal-practice` |", block)
        # Contexts table must not carry a Covers column
        self.assertNotIn("| `legal-practice` | ", block)

    def test_render_tagging_skill_block_row_count(self):
        block = gva.render_tagging_skill_block(sample_vocab())
        self.assertEqual(block.count("| `"), 4)  # 2 domains + 2 contexts

    def test_render_ingest_ui_block_structure(self):
        block = gva.render_ingest_ui_block(sample_vocab())
        self.assertIn("const COMPETENCY_DOMAINS = [", block)
        self.assertIn(
            '{id: "tool-evaluation-and-selection", label: "Tool Evaluation and Selection"}',
            block,
        )
        self.assertIn("const PROFESSIONAL_CONTEXTS = [", block)
        self.assertIn('{id: "legal-practice", label: "Legal Practice"}', block)
        # covers text must never appear in the HTML block
        self.assertNotIn("Assessing and choosing", block)

    def test_render_ingest_ui_block_is_valid_looking_js_array(self):
        block = gva.render_ingest_ui_block(sample_vocab())
        cd_section = block.split("const PROFESSIONAL_CONTEXTS")[0]
        self.assertEqual(cd_section.count("{id:"), 2)
        self.assertTrue(block.rstrip().endswith("];"))


class ValidationRejectionTests(unittest.TestCase):
    def _write_and_load(self, vocab_dict):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(vocab_dict, f)
            path = f.name
        try:
            return gva.load_and_validate_vocabulary(path)
        finally:
            os.remove(path)

    def test_valid_vocabulary_loads(self):
        vocab = self._write_and_load(sample_vocab())
        self.assertEqual(len(vocab["competency_domains"]), 2)

    def test_missing_file_raises(self):
        with self.assertRaises(gva.VocabularyError):
            gva.load_and_validate_vocabulary("/nonexistent/vocabulary.json")

    def test_invalid_json_raises(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write("{not valid json")
            path = f.name
        try:
            with self.assertRaises(gva.VocabularyError):
                gva.load_and_validate_vocabulary(path)
        finally:
            os.remove(path)

    def test_bad_id_rejected(self):
        vocab = sample_vocab()
        vocab["competency_domains"][0]["id"] = "Not Kebab Case!"
        with self.assertRaises(gva.VocabularyError):
            self._write_and_load(vocab)

    def test_empty_id_rejected(self):
        vocab = sample_vocab()
        vocab["competency_domains"][0]["id"] = ""
        with self.assertRaises(gva.VocabularyError):
            self._write_and_load(vocab)

    def test_embedded_quote_in_label_rejected(self):
        vocab = sample_vocab()
        vocab["competency_domains"][0]["label"] = 'Has "quotes" inside'
        with self.assertRaises(gva.VocabularyError):
            self._write_and_load(vocab)

    def test_embedded_quote_in_covers_rejected(self):
        vocab = sample_vocab()
        vocab["competency_domains"][0]["covers"] = 'Covers text with "quotes"'
        with self.assertRaises(gva.VocabularyError):
            self._write_and_load(vocab)

    def test_backslash_in_value_rejected(self):
        vocab = sample_vocab()
        vocab["professional_contexts"][0]["label"] = "Back\\slash"
        with self.assertRaises(gva.VocabularyError):
            self._write_and_load(vocab)

    def test_duplicate_id_rejected(self):
        vocab = sample_vocab()
        vocab["professional_contexts"].append(
            {"id": "legal-practice", "label": "Legal Practice (dup)"}
        )
        with self.assertRaises(gva.VocabularyError):
            self._write_and_load(vocab)

    def test_missing_label_rejected(self):
        vocab = sample_vocab()
        del vocab["professional_contexts"][0]["label"]
        with self.assertRaises(gva.VocabularyError):
            self._write_and_load(vocab)

    def test_empty_list_rejected(self):
        vocab = sample_vocab()
        vocab["competency_domains"] = []
        with self.assertRaises(gva.VocabularyError):
            self._write_and_load(vocab)

    def test_missing_key_rejected(self):
        vocab = sample_vocab()
        del vocab["professional_contexts"]
        with self.assertRaises(gva.VocabularyError):
            self._write_and_load(vocab)


class MarkerFaultHandlingTests(unittest.TestCase):
    BEGIN = "<!-- BEGIN GENERATED VOCABULARY -->"
    END = "<!-- END GENERATED VOCABULARY -->"

    def test_missing_begin_marker_raises(self):
        text = f"no begin here\nold\n{self.END}\n"
        with self.assertRaises(gva.VocabularyError):
            gva.locate_marker_block(text, self.BEGIN, self.END, "f.md")

    def test_missing_end_marker_raises(self):
        text = f"{self.BEGIN}\nold\nno end here\n"
        with self.assertRaises(gva.VocabularyError):
            gva.locate_marker_block(text, self.BEGIN, self.END, "f.md")

    def test_duplicated_begin_marker_raises(self):
        text = f"{self.BEGIN}\nold\n{self.BEGIN}\nold2\n{self.END}\n"
        with self.assertRaises(gva.VocabularyError):
            gva.locate_marker_block(text, self.BEGIN, self.END, "f.md")

    def test_duplicated_end_marker_raises(self):
        text = f"{self.BEGIN}\nold\n{self.END}\nextra\n{self.END}\n"
        with self.assertRaises(gva.VocabularyError):
            gva.locate_marker_block(text, self.BEGIN, self.END, "f.md")

    def test_end_before_begin_raises(self):
        text = f"{self.END}\nold\n{self.BEGIN}\n"
        with self.assertRaises(gva.VocabularyError):
            gva.locate_marker_block(text, self.BEGIN, self.END, "f.md")

    def test_valid_pair_locates_correctly(self):
        text = f"pre\n{self.BEGIN}\nold\n{self.END}\npost\n"
        begin_idx, end_idx = gva.locate_marker_block(text, self.BEGIN, self.END, "f.md")
        self.assertEqual(text[begin_idx : begin_idx + len(self.BEGIN)], self.BEGIN)
        self.assertEqual(text[end_idx : end_idx + len(self.END)], self.END)

    def test_replace_marker_block_reports_changed(self):
        text = f"{self.BEGIN}\nold\n{self.END}\n"
        new_text, changed = gva.replace_marker_block(
            text, self.BEGIN, self.END, "new", "f.md"
        )
        self.assertTrue(changed)
        self.assertIn("new", new_text)
        self.assertNotIn("old", new_text)

    def test_replace_marker_block_reports_unchanged(self):
        text = f"{self.BEGIN}\nsame\n{self.END}\n"
        new_text, changed = gva.replace_marker_block(
            text, self.BEGIN, self.END, "same", "f.md"
        )
        self.assertFalse(changed)
        self.assertEqual(new_text, text)


class CheckModeCliTests(unittest.TestCase):
    """Exercises the --check exit-code contract via subprocess against a scratch repo dir."""

    def _make_scratch_repo(
        self,
        vocab_dict,
        corrupt_vocab_json=False,
        drift=False,
        missing_marker=False,
        duplicate_marker=False,
    ):
        d = tempfile.mkdtemp()

        vocab_path = os.path.join(d, "vocabulary.json")
        if corrupt_vocab_json:
            with open(vocab_path, "w", encoding="utf-8") as f:
                f.write("{not valid json")
        else:
            with open(vocab_path, "w", encoding="utf-8") as f:
                json.dump(vocab_dict, f)

        tagging_block = (
            "" if missing_marker else gva.render_tagging_skill_block(vocab_dict)
        )
        if drift:
            tagging_block += "\nSTALE EXTRA LINE THAT DOES NOT MATCH THE SOURCE\n"

        if missing_marker:
            tagging_text = (
                "**Last Updated:** 01/01/2026 00:00 EST\nno markers in this file\n"
            )
        elif duplicate_marker:
            tagging_text = (
                "**Last Updated:** 01/01/2026 00:00 EST\n"
                f"{gva.TAGGING_BEGIN_MARKER}\n{tagging_block}\n{gva.TAGGING_END_MARKER}\n"
                f"{gva.TAGGING_BEGIN_MARKER}\n{tagging_block}\n{gva.TAGGING_END_MARKER}\n"
            )
        else:
            tagging_text = (
                "**Last Updated:** 01/01/2026 00:00 EST\n"
                f"{gva.TAGGING_BEGIN_MARKER}\n{tagging_block}\n{gva.TAGGING_END_MARKER}\n"
            )

        with open(os.path.join(d, "TAGGING-SKILL.md"), "w", encoding="utf-8") as f:
            f.write(tagging_text)

        html_block = gva.render_ingest_ui_block(vocab_dict)
        html_text = f"<script>\n{gva.HTML_BEGIN_MARKER}\n{html_block}\n{gva.HTML_END_MARKER}\n</script>\n"
        with open(
            os.path.join(d, "ingest-ui-template.html"), "w", encoding="utf-8"
        ) as f:
            f.write(html_text)

        return d

    def _run_check(self, cwd):
        return subprocess.run(
            [sys.executable, SCRIPT_PATH, "--check"],
            cwd=cwd,
            capture_output=True,
            text=True,
        )

    def test_check_exits_0_when_in_sync(self):
        d = self._make_scratch_repo(sample_vocab())
        result = self._run_check(d)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK", result.stdout)

    def test_check_exits_1_when_drifted(self):
        d = self._make_scratch_repo(sample_vocab(), drift=True)
        result = self._run_check(d)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("DRIFT", result.stdout)

    def test_check_exits_2_on_corrupt_vocabulary_json(self):
        d = self._make_scratch_repo(sample_vocab(), corrupt_vocab_json=True)
        result = self._run_check(d)
        self.assertEqual(result.returncode, 2)
        self.assertIn("FATAL", result.stderr)

    def test_check_exits_2_on_missing_marker(self):
        d = self._make_scratch_repo(sample_vocab(), missing_marker=True)
        result = self._run_check(d)
        self.assertEqual(result.returncode, 2)
        self.assertIn("FATAL", result.stderr)

    def test_check_exits_2_on_duplicated_marker(self):
        d = self._make_scratch_repo(sample_vocab(), duplicate_marker=True)
        result = self._run_check(d)
        self.assertEqual(result.returncode, 2)
        self.assertIn("FATAL", result.stderr)

    def test_default_mode_writes_regenerated_file(self):
        d = self._make_scratch_repo(sample_vocab(), drift=True)
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            cwd=d,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("regenerated: TAGGING-SKILL.md", result.stdout)
        with open(os.path.join(d, "TAGGING-SKILL.md"), encoding="utf-8") as f:
            new_text = f.read()
        self.assertNotIn("STALE EXTRA LINE", new_text)

    def test_default_mode_reports_unchanged_when_in_sync(self):
        d = self._make_scratch_repo(sample_vocab())
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            cwd=d,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unchanged: TAGGING-SKILL.md", result.stdout)
        self.assertIn("unchanged: ingest-ui-template.html", result.stdout)


class TimestampStampTests(unittest.TestCase):
    def test_render_last_updated_stamp_format(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo

        dt = datetime(2026, 7, 11, 6, 27, tzinfo=ZoneInfo("America/New_York"))
        stamp = gva.render_last_updated_stamp(dt)
        self.assertEqual(stamp, "07/11/2026 06:27 EDT")

    def test_render_last_updated_stamp_winter_is_est(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo

        dt = datetime(2026, 1, 15, 9, 0, tzinfo=ZoneInfo("America/New_York"))
        stamp = gva.render_last_updated_stamp(dt)
        self.assertTrue(stamp.endswith("EST"))

    def test_update_last_updated_line_replaces(self):
        text = "# Title\n**Last Updated:** old stamp\nbody text\n"
        new_text = gva.update_last_updated_line(text, "new stamp")
        self.assertIn("**Last Updated:** new stamp", new_text)
        self.assertNotIn("old stamp", new_text)

    def test_update_last_updated_line_missing_raises(self):
        text = "# Title\nno stamp line here\n"
        with self.assertRaises(gva.VocabularyError):
            gva.update_last_updated_line(text, "new stamp")


if __name__ == "__main__":
    unittest.main()
