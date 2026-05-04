# TDD Record

Date: 2026-05-04

## RED

Behavior tests were added before implementation for:

- sample env parsing
- source scanning across the MVP languages
- comparison and ignore rules
- CLI text, JSON, and exit behavior

Command:

```bash
python -m pytest -q
```

Observed failure:

```text
ModuleNotFoundError: No module named 'env_sample_guard'
```

Pytest stopped during collection with four import errors because the package did
not exist yet.

## GREEN

Minimal package code was added under `src/env_sample_guard/`.

Command:

```bash
python -m pytest tests/test_sample_parser.py tests/test_scanner.py tests/test_compare.py tests/test_cli.py -q
```

Observed result:

```text
10 passed
```

## REFACTOR

After the behavior tests passed, formatting and lint cleanup was applied with
Ruff. The full test suite and lint checks were then rerun.
