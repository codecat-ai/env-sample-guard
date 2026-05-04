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
    ignored_prefixes: set[str] | None = None,
) -> ComparisonResult:
    prefixes = tuple(ignored_prefixes or set())
    filtered_used = {name for name in used - ignored if not name.startswith(prefixes)}
    filtered_declared = {
        name for name in declared - ignored if not name.startswith(prefixes)
    }
    missing = filtered_used - filtered_declared
    stale = filtered_declared - filtered_used

    return ComparisonResult(
        used=sorted(filtered_used),
        declared=sorted(filtered_declared),
        missing=sorted(missing),
        stale=sorted(stale),
        ok=not missing and not stale,
    )
