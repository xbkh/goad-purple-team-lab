#!/usr/bin/env python3
"""Remove only our intermediate copies after successful VM deployment."""
from pathlib import Path
import shutil
import sys
import time

root = Path(__file__).resolve().parents[1]
cache = root / 'cache'
for name in sys.argv[1:]:
    if name not in ('dc01', 'ws01'):
        raise ValueError('Only the two lab machines are allowed')
    deadline = time.monotonic() + 10800
    while not (cache / f'{name}.boot-ok').exists():
        if time.monotonic() > deadline:
            raise TimeoutError(f'{name}: boot not confirmed, no cleanup performed')
        time.sleep(20)
    for filename in [f'{name}-source', f'{name}-libvirt', f'{name}-libvirt.box']:
        p = cache / filename
        if p.is_symlink():
            raise RuntimeError('Unexpected symbolic link: no cleanup')
        if p.is_dir():
            shutil.rmtree(p)
        elif p.is_file():
            p.unlink()
    print(f'{name}: intermediate copies removed; original verified box retained', flush=True)
