# Usage Guide

## Basic

    log-analyzer /var/log/nginx/access.log

## Top 20 paths/IPs

    log-analyzer access.log --top 20

## From stdin

    cat access.log | log-analyzer --stdin

## Supported formats

- Common Log Format (CLF)
- Combined Log Format (adds referrer + user agent)

Example line:

    127.0.0.1 - - [10/Oct/2026:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
