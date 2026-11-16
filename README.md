# Empty skies

A flight-tracking analysis of the nationwide U.S. ground stop on **Fri. Nov. 13, 2026**, and the weekend
recovery, built as a [marimo](https://marimo.io) notebook.

**Read it:** https://ktaletsk.github.io/261113-airplanes-grounded/ (runs in your browser, nothing to install)

Also on molab: [static preview](https://molab.marimo.io/github/ktaletsk/261113-airplanes-grounded/blob/main/grounded.py)

## What it shows

**Part 1: the stop**
- O'Hare went quiet at **12:16 p.m. PT**, about 20 minutes before the rest of the country.
- Airline departures across the U.S. collapsed at **12:38 p.m. PT**, 16 minutes before the FAA's nationwide
  ground stop took effect (2:54 p.m. CT). The collapse time is detected from the data, not typed in.
- Flights already in the air kept landing, so the sky drained for hours. Over Wyoming it emptied completely.

**Part 2: at the bottom**
- Alaska and Hawaii kept flying. Canada and Mexico stopped their U.S.-bound departures.
- Long-haul flights still left from coastal gateways; inland hubs mostly couldn't send them.
- Business jets flew less, and lower.

**Part 3: the return**
- The stop was lifted at 5:15 p.m. PT; departures restarted 21 minutes later, and the held backlog left in a wave.
- The weekend ran short: Saturday at 85% of a normal Saturday, Sunday at 93%, with American and JetBlue slowest.
- Estimated delays and cancellations, Friday to Sunday.

Plus a flightradar-style map of Friday with a time slider, and historical context on earlier nationwide stops.

## Data

Positions come from [adsb.lol](https://adsb.lol), an open, unfiltered ADS-B network, via its
**[daily archives on GitHub](https://github.com/adsblol/globe_history_2026/releases)**. Each archive holds 48
"heatmap" files per UTC day: every aircraft every 10 seconds, one file per half hour. Only those files are used;
the live adsb.lol server is never contacted.

Flight data is available from adsb.lol under the [Open Database License (ODbL) 1.0](https://opendatacommons.org/licenses/odbl/1-0/).
The derived snapshot `public/bundle.npz` is released under the ODbL 1.0 as well; see [DATA_LICENSE](DATA_LICENSE).

Window: Fri. Nov. 13, 8 a.m. PT to Sun. Nov. 15, 4 p.m. PT (the end of the Nov. 15 archive), compared with the day
before (Nov. 12) and the same days a week earlier (Nov. 6-8).

Also used: aircraft types from the [tar1090 database](https://github.com/wiedehopf/tar1090-db), borders from
[Natural Earth / world-atlas](https://github.com/topojson/world-atlas), airports from
[OurAirports](https://ourairports.com/data/), en-route center outlines from the
[VATSpy data project](https://github.com/vatsimnetwork/vatspy-data-project).

## How it is built

The notebook is static: it always opens the committed snapshot `public/bundle.npz` (about 23 MB), which holds
map positions for Friday (every 2 minutes), per-minute counts, and every takeoff and landing computed from the full
1-minute tracks.

To rebuild the snapshot:

```bash
scripts/download.sh          # optional: pre-fetch the heatmap files from the GitHub archives into data/heatmap
scripts/update_snapshot.sh   # runs the full pipeline, writes public/bundle.npz and the molab preview outputs
git add public/bundle.npz __marimo__/session && git commit -m "Update data snapshot" && git push
```

The pipeline fetches any missing day from the archives itself, streaming each archive and keeping only the heatmap
files. Pushing to `main` redeploys GitHub Pages (`.github/workflows/publish.yml` exports the notebook to
WebAssembly and deploys it; it downloads no data).

## Files

- `grounded.py`: the notebook, which is also the deployed app.
- `flightmap.js`, `flightmap.css`: the map widget, embedded into the notebook by `scripts/build_notebook_live.py`.
- `scripts/build_notebook_live.py`, `scripts/build_report.py`: generate the notebook's cells. Run
  `build_report.py` inside a running notebook with the marimo-pair tooling.
- `scripts/update_snapshot.sh`: rebuilds the published snapshot and the molab preview outputs.
- `scripts/download.sh`: pre-fetches the archive data into `data/`.
