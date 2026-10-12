#!/usr/bin/env python3
"""Download pinned upstream Windows boxes and verify publisher checksums."""
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BOXES = [
    ('dc01', 'windows_server2019', '2023.10.19', 'sha256', 'a2825bcec954bfe2f8e34240846773ef3bc23114f178878995f01c90afe0908c'),
    ('ws01', 'windows10', '2024.01.06', 'md5', '722d8592a4007413523f1fbcbde8ac33'),
]

def download(name, box, version, algorithm, expected):
    dest = ROOT / 'cache' / (name + '.box')
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        url = f'https://vagrantcloud.com/mayfly/boxes/{box}/versions/{version}/providers/virtualbox/unknown/vagrant.box'
        for _ in range(8):
            response = urllib.request.urlopen(url, timeout=90)
            location = response.headers.get('Location')
            if location:
                url = location
                response.close()
                continue
            break
        else:
            raise RuntimeError('Too many redirects')
        partial = dest.with_suffix('.partial')
        total = 0
        with response, partial.open('wb') as output:
            while chunk := response.read(8 * 1024 * 1024):
                output.write(chunk)
                total += len(chunk)
                if total % (256 * 1024 * 1024) == 0:
                    print(f'{name}: {total // (1024 * 1024)} MiB', flush=True)
        with partial.open('rb') as source:
            digest = hashlib.file_digest(source, algorithm).hexdigest()
        if digest != expected:
            raise RuntimeError(f'{name}: checksum mismatch; partial file retained')
        partial.rename(dest)
    with dest.open('rb') as source:
        if hashlib.file_digest(source, algorithm).hexdigest() != expected:
            raise RuntimeError(f'{name}: cached checksum mismatch')
    print(f'{name}: téléchargement vérifié ({algorithm})', flush=True)

if __name__ == '__main__':
    for spec in BOXES:
        download(*spec)
