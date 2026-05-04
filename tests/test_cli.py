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


def test_cli_json_ignore_prefix_is_repeatable_and_filters_all_sets(
    tmp_path: Path, capsys
) -> None:
    sample = tmp_path / ".env.example"
    sample.write_text(
        "DATABASE_URL=\nGITHUB_RUN_ID=\nAWS_DEFAULT_REGION=\nOLD_FLAG=\n",
        encoding="utf-8",
    )
    (tmp_path / "app.py").write_text(
        "\n".join(
            [
                "import os",
                "os.getenv('DATABASE_URL')",
                "os.getenv('GITHUB_TOKEN')",
                "os.getenv('AWS_REGION')",
                "os.getenv('API_TOKEN')",
            ]
        ),
        encoding="utf-8",
    )

    code = main(
        [
            "check",
            "--source",
            str(tmp_path),
            "--sample",
            str(sample),
            "--ignore-prefix",
            "GITHUB_",
            "--ignore-prefix",
            "AWS_",
            "--json",
        ]
    )

    data = json.loads(capsys.readouterr().out)
    assert code == 1
    assert data == {
        "declared": ["DATABASE_URL", "OLD_FLAG"],
        "missing": ["API_TOKEN"],
        "ok": False,
        "sample": str(sample),
        "stale": ["OLD_FLAG"],
        "used": ["API_TOKEN", "DATABASE_URL"],
    }


def test_cli_ignore_file_ignores_exact_names_and_combines_with_flags(
    tmp_path: Path, capsys
) -> None:
    sample = tmp_path / ".env.example"
    ignore_file = tmp_path / ".env-sample-guard-ignore"
    sample.write_text("DATABASE_URL=\nLOCAL_ONLY=\nEXPLICIT_ONLY=\n", encoding="utf-8")
    ignore_file.write_text("LOCAL_ONLY\n", encoding="utf-8")
    (tmp_path / "app.py").write_text(
        "\n".join(
            [
                "import os",
                "os.getenv('DATABASE_URL')",
                "os.getenv('LOCAL_ONLY')",
                "os.getenv('EXPLICIT_ONLY')",
                "os.getenv('API_TOKEN')",
            ]
        ),
        encoding="utf-8",
    )

    code = main(
        [
            "check",
            "--source",
            str(tmp_path),
            "--sample",
            str(sample),
            "--ignore-file",
            str(ignore_file),
            "--ignore",
            "EXPLICIT_ONLY",
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


def test_cli_ignore_file_ignores_wildcard_prefixes_and_combines_with_prefix_flags(
    tmp_path: Path, capsys
) -> None:
    sample = tmp_path / ".env.example"
    ignore_file = tmp_path / "ignore.env"
    sample.write_text(
        "DATABASE_URL=\nGITHUB_RUN_ID=\nAWS_DEFAULT_REGION=\nOLD_FLAG=\n",
        encoding="utf-8",
    )
    ignore_file.write_text("GITHUB_*\n", encoding="utf-8")
    (tmp_path / "app.py").write_text(
        "\n".join(
            [
                "import os",
                "os.getenv('DATABASE_URL')",
                "os.getenv('GITHUB_TOKEN')",
                "os.getenv('AWS_REGION')",
                "os.getenv('API_TOKEN')",
            ]
        ),
        encoding="utf-8",
    )

    code = main(
        [
            "check",
            "--source",
            str(tmp_path),
            "--sample",
            str(sample),
            "--ignore-file",
            str(ignore_file),
            "--ignore-prefix",
            "AWS_",
            "--json",
        ]
    )

    data = json.loads(capsys.readouterr().out)
    assert code == 1
    assert data == {
        "declared": ["DATABASE_URL", "OLD_FLAG"],
        "missing": ["API_TOKEN"],
        "ok": False,
        "sample": str(sample),
        "stale": ["OLD_FLAG"],
        "used": ["API_TOKEN", "DATABASE_URL"],
    }


def test_cli_ignore_file_skips_blank_lines_and_comments(tmp_path: Path, capsys) -> None:
    sample = tmp_path / ".env.example"
    ignore_file = tmp_path / "ignore.env"
    sample.write_text("DATABASE_URL=\nLOCAL_ONLY=\nGITHUB_RUN_ID=\n", encoding="utf-8")
    ignore_file.write_text(
        "\n  # local development values\n  LOCAL_ONLY  \n\t# ci values\n  GITHUB_*  \n",
        encoding="utf-8",
    )
    (tmp_path / "app.py").write_text(
        "\n".join(
            [
                "import os",
                "os.getenv('DATABASE_URL')",
                "os.getenv('LOCAL_ONLY')",
                "os.getenv('GITHUB_TOKEN')",
            ]
        ),
        encoding="utf-8",
    )

    code = main(
        [
            "check",
            "--source",
            str(tmp_path),
            "--sample",
            str(sample),
            "--ignore-file",
            str(ignore_file),
            "--json",
        ]
    )

    data = json.loads(capsys.readouterr().out)
    assert code == 0
    assert data == {
        "declared": ["DATABASE_URL"],
        "missing": [],
        "ok": True,
        "sample": str(sample),
        "stale": [],
        "used": ["DATABASE_URL"],
    }


def test_cli_ignore_file_missing_path_exits_with_argparse_error(
    tmp_path: Path, capsys
) -> None:
    missing = tmp_path / "missing.ignore"

    try:
        main(["check", "--ignore-file", str(missing)])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("missing ignore file should exit through argparse")

    error = capsys.readouterr().err
    assert "error:" in error
    assert "ignore file not found" in error
    assert str(missing) in error
