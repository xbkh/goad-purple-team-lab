#!/usr/bin/env python3
"""Convert verified single-disk VirtualBox boxes to local libvirt boxes."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile

download = importlib.import_module('download-box')
root = Path(__file__).resolve().parents[1]

for spec in download.BOXES:
    name = spec[0]
    if len(sys.argv) > 1 and name not in sys.argv[1:]:
        continue
    download.download(*spec)
    dest = root / 'cache' / f'{name}-libvirt.box'
    if dest.exists():
        print(f'{name}: déjà convertie', flush=True)
        continue
    source = root / 'cache' / f'{name}-source'
    source.mkdir(exist_ok=True)
    with tarfile.open(root / 'cache' / f'{name}.box') as archive:
        archive.extractall(source, filter='data')
    disks = list(source.rglob('*.vmdk'))
    if len(disks) != 1:
        raise RuntimeError(f'{name}: expected one VMDK, found {len(disks)}')
    output = root / 'cache' / f'{name}-libvirt'
    output.mkdir(exist_ok=True)
    disk = output / 'box.img'
    subprocess.run(['qemu-img', 'convert', '-p', '-f', 'vmdk', '-O', 'qcow2', str(disks[0]), str(disk)], check=True)
    info = json.loads(subprocess.check_output(['qemu-img', 'info', '--output=json', str(disk)]))
    subprocess.run(['qemu-img', 'check', str(disk)], check=True)
    subprocess.run([str(root / '.venv/bin/python'), str(root / 'scripts/warmup-box.py'), name, str(disk)], check=True)
    (output / 'metadata.json').write_text(json.dumps({'provider': 'libvirt', 'format': 'qcow2', 'virtual_size': (info['virtual-size'] + 2**30 - 1) // 2**30}))
    (output / 'Vagrantfile').write_text("Vagrant.configure('2') do |config|\n config.vm.guest = :windows\n config.vm.communicator = 'winrm'\n config.winrm.username = 'vagrant'\n config.winrm.password = 'vagrant'\nend\n")
    partial = dest.with_suffix('.partial')
    with tarfile.open(partial, 'w') as archive:
        for filename in ['box.img', 'metadata.json', 'Vagrantfile']:
            archive.add(output / filename, arcname=filename)
    partial.rename(dest)
    print(f'{name}: conversion terminée', flush=True)
