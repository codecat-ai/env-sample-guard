# Changelog

All notable changes to this project will be documented in this file.

The format follows Keep a Changelog conventions, and this project uses
Conventional Commit messages.

## [0.1.0] - 2026-05-04

### Added

- Initial `env-sample-guard check` CLI.
- Static environment-variable discovery for Python, JavaScript, TypeScript, Go,
  Rust, Ruby, and shell-like files.
- `.env.example` style parser.
- Missing and stale variable comparison.
- Deterministic JSON output.
- Behavior tests created before implementation; the RED run failed with
  `ModuleNotFoundError` before the package was added.
