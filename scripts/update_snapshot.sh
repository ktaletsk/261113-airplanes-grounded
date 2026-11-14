#!/bin/bash
# Rebuild the published data snapshot (public/bundle.npz) from the newest adsb.lol files, and the session
# file that gives the static molab preview its outputs. Run this from a normal home/office connection:
# adsb.lol blocks many cloud networks (including GitHub Actions runners).
set -euo pipefail
cd "$(dirname "$0")/.."
EMPTY_SKIES_EXPORT=public/bundle.npz uv run --quiet grounded.py
uvx marimo@0.25.2 export session --sandbox --force-overwrite grounded.py
ls -lh public/bundle.npz __marimo__/session/
echo
echo "Publish with:  git add public/bundle.npz __marimo__/session && git commit -m 'Update data snapshot' && git push"
