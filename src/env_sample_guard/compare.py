from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComparisonResult:
    used: list[str]
    declared: list[str]
    missing: list[str]
    stale: list[str]
    ok: bool


def compare_variables(
    *,
    used: set[str],
    declared: set[str],
    ignored: set[str],
) -> ComparisonResult:
    filtered_used = used - ignored
    filtered_declared = declared - ignored
    missing = filtered_used - filtered_declared
    stale = filtered_declared - filtered_used

    return ComparisonResult(
        used=sorted(filtered_used),
        declared=sorted(filtered_declared),
        missing=sorted(missing),
        stale=sorted(stale),
        ok=not missing and not stale,
    )
