import pytest
from reporters_validator.matcher import match_results, MatchResult


def test_match_by_signature():
    actual = [
        {"signature": "A.Test1", "title": "Test 1", "status": "passed"},
        {"signature": "A.Test2", "title": "Test 2", "status": "failed"},
    ]
    expected = [
        {"signature": "A.Test2", "status": "failed"},
        {"signature": "A.Test1", "status": "passed"},
    ]
    matches = match_results(actual, expected)
    assert len(matches) == 2
    assert all(isinstance(m, MatchResult) for m in matches)
    assert matches[0].actual["signature"] == matches[0].expected["signature"]


def test_match_by_title_fallback():
    actual = [{"title": "My test", "status": "passed"}]
    expected = [{"title": "My test", "status": "passed"}]
    matches = match_results(actual, expected)
    assert len(matches) == 1
    assert matches[0].actual is not None
    assert matches[0].expected is not None


def test_unmatched_expected_has_none_actual():
    actual = []
    expected = [{"signature": "A.Missing", "status": "passed"}]
    matches = match_results(actual, expected)
    assert len(matches) == 1
    assert matches[0].actual is None
    assert matches[0].expected["signature"] == "A.Missing"


def test_extra_actual_ignored():
    """Actual results not in expected are not reported as errors."""
    actual = [
        {"signature": "A.Test1", "status": "passed"},
        {"signature": "A.Extra", "status": "passed"},
    ]
    expected = [{"signature": "A.Test1", "status": "passed"}]
    matches = match_results(actual, expected)
    assert len(matches) == 1


def test_signature_preferred_over_title():
    actual = [
        {"signature": "A.Real", "title": "Same title", "status": "passed"},
        {"signature": "A.Other", "title": "Same title", "status": "failed"},
    ]
    expected = [{"signature": "A.Real", "title": "Same title", "status": "passed"}]
    matches = match_results(actual, expected)
    assert len(matches) == 1
    assert matches[0].actual["signature"] == "A.Real"
