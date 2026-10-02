"""Compute statistics over a list of LogEntry objects."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


@dataclass
class AnalysisResult:
    """Aggregated analysis of a log file."""

    total_lines: int = 0
    parsed_lines: int = 0
    status_counts: dict = field(default_factory=dict)
    method_counts: dict = field(default_factory=dict)
    top_paths: list = field(default_factory=list)
    top_ips: list = field(default_factory=list)
    total_bytes: int = 0
    error_rate: float = 0.0


def analyze(entries, raw_line_count: int = 0, top_n: int = 10) -> AnalysisResult:
    """Compute aggregate statistics from parsed log entries."""
    if not entries:
        return AnalysisResult(total_lines=raw_line_count)

    status_counter = Counter(e.status for e in entries)
    method_counter = Counter(e.method for e in entries if e.method)
    path_counter = Counter(e.path for e in entries if e.path)
    ip_counter = Counter(e.ip for e in entries)

    total_bytes = sum(e.size for e in entries)
    error_count = sum(1 for e in entries if 400 <= e.status < 600)
    error_rate = (error_count / len(entries)) * 100 if entries else 0.0

    return AnalysisResult(
        total_lines=raw_line_count,
        parsed_lines=len(entries),
        status_counts=dict(status_counter.most_common()),
        method_counts=dict(method_counter.most_common()),
        top_paths=path_counter.most_common(top_n),
        top_ips=ip_counter.most_common(top_n),
        total_bytes=total_bytes,
        error_rate=round(error_rate, 2),
    )
