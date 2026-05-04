from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from env_sample_guard.compare import ComparisonResult, compare_variables
from env_sample_guard.sample import parse_sample_file
from env_sample_guard.scanner import scan_sources


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "check":
        return _run_check(args)
    parser.print_help()
    return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="env-sample-guard",
        description="Check that source environment variables match an env sample file.",
    )
    subparsers = parser.add_subparsers(dest="command")
    check = subparsers.add_parser(
        "check", help="compare source usage with a sample file"
    )
    check.add_argument("--sample", type=Path, default=Path(".env.example"))
    check.add_argument("--source", action="append", type=Path, default=None)
    check.add_argument("--json", action="store_true", dest="json_output")
    check.add_argument("--strict-stale", action="store_true")
    check.add_argument("--ignore", action="append", default=[])
    return parser


def _run_check(args: argparse.Namespace) -> int:
    source_paths = args.source if args.source is not None else [Path.cwd()]
    declared = parse_sample_file(args.sample)
    used = scan_sources(source_paths)
    result = compare_variables(used=used, declared=declared, ignored=set(args.ignore))

    if args.json_output:
        print(_to_json(result, sample=args.sample))
    else:
        _print_text(result)

    if result.missing:
        return 1
    if args.strict_stale and result.stale:
        return 1
    return 0


def _to_json(result: ComparisonResult, *, sample: Path) -> str:
    return json.dumps(
        {
            "sample": str(sample),
            "used": result.used,
            "declared": result.declared,
            "missing": result.missing,
            "stale": result.stale,
            "ok": result.ok,
        },
        sort_keys=True,
    )


def _print_text(result: ComparisonResult) -> None:
    if result.missing:
        print(f"Missing variables: {', '.join(result.missing)}")
    if result.stale:
        print(f"Stale variables: {', '.join(result.stale)}")
    if not result.missing and not result.stale:
        print("Environment sample is in sync.")
