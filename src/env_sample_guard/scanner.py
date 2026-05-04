from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

ENV_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    ".env.test",
}
SKIP_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}
SOURCE_SUFFIXES = {
    ".bash",
    ".cjs",
    ".envrc",
    ".go",
    ".js",
    ".jsx",
    ".ksh",
    ".mjs",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".ts",
    ".tsx",
    ".zsh",
}
SOURCE_NAMES = {"bashrc", "profile", "zshrc"}
VAR_NAME = r"[A-Za-z_][A-Za-z0-9_]*"
ENV_PATTERNS = [
    re.compile(rf"os\.environ\[['\"]({VAR_NAME})['\"]\]"),
    re.compile(rf"os\.environ\.get\(['\"]({VAR_NAME})['\"]"),
    re.compile(rf"os\.getenv\(['\"]({VAR_NAME})['\"]"),
    re.compile(rf"process\.env\.({VAR_NAME})\b"),
    re.compile(rf"process\.env\[['\"]({VAR_NAME})['\"]\]"),
    re.compile(rf"os\.Getenv\(['\"]({VAR_NAME})['\"]\)"),
    re.compile(rf"env::var\(['\"]({VAR_NAME})['\"]\)"),
    re.compile(rf"ENV\[['\"]({VAR_NAME})['\"]\]"),
]
SHELL_PATTERNS = [
    re.compile(rf"\$\{{({VAR_NAME})\}}"),
    re.compile(rf"(?<![\w$])\$({VAR_NAME})\b"),
]


def scan_sources(paths: Iterable[Path]) -> set[str]:
    variables: set[str] = set()
    for path in paths:
        variables.update(_scan_path(Path(path)))
    return variables


def _scan_path(path: Path) -> set[str]:
    if path.is_file():
        return _scan_file(path)
    if not path.exists():
        return set()

    variables: set[str] = set()
    for child in path.rglob("*"):
        if _is_skipped(child):
            continue
        if child.is_file():
            variables.update(_scan_file(child))
    return variables


def _scan_file(path: Path) -> set[str]:
    if _is_secret_env_file(path) or not _is_supported_source(path):
        return set()
    text = path.read_text(encoding="utf-8", errors="ignore")
    variables: set[str] = set()
    for pattern in ENV_PATTERNS:
        variables.update(match.group(1) for match in pattern.finditer(text))
    if path.suffix in {".sh", ".bash", ".zsh", ".ksh", ".envrc"}:
        for pattern in SHELL_PATTERNS:
            variables.update(match.group(1) for match in pattern.finditer(text))
    return variables


def _is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts) or _is_secret_env_file(path)


def _is_secret_env_file(path: Path) -> bool:
    return path.name in ENV_FILE_NAMES


def _is_supported_source(path: Path) -> bool:
    return path.suffix in SOURCE_SUFFIXES or path.name in SOURCE_NAMES
