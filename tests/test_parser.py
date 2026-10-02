"""Tests for the log parser."""

from log_analyzer.parser import parse_line, parse_lines

COMMON = '127.0.0.1 - - [10/Oct/2026:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326'
COMBINED = (
    '10.0.0.5 - alice [10/Oct/2026:13:56:01 +0000] "POST /api/login HTTP/1.1" 401 512 '
    '"https://example.com/login" "Mozilla/5.0"'
)


def test_parse_common_line():
    entry = parse_line(COMMON)
    assert entry is not None
    assert entry.ip == "127.0.0.1"
    assert entry.method == "GET"
    assert entry.path == "/index.html"
    assert entry.status == 200
    assert entry.size == 2326


def test_parse_combined_line():
    entry = parse_line(COMBINED)
    assert entry is not None
    assert entry.ip == "10.0.0.5"
    assert entry.method == "POST"
    assert entry.status == 401
    assert entry.referrer == "https://example.com/login"
    assert entry.agent == "Mozilla/5.0"


def test_parse_garbage_returns_none():
    assert parse_line("this is not a log line") is None
    assert parse_line("") is None


def test_parse_lines_skips_invalid():
    lines = [COMMON, "garbage", COMBINED, ""]
    entries = parse_lines(iter(lines))
    assert len(entries) == 2


def test_parse_dash_size_is_zero():
    line = '1.2.3.4 - - [10/Oct/2026:13:55:36 +0000] "GET / HTTP/1.1" 304 -'
    entry = parse_line(line)
    assert entry is not None
    assert entry.size == 0
