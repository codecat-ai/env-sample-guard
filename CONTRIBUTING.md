# Contributing

Thanks for helping improve `env-sample-guard`.

## Development Setup

Use a local checkout:

```bash
git clone <repository-url>
cd env-sample-guard
python -m pip install -e .[dev]
```

## Workflow

1. Create or update behavior tests before changing implementation code.
2. Run the focused tests that cover your change.
3. Run the full suite and quality checks before opening a pull request.
4. Use Conventional Commit messages, for example `fix: handle env access in rb`.
5. Keep code comments in English.

## Checks

```bash
python -m pytest -q
ruff check .
ruff format --check .
python -m build
```

## Pull Requests

Pull requests should explain the problem, the chosen approach, and the tests
that prove the behavior. Do not include generated secrets, real `.env` files, or
unrelated formatting changes.
