import json
from pathlib import Path

from env_sample_guard.cli import main


def test_cli_missing_variable_returns_one_and_prints_concise_text(
    tmp_path: Path, capsys
) -> None:
    (tmp_path / ".env.example").write_text("DATABASE_URL=\n", encoding="utf-8")
    (tmp_path / "app.py").write_text(
        "import os\nos.getenv('DATABASE_URL')\nos.getenv('API_TOKEN')\n",
        encoding="utf-8",
    )

    code = main(
        ["check", "--source", str(tmp_path), "--sample", str(tmp_path / ".env.example")]
    )

    output = capsys.readouterr().out
    assert code == 1
    assert "Missing variables: API_TOKEN" in output
    assert "Stale variables:" not in output


def test_cli_stale_variable_is_advisory_unless_strict(tmp_path: Path, capsys) -> None:
    (tmp_path / ".env.example").write_text(
        "DATABASE_URL=\nOLD_FLAG=\n", encoding="utf-8"
    )
    (tmp_path / "app.py").write_text(
        "import os\nos.getenv('DATABASE_URL')\n", encoding="utf-8"
    )

    advisory = main(
        ["check", "--source", str(tmp_path), "--sample", str(tmp_path / ".env.example")]
    )
    strict = main(
        [
            "check",
            "--source",
            str(tmp_path),
            "--sample",
            str(tmp_path / ".env.example"),
            "--strict-stale",
        ]
    )

    output = capsys.readouterr().out
    assert advisory == 0
    assert strict == 1
    assert "Stale variables: OLD_FLAG" in output


def test_cli_json_output_is_parseable_sorted_and_deterministic(
    tmp_path: Path, capsys
) -> None:
    sample = tmp_path / "sample.env"
    sample.write_text("Z_STALE=\nDATABASE_URL=\n", encoding="utf-8")
    (tmp_path / "app.py").write_text(
        "import os\nos.getenv('API_TOKEN')\nos.getenv('DATABASE_URL')\n",
        encoding="utf-8",
    )

    code = main(
        [
            "check",
            "--source",
            str(tmp_path),
            "--sample",
            str(sample),
            "--ignore",
            "Z_STALE",
            "--json",
        ]
    )

    data = json.loads(capsys.readouterr().out)
    assert code == 1
    assert data == {
        "declared": ["DATABASE_URL"],
        "missing": ["API_TOKEN"],
        "ok": False,
        "sample": str(sample),
        "stale": [],
        "used": ["API_TOKEN", "DATABASE_URL"],
    }
