"""Format and display analysis results using rich."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from .analyzer import AnalysisResult

console = Console()


def _human_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"


def _status_style(code: int) -> str:
    if 200 <= code < 300:
        return "green"
    if 300 <= code < 400:
        return "cyan"
    if 400 <= code < 500:
        return "yellow"
    return "red"


def print_report(result: AnalysisResult, source: str) -> None:
    """Print the analysis report to the terminal."""
    console.print()
    console.rule("[bold cyan]Log Analysis Report[/bold cyan]")
    console.print(f"[bold]Source:[/bold] {source}\n")

    summary = Table(title="Summary", show_header=True, header_style="bold magenta")
    summary.add_column("Metric", style="cyan", no_wrap=True)
    summary.add_column("Value", style="green")
    summary.add_row("Total lines", str(result.total_lines))
    summary.add_row("Parsed lines", str(result.parsed_lines))
    summary.add_row("Total bytes", _human_bytes(result.total_bytes))
    summary.add_row("Error rate (4xx/5xx)", f"{result.error_rate:.2f}%")
    console.print(summary)

    if result.status_counts:
        status = Table(title="Status Codes", show_header=True, header_style="bold magenta")
        status.add_column("Code", style="cyan", no_wrap=True)
        status.add_column("Count", style="green")
        for code, count in sorted(result.status_counts.items()):
            status.add_row(f"[{_status_style(code)}]{code}[/]", str(count))
        console.print(status)

    if result.method_counts:
        methods = Table(title="Methods", show_header=True, header_style="bold magenta")
        methods.add_column("Method", style="cyan", no_wrap=True)
        methods.add_column("Count", style="green")
        for method, count in result.method_counts.items():
            methods.add_row(method, str(count))
        console.print(methods)

    if result.top_paths:
        paths = Table(title="Top Paths", show_header=True, header_style="bold magenta")
        paths.add_column("Path", style="cyan")
        paths.add_column("Hits", style="green")
        for path, count in result.top_paths:
            paths.add_row(path, str(count))
        console.print(paths)

    if result.top_ips:
        ips = Table(title="Top IPs", show_header=True, header_style="bold magenta")
        ips.add_column("IP", style="cyan")
        ips.add_column("Requests", style="green")
        for ip, count in result.top_ips:
            ips.add_row(ip, str(count))
        console.print(ips)
