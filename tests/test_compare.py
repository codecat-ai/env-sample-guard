from env_sample_guard.compare import compare_variables


def test_missing_and_stale_are_sorted_and_ignore_applies_to_both_sides() -> None:
    result = compare_variables(
        used={"DATABASE_URL", "IGNORED_USED", "API_TOKEN"},
        declared={"DATABASE_URL", "IGNORED_DECLARED", "OLD_FLAG"},
        ignored={"IGNORED_USED", "IGNORED_DECLARED"},
    )

    assert result.used == ["API_TOKEN", "DATABASE_URL"]
    assert result.declared == ["DATABASE_URL", "OLD_FLAG"]
    assert result.missing == ["API_TOKEN"]
    assert result.stale == ["OLD_FLAG"]
    assert result.ok is False


def test_ignore_prefix_filters_used_declared_missing_and_stale_variables() -> None:
    result = compare_variables(
        used={"DATABASE_URL", "GITHUB_TOKEN", "AWS_REGION", "API_TOKEN"},
        declared={"DATABASE_URL", "GITHUB_RUN_ID", "AWS_DEFAULT_REGION", "OLD_FLAG"},
        ignored=set(),
        ignored_prefixes={"GITHUB_", "AWS_"},
    )

    assert result.used == ["API_TOKEN", "DATABASE_URL"]
    assert result.declared == ["DATABASE_URL", "OLD_FLAG"]
    assert result.missing == ["API_TOKEN"]
    assert result.stale == ["OLD_FLAG"]
    assert result.ok is False


def test_ok_when_no_missing_or_stale_variables() -> None:
    result = compare_variables(
        used={"DATABASE_URL"},
        declared={"DATABASE_URL"},
        ignored=set(),
    )

    assert result.ok is True
