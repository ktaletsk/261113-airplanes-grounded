# Empty skies

A flight-tracking analysis of the nationwide U.S. ground stop on **Nov. 13, 2026**, built as a
[marimo](https://marimo.io) notebook.

**Read it**
- molab (interactive, runs in your browser): https://molab.marimo.io/github/ktaletsk/261113-airplanes-grounded/blob/main/grounded.py/wasm
- molab static preview: https://molab.marimo.io/github/ktaletsk/261113-airplanes-grounded/blob/main/grounded.py
- GitHub Pages: https://ktaletsk.github.io/261113-airplanes-grounded/

## What it shows

- Airline departures across the U.S. collapsed at **12:38 p.m. PT**, about 16 minutes before the FAA's
  nationwide ground stop officially took effect (2:54 p.m. CT, per News9). The collapse time is detected
  from the data, not typed in.
- Every region and every major hub stopped within the same few minutes.
- Flights already in the air kept landing, so the sky drained for hours.
- Alaska and Hawaii kept flying. Canada and Mexico stopped their U.S.-bound departures, and their other flights carried on.
- A flightradar-style map with a time slider, plus charts by altitude and aircraft category.

## Data

Positions come from [adsb.lol](https://adsb.lol), an open, unfiltered ADS-B network. Its "heatmap" files
hold every aircraft every 10 seconds, one file per half hour. Aircraft types come from the
[tar1090 database](https://github.com/wiedehopf/tar1090-db), and borders from
[Natural Earth / world-atlas](https://github.com/topojson/world-atlas).

## How the data gets in

The notebook opens on a **published snapshot**, `public/bundle.npz` (about 12 MB), so it loads in seconds
with nothing to download from adsb.lol. The snapshot holds:
- map positions every 2 minutes (every 4 minutes for the comparison day);
- per-minute counts;
- every takeoff and landing, computed from the full 1-minute tracks.

| Where | Default | "Fetch newest data" |
|---|---|---|
| molab server session / local `marimo edit` | the snapshot | downloads the newest half-hour files from adsb.lol, processes them (cached with `mo.persistent_cache`) and recomputes everything |
| browser (molab `/wasm`, GitHub Pages) | the snapshot | not available |

adsb.lol blocks many cloud networks (GitHub Actions runners are blocked). If a fetch is refused, the notebook
shows adsb.lol's message and keeps the snapshot.

**Refreshing the snapshot** (from a normal home or office connection):

```bash
scripts/update_snapshot.sh   # rebuilds public/bundle.npz and the static-preview session file
git add public/bundle.npz __marimo__/session && git commit -m "Update data snapshot" && git push
```

Pushing re-deploys GitHub Pages (`.github/workflows/publish.yml` only exports and deploys; it never contacts adsb.lol).

## Files

- `grounded.py`: the notebook, which is also the deployed app.
- `flightmap.js`, `flightmap.css`: the map widget source. They are embedded into the notebook by
  `scripts/build_notebook_live.py`.
- `scripts/build_report.py`: rebuilds the notebook's cells from source. Run it inside a running
  notebook with the marimo-pair tooling.
- `scripts/update_snapshot.sh`: rebuilds the published snapshot and the static-preview outputs.
- `scripts/download.sh`: optional; pre-downloads raw files into `data/` for faster local runs.
