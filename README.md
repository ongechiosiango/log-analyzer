# Log Analyzer

[![CI](https://github.com/ongechiosiango/log-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/ongechiosiango/log-analyzer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

Parse HTTP access logs and report status code counts, top paths, and top IPs.

## Features

- Parses Common and Combined Log Formats.
- Reports status code distribution, error rate, top URLs, top IPs, and total bytes.
- Reads from a file or stdin.
- Color-coded rich terminal output.

## Installation

From source:

    git clone git@github.com:ongechiosiango/log-analyzer.git
    cd log-analyzer
    python3 -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"

## Usage

    log-analyzer /var/log/nginx/access.log

Top 20 paths and IPs:

    log-analyzer access.log --top 20

From stdin:

    cat access.log | log-analyzer --stdin

See docs/usage.md for more.

## Development

    pip install -e ".[dev]"
    pytest -v

## Contributing

See CONTRIBUTING.md.

## License

MIT - see LICENSE.
