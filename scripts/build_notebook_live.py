# Run inside the marimo kernel (marimo-pair execute-code) to (re)build grounded.py as a self-contained notebook.
# Reads flightmap.js/css from disk at build time and embeds them, so the published notebook needs no side files.
import marimo._code_mode as cm
from pathlib import Path

PROJ = Path(mo.notebook_dir())   # run inside the notebook kernel, so mo is in scope
JS = (PROJ / "flightmap.js").read_text()
CSS = (PROJ / "flightmap.css").read_text()

C = {}

C["imports"] = r'''import marimo as mo
import numpy as np
import pandas as pd
import altair as alt
import anywidget, traitlets
import gzip, io, json, os, re, sys, time, urllib.request, datetime as dt
try:
    import tzdata  # noqa: F401  (time-zone database for zoneinfo in the browser build)
except ImportError:
    pass
from concurrent.futures import ThreadPoolExecutor, as_completed
from zoneinfo import ZoneInfo
from pathlib import Path

PT = ZoneInfo("America/Los_Angeles")
WASM = sys.platform == "emscripten"      # True in the browser (WebAssembly) build on GitHub Pages
alt.data_transformers.disable_max_rows()'''

C["title"] = r'''mo.md("""
# US air traffic on Nov 13, 2026: the nationwide ground stop

Live ADS-B from **[adsb.lol](https://adsb.lol)** (open, unfiltered feeder network). The notebook downloads the
30-minute snapshot files (every aircraft, every 10 s) straight from adsb.lol when it runs (processed files are kept
in marimo's persistent cache, so later runs only fetch what is new), keeps one position per
aircraft per minute inside the US (CONUS, Alaska, Hawaii boxes), and compares the **ground-stop day** with the
**same hours one day earlier**. New files appear about every 30 minutes with roughly a 30–60 minute delay; press
**Load newest data** to pull them in. Times are **Pacific** (PT).
""")'''

C["config"] = r'''WINDOW_START = dt.datetime(2026, 11, 13, 18, 0, tzinfo=dt.timezone.utc)   # 10:00 PT on the ground-stop day
MAX_HOURS = 24                       # stop downloading this many hours after WINDOW_START
BASELINE_SHIFT = 86400               # compare with the same clock time one day earlier
WORKERS = 6                          # parallel downloads (be gentle with adsb.lol)
PERIOD_LABEL = {"event": "Nov 13 (ground stop)", "baseline": "Nov 12 (day before)"}
CATS = ["Airline", "Business jet", "General aviation", "Helicopter", "Other"]

# key moments (PT, naive). FAA time per News9 (2:54 pm CT); the departure collapse is measured from this data.
EVENTS = pd.DataFrame([
    {"t": dt.datetime(2026, 11, 13, 12, 35), "label": "departures collapse 12:35 ", "color": "#f5a623", "align": "right",
     "hud": "Departures collapsing (12:35 PT)"},
    {"t": dt.datetime(2026, 11, 13, 12, 54), "label": " FAA ground stop 12:54 PT (2:54 CT)", "color": "#ff4d4f", "align": "left",
     "hud": "FAA nationwide ground stop in effect"},
])

refresh_btn = mo.ui.run_button(label="Fetch newest data", kind="neutral")'''

C["helpers"] = r'''# ---- adsb.lol readsb heatmap decoding -------------------------------------------------------------
# One gzip file per 30-min UTC slot: little-endian int32 quads.
#   slice marker  [0x0E7F7C9D, t_hi, t_lo(ms), _]  -> following rows belong to that 10 s snapshot
#   callsign row  [hex|flags, lat >= 2^30, 8 ASCII bytes in cols 2..3]
#   position row  [hex|flags, lat*1e6, lon*1e6, (gs*10)<<16 | alt/25 (int16, -123 = on ground)]
HEAT_MAGIC = 0x0E7F7C9D
US_BOXES = {"CONUS": (24.4, 49.4, -125.0, -66.9), "Alaska": (51.0, 71.5, -170.0, -129.0), "Hawaii": (18.5, 22.5, -160.6, -154.5)}
AIRLINE_CS = re.compile(r"^[A-Z]{3}\d{1,4}[A-Z]{0,2}$")
LOCAL = mo.notebook_dir() / "data"
UA = {"User-Agent": "Mozilla/5.0 (marimo notebook; ground-stop visualization)"}


BUNDLE_URL = "https://raw.githubusercontent.com/ktaletsk/261113-airplanes-grounded/main/public/bundle.npz"


class Blocked(Exception):
    """adsb.lol refused this network (it blocks many cloud/data-center IP ranges)."""


def fetch(url, timeout=180, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (401, 403) and "adsb.lol" in url:
                raise Blocked(e.read()[:400].decode("utf-8", "replace").strip()) from None
            if e.code in (404, 502, 503) and i == tries - 1:
                return None
        except Exception:
            if i == tries - 1:
                raise
    return None


def local_or_fetch(name, url, valid=lambda b: True):
    """Use data/<name> if it exists (e.g. pre-downloaded with scripts/download.sh), else download into memory."""
    p = LOCAL / name
    if p.exists():
        b = p.read_bytes()
        if valid(b):
            return b
    b = fetch(url)
    return b if b is not None and valid(b) else None


class NotPublished(Exception):
    """Raised (never cached) when adsb.lol has not published a slot yet."""


def decode_heatmap(raw):
    a = np.frombuffer(gzip.decompress(raw), dtype="<i4").reshape(-1, 4)
    magic = a[:, 0] == HEAT_MAGIC
    slice_t = ((a[magic, 1].astype(np.int64) << 32) | (a[magic, 2].astype(np.int64) & 0xFFFFFFFF)) / 1000
    sid = np.cumsum(magic) - 1
    hexv = (a[:, 0] & 0xFFFFFF).astype(np.int32)
    is_cs = ~magic & (a[:, 1] >= 1 << 30) & (sid >= 0)
    is_pos = ~magic & (a[:, 1] < 1 << 30) & (sid >= 0)
    cs_bytes = a[is_cs][:, 2:4].copy().view(np.uint8).reshape(-1, 8)
    calls = pd.DataFrame({"hex": hexv[is_cs],
                          "callsign": [bytes(b).split(b"\x00")[0].decode("ascii", "replace").strip() for b in cs_bytes]})
    alt16 = (a[is_pos, 3] & 0xFFFF).astype(np.uint16).view(np.int16)
    pos = pd.DataFrame({
        "t": slice_t[sid[is_pos]], "hex": hexv[is_pos],
        "lat": (a[is_pos, 1] / 1e6).astype(np.float32), "lon": (a[is_pos, 2] / 1e6).astype(np.float32),
        "alt_ft": np.where(alt16 == -123, -1, alt16.astype(np.int32) * 25).astype(np.int32),
        "gs_kt": (((a[is_pos, 3] >> 16) & 0xFFFF) / 10).astype(np.float32),
    })
    return pos, calls


@mo.persistent_cache
def load_slot(slot_start: str):
    """One 30-min UTC slot (ISO start time) -> (one row per aircraft-minute inside the US, callsigns).
    Published slots never change, so the result is cached on disk (and on molab across sessions);
    a slot that is not published yet raises NotPublished, which is not cached."""
    ts = dt.datetime.fromisoformat(slot_start)
    slot = ts.hour * 2 + ts.minute // 30
    url = f"https://adsb.lol/globe_history/{ts:%Y/%m/%d}/heatmap/{slot:02d}.bin.ttf"
    raw = local_or_fetch(f"heatmap/{ts:%Y%m%d}_{slot:02d}.bin", url, valid=lambda b: b[:2] == b"\x1f\x8b")
    if raw is None:
        raise NotPublished(slot_start)
    pos, calls = decode_heatmap(raw)
    la, lo = pos.lat.values, pos.lon.values
    pos = pos[(la >= NA_BBOX[0]) & (la <= NA_BBOX[1]) & (lo >= NA_BBOX[2]) & (lo <= NA_BBOX[3])]
    pos["minute"] = (pos.t // 60 * 60).astype(np.int64)
    pos = pos.sort_values("t").drop_duplicates(["hex", "minute"], keep="last").drop(columns="t")
    calls = calls[calls.callsign != ""].drop_duplicates("hex", keep="last")
    return pos, calls


@mo.persistent_cache
def load_type_db():
    """wiedehopf tar1090-db: registration/type per ICAO hex, and type descriptions (e.g. L2J, wake category)."""
    import io
    ac_raw = local_or_fetch("acdb/aircraft.csv.gz", "https://raw.githubusercontent.com/wiedehopf/tar1090-db/csv/aircraft.csv.gz")
    ty_raw = local_or_fetch("acdb/icao_aircraft_types2.js", "https://raw.githubusercontent.com/wiedehopf/tar1090-db/master/db/icao_aircraft_types2.js")
    ac = pd.read_csv(io.BytesIO(ac_raw), sep=";", header=None, usecols=[0, 1, 2], names=["hex", "reg", "type"],
                     dtype=str, compression="gzip")
    ac = ac[ac.hex.str.fullmatch(r"[0-9A-Fa-f]{6}", na=False)]
    ac["hex"] = ac.hex.map(lambda h: int(h, 16))
    if ty_raw[:2] == b"\x1f\x8b":
        ty_raw = gzip.decompress(ty_raw)
    types = json.loads(ty_raw)
    tdesc = pd.DataFrame([(k, v[0], v[1], v[2]) for k, v in types.items()], columns=["type", "type_name", "desc", "wtc"])
    return ac.merge(tdesc, on="type", how="left")


def categorize(callsign, desc, wtc):
    """Airline (airline-style callsign or large jet), Business jet, General aviation, Helicopter, Other."""
    cs, d, w = callsign.fillna(""), desc.fillna(""), wtc.fillna("")
    cat = pd.Series("Other", index=callsign.index)
    jet = d.str[2].eq("J")
    cat[d.str[0].eq("H")] = "Helicopter"
    cat[d.str[2].isin(["P", "T", "E"]) & ~d.str[0].eq("H")] = "General aviation"
    cat[jet & w.eq("L")] = "Business jet"
    cat[jet & w.isin(["M", "H", "J"])] = "Airline"
    bizjet_ops = r"^(EJA|LXJ|XOJ|JTL|FFL|TWY|PCM|SVW|EJM|JRE|VJA|GPD|PRD|CNS|KOW|NJE)\d"
    cat[cs.str.match(AIRLINE_CS) & ~cs.str.match(bizjet_ops) & ~d.str[0].eq("H")] = "Airline"
    return cat


def add_heading(df):
    """Track angle (deg clockwise from north) from neighbouring minute samples of the same aircraft."""
    df = df.sort_values(["hex", "minute"]).reset_index(drop=True)
    same_next = (df.hex.shift(-1) == df.hex) & (df.minute.shift(-1) - df.minute <= 180)
    same_prev = (df.hex.shift(1) == df.hex) & (df.minute - df.minute.shift(1) <= 180)
    lat, lon = df.lat.values.astype(float), df.lon.values.astype(float)
    lat_n = np.where(same_next, df.lat.shift(-1), np.where(same_prev, lat, np.nan))
    lon_n = np.where(same_next, df.lon.shift(-1), np.where(same_prev, lon, np.nan))
    lat_p = np.where(same_next, lat, df.lat.shift(1))
    lon_p = np.where(same_next, lon, df.lon.shift(1))
    hdg = (np.degrees(np.arctan2((lon_n - lon_p) * np.cos(np.radians(lat)), lat_n - lat_p)) + 360) % 360
    df["heading"] = np.where(np.isfinite(hdg), hdg, 0).astype(np.int16)
    return df


def movements(df, low_ft=2500, gap_s=15 * 60):
    """Takeoffs / landings from each aircraft's minute track.
    takeoff: ground -> air, or a track (re)appearing airborne below low_ft after a gap
    landing: air -> ground, or a track ending airborne below low_ft followed by a gap"""
    df = df.sort_values(["hex", "minute"])
    hx, mn, alt_ = df.hex.values, df.minute.values, df.alt_ft.values
    new_track = np.r_[True, (hx[1:] != hx[:-1]) | (mn[1:] - mn[:-1] > gap_s)]
    end_track = np.r_[new_track[1:], True]
    on_ground = alt_ < 0
    air = ~on_ground
    prev_ground = np.r_[False, on_ground[:-1]] & ~new_track
    next_ground = np.r_[on_ground[1:], False] & ~end_track
    low = air & (alt_ <= low_ft)
    out = []
    for kind, m in (("takeoff", (air & prev_ground) | (new_track & low)), ("landing", (air & next_ground) | (end_track & low))):
        out.append(df.loc[m, ["minute", "t", "period", "hex", "category"]].assign(kind=kind))
    return pd.concat(out, ignore_index=True)


NA_BBOX = (14.0, 72.0, -180.0, -50.0)        # lat0, lat1, lon0, lon1 kept from the heatmaps
GRID_RES = 0.02
COUNTRY_CODES = {"840": 1, "124": 2, "484": 3}   # ISO numeric -> 1 US, 2 Canada, 3 Mexico
COUNTRY_NAMES = np.array(["", "US", "Canada", "Mexico"], dtype=object)


@mo.persistent_cache
def country_grid(buffer_deg=1.0):
    """Raster (GRID_RES deg) of US / Canada / Mexico over NA_BBOX from world-atlas 50m borders,
    grown `buffer_deg` into the sea so coastal and offshore traffic is attributed to the nearest country."""
    topo = json.loads(fetch("https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-50m.json"))
    (sx, sy), (tx, ty) = topo["transform"]["scale"], topo["transform"]["translate"]
    arcs = []
    for a in topo["arcs"]:
        q = np.cumsum(np.array(a, dtype=np.float64), axis=0)
        arcs.append(np.c_[q[:, 0] * sx + tx, q[:, 1] * sy + ty])
    lat0, lat1, lon0, lon1 = NA_BBOX
    ny, nx = int(round((lat1 - lat0) / GRID_RES)), int(round((lon1 - lon0) / GRID_RES))
    grid = np.zeros((ny, nx), dtype=np.int8)
    yc = lat0 + (np.arange(ny) + 0.5) * GRID_RES
    for g in topo["objects"]["countries"]["geometries"]:
        code = COUNTRY_CODES.get(str(g.get("id")))
        if not code:
            continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        segs = []
        for poly in polys:
            for ring in poly:
                pts = np.concatenate([arcs[i] if i >= 0 else arcs[~i][::-1] for i in ring])
                segs.append(np.c_[pts[:-1], pts[1:]])
        e = np.concatenate(segs)                       # x1 y1 x2 y2
        e = e[(np.maximum(e[:, 1], e[:, 3]) >= lat0) & (np.minimum(e[:, 1], e[:, 3]) <= lat1)]
        ylo, yhi = np.minimum(e[:, 1], e[:, 3]), np.maximum(e[:, 1], e[:, 3])
        order = np.argsort(ylo); e, ylo, yhi = e[order], ylo[order], yhi[order]
        for r, y in enumerate(yc):
            k = np.searchsorted(ylo, y, side="right")
            s = e[:k][yhi[:k] > y]
            if len(s) < 2:
                continue
            xs = np.sort(s[:, 0] + (y - s[:, 1]) * (s[:, 2] - s[:, 0]) / (s[:, 3] - s[:, 1]))
            c0 = np.clip(((xs[0::2] - lon0) / GRID_RES).astype(int), 0, nx)
            c1 = np.clip(((xs[1::2] - lon0) / GRID_RES).astype(int), 0, nx)
            d = np.zeros(nx + 1, dtype=np.int32)
            np.add.at(d, c0, 1); np.add.at(d, c1, -1)
            grid[r][np.cumsum(d[:-1]) > 0] = code
    for _ in range(int(buffer_deg / GRID_RES)):        # grow into the sea, never over another country
        empty = grid == 0
        for sh in ((1, 0), (-1, 0), (1, 1), (-1, 1)):
            nb = np.roll(grid, sh[0], axis=sh[1])
            grid = np.where(empty & (grid == 0) & (nb > 0), nb, grid)
    return grid


def country_of(lat, lon, grid):
    lat0, lat1, lon0, lon1 = NA_BBOX
    r = ((np.asarray(lat) - lat0) / GRID_RES).astype(int)
    c = ((np.asarray(lon) - lon0) / GRID_RES).astype(int)
    ok = (r >= 0) & (r < grid.shape[0]) & (c >= 0) & (c < grid.shape[1])
    out = np.zeros(len(r), dtype=np.int8)
    out[ok] = grid[r[ok], c[ok]]
    return COUNTRY_NAMES[out]


def region_of(country, lat, lon):
    """US positions -> Lower 48 / Alaska / Hawaii; others keep their country name."""
    country, lat, lon = np.asarray(country, dtype=object), np.asarray(lat), np.asarray(lon)
    us_reg = np.where(lat > 50, "Alaska", np.where((lon < -150) & (lat < 30), "Hawaii", "Lower 48"))
    return np.where(country == "US", us_reg, country)


PERIODS, KINDS = ["event", "baseline"], ["takeoff", "landing"]
COUNTRIES, REGIONS = ["US", "Canada", "Mexico"], ["Lower 48", "Alaska", "Hawaii", "Canada", "Mexico"]


def _codes(values, cats):
    return pd.Categorical(pd.Series(values).astype(str), categories=cats).codes.astype(np.int8)


def pack_bundle(path, snap, aircraft, counts, moves_all, meta, steps=None):
    """Compact snapshot for the browser build. Map positions are kept every steps[period] minutes,
    quantized (~100-200 m) and delta-encoded along each aircraft's track; the per-minute counts and
    takeoff/landing events (which need full 1-minute tracks) are shipped precomputed."""
    steps = steps or {"event": 2, "baseline": 4}
    keep = np.zeros(len(snap), dtype=bool)
    for per, st in steps.items():
        keep |= (snap.period.values == per) & (snap.minute.values % (60 * st) == 0)
    s = snap[keep].sort_values(["period", "hex", "minute"])
    ac = aircraft[aircraft.hex.isin(s.hex.unique())]
    m = moves_all
    d = lambda a: np.diff(np.asarray(a, dtype=np.int64), prepend=0).astype(np.int32)
    ustr = lambda col, n: np.asarray(col.fillna("").astype(str).str[:n].tolist(), dtype=f"U{n}")
    arrays = {
        "s_period": _codes(s.period, PERIODS), "s_hex": d(s.hex), "s_min": d(s.minute // 60),
        "s_lat": d(np.round((s.lat.values - 14) * 1000)), "s_lon": d(np.round((s.lon.values + 180) * 500)),
        "s_alt": d(s.alt_ft // 25).astype(np.int16), "s_gs": (np.round(s.gs_kt.values) // 2).clip(0, 255).astype(np.uint8),
        "s_hdg": (s.heading.values.astype(np.int32) * 256 // 360).astype(np.uint8),
        "s_cat": _codes(s.category, CATS), "s_country": _codes(s.country, COUNTRIES), "s_region": _codes(s.region, REGIONS),
        "a_hex": ac.hex.astype(np.int32), "a_cs": ustr(ac.callsign, 8), "a_type": ustr(ac.type, 4), "a_cat": _codes(ac.category, CATS),
        "c_period": _codes(counts.period, PERIODS), "c_cat": _codes(counts.category, CATS),
        "c_t": (counts.t // 60).astype(np.int32), "c_n": counts.n.astype(np.int32),
        "m_period": _codes(m.period, PERIODS), "m_min": (m.minute // 60).astype(np.int32), "m_hex": m.hex.astype(np.int32),
        "m_cat": _codes(m.category, CATS), "m_lat": m.lat.astype(np.float32), "m_lon": m.lon.astype(np.float32),
        "m_kind": _codes(m.kind, KINDS), "m_country": _codes(m.country, COUNTRIES), "m_region": _codes(m.region, REGIONS),
        "meta": np.frombuffer(json.dumps({**meta, "map_step": steps}).encode(), dtype=np.uint8),
    }
    np.savez_compressed(path, **{k: np.asarray(v) for k, v in arrays.items()})


def unpack_bundle(raw):
    z = np.load(io.BytesIO(raw))
    meta = json.loads(bytes(z["meta"]).decode())
    pick = lambda codes, cats: np.array(cats, dtype=object)[codes]
    cs = lambda k: np.cumsum(z[k].astype(np.int64))
    alt_ = cs("s_alt") * 25
    snap = pd.DataFrame({
        "hex": cs("s_hex").astype(np.int32), "lat": (cs("s_lat") / 1000 + 14).astype(np.float32),
        "lon": (cs("s_lon") / 500 - 180).astype(np.float32), "alt_ft": np.where(alt_ < 0, -1, alt_),
        "gs_kt": z["s_gs"].astype(np.float32) * 2, "minute": cs("s_min") * 60,
        "period": pick(z["s_period"], PERIODS), "category": pick(z["s_cat"], CATS),
        "heading": (z["s_hdg"].astype(np.int32) * 360 // 256).astype(np.int16),
        "country": pd.Categorical(pick(z["s_country"], COUNTRIES)), "region": pd.Categorical(pick(z["s_region"], REGIONS)),
    })
    snap["t"] = snap.minute + np.where(snap.period == "baseline", BASELINE_SHIFT, 0)
    aircraft = pd.DataFrame({"hex": z["a_hex"], "callsign": z["a_cs"].astype(object), "type": z["a_type"].astype(object),
                             "category": pick(z["a_cat"], CATS)})
    counts = pd.DataFrame({"period": pick(z["c_period"], PERIODS), "category": pick(z["c_cat"], CATS),
                           "t": z["c_t"].astype(np.int64) * 60, "n": z["c_n"]})
    m_period = pick(z["m_period"], PERIODS)
    m_minute = z["m_min"].astype(np.int64) * 60
    moves_all = pd.DataFrame({
        "minute": m_minute, "t": m_minute + np.where(m_period == "baseline", BASELINE_SHIFT, 0), "period": m_period,
        "hex": z["m_hex"], "category": pick(z["m_cat"], CATS), "lat": z["m_lat"], "lon": z["m_lon"],
        "kind": pick(z["m_kind"], KINDS), "country": pick(z["m_country"], COUNTRIES), "region": pick(z["m_region"], REGIONS),
    })
    return snap, aircraft, {"counts": counts, "moves": moves_all}, meta


def read_bundle():
    """Server side (molab / local): the published snapshot next to the notebook, else the copy on GitHub."""
    p = mo.notebook_dir() / "public" / "bundle.npz"
    return unpack_bundle(p.read_bytes() if p.exists() else fetch(BUNDLE_URL))


async def load_bundle(url):
    """Browser build: fetch the snapshot that GitHub Actions publishes next to the page."""
    from pyodide.http import pyfetch
    resp = await pyfetch(f"{url}?v={int(time.time() // 300)}")
    if not resp.ok:
        raise RuntimeError(f"could not load {url}: HTTP {resp.status}")
    return unpack_bundle(await resp.bytes())


def to_pt(unix):
    """unix seconds -> naive Pacific datetimes (what the charts use)."""
    return pd.to_datetime(unix, unit="s", utc=True).dt.tz_convert(PT).dt.tz_localize(None)'''

C["load"] = r'''# Default: the precomputed snapshot (public/bundle.npz) -> opens instantly, no download from adsb.lol.
# "Fetch newest data" (or EMPTY_SKIES_EXPORT, used to rebuild the snapshot) downloads and processes the raw files.
T0 = int(WINDOW_START.timestamp())
_fresh = bool(refresh_btn.value) or bool(os.environ.get("EMPTY_SKIES_EXPORT"))
DATA_SOURCE, NOTICE, PRE = "snapshot", None, None

if WASM:
    try:
        snap, aircraft, PRE, _meta = await load_bundle(mo.notebook_location() / "public" / "bundle.npz")
    except Exception:
        snap, aircraft, PRE, _meta = await load_bundle(BUNDLE_URL)
elif not _fresh:
    snap, aircraft, PRE, _meta = read_bundle()
else:
    try:
        _now = dt.datetime.now(dt.timezone.utc)
        _end = min(_now, WINDOW_START + dt.timedelta(hours=MAX_HOURS))
        _jobs = []
        _t = WINDOW_START
        while _t < _end:
            _jobs += [("event", _t), ("baseline", _t - dt.timedelta(seconds=BASELINE_SHIFT))]
            _t += dt.timedelta(minutes=30)

        _frames, _calls, missing = [], [], []
        with mo.status.progress_bar(total=len(_jobs) + 1, title="Downloading ADS-B snapshots from adsb.lol",
                                    subtitle=f"{len(_jobs)} half-hour files (~10–25 MB each; cached after the first load)", remove_on_exit=True) as _bar:
            with ThreadPoolExecutor(WORKERS) as _ex:
                _futs = {_ex.submit(load_slot, _ts.isoformat()): (_p, _ts) for _p, _ts in _jobs}
                _types = _ex.submit(load_type_db)
                for _f in as_completed(_futs):
                    _p, _ts = _futs[_f]
                    try:
                        _pos, _cs1 = _f.result()
                        _frames.append(_pos.assign(period=_p))
                        _calls.append(_cs1)
                    except NotPublished:
                        missing.append(f"{_p} {_ts:%m-%d %H:%M} UTC")
                    _bar.update()
                type_db = _types.result()
                _bar.update()

        snap = pd.concat(_frames, ignore_index=True)
        # country from real borders (world-atlas 50m), extended ~100 km offshore; drop everything else
        COUNTRY_GRID = country_grid(1.0)
        snap["country"] = country_of(snap.lat.values, snap.lon.values, COUNTRY_GRID)
        snap = snap[snap.country != ""]
        snap["region"] = pd.Categorical(region_of(snap.country.values, snap.lat.values, snap.lon.values))
        snap["country"] = pd.Categorical(snap.country)
        # drop feed hiccups: minutes with < 60% of the aircraft seen in the surrounding minutes
        _n = snap.groupby(["period", "minute"]).size()
        _bad = _n[_n < 0.6 * _n.rolling(9, center=True, min_periods=1).median()].index.get_level_values("minute")
        snap = snap[~snap.minute.isin(_bad)]
        snap["t"] = snap.minute + np.where(snap.period == "baseline", BASELINE_SHIFT, 0)   # aligned clock (event day)

        _cs = pd.concat(_calls).drop_duplicates("hex", keep="last")
        aircraft = (pd.DataFrame({"hex": snap.hex.unique()}).merge(_cs, on="hex", how="left")
                    .merge(type_db, on="hex", how="left"))
        aircraft["category"] = categorize(aircraft.callsign, aircraft.desc, aircraft.wtc)
        snap = add_heading(snap.merge(aircraft[["hex", "category"]], on="hex", how="left"))
        if not _frames:
            raise NotPublished("no half-hour files could be downloaded")
        DATA_SOURCE = "live"
    except (Blocked, NotPublished) as _e:
        NOTICE = f"Could not fetch new data from adsb.lol, so this shows the published snapshot instead. adsb.lol said: {_e}"
        snap, aircraft, PRE, _meta = read_bundle()

if DATA_SOURCE == "live":
    PRE, MAP_STEP, DATA_BUILT = None, {"event": 1, "baseline": 1}, int(time.time())
    T_END = int(snap[snap.period == "event"].t.max())
else:
    missing, T_END, MAP_STEP, DATA_BUILT = _meta["missing"], _meta["T_END"], _meta["map_step"], _meta["built"]

_built = dt.datetime.fromtimestamp(DATA_BUILT, PT)
_status = (f"<b>Live data</b> fetched from adsb.lol at {_built:%-I:%M %p} PT, through {fmt_pt(T_END)} PT."
           if DATA_SOURCE == "live" else
           f"Showing the <b>published snapshot</b>: built {_built:%b %-d, %-I:%M %p} PT, data through {fmt_pt(T_END)} PT."
           + ("" if WASM else " The button downloads the newest data from adsb.lol and recomputes everything (a minute or two)."))
mo.vstack([
    mo.Html(f'<div class="er-databar"><span>{_status}</span>{"" if WASM else refresh_btn}</div>'),
    mo.Html(f'<div class="er-databar-note">{mo.callout(mo.md(NOTICE), kind="warn").text}</div>') if NOTICE else mo.md(""),
])'''

C["events_fn"] = r'''def with_events(chart):
    """Layer the EVENTS markers (dashed rule + label) on a chart whose x is time_pt."""
    layers = [chart]
    for e in EVENTS.to_dict("records"):
        _d = pd.DataFrame([e])
        layers.append(alt.Chart(_d).mark_rule(color=e["color"], strokeWidth=1.5, strokeDash=[5, 3]).encode(x="t:T"))
        layers.append(alt.Chart(_d).mark_text(color=e["color"], align=e["align"], baseline="top", fontSize=11, fontWeight="bold")
                      .encode(x="t:T", y=alt.value(4), text="label:N"))
    return alt.layer(*layers)'''

C["derive"] = r'''# airborne aircraft per (aligned) minute over the US, by period and category; takeoffs/landings
if PRE is None:
    _air = snap[(snap.alt_ft >= 0) & (snap.country == "US")]
    counts = _air.groupby(["period", "category", "t"]).size().rename("n").reset_index()
    moves_all = movements(snap)
    moves_all["country"] = country_of(moves_all.lat.values, moves_all.lon.values, COUNTRY_GRID)
    moves_all["region"] = region_of(moves_all.country.values, moves_all.lat.values, moves_all.lon.values)
else:                                   # browser build: computed upstream from full 1-minute tracks
    counts, moves_all = PRE["counts"], PRE["moves"]
counts = counts[(counts.t >= T0) & (counts.t <= T_END)].copy()
counts["time_pt"] = to_pt(counts.t)
total = counts.groupby(["period", "t", "time_pt"]).n.sum().reset_index()
total["label"] = total.period.map(PERIOD_LABEL)

# ignore the first and last 15 min, where tracks are cut by the window edges
moves = moves_all[(moves_all.t >= T0 + 900) & (moves_all.t <= T_END - 900)].copy()
moves["bin"] = moves.t // 300 * 300
moves["time_pt"] = to_pt(moves["bin"])'''

C["airborne_chart"] = r'''_base = alt.Chart(total).encode(
    x=alt.X("time_pt:T", title="time (PT)", axis=alt.Axis(format="%H:%M")),
    y=alt.Y("n:Q", title="aircraft airborne over the US"),
    color=alt.Color("label:N", title=None, sort=list(PERIOD_LABEL.values()), scale=alt.Scale(range=["#4aa3ff", "#9aa5b1"])),
    strokeDash=alt.StrokeDash("label:N", legend=None, sort=list(PERIOD_LABEL.values()), scale=alt.Scale(range=[[1, 0], [4, 3]])),
    tooltip=[alt.Tooltip("time_pt:T", format="%H:%M", title="PT"), "label:N", alt.Tooltip("n:Q", title="airborne")],
)
airborne_chart = with_events(_base.mark_line(strokeWidth=2)).properties(
    width="container", height=260, title="Aircraft airborne over the US: ground-stop day vs the day before (same clock time)")
airborne_chart'''

C["widget"] = r'''class FlightMap(anywidget.AnyWidget):
    """Flightradar-style map. JS owns the view, slider and playback; Python serves the frame for the chosen minute."""
    minute = traitlets.Int(0).tag(sync=True)
    bounds = traitlets.List([0, 0, 60]).tag(sync=True)          # [first, last, step] in unix seconds
    frame = traitlets.Dict({}).tag(sync=True)
    aircraft = traitlets.Dict({}).tag(sync=True)                # hex -> [callsign, type, category index]
    categories = traitlets.List([]).tag(sync=True)
    events = traitlets.List([]).tag(sync=True)                  # [[unix, label, color, hud text], ...]
    series = traitlets.List([]).tag(sync=True)                  # [[minute, airborne], ...] for the sparkline
    _esm = FLIGHTMAP_JS
    _css = FLIGHTMAP_CSS


def make_flightmap(period, cats):
    s = snap[(snap.period == period) & snap.category.isin(cats) & (snap.t >= T0) & (snap.t <= T_END)]
    by_min = {m: g for m, g in s.groupby("minute")}
    mins = sorted(by_min)
    shift = BASELINE_SHIFT if period == "baseline" else 0
    _n = s[(s.alt_ft >= 0) & (s.country == "US")].groupby("minute").size()
    step = 60 * MAP_STEP[period]
    w = FlightMap(bounds=[int(mins[0]), int(mins[-1]), step], categories=CATS,
                  series=[[int(m), int(v)] for m, v in _n.items()],
                  events=[[int(e["t"].replace(tzinfo=PT).timestamp()) - shift, e["label"].strip(), e["color"], e["hud"]]
                          for e in EVENTS.to_dict("records")])
    ac = aircraft[aircraft.hex.isin(s.hex.unique())]
    w.aircraft = {f"{h:06x}": [c if isinstance(c, str) else "", t if isinstance(t, str) else "", CATS.index(k)]
                  for h, c, t, k in zip(ac.hex, ac.callsign, ac.type, ac.category)}

    def send(_=None):
        g = by_min.get(int(w.minute) // step * step)
        if g is None:
            w.frame = {"minute": int(w.minute), "n": 0}
            return
        w.frame = {
            "minute": int(w.minute), "n": int(len(g)),
            "hex": [f"{h:06x}" for h in g.hex.values],
            "lat": np.round(g.lat.values, 4).tolist(), "lon": np.round(g.lon.values, 4).tolist(),
            "alt": g.alt_ft.values.tolist(), "gs": np.round(g.gs_kt.values).astype(int).tolist(),
            "hdg": g.heading.values.tolist(),
            "us": (g.country.values == "US").astype(int).tolist(),
        }
    w.observe(send, names=["minute"])
    w.minute = int(mins[-1]) if period == "event" else int(mins[0])
    send()
    return w'''

C["map_controls"] = r'''day_pick = mo.ui.dropdown({v: k for k, v in PERIOD_LABEL.items()}, value=PERIOD_LABEL["event"], label="day")
cat_pick = mo.ui.multiselect(CATS, value=CATS, label="categories")
mo.hstack([day_pick, cat_pick], justify="start", gap=2)'''

C["map"] = r'''flightmap = make_flightmap(day_pick.value, cat_pick.value)
flightmap'''

C["moves_chart"] = r'''_m = moves[moves.country == "US"].groupby(["period", "time_pt", "kind"]).size().rename("n").reset_index()
_m["series"] = _m.kind.str.title() + "s · " + _m.period.map(PERIOD_LABEL)
moves_chart = with_events(alt.Chart(_m).mark_line(point=alt.OverlayMarkDef(size=12), strokeWidth=1.8).encode(
    x=alt.X("time_pt:T", title="time (PT)", axis=alt.Axis(format="%H:%M")),
    y=alt.Y("n:Q", title="events per 5 min"),
    color=alt.Color("kind:N", title=None, scale=alt.Scale(domain=["takeoff", "landing"], range=["#2ec27e", "#e5534b"])),
    strokeDash=alt.StrokeDash("period:N", title=None, scale=alt.Scale(domain=["event", "baseline"], range=[[1, 0], [4, 3]]),
                              legend=alt.Legend(labelExpr="datum.value == 'event' ? 'Nov 13' : 'Nov 12'")),
    tooltip=["series:N", alt.Tooltip("time_pt:T", format="%H:%M"), "n:Q"],
)).properties(width="container", height=260, title="Takeoffs vs landings per 5 min (all US)")
moves_chart'''

C["category_chart"] = r'''_c = counts[counts.t % 600 == 0]                                     # every 10 min keeps the chart light
_y = _c[_c.period == "baseline"][["category", "t", "n"]].rename(columns={"n": "n_before"})
_t = _c[_c.period == "event"].merge(_y, on=["category", "t"], how="left")
_t["pct"] = 100 * _t.n / _t.n_before
category_chart = with_events(alt.Chart(_t).mark_line(strokeWidth=2).encode(
    x=alt.X("time_pt:T", title="time (PT)", axis=alt.Axis(format="%H:%M")),
    y=alt.Y("pct:Q", title="airborne, % of the day before"),
    color=alt.Color("category:N", title=None, sort=CATS),
    tooltip=["category:N", alt.Tooltip("time_pt:T", format="%H:%M"), "n:Q", "n_before:Q", alt.Tooltip("pct:Q", format=".0f")],
)).properties(width="container", height=240, title="Who is still flying? Airborne by category vs the day before")
category_chart'''

C["alt_chart"] = r'''# altitude bands: stacked counts (left) and each band relative to its own 10:00-12:00 PT level (right)
_edges = [0, 5000, 15000, 25000, 35000, 99999]
_names = ["< 5k ft", "5–15k", "15–25k", "25–35k", "35k+ (cruise)"]
_a = snap[(snap.period == "event") & (snap.alt_ft >= 0) & (snap.country == "US") & (snap.t >= T0) & (snap.minute % 120 == 0)]
_h = (_a.assign(band=pd.cut(_a.alt_ft, _edges, right=False, labels=_names))
      .groupby(["t", "band"], observed=False).size().rename("n").reset_index())
_h["time_pt"] = to_pt(_h.t)
_base_n = _h[_h.t < T0 + 2 * 3600].groupby("band", observed=False).n.mean()
_h["pct"] = 100 * _h.n / _h.band.map(_base_n).astype(float)
_band_color = alt.Color("band:N", title="altitude", sort=_names,
                        scale=alt.Scale(domain=_names, range=["#56d364", "#b4e63c", "#ffd84a", "#ff9f43", "#ff5e3a"]))
_x = alt.X("time_pt:T", title="time (PT)", axis=alt.Axis(format="%H:%M"))
_stack = with_events(alt.Chart(_h).mark_area(opacity=0.9).encode(
    x=_x, y=alt.Y("n:Q", stack="zero", title="aircraft airborne"), color=_band_color, order=alt.Order("band:N", sort="ascending"),
    tooltip=["band:N", alt.Tooltip("time_pt:T", format="%H:%M"), "n:Q"])).properties(
    width=520, height=260, title="Airborne by altitude band (ground-stop day)")
_rel = with_events(alt.Chart(_h).mark_line(strokeWidth=2).encode(
    x=_x, y=alt.Y("pct:Q", title="% of the band's 10:00–12:00 average"), color=_band_color,
    tooltip=["band:N", alt.Tooltip("time_pt:T", format="%H:%M"), "n:Q", alt.Tooltip("pct:Q", format=".0f")])).properties(
    width=520, height=260, title="Which layers empty first?")
alt_chart = alt.hconcat(_stack, _rel).resolve_scale(color="shared")
alt_chart'''

C["export"] = r'''# GitHub Actions sets EMPTY_SKIES_EXPORT=public/bundle.npz to build the snapshot for the browser version
EXPORT_TO = os.environ.get("EMPTY_SKIES_EXPORT", "")
if EXPORT_TO and not WASM:
    _p = Path(EXPORT_TO)
    _p.parent.mkdir(parents=True, exist_ok=True)
    pack_bundle(_p, snap, aircraft, counts, moves_all,
                {"T_END": T_END, "missing": missing, "built": int(time.time())})
    print(f"wrote {_p} ({_p.stat().st_size / 1e6:.1f} MB)")'''

C["assets"] = "# Front end of the FlightMap widget (anywidget ESM + CSS), embedded so the notebook is a single file.\n" \
    f"FLIGHTMAP_JS = r'''{JS}'''\n\nFLIGHTMAP_CSS = r'''{CSS}'''"

ORDER = ["imports", "title", "config", "load", "derive", "airborne_chart", "map_controls", "map",
         "moves_chart", "category_chart", "alt_chart", "events_fn", "widget", "helpers", "assets"]

async with cm.get_context() as ctx:
    cells = [c.id for c in ctx.cells]
    first = cells[0]
    for cid in cells[1:]:
        ctx.delete_cell(cid)
    ctx.edit_cell(first, code=C["imports"])
    prev, ids = first, [first]
    for k in ORDER[1:]:
        prev = ctx.create_cell(C[k], after=prev, hide_code=k not in ("helpers",))
        ids.append(prev)
print(dict(zip(ORDER, ids)))
