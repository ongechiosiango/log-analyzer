"""Tests for the analyzer."""

from log_analyzer.analyzer import analyze
from log_analyzer.parser import LogEntry


def _entry(ip="1.1.1.1", path="/", status=200, size=100, method="GET"):
    return LogEntry(
        ip=ip, timestamp="x", method=method, path=path,
        status=status, size=size,
    )


def test_analyze_empty():
    result = analyze([], raw_line_count=5)
    assert result.total_lines == 5
    assert result.parsed_lines == 0
    assert result.status_counts == {}


def test_analyze_status_counts():
    entries = [
        _entry(status=200),
        _entry(status=200),
        _entry(status=404),
        _entry(status=500),
    ]
    result = analyze(entries, raw_line_count=4)
    assert result.status_counts == {200: 2, 404: 1, 500: 1}


def test_analyze_error_rate():
    entries = [
        _entry(status=200),
        _entry(status=500),
    ]
    result = analyze(entries, raw_line_count=2)
    assert result.error_rate == 50.0


def test_analyze_top_paths_and_ips():
    entries = [
        _entry(ip="10.0.0.1", path="/a"),
        _entry(ip="10.0.0.1", path="/a"),
        _entry(ip="10.0.0.1", path="/b"),
        _entry(ip="10.0.0.2", path="/a"),
    ]
    result = analyze(entries, raw_line_count=4, top_n=2)
    assert result.top_paths[0] == ("/a", 3)
    assert result.top_ips[0] == ("10.0.0.1", 3)


def test_analyze_total_bytes():
    entries = [_entry(size=1000), _entry(size=2000)]
    result = analyze(entries, raw_line_count=2)
    assert result.total_bytes == 3000
