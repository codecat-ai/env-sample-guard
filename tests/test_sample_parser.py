from pathlib import Path

from env_sample_guard.sample import parse_sample_file


def test_parse_env_sample_comments_exports_blank_and_quoted_values(
    tmp_path: Path,
) -> None:
    sample = tmp_path / ".env.example"
    sample.write_text(
        "\n".join(
            [
                "# comment",
                "export DATABASE_URL=postgres://localhost/app",
                "API_TOKEN=",
                "QUOTED='abc=123'",
                'DOUBLE_QUOTED="value"',
                "INVALID-NAME=value",
                "",
            ]
        ),
        encoding="utf-8",
    )

    assert parse_sample_file(sample) == {
        "API_TOKEN",
        "DATABASE_URL",
        "DOUBLE_QUOTED",
        "QUOTED",
    }


def test_parse_missing_sample_as_empty(tmp_path: Path) -> None:
    assert parse_sample_file(tmp_path / ".env.example") == set()
