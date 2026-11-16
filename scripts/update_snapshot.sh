#!/bin/bash
# Rebuild the published data snapshot (public/bundle.npz) from adsb.lol's daily archives on GitHub, and the session
# file that gives the static molab preview its outputs.
# Data comes only from the GitHub archives (scripts/download.sh pre-fetches them); the live adsb.lol server is never used.
set -euo pipefail
cd "$(dirname "$0")/.."
EMPTY_SKIES_EXPORT=public/bundle.npz uv run --quiet grounded.py
uvx marimo@0.25.2 export session --sandbox --force-overwrite grounded.py
ls -lh public/bundle.npz __marimo__/session/
echo
echo "Publish with:  git add public/bundle.npz __marimo__/session && git commit -m 'Update data snapshot' && git push"
