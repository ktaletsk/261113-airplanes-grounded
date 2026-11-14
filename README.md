# Empty skies

A flight-tracking analysis of the nationwide U.S. ground stop on **Nov. 13, 2026**, built as a
[marimo](https://marimo.io) notebook.

**Read it:** https://ktaletsk.github.io/261113-airplanes-grounded/ (runs in your browser, nothing to install)

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

## Two ways to run it

| | Data | How |
|---|---|---|
| **GitHub Pages** (WebAssembly) | A compact snapshot (`public/bundle.npz`), rebuilt by GitHub Actions about every 30 minutes | Just open the link above |
| **molab or locally** | Downloads the newest adsb.lol files itself; the **Load newest data** button pulls in new half hours | `uvx marimo edit --sandbox grounded.py` |

The notebook checks whether it is running in the browser (`sys.platform == "emscripten"`). There it loads
the snapshot; everywhere else it downloads and processes the raw files, caching each processed half hour
with `mo.persistent_cache`.

The workflow in `.github/workflows/publish.yml` runs the notebook as a script with
`EMPTY_SKIES_EXPORT=public/bundle.npz` to write the snapshot, then runs
`marimo export html-wasm --mode run` and deploys the result to Pages.

## Files

- `grounded.py`: the notebook, which is also the deployed app.
- `flightmap.js`, `flightmap.css`: the map widget source. They are embedded into the notebook by
  `scripts/build_notebook_live.py`.
- `scripts/build_report.py`: rebuilds the notebook's cells from source. Run it inside a running
  notebook with the marimo-pair tooling.
- `scripts/download.sh`: optional; pre-downloads raw files into `data/` for faster local runs.
