#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
source_dir="$(dirname "$root")/GOAD"
revision=992307adf944b934a3b76a2f56a637104c54b805
if [[ ! -d "$source_dir/.git" ]]; then
  git clone https://github.com/Orange-Cyberdefense/GOAD.git "$source_dir"
  git -C "$source_dir" checkout --detach "$revision"
fi
if [[ "$(git -C "$source_dir" rev-parse HEAD)" != "$revision" ]]; then
  printf 'Révision GOAD différente de la révision validée ; vérifier avant de poursuivre.\n' >&2
  exit 1
fi
python3 -m venv "$root/.venv"
"$root/.venv/bin/pip" install -r "$root/requirements.lock.txt"
export ANSIBLE_LOCAL_TEMP="$root/.ansible-tmp"
export ANSIBLE_COLLECTIONS_PATH="$root/collections"
export ANSIBLE_ROLES_PATH="$root/roles"
"$root/.venv/bin/ansible-galaxy" collection install -r "$root/collections.lock.yml" -p "$root/collections" --timeout 20
"$root/.venv/bin/ansible-galaxy" role install geerlingguy.mysql,6.5.0 -p "$root/roles"
python3 - "$root" <<'PY'
from pathlib import Path
import secrets,sys
p=Path(sys.argv[1])/'wazuh/secrets'
p.mkdir(mode=0o700,exist_ok=True)
f=p/'authd.pass'
if not f.exists():
 f.write_text(secrets.token_hex(24)+'\n');f.chmod(0o600)
PY
curl -fL --retry 3 https://packages.wazuh.com/4.x/windows/wazuh-agent-4.14.0-1.msi -o "$root/wazuh/agent.msi"
printf '9a981846041bd289125c35aba5921ffcb6444d4c3c19326cb17ae37a684bfd6e  %s\n' "$root/wazuh/agent.msi" | sha256sum -c -
for item in goad-purple-lab:lab-network.xml goad-purple-mgmt:management-network.xml; do
  IFS=: read -r network xml <<< "$item"
  if ! virsh -c qemu:///system net-info "$network" >/dev/null 2>&1; then
    virsh -c qemu:///system net-define "$root/$xml"
  fi
  if ! virsh -c qemu:///system net-list --name | grep -qx "$network"; then
    virsh -c qemu:///system net-start "$network"
  fi
done
docker pull vagrantlibvirt/vagrant-libvirt@sha256:7939a158c938231361c8af26940fcb7f648c7f6e51abfcbcb2a6e6758fbdf826
docker pull wazuh/wazuh-manager@sha256:d2387a8304391600154c7b8604b390c8b798ec1403b5f1f707703bafdb230f84
