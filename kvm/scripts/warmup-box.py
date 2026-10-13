#!/usr/bin/env python3
"""Finish Windows first boot in a temporary VM before Vagrant uses WinRM."""
import json
from pathlib import Path
import subprocess
import sys
import time
import winrm

root = Path(__file__).resolve().parents[1]
name, disk_arg = sys.argv[1:3]
assert name in ('dc01', 'ws01')
disk = Path(disk_arg).resolve()
assert disk.is_relative_to(root / 'cache')
resume = len(sys.argv) == 4
prefix = sys.argv[3] if resume else f'goad_warm_{name}_{int(time.time())}'
assert prefix.startswith(f'goad_warm_{name}_') and prefix.rsplit('_', 1)[-1].isdigit()
base = prefix + '_base.qcow2'
overlay = prefix + '_overlay.qcow2'
folder = root / 'cache' / prefix
folder.mkdir(exist_ok=resume)

def virsh(*args, capture=False):
    command = ['virsh', '-c', 'qemu:///system', *args]
    if capture:
        return subprocess.check_output(command, text=True)
    subprocess.run(command, check=True)

info = json.loads(subprocess.check_output(['qemu-img', 'info', '--output=json', str(disk)]))
for volume, backing in ([] if resume else [(base, ''), (overlay, f'<backingStore><path>/var/lib/libvirt/images/{base}</path><format type="qcow2"/></backingStore>')]):
    xml = folder / (volume + '.xml')
    xml.write_text(f'<volume><name>{volume}</name><capacity>{info["virtual-size"]}</capacity><allocation>0</allocation><target><format type="qcow2"/></target>{backing}</volume>')
    virsh('vol-create', 'default', str(xml))
if not resume:
    virsh('vol-upload', base, str(disk), '--pool', 'default')
domain = folder / 'domain.xml'
domain.write_text(f'''<domain type="kvm"><name>{prefix}</name><memory unit="MiB">2048</memory><vcpu>2</vcpu><os><type arch="x86_64" machine="pc">hvm</type><boot dev="hd"/></os><features><acpi/><apic/></features><cpu mode="host-passthrough"/><clock offset="localtime"/><devices><disk type="file" device="disk"><driver name="qemu" type="qcow2"/><source file="/var/lib/libvirt/images/{overlay}"/><target dev="hda" bus="ide"/></disk><interface type="network"><source network="goad-purple-mgmt"/><model type="e1000"/></interface><graphics type="vnc" port="-1" listen="127.0.0.1"/><video><model type="vga"/></video><input type="mouse" bus="ps2"/></devices></domain>''')
if not resume:
    virsh('define', str(domain))
    virsh('start', prefix)
deadline = time.monotonic() + 1200
ready = False
while time.monotonic() < deadline:
    interfaces = virsh('domifaddr', prefix, '--source', 'lease', capture=True)
    ips = [word.split('/')[0] for word in interfaces.split() if word.startswith('192.168.57.') and '/' in word]
    if ips:
        try:
            session = winrm.Session(f'http://{ips[0]}:5985/wsman', auth=('vagrant', 'vagrant'), transport='ntlm', operation_timeout_sec=30, read_timeout_sec=40)
            response = session.run_ps("$s = Get-ItemProperty 'HKLM:\\SYSTEM\\Setup'; if ($s.SystemSetupInProgress -eq 0 -and $s.OOBEInProgress -eq 0) { hostname; exit 0 } else { exit 1 }")
            if response.status_code == 0:
                ready = True
                print(f'{name}: Windows setup complete, WinRM usable ({ips[0]})', flush=True)
                break
        except Exception:
            pass
    time.sleep(10)
if not ready:
    raise RuntimeError(f'Windows first boot incomplete: temporary VM {prefix} retained for diagnosis')
try:
    session.run_cmd('shutdown.exe', ['/s', '/f', '/t', '0'])
except Exception:
    # WinRM can close while the guest performs the requested orderly shutdown.
    pass
for _ in range(60):
    if virsh('domstate', prefix, capture=True).strip() == 'shut off':
        break
    time.sleep(2)
else:
    raise RuntimeError('Shutdown incomplete: disk conversion cancelled')
local_overlay = folder / 'overlay.qcow2'
virsh('vol-download', overlay, str(local_overlay), '--pool', 'default')
subprocess.run(['qemu-img', 'rebase', '-u', '-f', 'qcow2', '-F', 'qcow2', '-b', str(disk), str(local_overlay)], check=True)
warmed = disk.with_suffix('.warmed')
subprocess.run(['qemu-img', 'convert', '-p', '-f', 'qcow2', '-O', 'qcow2', str(local_overlay), str(warmed)], check=True)
subprocess.run(['qemu-img', 'check', str(warmed)], check=True)
warmed.replace(disk)
(disk.parent / '.warmup-ok').write_text('Windows setup and WinRM validated\n')
virsh('undefine', prefix)
virsh('vol-delete', overlay, '--pool', 'default')
virsh('vol-delete', base, '--pool', 'default')
local_overlay.unlink()
(folder / 'completed.json').write_text(json.dumps({'machine': name, 'windows_first_boot': 'completed', 'winrm': 'validated'}))
