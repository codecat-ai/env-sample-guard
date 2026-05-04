# Clean-room brief: env-sample-guard

## Decision report
- Community need: 8/10. Many projects rely on environment variables, but `.env.example` files drift from code and onboarding breaks quietly.
- Originality: 7/10. Instead of loading secrets or validating runtime config, this CLI performs static cross-language discovery and compares docs/examples.
- Implementation feasibility: 8/10. A focused static scanner and CLI can be built as a Python package in one run.
- Maintenance cost: 6/10. Heuristics can expand by language without complex dependencies.
- Testing feasibility: 9/10. Temporary fixtures can verify parsing, comparison, JSON, and exit codes.
- Documentation clarity: 8/10. The behavior is easy to explain with small examples.
- Legal/security/platform risk: low. The tool must never read `.env` secret values by default; it inspects variable names only.

## Target users
Maintainers, CI authors, and developer-experience engineers who keep `.env.example`, README configuration sections, and source code in sync.

## Problem statement
Projects often add `DATABASE_URL`, `API_TOKEN`, or feature flags in code but forget to update `.env.example`. New contributors then hit unclear runtime errors. Conversely, old variables remain documented after code no longer uses them.

## Non-goals
- Do not load or print real `.env` secret values.
- Do not execute project code.
- Do not perform complete language parsing; use safe static heuristics.
- Do not publish to PyPI in this run.

## MVP features
- Python CLI command `env-sample-guard check`.
- Recursively scan source files for common environment-variable access patterns in Python, JavaScript/TypeScript, Go, Rust, Ruby, and shell-like files.
- Parse `.env.example` style files for declared variable names.
- Report missing variables (used in code but absent from sample) and stale variables (declared in sample but not used in code).
- Options: `--sample PATH`, `--source PATH` repeatable, `--json`, `--strict-stale`, `--ignore NAME` repeatable.
- Exit non-zero on missing variables, and on stale variables only when `--strict-stale` is set.
- Never inspect `.env`, `.env.local`, or obvious secret files unless explicitly passed as `--sample`.

## Expected CLI behavior
- Text output is concise and CI-friendly.
- JSON output is deterministic and contains `sample`, `used`, `declared`, `missing`, `stale`, and `ok`.
- Default source is current directory; default sample is `.env.example`.

## Test scenarios
- Python and JS env access detection.
- `.env.example` comments, `export NAME=value`, blank values, and quoted values.
- Missing variable causes exit code 1.
- Stale variable is advisory by default and strict with `--strict-stale`.
- `--ignore` removes variables from both sides.
- JSON output is parseable and sorted.
- Scanner skips `.env` secret files and common build directories.

## File structure
- `src/env_sample_guard/` package with scanner, env sample parser, comparison, and CLI modules.
- `tests/` pytest suite with fixture-based tests.
- Standard open-source docs: README.md, README-zh.md, README-jp.md, LICENSE, CHANGELOG.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, issue templates, PR template.
- GitHub Actions CI running tests, ruff, format check, and package build.

## CI plan
Use Python 3.11 on GitHub Actions. Install with `python -m pip install -e .[dev]`, run `ruff check .`, `ruff format --check .`, `pytest -q`, and `python -m build`.

## README outline
Name/value proposition, problem, features, installation from GitHub clone/local editable install only, quick start, examples, configuration, development, testing, roadmap, contributing, MIT license, short AI-assisted maintenance note.
