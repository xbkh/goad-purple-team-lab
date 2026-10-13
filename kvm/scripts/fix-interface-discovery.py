#!/usr/bin/env python3
"""Correct upstream run_once propagation for Windows NIC discovery in MINILAB."""
from pathlib import Path

source = Path(__file__).resolve().parents[2] / 'GOAD/ansible/data.yml'
text = source.read_text()
head, marker, tail = text.partition('    - name: find domain_adapter\n')
if not marker:
    raise SystemExit('Unexpected upstream data.yml: interface discovery task missing')
# Lab configuration is shared; NIC facts must be determined separately per host.
fixed = head + marker + tail.replace('      run_once: true\n', '')
if fixed != text:
    source.write_text(fixed)
    print('Windows NIC discovery now runs on each host')
