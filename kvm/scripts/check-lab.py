#!/usr/bin/env python3
"""Read-only checks, restricted to the two lab IP addresses."""
import json
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

results = {'checked_at': datetime.now(timezone.utc).isoformat(), 'hosts': {}}
for host, ip, ports in [('dc01', '192.168.56.30', [53, 88, 389, 445, 5985]), ('ws01', '192.168.56.31', [445, 5985])]:
    results['hosts'][host] = {'ip': ip, 'ports': {}}
    for port in ports:
        try:
            with socket.create_connection((ip, port), timeout=3):
                results['hosts'][host]['ports'][str(port)] = 'open'
        except OSError:
            results['hosts'][host]['ports'][str(port)] = 'unreachable'
print(json.dumps(results, indent=2))
out = Path(__file__).resolve().parents[1] / 'logs'
out.mkdir(exist_ok=True)
(out / 'health.json').write_text(json.dumps(results, indent=2))
sys.exit(0 if all(status == 'open' for host in results['hosts'].values() for status in host['ports'].values()) else 1)
