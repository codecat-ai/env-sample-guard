from pathlib import Path

from env_sample_guard.scanner import scan_sources


def test_detects_python_and_javascript_environment_access(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text(
        "import os\n"
        "os.environ['DATABASE_URL']\n"
        'os.getenv("API_TOKEN")\n'
        "os.environ.get('FEATURE_FLAG')\n",
        encoding="utf-8",
    )
    (tmp_path / "web.ts").write_text(
        "const a = process.env.PUBLIC_URL;\nconst b = process.env['NODE_ENV'];\n",
        encoding="utf-8",
    )

    assert scan_sources([tmp_path]) == {
        "API_TOKEN",
        "DATABASE_URL",
        "FEATURE_FLAG",
        "NODE_ENV",
        "PUBLIC_URL",
    }


def test_detects_go_rust_ruby_and_shell_patterns(tmp_path: Path) -> None:
    (tmp_path / "main.go").write_text('os.Getenv("GO_ENV")\n', encoding="utf-8")
    (tmp_path / "lib.rs").write_text('env::var("RUST_LOG")\n', encoding="utf-8")
    (tmp_path / "task.rb").write_text("ENV['RAILS_ENV']\n", encoding="utf-8")
    (tmp_path / "run.sh").write_text(
        "echo $SHELL_ENV ${BRACED_ENV}\n", encoding="utf-8"
    )

    assert scan_sources([tmp_path]) == {
        "BRACED_ENV",
        "GO_ENV",
        "RAILS_ENV",
        "RUST_LOG",
        "SHELL_ENV",
    }


def test_skips_secret_env_files_and_common_build_directories(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("SECRET_FROM_ENV=value\n", encoding="utf-8")
    (tmp_path / ".env.local").write_text("LOCAL_SECRET=value\n", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "app.js").write_text(
        "process.env.FROM_NODE_MODULES\n", encoding="utf-8"
    )
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist" / "app.py").write_text(
        "os.getenv('FROM_DIST')\n", encoding="utf-8"
    )
    (tmp_path / "app.py").write_text("os.getenv('REAL_VAR')\n", encoding="utf-8")

    assert scan_sources([tmp_path]) == {"REAL_VAR"}
