#!/usr/bin/env python3
"""Validate the two lab identities, Wazuh services and member secure channel."""
from datetime import datetime, timezone
import json
from pathlib import Path
import winrm

root = Path(__file__).resolve().parents[1]
proof = {'checked_at': datetime.now(timezone.utc).isoformat(), 'hosts': {}}
for host, ip, expected in [('dc01', '192.168.56.30', 'dc'), ('ws01', '192.168.56.31', 'ws')]:
    client = winrm.Session(f'http://{ip}:5985/wsman', auth=('vagrant', 'vagrant'), transport='ntlm', operation_timeout_sec=30, read_timeout_sec=40)
    result = client.run_ps("$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue'; $c=Get-CimInstance Win32_ComputerSystem; @{name=$c.Name;domain=$c.Domain;joined=$c.PartOfDomain;wazuh=(Get-Service WazuhSvc).Status.ToString()} | ConvertTo-Json -Compress")
    if result.status_code:
        raise SystemExit(f'{host}: Windows status query failed')
    state = json.loads(result.std_out.decode().strip())
    if state['name'].lower() != expected or state['domain'].lower() != 'mini.lab' or not state['joined'] or state['wazuh'] != 'Running':
        raise SystemExit(f'{host}: unexpected name, domain or Wazuh service state')
    if host == 'ws01':
        # Netlogon can cache a failed discovery when WS boots before the DC.
        # Refresh discovery once; never reset the machine account password.
        result = client.run_ps("$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue'; if (-not (Test-ComputerSecureChannel -Server dc.mini.lab)) { Restart-Service Netlogon }; Test-ComputerSecureChannel -Server dc.mini.lab")
        state['secure_channel'] = result.status_code == 0 and result.std_out.decode().strip() == 'True'
        if not state['secure_channel']:
            raise SystemExit('WS01: secure channel validation failed')
    proof['hosts'][host] = state
(root / 'logs').mkdir(exist_ok=True)
(root / 'logs/domain-validation.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
