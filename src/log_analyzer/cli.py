"""Command-line interface for Log Analyzer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console

from .analyzer import analyze
from .parser import parse_lines
from .reporter import print_report

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="log-analyzer",
        description="Parse HTTP access logs and report statistics.",
    )
    parser.add_argument("logfile", nargs="?", default="-",
                        help="Path to the access log file (default: stdin).")
    parser.add_argument("--top", "-n", type=int, default=10,
                        help="How many top paths/IPs to show (default: 10).")
    parser.add_argument("--stdin", action="store_true",
                        help="Read the log from stdin.")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.stdin or args.logfile == "-":
        source = "<stdin>"
        lines = list(sys.stdin)
    else:
        source = args.logfile
        path = Path(args.logfile)
        if not path.exists():
            console.print(f"[bold red]Error:[/bold red] file not found: {args.logfile}")
            return 1
        if not path.is_file():
            console.print(f"[bold red]Error:[/bold red] not a file: {args.logfile}")
            return 1
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            lines = list(fh)

    entries = parse_lines(iter(lines))
    result = analyze(entries, raw_line_count=len(lines), top_n=args.top)
    print_report(result, source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
