#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
name="${1:?Usage: deploy-machine.sh dc01|ws01}"
case "$name" in dc01|ws01) ;; *) exit 2;; esac
rm -f "$root/cache/$name.boot-failed"
trap 'touch "$root/cache/$name.boot-failed"' ERR
deadline=$((SECONDS + 7200))
while [[ ! -f "$root/cache/$name.box" ]]; do
  if (( SECONDS >= deadline )); then
    printf 'Téléchargement indisponible après deux heures : %s\n' "$name" >&2
    exit 1
  fi
  sleep 20
done
python3 "$root/scripts/convert-box.py" "$name"
if ! bash "$root/scripts/vagrant.sh" box list | grep -q "goad-kvm/$name "; then
  bash "$root/scripts/vagrant.sh" box add --provider libvirt --name "goad-kvm/$name" "$root/cache/$name-libvirt.box"
fi
bash "$root/scripts/vagrant.sh" up "$name" --provider libvirt
touch "$root/cache/$name.boot-ok"
