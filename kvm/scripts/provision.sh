#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
export ANSIBLE_COLLECTIONS_PATH="$root/collections"
export ANSIBLE_ROLES_PATH="$root/roles:$(dirname "$root")/GOAD/ansible/roles"
export ANSIBLE_CONFIG="$(dirname "$root")/GOAD/ansible/ansible.cfg"
export ANSIBLE_LOCAL_TEMP="$root/.ansible-tmp"
mkdir -p "$root/logs"
export ANSIBLE_LOG_PATH="$root/logs/provision.log"
cd "$(dirname "$root")/GOAD/ansible"
# MINILAB has no dedicated list in upstream playbooks.yml: upstream uses default.
mapfile -t playbooks < <("$root/.venv/bin/python" -c "import yaml; print('\n'.join(yaml.safe_load(open('../playbooks.yml'))['default']))")
for playbook in "${playbooks[@]}"; do
  "$root/.venv/bin/ansible-playbook" \
    -i ../ad/MINILAB/data/inventory -i "$root/inventory" -i ../globalsettings.ini \
    -e domain_name=MINILAB -e data_path=../ad/MINILAB/data/ "$playbook" "$@"
done
