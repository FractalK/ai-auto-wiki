#!/usr/bin/env python3
"""
test_wiki_lint.py — unit tests for wiki-lint.py's structured-data extraction
normalization utilities (BL-W-02, DM-128, structured-data-extraction-spec.md).

Run from the wiki repository root:

    python3 -m unittest test_wiki_lint -v

Covers Step 2 of the BL-W-02 execution spec: canonicalize_metric, parse_value,
divergence, claim_similarity, conditions_similarity. Step 4's L20 class tests
(synthetic claim/record fixtures) live in a separate suite added at Step 4.
"""

import importlib.util
import os
import unittest

# wiki-lint.py is not import-safe by module name (hyphens), so load it
# explicitly — same pattern as test_generate_vocab_artifacts.py.
_spec = importlib.util.spec_from_file_location(
    "wiki_lint",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki-lint.py"),
)
wl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(wl)


class TestCanonicalizeMetric(unittest.TestCase):
    def test_strips_generic_suffix(self):
        self.assertEqual(wl.canonicalize_metric("MMLU accuracy"), "mmlu")
        self.assertEqual(wl.canonicalize_metric("Hallucination Rate"), "hallucination")

    def test_one_token_remaining_guard(self):
        # "Accuracy" alone must not be stripped to the empty string.
        self.assertEqual(wl.canonicalize_metric("Accuracy"), "accuracy")
        # "Rate Score" strips "score" once, then the guard blocks stripping
        # "rate" itself because doing so would leave zero tokens.
        self.assertEqual(wl.canonicalize_metric("Rate Score"), "rate")

    def test_does_not_incorrectly_merge_distinct_metrics(self):
        # swe-bench and swe-bench-verified must remain distinct — "verified"
        # is not a generic suffix, so no merge occurs.
        self.assertEqual(wl.canonicalize_metric("SWE-bench"), "swe-bench")
        self.assertEqual(
            wl.canonicalize_metric("SWE-bench Verified"), "swe-bench-verified"
        )
        self.assertNotEqual(
            wl.canonicalize_metric("SWE-bench"),
            wl.canonicalize_metric("SWE-bench Verified"),
        )

    def test_alias_map_applied_as_final_rewrite(self):
        wl.METRIC_ALIASES["gpqa-diamond-acc"] = "gpqa-diamond"
        try:
            self.assertEqual(wl.canonicalize_metric("GPQA Diamond Acc"), "gpqa-diamond")
        finally:
            wl.METRIC_ALIASES.pop("gpqa-diamond-acc", None)

    def test_empty_input(self):
        self.assertEqual(wl.canonicalize_metric(""), "")
        self.assertEqual(wl.canonicalize_metric(None), "")


class TestParseValue(unittest.TestCase):
    def test_escaped_currency(self):
        self.assertEqual(wl.parse_value("\\$15"), (15.0, None, "$"))

    def test_bare_currency(self):
        self.assertEqual(wl.parse_value("$15"), (15.0, None, "$"))

    def test_multiplier_without_unit(self):
        self.assertEqual(wl.parse_value("1.2M"), (1200000.0, None, None))

    def test_currency_and_multiplier_combined(self):
        self.assertEqual(wl.parse_value("\\$1.2M"), (1200000.0, None, "$"))

    def test_percent(self):
        self.assertEqual(wl.parse_value("87.5%"), (87.5, None, "%"))

    def test_comma_thousands_separator(self):
        self.assertEqual(wl.parse_value("1,200"), (1200.0, None, None))

    def test_ms_converted_to_seconds(self):
        numeric, high, unit = wl.parse_value("230ms")
        self.assertAlmostEqual(numeric, 0.23)
        self.assertIsNone(high)
        self.assertEqual(unit, "s")

    def test_range_with_explicit_unit_on_high_side(self):
        self.assertEqual(wl.parse_value("1.2-1.5s"), (1.2, 1.5, "s"))

    def test_range_with_word_separator_and_ms_conversion(self):
        low, high, unit = wl.parse_value("100 to 200 ms")
        self.assertAlmostEqual(low, 0.1)
        self.assertAlmostEqual(high, 0.2)
        self.assertEqual(unit, "s")

    def test_non_parsable_value(self):
        self.assertEqual(wl.parse_value("supported"), (None, None, None))
        self.assertEqual(wl.parse_value(""), (None, None, None))

    def test_unrecognized_unit_yields_none_unit_but_keeps_numeric(self):
        # "/month" is not in UNIT_TOKENS — value still parses, unit is None,
        # which downstream renders the row non-comparable (not a crash).
        numeric, high, unit = wl.parse_value("\\$20/month")
        self.assertEqual(numeric, 20.0)
        self.assertIsNone(unit)


class TestDivergence(unittest.TestCase):
    def test_diverges_true(self):
        self.assertTrue(wl.divergence(87.5, None, "%", 82.0, None, "%"))

    def test_comparable_not_divergent(self):
        self.assertFalse(wl.divergence(87.5, None, "%", 87.4, None, "%"))

    def test_non_comparable_units_returns_none(self):
        self.assertIsNone(wl.divergence(50.0, None, "%", 15.0, None, "tok/s"))

    def test_non_comparable_missing_value_returns_none(self):
        self.assertIsNone(wl.divergence(None, None, "%", 15.0, None, "%"))

    def test_disjoint_ranges_divergent(self):
        self.assertTrue(wl.divergence(10, 20, "%", 30, 40, "%"))

    def test_overlapping_ranges_not_divergent(self):
        self.assertFalse(wl.divergence(10, 20, "%", 15, 25, "%"))

    def test_value_inside_range_not_divergent(self):
        self.assertFalse(wl.divergence(90, None, "%", 80, 95, "%"))

    def test_and_condition_relative_exceeded_absolute_not(self):
        # rel = 0.01/0.02 = 0.5 (>> REL_DIVERGENCE) but abs = 0.01 (< 0.1 floor)
        self.assertFalse(wl.divergence(0.01, None, "s", 0.02, None, "s"))

    def test_and_condition_absolute_exceeded_relative_not(self):
        # abs = 15 (>> ABS_DIVERGENCE_FLOOR) but rel = 15/1015 ~= 0.0148 (< 0.02)
        self.assertFalse(wl.divergence(1000, None, "$", 1015, None, "$"))

    def test_and_condition_both_exceeded(self):
        # abs = 5 (> 0.1) and rel = 5/105 ~= 0.048 (> 0.02)
        self.assertTrue(wl.divergence(100, None, "%", 105, None, "%"))


class TestClaimSimilarity(unittest.TestCase):
    def test_entity_guard_suppresses_different_entities(self):
        sim = wl.claim_similarity(
            "GPT-4o scores 86% on MMLU",
            "Claude Opus scores 88% on MMLU",
            metric_terms=["MMLU"],
        )
        self.assertLess(sim, wl.CLAIM_SIM_THRESHOLD)

    def test_same_entity_rival_claims_pass(self):
        sim = wl.claim_similarity(
            "GPT-4o scores 86% on MMLU under zero-shot evaluation",
            "GPT-4o achieves 82% on MMLU in zero-shot evaluation",
            metric_terms=["MMLU"],
        )
        self.assertGreaterEqual(sim, wl.CLAIM_SIM_THRESHOLD)

    def test_both_empty_after_stripping_is_fully_similar(self):
        self.assertEqual(
            wl.claim_similarity("MMLU", "MMLU", metric_terms=["MMLU"]), 1.0
        )


class TestConditionsSimilarity(unittest.TestCase):
    def test_partial_overlap(self):
        self.assertEqual(
            wl.conditions_similarity(["zero-shot"], ["zero-shot", "standard"]), 0.5
        )

    def test_both_empty_fully_similar(self):
        self.assertEqual(wl.conditions_similarity([], []), 1.0)

    def test_one_empty_fully_dissimilar(self):
        self.assertEqual(wl.conditions_similarity([], ["zero-shot"]), 0.0)


# ─── Step 4: L20 contradiction pre-screen — synthetic fixtures ──────────────


def make_claim(
    page,
    claim_text,
    metric_canonical,
    matched_text,
    value_numeric,
    unit,
    value_raw,
    date,
    support_score,
    status="current",
    derived=False,
    ctrd_ids=None,
    sources=None,
):
    """Build a claims.json-shaped dict for L20 fixtures."""
    signature = None
    if metric_canonical is not None:
        signature = {
            "metric_canonical": metric_canonical,
            "metric_matched_text": matched_text,
            "values": [{"numeric": value_numeric, "unit": unit, "raw": value_raw}],
        }
    return {
        "page": page,
        "page_type": "tool",
        "row_index": 1,
        "claim": claim_text,
        "sources": sources or ["some-source"],
        "source_annotations": {},
        "derived": derived,
        "date": date,
        "status": status,
        "ctrd_ids": ctrd_ids or [],
        "support_score": support_score,
        "decay_exempt": False,
        "signature": signature,
    }


def make_record(
    page,
    metric_canonical,
    metric_raw,
    value_numeric,
    unit,
    value_raw,
    measurement_date,
    conditions_tokens=None,
    sources=None,
    status="current",
    value_numeric_high=None,
):
    """Build a data-records.json-shaped dict for L20 fixtures."""
    return {
        "page": page,
        "page_type": "tool",
        "metric_raw": metric_raw,
        "metric_canonical": metric_canonical,
        "value_raw": value_raw,
        "value_numeric": value_numeric,
        "value_numeric_high": value_numeric_high,
        "unit": unit,
        "conditions_raw": ", ".join(conditions_tokens or []),
        "conditions_tokens": conditions_tokens or [],
        "measurement_date": measurement_date,
        "sources": sources or ["some-source"],
        "status": status,
    }


def run_l20(claims_list, records_list):
    """Run check_L20_contradiction_prescreen against a clean findings state."""
    wl.findings = []
    wl.agent_review = []
    wl.check_L20_contradiction_prescreen(claims_list, records_list)
    return wl.agent_review, wl.findings


class TestL20Class1(unittest.TestCase):
    def test_class1_hit_same_entity_diverging_values(self):
        claims = [
            make_claim(
                "tools/model-a", "Model Alpha achieves 90% on MMLU under standard evaluation",
                "mmlu", "MMLU", 90.0, "%", "90%", "2026-01-01", 3.0,
            ),
            make_claim(
                "tools/model-a-update", "Model Alpha achieves 70% on MMLU under standard evaluation",
                "mmlu", "MMLU", 70.0, "%", "70%", "2026-02-01", 2.0,
            ),
        ]
        agent_review, _ = run_l20(claims, [])
        kc_kc = [r for r in agent_review if r["class"] == "kc-kc"]
        self.assertEqual(len(kc_kc), 1)
        # Contested side is the lower-support claim (support_score 2.0).
        self.assertEqual(kc_kc[0]["side_a"]["page"], "tools/model-a-update")
        self.assertEqual(kc_kc[0]["side_b"]["page"], "tools/model-a")

    def test_class1_suppressed_by_entity_guard(self):
        claims = [
            make_claim(
                "tools/openai-gpt-4o", "GPT-4o scores 86% on MMLU",
                "mmlu", "MMLU", 86.0, "%", "86%", "2026-01-01", 3.0,
            ),
            make_claim(
                "tools/claude-opus", "Claude Opus scores 55% on MMLU",
                "mmlu", "MMLU", 55.0, "%", "55%", "2026-01-01", 3.0,
            ),
        ]
        agent_review, _ = run_l20(claims, [])
        self.assertEqual([r for r in agent_review if r["class"] == "kc-kc"], [])

    def test_ctrd_excluded_claim_skipped(self):
        claims = [
            make_claim(
                "tools/model-a", "Model Alpha achieves 90% on MMLU under standard evaluation",
                "mmlu", "MMLU", 90.0, "%", "90%", "2026-01-01", 3.0,
                ctrd_ids=["CTRD-001"],
            ),
            make_claim(
                "tools/model-a-update", "Model Alpha achieves 70% on MMLU under standard evaluation",
                "mmlu", "MMLU", 70.0, "%", "70%", "2026-02-01", 2.0,
            ),
        ]
        agent_review, _ = run_l20(claims, [])
        self.assertEqual([r for r in agent_review if r["class"] == "kc-kc"], [])


class TestL20Class2(unittest.TestCase):
    def test_class2_hit_same_page_record_postdates_claim(self):
        claims = [
            make_claim(
                "tools/model-a", "Model Alpha achieves 90% on MMLU under standard evaluation",
                "mmlu", "MMLU", 90.0, "%", "90%", "2026-01-01", 3.0,
            ),
        ]
        records = [
            make_record(
                "tools/model-a", "mmlu", "MMLU", 70.0, "%", "70%", "2026-02",
            ),
        ]
        agent_review, _ = run_l20(claims, records)
        dr_kc = [r for r in agent_review if r["class"] == "dr-kc"]
        self.assertEqual(len(dr_kc), 1)
        self.assertEqual(dr_kc[0]["side_a"]["page"], "tools/model-a")
        self.assertEqual(dr_kc[0]["side_b"]["page"], "tools/model-a")

    def test_class2_suppressed_by_date_direction(self):
        claims = [
            make_claim(
                "tools/model-a", "Model Alpha achieves 90% on MMLU under standard evaluation",
                "mmlu", "MMLU", 90.0, "%", "90%", "2026-03-01", 3.0,
            ),
        ]
        records = [
            # Record predates the claim — must be excluded per the Class 2 gate.
            make_record(
                "tools/model-a", "mmlu", "MMLU", 70.0, "%", "70%", "2026-01",
            ),
        ]
        agent_review, _ = run_l20(claims, records)
        self.assertEqual([r for r in agent_review if r["class"] == "dr-kc"], [])


class TestL20Class3(unittest.TestCase):
    def test_class3a_inconsistent_replication_hit(self):
        records = [
            make_record(
                "tools/model-a", "mmlu", "MMLU", 90.0, "%", "90%", "2026-02",
                conditions_tokens=["zero-shot", "standard"], sources=["shared-source"],
            ),
            make_record(
                "tools/model-a-mirror", "mmlu", "MMLU", 70.0, "%", "70%", "2026-02",
                conditions_tokens=["zero-shot", "standard"], sources=["shared-source"],
            ),
        ]
        _, findings = run_l20([], records)
        l20_3a = [
            f for f in findings
            if f["step"] == "L20" and f["description"].startswith("Class 3a")
        ]
        self.assertEqual(len(l20_3a), 1)

    def test_class3b_supersession_asymmetry_hit(self):
        records = [
            make_record(
                "tools/model-a", "mmlu", "MMLU", 90.0, "%", "90%", "2026-03",
                conditions_tokens=["zero-shot"], sources=["shared-source"],
            ),
            make_record(
                "tools/model-a-mirror", "mmlu", "MMLU", 90.0, "%", "90%", "2026-01",
                conditions_tokens=["zero-shot"], sources=["shared-source"],
            ),
        ]
        _, findings = run_l20([], records)
        l20_3b = [
            f for f in findings
            if f["step"] == "L20" and f["description"].startswith("Class 3b")
        ]
        self.assertEqual(len(l20_3b), 1)


class TestL20Ceiling(unittest.TestCase):
    def test_ceiling_overflow_deferred(self):
        # Build 12 independent Class 1 candidate pairs (> MAX_PRESCREEN_CANDIDATES=10),
        # each pair using a distinct metric so pairs don't cross-match each other.
        claims = []
        for i in range(12):
            metric = f"benchmark-{i}"
            claims.append(make_claim(
                f"tools/model-{i}-a", f"Model {i} achieves 90% on Benchmark{i} under standard evaluation",
                metric, f"Benchmark{i}", 90.0, "%", "90%", "2026-01-01", 3.0,
            ))
            claims.append(make_claim(
                f"tools/model-{i}-b", f"Model {i} achieves 70% on Benchmark{i} under standard evaluation",
                metric, f"Benchmark{i}", 70.0, "%", "70%", "2026-02-01", 2.0,
            ))
        agent_review, findings = run_l20(claims, [])
        kc_kc = [r for r in agent_review if r["class"] == "kc-kc"]
        self.assertEqual(len(kc_kc), wl.MAX_PRESCREEN_CANDIDATES)
        deferred_findings = [
            f for f in findings if f["step"] == "L20" and "deferred to next lint pass" in f["description"]
        ]
        self.assertEqual(len(deferred_findings), 1)
        self.assertEqual(deferred_findings[0]["data"]["deferred_count"], 2)


class TestStripOuterQuotes(unittest.TestCase):
    """BL-W-13 (DM-161/163/164/165): _strip_outer_quotes single-quote un-doubling."""

    def test_single_quoted_with_doubled_apostrophe(self):
        self.assertEqual(
            wl._strip_outer_quotes("'Anthropic''s model: 2.0%'"),
            "Anthropic's model: 2.0%",
        )

    def test_double_quoted_wikilink(self):
        self.assertEqual(
            wl._strip_outer_quotes('"[[tools/openai-gpt-4o]]"'),
            "[[tools/openai-gpt-4o]]",
        )

    def test_unquoted_value_passes_through(self):
        self.assertEqual(wl._strip_outer_quotes("unquoted value"), "unquoted value")

    def test_empty_string(self):
        self.assertEqual(wl._strip_outer_quotes(""), "")

    def test_single_character(self):
        # Len < 2, so the quote-pair branch cannot fire; falls through to
        # the historical strip('"'), which only acts on double-quote chars —
        # a lone double quote strips away to empty, a lone single quote or
        # any other char passes through unchanged.
        self.assertEqual(wl._strip_outer_quotes("x"), "x")
        self.assertEqual(wl._strip_outer_quotes("'"), "'")
        self.assertEqual(wl._strip_outer_quotes('"'), "")


if __name__ == "__main__":
    unittest.main()
