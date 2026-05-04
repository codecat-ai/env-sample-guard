from __future__ import annotations

import re
from pathlib import Path

NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def parse_sample_file(path: Path) -> set[str]:
    if not path.exists():
        return set()

    names: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[len("export ") :].lstrip()
        name, separator, _value = stripped.partition("=")
        if separator and NAME_RE.match(name.strip()):
            names.add(name.strip())
    return names
