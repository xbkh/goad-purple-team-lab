#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$root/logs"
bash "$root/scripts/vagrant.sh" halt dc01 ws01
for name in goad-purple-mgmt goad-purple-lab; do
  virsh -c qemu:///system net-dumpxml "$name" > "$root/logs/$name-before.xml"
  python3 - "$name" "$root/logs" <<'PY'
import sys,xml.etree.ElementTree as E
from pathlib import Path
name,folder=sys.argv[1:]
p=Path(folder)
t=E.parse(p/f'{name}-before.xml');r=t.getroot()
assert r.findtext('name') == name and name in ('goad-purple-mgmt','goad-purple-lab')
for tag in ('forward','dns'):
 for node in r.findall(tag):r.remove(node)
E.SubElement(r,'dns',{'enable':'no'})
t.write(p/f'{name}-isolated.xml')
PY
  virsh -c qemu:///system net-destroy "$name"
  virsh -c qemu:///system net-define "$root/logs/$name-isolated.xml"
  virsh -c qemu:///system net-start "$name"
done
touch "$root/.isolated"
# Start the DC first so the member can discover it during Netlogon startup.
bash "$root/scripts/vagrant.sh" up dc01 --provider libvirt --no-provision
bash "$root/scripts/vagrant.sh" up ws01 --provider libvirt --no-provision
for name in goad-purple-mgmt goad-purple-lab; do
  virsh -c qemu:///system net-dumpxml "$name" > "$root/logs/$name-final.xml"
done
python3 - "$root/logs" <<'PY'
import sys,xml.etree.ElementTree as E
from pathlib import Path
for name in ('goad-purple-mgmt','goad-purple-lab'):
 r=E.parse(Path(sys.argv[1])/f'{name}-final.xml').getroot()
 assert r.find('forward') is None, f'{name}: forwarding still active'
 assert r.find('dns').get('enable') == 'no', f'{name}: DNS forwarding still enabled'
print('Deux réseaux libvirt sans transfert extérieur ni relais DNS')
PY
