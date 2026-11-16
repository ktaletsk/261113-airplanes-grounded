#!/bin/bash
# Pre-download the 30-minute heatmap files for the days this notebook uses, from adsb.lol's daily archives on GitHub
# (https://github.com/adsblol/globe_history_2026/releases). Only the heatmap files are kept; the rest of each archive
# is streamed past. Optional: the notebook fetches missing days from the same archives itself.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/heatmap
for day in ${@:-2026.11.06 2026.11.07 2026.11.08 2026.11.12 2026.11.13 2026.11.14 2026.11.15}; do
  tag=${day//./}
  if [ "$(ls data/heatmap/${tag}_*.bin 2>/dev/null | wc -l)" -ge 48 ]; then echo "$day: already here"; continue; fi
  base=https://github.com/adsblol/globe_history_2026/releases/download/v$day-planes-readsb-prod-0/v$day-planes-readsb-prod-0.tar
  { curl -sfL "$base.aa"; curl -sfL "$base.ab" || true; curl -sfL "$base.ac" 2>/dev/null || true; } | python3 -I -c '
import sys, tarfile, pathlib
tag, out, got = sys.argv[1], pathlib.Path(sys.argv[2]), 0
with tarfile.open(fileobj=sys.stdin.buffer, mode="r|") as tf:
    for m in tf:
        n = m.name.lstrip("./")
        if n.startswith("heatmap/") and n.endswith(".bin.ttf") and m.isfile():
            (out / f"{tag}_{n.split(chr(47))[1][:2]}.bin").write_bytes(tf.extractfile(m).read()); got += 1
            if got >= 48: break
print(tag, "heatmap files:", got)' "$tag" data/heatmap
done
[ -s data/acdb/aircraft.csv.gz ] || { mkdir -p data/acdb; curl -sL -o data/acdb/aircraft.csv.gz https://raw.githubusercontent.com/wiedehopf/tar1090-db/csv/aircraft.csv.gz; }
[ -s data/acdb/icao_aircraft_types2.js ] || curl -sL -o data/acdb/icao_aircraft_types2.js https://raw.githubusercontent.com/wiedehopf/tar1090-db/master/db/icao_aircraft_types2.js
