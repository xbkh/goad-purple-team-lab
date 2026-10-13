#!/usr/bin/env python3
"""Regenerate only an unjoined WS01 that has the same SID as the DC base."""
import base64
import json
import os
from pathlib import Path
import subprocess
import time
import winrm

root = Path(__file__).resolve().parents[1]

def session(ip):
    return winrm.Session(f'http://{ip}:5985/wsman', auth=('vagrant', 'vagrant'), transport='ntlm', operation_timeout_sec=30, read_timeout_sec=40)

def ps(client, command):
    result = client.run_ps("$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue'; " + command)
    if result.status_code:
        raise RuntimeError('Windows preparation failed; inspect guest Sysprep logs')
    return result.std_out.decode().strip()

def identity(client):
    return json.loads(ps(client, "$c=Get-CimInstance Win32_ComputerSystem; @{domain=$c.Domain;joined=$c.PartOfDomain;sid=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value} | ConvertTo-Json -Compress"))

def prepare_hostname():
    env = dict(os.environ, ANSIBLE_COLLECTIONS_PATH=str(root / 'collections'), ANSIBLE_LOCAL_TEMP=str(root / '.ansible-tmp'))
    subprocess.run([str(root / '.venv/bin/ansible-playbook'), '-i', str(root.parent / 'GOAD/ad/MINILAB/data/inventory'), '-i', str(root / 'inventory'), str(root / 'member-preparation.yml')], env=env, check=True)

ws = session('192.168.56.31')
before = identity(ws)
if before['joined']:
    if before['domain'].lower() != 'mini.lab':
        raise SystemExit('WS01 belongs to an unexpected domain; no changes made')
    print('WS01 already belongs to mini.lab; no generalization needed')
    raise SystemExit(0)
dc = identity(session('192.168.56.30'))
if before['sid'].rsplit('-', 1)[0] != dc['sid'].rsplit('-', 1)[0]:
    print('WS01 has a distinct Windows identity; no generalization needed')
    prepare_hostname()
    raise SystemExit(0)
encoded = base64.b64encode((root / 'member-unattend.xml').read_bytes()).decode()
ps(ws, "[IO.File]::WriteAllBytes('C:\\goad-sysprep.xml',[Convert]::FromBase64String('" + encoded + "')); $a=New-ScheduledTaskAction -Execute 'C:\\Windows\\System32\\Sysprep\\Sysprep.exe' -Argument '/generalize /oobe /shutdown /quiet /unattend:C:\\goad-sysprep.xml'; Register-ScheduledTask -TaskName 'GOAD-Generalize-WS01' -Action $a -User 'SYSTEM' -RunLevel Highest -Force | Out-Null; Start-ScheduledTask -TaskName 'GOAD-Generalize-WS01'")
deadline = time.monotonic() + 600
while time.monotonic() < deadline:
    state = subprocess.check_output(['virsh', '-c', 'qemu:///system', 'domstate', 'kvm_ws01'], text=True).strip()
    if state == 'shut off':
        break
    time.sleep(5)
else:
    raise RuntimeError('Sysprep did not shut down WS01; inspect guest Sysprep logs')
subprocess.run(['bash', str(root / 'scripts/vagrant.sh'), 'up', 'ws01', '--provider', 'libvirt', '--no-provision'], check=True)
leases = subprocess.check_output(['virsh', '-c', 'qemu:///system', 'domifaddr', 'kvm_ws01', '--source', 'lease'], text=True)
ips = [word.split('/')[0] for word in leases.split() if word.startswith('192.168.57.') and '/' in word]
if len(ips) != 1:
    raise RuntimeError('Unexpected WS01 management address after Sysprep')
# Sysprep resets the private NIC to DHCP; Vagrant does not always reconfigure
# an already-created domain. Restore only the NIC on the owned lab subnet.
ps(session(ips[0]), "$m=@(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like '192.168.57.*'}); if($m.Count -ne 1){throw 'Unexpected management adapters'}; $a=@(Get-NetAdapter | Where-Object {$_.Status -eq 'Up' -and $_.ifIndex -ne $m[0].InterfaceIndex}); if($a.Count -ne 1){throw 'Unexpected lab adapters'}; $i=$a[0].ifIndex; Set-NetIPInterface -InterfaceIndex $i -AddressFamily IPv4 -Dhcp Disabled; if(-not(Get-NetIPAddress -InterfaceIndex $i -AddressFamily IPv4 | Where-Object {$_.IPAddress -eq '192.168.56.31'})){Get-NetIPAddress -InterfaceIndex $i -AddressFamily IPv4 | Where-Object {$_.IPAddress -like '192.168.56.*'} | Remove-NetIPAddress -Confirm:$false; New-NetIPAddress -InterfaceIndex $i -IPAddress 192.168.56.31 -PrefixLength 24 | Out-Null}; Set-DnsClientServerAddress -InterfaceIndex $i -ServerAddresses 192.168.56.30; Set-NetIPInterface -InterfaceIndex $i -InterfaceMetric 10")
after = identity(ws)
if after['sid'].rsplit('-', 1)[0] == before['sid'].rsplit('-', 1)[0]:
    raise RuntimeError('WS01 SID unchanged; domain join must not proceed')
ps(ws, "Unregister-ScheduledTask -TaskName 'GOAD-Generalize-WS01' -Confirm:$false; Remove-Item C:\\goad-sysprep.xml -Force")
prepare_hostname()
print('WS01 Windows identity regenerated and WinRM verified')
