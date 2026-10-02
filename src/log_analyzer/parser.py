"""Parse HTTP access log lines in Common and Combined formats.

Example Common:
    127.0.0.1 - - [10/Oct/2026:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326

Example Combined (adds referrer and user agent):
    127.0.0.1 - - [10/Oct/2026:13:55:36 +0000] "GET / HTTP/1.1" 200 2326 "-" "curl/8.0"
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+'
    r'\S+\s+'
    r'\S+\s+'
    r'\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<request>[^"]*)"\s+'
    r'(?P<status>\d{3})\s+'
    r'(?P<size>\S+)'
    r'(?:\s+"(?P<referrer>[^"]*)"\s+"(?P<agent>[^"]*)")?'
    r'\s*$'
)

REQUEST_PATTERN = re.compile(r'^(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+(?P<proto>HTTP/\d\.\d)$')


@dataclass
class LogEntry:
    """A single parsed log line."""

    ip: str
    timestamp: str
    method: Optional[str]
    path: Optional[str]
    status: int
    size: int
    referrer: Optional[str] = None
    agent: Optional[str] = None


def parse_line(line: str) -> Optional[LogEntry]:
    """Parse a single log line. Returns None if it doesn't match."""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    method = path = None
    request_match = REQUEST_PATTERN.match(match.group("request"))
    if request_match:
        method = request_match.group("method")
        path = request_match.group("path")

    size_str = match.group("size")
    size = int(size_str) if size_str.isdigit() else 0

    return LogEntry(
        ip=match.group("ip"),
        timestamp=match.group("time"),
        method=method,
        path=path,
        status=int(match.group("status")),
        size=size,
        referrer=match.group("referrer"),
        agent=match.group("agent"),
    )


def parse_lines(lines):
    """Parse an iterable of lines, skipping any that don't match."""
    entries = []
    for raw in lines:
        entry = parse_line(raw)
        if entry is not None:
            entries.append(entry)
    return entries
