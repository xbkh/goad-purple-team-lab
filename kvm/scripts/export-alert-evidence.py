#!/usr/bin/env python3
"""Export minimal lab alert metadata without raw logs, command lines or secrets."""
import json
import re
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
output = root / 'logs' / 'alert-evidence.json'
output.parent.mkdir(exist_ok=True)
process = subprocess.Popen(
    ['docker', 'exec', 'goad-purple-wazuh', 'cat', '/var/ossec/logs/alerts/alerts.json'],
    stdout=subprocess.PIPE, text=True,
)
rows = []
for line in process.stdout:
    try:
        alert = json.loads(line)
    except json.JSONDecodeError:
        continue
    agent = alert.get('agent', {})
    rule = alert.get('rule', {})
    if agent.get('name') not in ('dc', 'ws') or str(rule.get('id')) not in ('100100', '100101', '100102'):
        continue
    win = alert.get('data', {}).get('win', {})
    event = win.get('eventdata', {})
    row = {
        'timestamp': alert.get('timestamp'),
        'agent': agent['name'],
        'rule_id': str(rule['id']),
        'event_id': str(win.get('system', {}).get('eventID', '')),
    }
    # Only an explicit allowlist is exported. Properties can contain GUIDs but
    # are never exported as raw text. Never include full_log or script blocks.
    if event.get('ipAddress') in ('192.168.56.1', '192.168.56.30', '192.168.56.31'):
        row['source_ip'] = event['ipAddress']
    if str(event.get('logonType', '')) in ('2', '3', '4', '5', '7', '8', '9', '10', '11'):
        row['logon_type'] = str(event['logonType'])
    for field in ('subjectUserName', 'targetUserName'):
        name = event.get(field, '')
        if name.lower() in ('alice', 'bob', 'carol', 'dave', 'administrator', 'vagrant', 'dc$', 'ws$', 'goad-telemetry-test'):
            row[field] = name
    guids = re.findall(r'(?i)(?:1131f6aa|1131f6ad|89e95b76)-[0-9a-f-]{27,}', event.get('properties', ''))
    if guids:
        row['replication_guids'] = sorted(set(g.lower() for g in guids))
    rows.append(row)
if process.wait() != 0:
    raise SystemExit('Cannot read Wazuh alerts; evidence file not updated')
output.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'exported_alerts': len(rows), 'agents': sorted(set(r['agent'] for r in rows)), 'output': str(output)}))
