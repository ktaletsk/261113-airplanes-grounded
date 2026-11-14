#!/bin/bash
# Download adsb.lol readsb heatmaps (all aircraft, 10 s snapshots, one gz file per 30-min UTC slot).
cd "$(dirname "$0")/.."
get() { # yyyy/mm/dd first last
  d=${1//\//}
  for s in $(seq $2 $3); do ss=$(printf %02d $s); f=data/heatmap/${d}_${ss}.bin
    [ -s $f ] && [ "$(head -c2 $f | xxd -p)" = "1f8b" ] && continue
    curl -sL -m 300 -A Mozilla/5.0 -o $f.tmp https://adsb.lol/globe_history/$1/heatmap/$ss.bin.ttf
    if [ "$(head -c2 $f.tmp | xxd -p)" = "1f8b" ]; then mv $f.tmp $f; else rm -f $f.tmp; echo "missing ${d}_${ss}"; fi
  done
}
[ -s data/acdb/aircraft.csv.gz ] || curl -sL -m 120 -o data/acdb/aircraft.csv.gz https://raw.githubusercontent.com/wiedehopf/tar1090-db/csv/aircraft.csv.gz
[ -s data/acdb/icao_aircraft_types2.js ] || curl -sL -m 60 -o data/acdb/icao_aircraft_types2.js https://raw.githubusercontent.com/wiedehopf/tar1090-db/master/db/icao_aircraft_types2.js
get 2026/11/13 0 ${1:-43}
get 2026/11/12 0 47
echo "done: $(ls data/heatmap | wc -l) files, $(du -sh data/heatmap | cut -f1)"
