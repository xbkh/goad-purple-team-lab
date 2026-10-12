#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$root/.vagrant-home"
exec docker run --rm --network host \
  -e LIBVIRT_DEFAULT_URI=qemu:///system \
  -e VAGRANT_DEFAULT_PROVIDER=libvirt \
  -e GOAD_VM_MEMORY="${GOAD_VM_MEMORY:-2048}" \
  -v /var/run/libvirt:/var/run/libvirt \
  -v "$root/.vagrant-home:/.vagrant.d" \
  -v "$root:$root" \
  -v "$(dirname "$root")/GOAD:$(dirname "$root")/GOAD:ro" \
  -w "$root" \
  vagrantlibvirt/vagrant-libvirt@sha256:7939a158c938231361c8af26940fcb7f648c7f6e51abfcbcb2a6e6758fbdf826 vagrant "$@"
