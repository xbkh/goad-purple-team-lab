#!/usr/bin/env bash
set -euo pipefail
# Only container files: no indexer/dashboard in the lightweight lab manager.
rm -rf /etc/services.d/filebeat
exec /init
