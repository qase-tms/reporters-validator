from dataclasses import dataclass


@dataclass
class MatchResult:
    actual: dict | None
    expected: dict


def match_results(actual_results: list[dict], expected_results: list[dict]) -> list[MatchResult]:
    """Match actual results to expected by signature (fallback: title).

    Returns one MatchResult per expected entry. If no actual matches, actual is None.
    Extra actual results (not in expected) are ignored.
    """
    # Build lookup indexes from actual results
    by_signature: dict[str, dict] = {}
    by_title: dict[str, dict] = {}
    for result in actual_results:
        sig = result.get("signature")
        if sig:
            by_signature[sig] = result
        title = result.get("title")
        if title:
            by_title[title] = result

    matched_ids: set[int] = set()
    matches: list[MatchResult] = []

    for exp in expected_results:
        actual = None
        # Try signature first
        sig = exp.get("signature")
        if sig and sig in by_signature:
            actual = by_signature[sig]
        else:
            # Fallback to title
            title = exp.get("title")
            if title and title in by_title:
                candidate = by_title[title]
                if id(candidate) not in matched_ids:
                    actual = candidate

        if actual is not None:
            matched_ids.add(id(actual))

        matches.append(MatchResult(actual=actual, expected=exp))

    return matches
