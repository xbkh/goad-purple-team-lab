#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$root/logs"
trap 'printf "Arrêt sur une erreur : consulter logs/finish-setup.log\n" > "$root/logs/setup-status.txt"' ERR
printf 'En attente des deux VM Windows\n' > "$root/logs/setup-status.txt"
deadline=$((SECONDS + 10800))
while [[ ! -f "$root/cache/dc01.boot-ok" || ! -f "$root/cache/ws01.boot-ok" ]]; do
  if [[ -f "$root/cache/dc01.boot-failed" || -f "$root/cache/ws01.boot-failed" ]]; then
    printf 'Échec de démarrage Windows : consulter cache/deploy-*.log\n' > "$root/logs/setup-status.txt"
    exit 1
  fi
  if (( SECONDS >= deadline )); then
    printf 'Le démarrage des VM a dépassé trois heures\n' >&2
    exit 1
  fi
  sleep 20
done
printf 'Provisionnement du domaine en cours\n' > "$root/logs/setup-status.txt"
bash "$root/scripts/provision.sh"
printf 'Installation des agents Wazuh en cours\n' > "$root/logs/setup-status.txt"
export ANSIBLE_LOCAL_TEMP="$root/.ansible-tmp"
export ANSIBLE_COLLECTIONS_PATH="$root/collections"
export ANSIBLE_CONFIG="$(dirname "$root")/GOAD/ansible/ansible.cfg"
"$root/.venv/bin/ansible-playbook" \
  -i "$(dirname "$root")/GOAD/ad/MINILAB/data/inventory" -i "$root/inventory" \
  "$root/wazuh/install-agents.yml"
printf 'Isolation des réseaux et redémarrage du lab en cours\n' > "$root/logs/setup-status.txt"
bash "$root/scripts/isolate.sh"
python3 "$root/scripts/check-lab.py"
printf 'Domaine provisionné, agents installés, réseaux isolés ; collecte réelle à vérifier avant les attaques\n' > "$root/logs/setup-status.txt"
