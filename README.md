# env-sample-guard

`env-sample-guard` is a small CLI that checks whether environment variables used
in source code are documented in a sample file such as `.env.example`.

It scans source files with static heuristics, parses sample env declarations, and
reports:

- missing variables used by code but absent from the sample
- stale variables declared in the sample but not found in code
- deterministic JSON for CI and other tooling

The tool does not execute project code and does not read real `.env` secret files
while scanning source directories.

## Supported Patterns

The MVP scanner recognizes common environment access patterns in:

- Python
- JavaScript and TypeScript
- Go
- Rust
- Ruby
- shell-like files

It skips common generated or dependency directories such as `node_modules`,
`dist`, `build`, `target`, `.git`, and cache directories.

## Local Setup

Clone this repository and install it from the local checkout:

```bash
git clone <repository-url>
cd env-sample-guard
python -m pip install -e .[dev]
```

## Quick Start

Check the current directory against `.env.example`:

```bash
env-sample-guard check
```

Check explicit source paths and a sample file:

```bash
env-sample-guard check --source src --source scripts --sample .env.example
```

Return JSON:

```bash
env-sample-guard check --json
```

Treat stale sample variables as failures:

```bash
env-sample-guard check --strict-stale
```

Ignore known variables:

```bash
env-sample-guard check --ignore CI --ignore NODE_ENV
```

## Exit Codes

- `0`: no missing variables were found; stale variables are advisory unless
  `--strict-stale` is set
- `1`: missing variables were found, or stale variables were found with
  `--strict-stale`
- `2`: invalid CLI usage

## JSON Shape

```json
{
  "declared": ["DATABASE_URL"],
  "missing": ["API_TOKEN"],
  "ok": false,
  "sample": ".env.example",
  "stale": [],
  "used": ["API_TOKEN", "DATABASE_URL"]
}
```

## Development

Run the test suite:

```bash
python -m pytest -q
```

Run linting and formatting checks:

```bash
ruff check .
ruff format --check .
```

Build the package artifact locally:

```bash
python -m build
```

## Roadmap

- add more environment access patterns by language
- include optional reporter formats for CI annotations
- expose scanner configuration for unusual repository layouts

## AI-Assisted Maintenance Note

This project may be maintained with AI assistance, but changes should remain
reviewable, tested, and original to this repository.

## License

MIT. See [LICENSE](LICENSE).
