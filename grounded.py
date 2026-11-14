# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
#     "pandas",
#     "altair",
#     "anywidget",
#     "traitlets",
#     "tzdata",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Empty skies")


@app.cell
def _(mo):
    def prose(text, cls="er-prose"):
        """Markdown rendered in the report's article column."""
        return mo.Html(f'<div class="{cls}">{mo.md(text).text}</div>')


    mo.Html("""
    <div class="er-loading">
      <div class="er-loading-t">Empty skies</div>
      <div class="er-loading-d">Loading the flight data and building the charts in your browser. This usually takes
      10 to 30 seconds; the report appears here when it is ready.</div>
      <div class="er-loading-bar"><span></span></div>
    </div>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,800;1,8..60,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
      .er-prose, .er-hero, .er-stats, .er-method { max-width: 720px; margin: 0 auto; }
      .er-prose { font-family: 'Source Serif 4', Georgia, serif; font-size: 19px; line-height: 1.62; }
        .er-prose p, .er-prose li, .er-prose span, .er-prose strong, .er-prose em, .er-prose a {
         font-family: 'Source Serif 4', Georgia, serif !important; font-size: 19px !important; line-height: 1.6 !important; }
      .er-prose p { margin: 0 0 1em !important; }
      .er-prose strong { font-weight: 700; }
        .er-prose h2, .er-prose h2 span { font-family: Inter !important; font-size: 13px !important; }
      .er-prose h2 { font-family: Inter, sans-serif; font-size: 13px; letter-spacing: .12em; text-transform: uppercase;
                     font-weight: 700; margin: 2.2em 0 .6em; opacity: .65; border-top: 1px solid rgba(127,127,127,.3); padding-top: 1.4em; }
      .er-prose a { color: inherit; text-decoration-thickness: 1px; text-underline-offset: 3px; }
      .er-hero { padding: 28px 0 8px; }
      .er-kicker { font: 700 12px Inter, sans-serif; letter-spacing: .16em; text-transform: uppercase; color: #e03131; }
      .er-h1 { margin: 6px 0 14px; line-height: 0; }
      .er-title { width: 100%; height: auto; display: block; overflow: visible; }
      .er-hero h1 { font-family: 'Source Serif 4', Georgia, serif; font-weight: 800; font-size: clamp(44px, 7vw, 76px);
                    line-height: 1.0; letter-spacing: -.02em; margin: 10px 0 14px; }
      .er-dek { font-family: 'Source Serif 4', Georgia, serif; font-size: 23px; line-height: 1.4; opacity: .85; margin: 0 0 18px; }
      .er-byline { font: 500 13px Inter, sans-serif; opacity: .6; border-top: 1px solid rgba(127,127,127,.3); padding-top: 12px; }
      .er-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 18px; padding: 14px 0 6px; }
      .er-stat .v { font: 700 34px/1.1 Inter, sans-serif; letter-spacing: -.02em; font-variant-numeric: tabular-nums; }
      .er-stat .v.hot { color: #e03131; } .er-stat .v.warm { color: #f08c00; } .er-stat .v.good { color: #2f9e44; }
      .er-stat .l { font: 400 13.5px/1.35 Inter, sans-serif; opacity: .7; margin-top: 4px; }
        .er-note p, .er-note em { font-family: Inter, sans-serif !important; font-size: 12.5px !important; }
      .er-note { font: 400 12.5px/1.5 Inter, sans-serif; opacity: .6; max-width: 720px; margin: 4px auto 0; }
      .er-method { font: 400 14.5px/1.6 Inter, sans-serif; }
      .er-part { max-width: 720px; margin: 64px auto 8px; padding-top: 22px; border-top: 3px solid currentColor; }
      .er-part-n { font: 700 12px Inter, sans-serif; letter-spacing: .16em; text-transform: uppercase; color: #e03131; }
      .er-part-t { font: 800 40px/1.1 'Source Serif 4', Georgia, serif; margin: 6px 0 6px; }
      .er-part-d { font: 400 19px/1.4 'Source Serif 4', Georgia, serif; opacity: .7; }
      .er-prose table { width: 100%; border-collapse: collapse; margin: 6px 0 22px; }
      .er-prose th, .er-prose td { font: 400 14px/1.45 Inter, sans-serif !important; text-align: left !important; vertical-align: top;
                                   padding: 8px 10px; border-bottom: 1px solid rgba(127,127,127,.25); }
      .er-prose th { font-weight: 700 !important; opacity: .7; }
      .er-prose td:first-child { white-space: nowrap; }
      .er-prose td strong { font-family: Inter, sans-serif !important; font-size: 14px !important; }
      .er-prose small, .er-prose small a { font: 400 12.5px/1.5 Inter, sans-serif !important; opacity: .75; }
      .er-loading { max-width: 720px; margin: 48px auto; font: 400 16px/1.5 Inter, sans-serif; }
      .er-loading-t { font: 800 56px/1 'Source Serif 4', Georgia, serif; margin-bottom: 14px; opacity: .9; }
      .er-loading-d { opacity: .7; }
      .er-loading-bar { height: 3px; margin-top: 18px; background: rgba(127,127,127,.2); overflow: hidden; border-radius: 2px; }
      .er-loading-bar span { display: block; height: 100%; width: 30%; background: #e03131;
                             animation: er-slide 1.4s ease-in-out infinite; }
      @keyframes er-slide { 0% { transform: translateX(-100%); } 100% { transform: translateX(340%); } }
      body:has(.er-hero) .er-loading { display: none; }
      .er-databar { max-width: 720px; margin: 0 auto; display: flex; align-items: center; gap: 16px;
                    font: 400 13px/1.45 Inter, sans-serif; padding: 10px 14px; border-radius: 8px;
                    background: rgba(127,127,127,.10); }
      .er-databar span { flex: 1; opacity: .8; }
      .er-databar button { flex-shrink: 0; white-space: nowrap; }
      .er-databar-note { max-width: 720px; margin: 8px auto 0; }
      .er-method h3 { font-size: 15px; margin: 1.2em 0 .3em; }
    </style>
    """)
    return (prose,)


@app.cell(hide_code=True)
def _(
    COLLAPSE_T,
    GAP_MIN,
    LAG_MIN,
    LIFTED,
    LIFT_T,
    T0,
    T_END,
    fmt_pt,
    mo,
    np,
    total,
):
    _ser = total[total.period == "event"].set_index("t").n.sort_index()
    _W, _H, _FS = 720, 118, 112
    _rng = np.random.default_rng(1113)
    _N = 2600
    _x, _y = _rng.uniform(-6, _W + 6, _N), _rng.uniform(0, _H, _N)
    _tt = T0 + np.clip(_x / _W, 0, 1) * (T_END - T0)
    _dens = np.interp(_tt, _ser.index.values, _ser.values) / max(1, _ser.max())     # airborne count, 10 a.m. -> latest
    _keep = _rng.uniform(0, 1, _N) < _dens ** 1.6
    _pal = np.array(["#56d364", "#b4e63c", "#ffd84a", "#ff9f43", "#ff5e3a"])
    _planes = "".join(
        f'<use href="#er-pl" transform="translate({x:.1f},{y:.1f}) rotate({r:.0f}) scale(.62)" fill="{c}"/>'
        for x, y, r, c in zip(_x[_keep], _y[_keep], _rng.uniform(0, 360, _N)[_keep], _rng.choice(_pal, _N)[_keep]))
    _txt = (f'x="0" y="{_H * 0.80:.0f}" textLength="{_W}" lengthAdjust="spacingAndGlyphs" '
            f'style="font: 800 {_FS}px \'Source Serif 4\', Georgia, serif"')
    _title_svg = f"""<svg class="er-title" viewBox="0 0 {_W} {_H}" role="img" aria-label="Empty skies">
      <defs>
        <path id="er-pl" d="M0,-9 L1.4,-5 L1.4,-1.5 L8,2.5 L8,4 L1.4,2 L1,6 L3.5,8 L3.5,9 L0,8 L-3.5,9 L-3.5,8 L-1,6 L-1.4,2 L-8,4 L-8,2.5 L-1.4,-1.5 L-1.4,-5 Z"/>
        <clipPath id="er-ttl"><text {_txt}>Empty skies</text></clipPath>
      </defs>
      <text {_txt} fill="currentColor" fill-opacity=".06">Empty skies</text>
      <g clip-path="url(#er-ttl)">{_planes}</g>
      <text {_txt} fill="none" stroke="currentColor" stroke-opacity=".55" stroke-width="1.1">Empty skies</text>
    </svg>"""
    mo.Html(f"""
    <div class="er-hero">
      <div class="er-kicker">Flight-tracking analysis · Nov. 13, 2026</div>
      <h1 class="er-h1">{_title_svg}</h1>
      <p class="er-dek">On Nov. 13, departures from U.S. airports stopped almost all at once at {fmt_pt(COLLAPSE_T) if COLLAPSE_T else "midday"} Pacific,
      {f"{GAP_MIN} minutes" if GAP_MIN else "shortly"} before the FAA's nationwide ground stop officially took effect, and the sky
      slowly emptied.{f" When the stop was lifted at {fmt_pt(LIFT_T)}, departures took {LAG_MIN} more minutes to restart." if LAG_MIN and LAG_MIN > 0 else (f" The stop was lifted at {fmt_pt(LIFT_T)}." if LIFTED else "")}</p>
      <div class="er-byline">Data: adsb.lol open ADS-B network · data through {fmt_pt(T_END)} PT
      · Each plane inside the title stands for aircraft in the air, from 10 a.m. (left) to the latest data (right)</div>
    </div>""")
    return


@app.cell(hide_code=True)
async def _(
    ALL_PERIODS,
    BUNDLE_URL,
    Blocked,
    LOAD_START,
    MAX_HOURS,
    NotPublished,
    PT,
    SHIFTS,
    ThreadPoolExecutor,
    WASM,
    WINDOW_START,
    WORKERS,
    add_heading,
    as_completed,
    categorize,
    country_grid,
    country_of,
    dt,
    fmt_pt,
    load_airports,
    load_airspace,
    load_bundle,
    load_slot,
    load_type_db,
    mo,
    np,
    os,
    pd,
    read_bundle,
    region_of,
    time,
):
    # Default: the precomputed snapshot (public/bundle.npz) -> opens instantly, no download from adsb.lol.
    # "Fetch newest data" (or EMPTY_SKIES_EXPORT, used to rebuild the snapshot) downloads and processes the raw files.
    T0 = int(WINDOW_START.timestamp())
    _fresh = bool(os.environ.get("EMPTY_SKIES_EXPORT"))
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
            _t = LOAD_START
            while _t < _end:
                _jobs += [(_p, _t - dt.timedelta(seconds=SHIFTS[_p])) for _p in ALL_PERIODS]
                _t += dt.timedelta(minutes=30)

            _frames, _calls, missing = [], [], []
            with mo.status.progress_bar(total=len(_jobs) + 1, title="Fetching the latest flight-tracking data from adsb.lol",
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
            snap["t"] = snap.minute + snap.period.map(SHIFTS).astype(np.int64)   # aligned clock (event day)
            snap["cs"] = snap.cs.astype("category")

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
        AIRPORTS, AIRSPACE = load_airports(), load_airspace()
    else:
        missing, T_END, MAP_STEP, DATA_BUILT = _meta["missing"], _meta["T_END"], _meta["map_step"], _meta["built"]
        AIRPORTS, AIRSPACE = PRE["airports"], _meta.get("airspace", [])

    _built = dt.datetime.fromtimestamp(DATA_BUILT, PT)
    _status = (f"Data: adsb.lol flight tracking, 10 a.m. Pacific on Nov. 13 to {fmt_pt(T_END)} "
               f"{'on Nov. 14' if T_END >= T0 + 14 * 3600 else 'PT'} · snapshot built {_built:%b %-d, %-I:%M %p} PT")
    mo.vstack([
        mo.Html(f'<div class="er-databar"><span>{_status}</span></div>'),
        mo.Html(f'<div class="er-databar-note">{mo.callout(mo.md(NOTICE), kind="warn").text}</div>') if NOTICE else mo.md(""),
    ])
    return (
        AIRPORTS,
        AIRSPACE,
        COUNTRY_GRID,
        MAP_STEP,
        PRE,
        T0,
        T_END,
        aircraft,
        missing,
        snap,
    )


@app.cell(hide_code=True)
def _(
    AIR_MIN,
    AIR_MIN_BASE,
    AIR_MIN_T,
    COLLAPSE_T,
    DEP_NOW_PCT,
    GAP_MIN,
    LAG_MIN,
    LIFTED,
    LIFT_T,
    T_END,
    fmt_pt,
    mo,
):
    _stat = lambda v, l, cls="": f'<div class="er-stat"><div class="v {cls}">{v}</div><div class="l">{l}</div></div>'
    mo.Html('<div class="er-stats">'
            + _stat(fmt_pt(COLLAPSE_T).split()[0] if COLLAPSE_T else "–",
                    f"p.m. PT: airline departures collapse, {GAP_MIN} minutes before the FAA's ground stop", "warm")
            + _stat(f"{AIR_MIN:,}", f"aircraft over the U.S. at the low point, {fmt_pt(AIR_MIN_T)} (normally {AIR_MIN_BASE:,})", "hot")
            + (_stat(fmt_pt(LIFT_T).split()[0], f"p.m. PT: the stop is lifted; departures restart {LAG_MIN} minutes later"
                     if LAG_MIN is not None else "p.m. PT: the stop is lifted", "good") if LIFTED else "")
            + _stat(f"{DEP_NOW_PCT}%" if DEP_NOW_PCT is not None else "–",
                    f"of normal airline departures in the latest data ({fmt_pt(T_END)})")
            + '</div>')
    return


@app.cell(hide_code=True)
def _(
    DAY3,
    T0,
    TOT_BS,
    TOT_EV,
    T_END,
    alt,
    pd,
    rec_bs,
    rec_ev,
    to_pt,
    week_moves,
    week_total,
    with_events,
):
    _r30 = lambda s: s.rolling(30, min_periods=10).sum()
    _wk = week_moves[(week_moves.kind == "takeoff") & (week_moves.category == "Airline") & (week_moves.country == "US")]
    rec_wk = _wk.groupby(_wk.t // 60 * 60).size().reindex(rec_ev.index, fill_value=0)
    _order = [DAY3["event"], DAY3["baseline"], DAY3["week"]]
    _dep = pd.concat([pd.DataFrame({"t": s.index, "n": _r30(s).values, "day": DAY3[p]})
                      for p, s in [("event", rec_ev), ("baseline", rec_bs), ("week", rec_wk)]]).dropna()
    _air = pd.concat([pd.DataFrame({"t": s.index, "n": s.values, "day": DAY3[p]})
                      for p, s in [("event", TOT_EV), ("baseline", TOT_BS), ("week", week_total)]])
    _air = _air[(_air.t >= T0) & (_air.t <= T_END)]
    for _d in (_dep, _air):
        _d["time_pt"] = to_pt(_d.t)
    _dash = alt.StrokeDash("day:N", sort=_order, legend=None, scale=alt.Scale(domain=_order, range=[[1, 0], [5, 3], [1, 3]]))
    _width = alt.StrokeWidth("day:N", sort=_order, legend=None, scale=alt.Scale(domain=_order, range=[2.6, 1.3, 1.3]))
    _op = alt.Opacity("day:N", sort=_order, legend=None, scale=alt.Scale(domain=_order, range=[1, 0.55, 0.55]))
    _x = alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M"))
    def _panel(d, main, ytitle, legend):
        return with_events(alt.Chart(d).mark_line().encode(
            x=_x, y=alt.Y("n:Q", title=ytitle),
            color=alt.Color("day:N", sort=_order, title=None, legend=alt.Legend(orient="top") if legend else None,
                            scale=alt.Scale(domain=_order, range=[main, "#9aa5b1", "#9aa5b1"])),
            strokeDash=_dash, strokeWidth=_width, opacity=_op,
            tooltip=["day:N", alt.Tooltip("time_pt:T", format="%-I:%M %p"), alt.Tooltip("n:Q", format=",.0f")])
        ).properties(width=880, height=210)
    recovery_chart = alt.vconcat(
        _panel(_dep, "#1c7ed6", "airline departures / 30 min", True),
        _panel(_air, "#f08c00", "aircraft in the air", False),
    ).resolve_scale(color="independent").properties(title=alt.Title(
        "The day in one chart",
        subtitle="U.S. airline departures and aircraft in the air, Pacific time · bold: Nov. 13 · faint dashed: Nov. 12 · faint dotted: Nov. 6, a normal Friday"))
    recovery_chart
    return


@app.cell(hide_code=True)
def _(AIR_MIN, AIR_MIN_T, COLLAPSE_T, LIFTED, LIFT_T, fmt_pt, prose):
    prose(f'''
    The bold lines are Nov. 13; the faint lines show the same hours on Nov. 12 (dashed) and on Nov. 6, a normal Friday
    (dotted). Departures always thin out late in the evening, so compare the bold line with the faint ones, not with its
    own afternoon.

    At {fmt_pt(COLLAPSE_T)} Pacific, departures fell off a cliff. The number of aircraft in the air drained for hours as
    flights already aloft landed, bottoming out at {AIR_MIN:,} at {fmt_pt(AIR_MIN_T)}{f". After the FAA lifted the stop at {fmt_pt(LIFT_T)}, departures surged, briefly overshot and then settled well below normal; Part 3 explains why." if LIFTED else "."}

    This page tells it in three parts: how the sky emptied, what kept flying when it was nearly empty, and how it came back.
    ''')
    return


@app.cell(hide_code=True)
def _(part):
    part(1, "The stop", "Departures halt, and the sky drains")
    return


@app.cell(hide_code=True)
def _(
    AFTER_RATE,
    AIR_BEFORE,
    AIR_MIN,
    AIR_MIN_BASE,
    AIR_MIN_T,
    BEFORE_RATE,
    COLLAPSE_T,
    GAP_MIN,
    fmt_pt,
    prose,
):
    prose(f"""
    Just after {fmt_pt(COLLAPSE_T)} Pacific time on Friday, the steady stream of departures from American airports
    stopped. For the half hour before, about **{BEFORE_RATE:.0f} airline flights took off every minute**, much like
    the same hour a day earlier. Within two minutes, the rate had dropped to a handful, and it stayed there:
    **{AFTER_RATE:.0f} a minute** on average over the following half hour.

    The Federal Aviation Administration's nationwide ground stop, which the agency attributed to a telecommunications
    outage affecting air traffic control, took effect at 2:54 p.m. Central (12:54 p.m. Pacific),
    [according to News9](https://www.news9.com/oklahoma-city-news/faa-reportedly-issues-nationwide-ground-stop).
    Public flight-tracking data shows **the departures stopped {GAP_MIN} minutes before that**.

    Nothing new was going up. The flights already in the air carried on to their destinations, and the number of
    aircraft over the country fell steadily, from **{AIR_BEFORE:,}** at the moment of the collapse to **{AIR_MIN:,}**
    at the low point, {fmt_pt(AIR_MIN_T)} Pacific. A day earlier at the same time, {AIR_MIN_BASE:,} aircraft were airborne.
    """)
    return


@app.cell(hide_code=True)
def _(AFTER_RATE, BEFORE_RATE, COLLAPSE_T, GAP_MIN, fmt_pt, prose):
    prose(f"""
    ## The cliff came first

    Counting airline takeoffs minute by minute makes the timing plain. The rate did not taper off as you might expect if
    airlines were holding flights at the gate one by one. It fell off a cliff, from about {BEFORE_RATE:.0f} a minute to {AFTER_RATE:.0f},
    between {fmt_pt(COLLAPSE_T)} and {fmt_pt(COLLAPSE_T + 120)}. The official ground-stop time comes
    {GAP_MIN} minutes later, in the shaded gap below.

    Early reports cited the 2:54 p.m. Central time. The data suggests departures were already being held in practice
    before the formal nationwide order. One possibility is that facilities hit by the communications outage stopped
    releasing flights on their own first. We could not find an official FAA timeline that settles it.
    """)
    return


@app.cell(hide_code=True)
def _(
    COLLAPSE_T,
    GAP_MIN,
    GROUND_STOP,
    PERIOD_LABEL,
    PT,
    T0,
    T_END,
    alt,
    dt,
    pd,
    tk_base,
    tk_event,
    to_pt,
    with_events,
):
    _lo, _hi = (COLLAPSE_T or T0) - 45 * 60, min(T_END - 900, (COLLAPSE_T or T0) + 40 * 60)
    _c = pd.concat([tk_event.rename("n").to_frame().assign(day=PERIOD_LABEL["event"]),
                    tk_base.rename("n").to_frame().assign(day=PERIOD_LABEL["baseline"])]).rename_axis("t").reset_index()
    _c = _c[(_c.t >= _lo) & (_c.t <= _hi)]
    _c["time_pt"] = to_pt(_c.t)
    _gap = pd.DataFrame([{"a": dt.datetime.fromtimestamp(COLLAPSE_T, PT).replace(tzinfo=None), "b": GROUND_STOP,
                          "label": f"{GAP_MIN}-minute gap"}])
    _band = alt.Chart(_gap).mark_rect(color="#e03131", opacity=0.08).encode(x="a:T", x2="b:T")
    _gap_txt = alt.Chart(_gap.assign(mid=_gap.a + (_gap.b - _gap.a) / 2)).mark_text(
        color="#e03131", fontSize=12, fontWeight="bold", baseline="bottom").encode(x="mid:T", y=alt.value(40), text="label:N")
    _lines = alt.Chart(_c).mark_line(strokeWidth=2.2, interpolate="step-after").encode(
        x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")),
        y=alt.Y("n:Q", title="airline takeoffs per minute"),
        color=alt.Color("day:N", sort=list(PERIOD_LABEL.values()), scale=alt.Scale(range=["#1c7ed6", "#adb5bd"])),
        strokeDash=alt.StrokeDash("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=[[1, 0], [4, 3]])),
        tooltip=[alt.Tooltip("time_pt:T", format="%-I:%M %p", title="PT"), "day:N", alt.Tooltip("n:Q", title="takeoffs")])
    cliff_chart = with_events(alt.layer(_band, _lines, _gap_txt), hi=_hi).properties(
        width="container", height=280,
        title=alt.Title("Airline takeoffs stopped before the ground stop was declared",
                        subtitle="Airline takeoffs per minute across the U.S., Pacific time · blue: Nov. 13 · dashed grey: Nov. 12"))
    cliff_chart
    return


@app.cell(hide_code=True)
def _(
    APT_Q,
    APT_STOP,
    CNN_ORIGIN,
    COLLAPSE_T,
    FIRST_APT,
    GROUND_STOP_T,
    MDW_STOP,
    ORD_MISSED,
    ORD_STOP,
    T0,
    ZoneInfo,
    dt,
    fmt_pt,
    prose,
):
    _f, _q = FIRST_APT, APT_Q
    _ord = (f"At O'Hare, departures stopped at **{fmt_pt(ORD_STOP)} Pacific** ({dt.datetime.fromtimestamp(ORD_STOP, ZoneInfo('America/Chicago')):%-I:%M} in Chicago), "
            f"{round(((COLLAPSE_T or T0) - ORD_STOP) / 60)} minutes before the nationwide collapse and "
            f"{round((GROUND_STOP_T - ORD_STOP) / 60)} minutes before the FAA's order. By the time departures stopped everywhere, "
            f"O'Hare would normally have sent off about {ORD_MISSED} more airline flights. It sent none. ") if ORD_STOP else ""
    _mdw = (f"Midway itself is too small to time precisely: its last departure was at {fmt_pt(MDW_STOP)}, a few minutes "
            f"ahead of most airports. ") if MDW_STOP else ""
    prose(f'''
    ## Where it started

    Airline sources told CNN that the failure began with network routers at Chicago's Midway airport and spread
    nationwide ([CNN]({CNN_ORIGIN})). The tracking data points to Chicago too. {_ord}{_mdw}It was not one airline
    pausing: United, American, their regional partners and foreign carriers all stopped at O'Hare at once, while
    Southwest, United, American and Delta kept departing elsewhere at normal rates until about 12:35. That pattern
    fits a problem in Chicago's air traffic control.

    Then it reached everyone else within minutes. Half of the {len(APT_STOP)} busiest airports sent off their last
    departure between {fmt_pt(_q[0])} and {fmt_pt(_q[2])}. The map below shows when each one went quiet.
    ''') if _f else prose("## Where it started\\n\\nNot enough data.")
    return


@app.cell(hide_code=True)
def _(APT_STOP, alt, fmt_pt, np):
    _states = alt.topo_feature("https://cdn.jsdelivr.net/npm/us-atlas@3.0.1/states-10m.json", "states")
    _d = APT_STOP.copy()
    _d["when"] = _d.stop.map(fmt_pt)
    _d["label"] = np.where(_d.index < 3, _d.apt + " " + _d.when, np.where(_d.apt.isin(["MDW"]), _d.apt + " " + _d.when, ""))
    _base = alt.Chart(_states).mark_geoshape(fill="#2b2f33", stroke="#555b61", strokeWidth=0.6)
    _pts = alt.Chart(_d).mark_circle(stroke="#111", strokeWidth=0.6, opacity=0.95).encode(
        longitude="lon:Q", latitude="lat:Q",
        size=alt.Size("per_hr:Q", title="normal departures / hour", scale=alt.Scale(range=[40, 900]), legend=None),
        color=alt.Color("vs_collapse:Q", title="minutes vs. 12:38 p.m.",
                        scale=alt.Scale(scheme="inferno", domain=[-25, 5], clamp=True), legend=alt.Legend(orient="bottom-left")),
        tooltip=["apt:N", alt.Tooltip("when:N", title="last departure (PT)"), alt.Tooltip("per_hr:Q", title="normal deps/hr", format=".0f"),
                 alt.Tooltip("missed:Q", title="normally in next 25 min")])
    _lab = alt.layer(*[alt.Chart(_d[(_d.label != "") & m]).mark_text(
        align="left", dx=16, dy=dy, fontSize=12, fontWeight="bold", color="#ffd84a").encode(longitude="lon:Q", latitude="lat:Q", text="label:N")
        for m, dy in [(_d.apt != "MDW", -10), (_d.apt == "MDW", 12)]])
    origin_map = alt.layer(_base, _pts, _lab).project(type="albersUsa").properties(
        width="container", height=430, title=alt.Title("Chicago went quiet first",
        subtitle="Last airline departure before each busy airport fell silent, Pacific time; darker = earlier, size = normal traffic"))
    origin_map
    return


@app.cell(hide_code=True)
def _(
    APT_STOP,
    APT_TK,
    COLLAPSE_T,
    GRID_APTS,
    PERIODS,
    PERIOD_LABEL,
    T0,
    alt,
    fmt_pt,
    pd,
    to_pt,
):
    _lo = ((COLLAPSE_T or T0) - 3000) // 300 * 300
    _hi = _lo + 4800
    _d = APT_TK[APT_TK.apt.isin(GRID_APTS) & (APT_TK.t >= _lo) & (APT_TK.t < _hi)]
    _d = (_d.assign(b=_d.t // 300 * 300).groupby(["apt", "period", "b"]).size()
          .reindex(pd.MultiIndex.from_product([GRID_APTS, PERIODS, range(_lo, _hi, 300)], names=["apt", "period", "b"]), fill_value=0)
          .rename("n").reset_index())
    _d["time_pt"] = to_pt(_d.b + 150)
    _d["day"] = _d.period.map(PERIOD_LABEL)
    _panels = []
    for _a in GRID_APTS:
        _s = int(APT_STOP.set_index("apt").stop[_a])
        _p = alt.Chart(_d[_d.apt == _a]).mark_line(strokeWidth=2, interpolate="step-after").encode(
            x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M", tickCount=3, labelFontSize=9)),
            y=alt.Y("n:Q", title=None, axis=alt.Axis(tickCount=3, labelFontSize=9)),
            color=alt.Color("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=["#1c7ed6", "#adb5bd"])),
            strokeDash=alt.StrokeDash("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=[[1, 0], [4, 3]])))
        _r = alt.Chart(pd.DataFrame({"t": [to_pt(pd.Series([_s])).iloc[0]]})).mark_rule(color="#f08c00", strokeDash=[3, 2]).encode(x="t:T")
        _panels.append(alt.layer(_p, _r).properties(width=150, height=80, title=alt.Title(
            f"{_a} · {fmt_pt(_s)}", fontSize=12, color="#ffd84a" if _a in ("ORD", "MDW") else None)))
    origin_grid = alt.concat(*_panels, columns=4).properties(title=alt.Title(
        "Airport by airport", subtitle="Airline departures per 5 minutes, ordered by when each went quiet (orange line); solid = Nov. 13, dashed = Nov. 12"))
    origin_grid
    return


@app.cell(hide_code=True)
def _(ZONE_COLLAPSE, fmt_pt, prose):
    prose(f'''
    ## Then everywhere at once

    Outside Chicago, there was little sign of a wave rolling across the country. Splitting departures into rough
    time-zone bands finds the collapse at **{({k: fmt_pt(v) for k, v in ZONE_COLLAPSE.items()}).get("East", "—")}** in the East,
    **{({k: fmt_pt(v) for k, v in ZONE_COLLAPSE.items()}).get("Central", "—")}** in the Central band,
    **{({k: fmt_pt(v) for k, v in ZONE_COLLAPSE.items()}).get("Mountain", "—")}** in the Mountain band and
    **{({k: fmt_pt(v) for k, v in ZONE_COLLAPSE.items()}).get("West", "—")}** in the West (all Pacific time). At the biggest
    hubs, the half hour after the cliff looked like an airport closed for the night.
    ''')
    return


@app.cell(hide_code=True)
def _(
    COLLAPSE_T,
    EVENTS,
    PERIOD_LABEL,
    T0,
    T_END,
    ZONE_COLLAPSE,
    alt,
    fmt_pt,
    moves,
    pd,
    to_pt,
):
    _zt = moves[(moves.kind == "takeoff") & (moves.category == "Airline") & (moves.region == "Lower 48")].copy()
    _zt["zone"] = pd.cut(_zt.lon, [-180, -115, -102, -87, -60], labels=["West", "Mountain", "Central", "East"])
    _lo, _hi = (COLLAPSE_T or T0) - 45 * 60, min(T_END - 900, (COLLAPSE_T or T0) + 40 * 60)
    _zt = _zt[(_zt.t >= _lo) & (_zt.t < _hi)]
    _zc = _zt.groupby([_zt.t // 120 * 120, "zone", "period"], observed=False).size().rename("n").reset_index()
    _zc["time_pt"] = to_pt(_zc.t)
    _zc["day"] = _zc.period.map(PERIOD_LABEL)
    _panels = []
    for _name in ["West", "Mountain", "Central", "East"]:
        _p = alt.Chart(_zc[_zc.zone == _name]).mark_line(strokeWidth=1.8, interpolate="monotone").encode(
            x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M", tickCount=4)),
            y=alt.Y("n:Q", title="takeoffs / 2 min" if _name == "West" else None),
            color=alt.Color("day:N", sort=list(PERIOD_LABEL.values()), scale=alt.Scale(range=["#1c7ed6", "#adb5bd"]),
                            legend=None),
            strokeDash=alt.StrokeDash("day:N", sort=list(PERIOD_LABEL.values()), legend=None,
                                      scale=alt.Scale(range=[[1, 0], [4, 3]])),
            tooltip=["day:N", alt.Tooltip("time_pt:T", format="%-I:%M %p"), "n:Q"])
        _rules = [alt.Chart(pd.DataFrame([e])).mark_rule(color=e["color"], strokeDash=[5, 3]).encode(x="t:T")
                  for e in EVENTS.to_dict("records") if e["t"] <= to_pt(pd.Series([_hi])).iloc[0]]
        _panels.append(alt.layer(_p, *_rules).properties(width=205, height=150, title=alt.Title(
            _name, subtitle=f"collapse {fmt_pt(ZONE_COLLAPSE[_name])}" if ZONE_COLLAPSE[_name] else "", fontSize=13)))
    zones_chart = alt.hconcat(*_panels).resolve_scale(y="independent").properties(
        title=alt.Title("The same minute in every region", subtitle="Airline takeoffs per 2 minutes by longitude band; "
                        "solid = Nov. 13, dashed = Nov. 12 · orange = collapse, red = FAA ground stop"))
    zones_chart
    return


@app.cell(hide_code=True)
def _(alt, hubs):
    _h = hubs[hubs.before > 0].melt(id_vars="hub", value_vars=["before", "after"], var_name="when", value_name="n")
    _h["when"] = _h.when.map({"before": "30 min before the collapse", "after": "30 min after"})
    _order = list(hubs[hubs.before > 0].hub)
    _y = alt.Y("hub:N", sort=_order, title=None, axis=alt.Axis(labelFontSize=12))
    _rule = alt.Chart(hubs[hubs.before > 0]).mark_rule(color="#adb5bd", strokeWidth=2).encode(y=_y, x="after:Q", x2="before:Q")
    _pts = alt.Chart(_h).mark_circle(size=110, opacity=1).encode(
        y=_y, x=alt.X("n:Q", title="airline departures in 30 minutes"),
        color=alt.Color("when:N", sort=["30 min before the collapse", "30 min after"],
                        scale=alt.Scale(range=["#1c7ed6", "#e03131"])),
        tooltip=["hub:N", "when:N", "n:Q"])
    hubs_chart = alt.layer(_rule, _pts).properties(width=620, height=alt.Step(22), title=alt.Title(
        "At the big hubs, departures went to almost zero",
        subtitle="Airline departures within ~30 km of each airport (nearby airports included), 30 min before vs after the collapse"))
    hubs_chart
    return


@app.cell(hide_code=True)
def _(COLLAPSE_T, fmt_pt, prose):
    prose(f"""
    ## Landings kept coming

    Takeoffs and landings normally track each other closely. That's how the number of aircraft aloft stays roughly
    level through the afternoon. After {fmt_pt(COLLAPSE_T)} the two lines split: takeoffs dropped to near zero, while
    landings continued at close to their usual pace as flights already en route reached their destinations. The gap
    between the lines is the sky draining.
    """)
    return


@app.cell(hide_code=True)
def _(PERIOD_LABEL, alt, total, with_events):
    _base = alt.Chart(total).encode(
        x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")),
        y=alt.Y("n:Q", title="aircraft airborne over the US"),
        color=alt.Color("label:N", title=None, sort=list(PERIOD_LABEL.values()), scale=alt.Scale(range=["#4aa3ff", "#9aa5b1"])),
        strokeDash=alt.StrokeDash("label:N", legend=None, sort=list(PERIOD_LABEL.values()), scale=alt.Scale(range=[[1, 0], [4, 3]])),
        tooltip=[alt.Tooltip("time_pt:T", format="%H:%M", title="PT"), "label:N", alt.Tooltip("n:Q", title="airborne")],
    )
    airborne_chart = with_events(_base.mark_line(strokeWidth=2)).properties(
        width="container", height=260, title=alt.Title("The sky drained for hours", subtitle="Aircraft airborne over the U.S. each minute, Pacific time"))
    airborne_chart
    return


@app.cell(hide_code=True)
def _(PERIOD_LABEL, alt, moves, with_events):
    _m = moves[moves.country == "US"].groupby(["period", "time_pt", "kind"]).size().rename("n").reset_index()
    _m["series"] = _m.kind.str.title() + "s · " + _m.period.map(PERIOD_LABEL)
    moves_chart = with_events(alt.Chart(_m).mark_line(point=alt.OverlayMarkDef(size=12), strokeWidth=1.8).encode(
        x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")),
        y=alt.Y("n:Q", title="events per 5 min"),
        color=alt.Color("kind:N", title=None, scale=alt.Scale(domain=["takeoff", "landing"], range=["#2ec27e", "#e5534b"])),
        strokeDash=alt.StrokeDash("period:N", title=None, scale=alt.Scale(domain=["event", "baseline"], range=[[1, 0], [4, 3]]),
                                  legend=None),
        tooltip=["series:N", alt.Tooltip("time_pt:T", format="%H:%M"), "n:Q"],
    )).properties(width="container", height=260, title=alt.Title("Takeoffs stopped; landings didn't", subtitle="All U.S. takeoffs and landings per 5 minutes, Pacific time · solid: Nov. 13 · dashed: Nov. 12"))
    moves_chart
    return


@app.cell(hide_code=True)
def _(prose):
    prose("""
    ## The middle of the sky emptied first

    Sorting airborne aircraft by altitude shows the order the sky emptied in. The layers between 15,000 and 35,000 feet,
    where jets climb out after takeoff, thinned fastest because nothing new was climbing through them. Two layers held
    up longer: cruise altitudes above 35,000 feet, where long flights already en route kept going, and the lowest band
    under 5,000 feet, which is mostly small private planes and helicopters.
    """)
    return


@app.cell(hide_code=True)
def _(T0, alt, pd, snap, to_pt, with_events):
    # altitude bands: stacked counts (left) and each band relative to its own 10:00-12:00 PT level (right)
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
    _x = alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M", tickCount=6))
    _stack = with_events(alt.Chart(_h).mark_area(opacity=0.9).encode(
        x=_x, y=alt.Y("n:Q", stack="zero", title="aircraft airborne"), color=_band_color, order=alt.Order("band:N", sort="ascending"),
        tooltip=["band:N", alt.Tooltip("time_pt:T", format="%H:%M"), "n:Q"])).properties(
        width=430, height=260, title=alt.Title("Airborne by altitude", subtitle="Nov. 13, Pacific time"))
    _rel = with_events(alt.Chart(_h).mark_line(strokeWidth=2).encode(
        x=_x, y=alt.Y("pct:Q", title="% of the band's 10:00–12:00 average"), color=_band_color,
        tooltip=["band:N", alt.Tooltip("time_pt:T", format="%H:%M"), "n:Q", alt.Tooltip("pct:Q", format=".0f")])).properties(
        width=430, height=260, title=alt.Title("Which layers emptied first", subtitle="Each band as % of its 10 a.m.–noon average"))
    alt_chart = alt.hconcat(_stack, _rel).resolve_scale(color="shared")
    alt_chart
    return


@app.cell(hide_code=True)
def _(WY_BASE_AT, WY_MIN, WY_NOON, WY_ZERO_T, fmt_pt, prose):
    prose(f'''
    ## An empty state

    One moment on the map sums it up. At **{fmt_pt(WY_ZERO_T)} Pacific**, not a single aircraft was visible in the sky
    over Wyoming. At noon there had been {WY_NOON}. At the same time a day earlier there were {WY_BASE_AT}.
    Receiver coverage is thin at low altitude over the rural West, so a small plane flying low could be missed. The jets
    at cruise altitude that normally cross the state all day are hard to miss.
    ''') if WY_ZERO_T else prose(f'''
    ## An emptying state

    Over Wyoming, the number of aircraft in the air fell from {WY_NOON} at noon to as few as {WY_MIN}.
    ''')
    return


@app.cell(hide_code=True)
def _(
    PERIODS,
    PERIOD_LABEL,
    T0,
    T_END,
    WY_ZERO_T,
    alt,
    fmt_pt,
    pd,
    to_pt,
    with_events,
    wy_series,
):
    _d = pd.concat([wy_series[p].rename("n").to_frame().assign(day=PERIOD_LABEL[p]) for p in PERIODS]).rename_axis("t").reset_index()
    _d = _d[(_d.t >= T0) & (_d.t <= T_END)]
    _d["time_pt"] = to_pt(_d.t)
    _line = alt.Chart(_d).mark_line(strokeWidth=2, interpolate="step-after").encode(
        x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")),
        y=alt.Y("n:Q", title="aircraft airborne over Wyoming"),
        color=alt.Color("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=["#1c7ed6", "#adb5bd"])),
        strokeDash=alt.StrokeDash("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=[[1, 0], [4, 3]])),
        tooltip=["day:N", alt.Tooltip("time_pt:T", format="%-I:%M %p"), "n:Q"])
    _layers = [_line]
    if WY_ZERO_T:
        _z = pd.DataFrame([{"time_pt": to_pt(pd.Series([WY_ZERO_T])).iloc[0], "n": 0, "label": f"0 aircraft at {fmt_pt(WY_ZERO_T)}"}])
        _layers += [alt.Chart(_z).mark_point(size=90, filled=True, color="#e03131").encode(x="time_pt:T", y="n:Q"),
                    alt.Chart(_z).mark_text(align="right", dx=-6, dy=-34, color="#e03131", fontWeight="bold").encode(
                        x="time_pt:T", y="n:Q", text="label:N")]
    wy_chart = with_events(alt.layer(*_layers)).properties(width="container", height=220, title=alt.Title(
        "Wyoming's sky, emptied", subtitle="Aircraft airborne over Wyoming; solid = Nov. 13, dashed = Nov. 12"))
    wy_chart
    return


@app.cell(hide_code=True)
def _(COLLAPSE_T, LIFTED, LIFT_T, T_END, WY_ZERO_T, fmt_pt, prose):
    prose(f'''
    ## Replay the day

    Every aircraft broadcasting its position over the U.S., one frame per minute, from 10 a.m. to {fmt_pt(T_END)} Pacific.
    The map opens at the low point. Drag the slider back to {fmt_pt(COLLAPSE_T)} to watch departures stop,
    {f"to {fmt_pt(WY_ZERO_T)} to see Wyoming empty, " if WY_ZERO_T else ""}{f"and past {fmt_pt(LIFT_T)} to watch the sky refill" if LIFTED else ""}.
    Aircraft are colored by altitude; grey ones are on the ground with transponders on. Canadian and Mexican traffic is
    faded. Hover over a plane for its callsign and type.
    ''')
    return


@app.cell(hide_code=True)
def _(CATS, PERIOD_LABEL, mo):
    day_pick = mo.ui.dropdown({v: k for k, v in PERIOD_LABEL.items()}, value=PERIOD_LABEL["event"], label="day")
    cat_pick = mo.ui.multiselect(CATS, value=CATS, label="categories")
    mo.hstack([day_pick, cat_pick], justify="start", gap=2)
    return cat_pick, day_pick


@app.cell(hide_code=True)
def _(cat_pick, day_pick, make_flightmap):
    flightmap = make_flightmap(day_pick.value, cat_pick.value)
    flightmap
    return


@app.cell(hide_code=True)
def _(part):
    part(2, "At the bottom", "What kept flying, and what didn't")
    return


@app.cell(hide_code=True)
def _(AIR_MIN_T, CAT_NOW, fmt_pt, prose):
    _cat = ", ".join(f"{k.lower()} {v}%" for k, v in sorted(CAT_NOW.items(), key=lambda kv: -kv[1]))
    prose(f"""
    ## Who kept flying

    Airline traffic fell furthest, and the mix of what stayed aloft shows it. At the low point, {fmt_pt(AIR_MIN_T)} Pacific,
    compared with the same time a day earlier, airborne traffic by category stood at: {_cat}. Helicopters (police,
    medical, news) and small private planes made up a growing share of what was still flying.
    """)
    return


@app.cell(hide_code=True)
def _(CATS, alt, counts, with_events):
    _c = counts[counts.t % 600 == 0]                                     # every 10 min keeps the chart light
    _y = _c[_c.period == "baseline"][["category", "t", "n"]].rename(columns={"n": "n_before"})
    _t = _c[_c.period == "event"].merge(_y, on=["category", "t"], how="left")
    _t["pct"] = 100 * _t.n / _t.n_before
    category_chart = with_events(alt.Chart(_t).mark_line(strokeWidth=2).encode(
        x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")),
        y=alt.Y("pct:Q", title="airborne, % of the day before"),
        color=alt.Color("category:N", title=None, sort=CATS),
        tooltip=["category:N", alt.Tooltip("time_pt:T", format="%H:%M"), "n:Q", "n_before:Q", alt.Tooltip("pct:Q", format=".0f")],
    )).properties(width="container", height=240, title=alt.Title("What is left in the air", subtitle="Aircraft airborne by category, as a share of the same time a day earlier"))
    category_chart
    return


@app.cell(hide_code=True)
def _(BJ_HIGH, BJ_TK, GA_HIGH, OSINT_POST, prose):
    prose(f'''
    Below 18,000 feet, pilots can fly under visual flight rules without clearances from the en-route centers that were
    failing, a point also made in a [parallel analysis of the same data]({OSINT_POST}). Business jets show it. Only
    **{BJ_TK["event"]}** took off from lower-48 airports during the stop, against {BJ_TK["baseline"]} in the same hours a
    day earlier, and those that flew stayed lower: {BJ_HIGH["event"]}% of their positions were above 18,000 feet, against
    {BJ_HIGH["baseline"]}% normally. Small propeller planes, which rarely climb that high anyway
    ({GA_HIGH["event"]}% vs. {GA_HIGH["baseline"]}%), carried on much as usual.
    ''')
    return


@app.cell(hide_code=True)
def _(COLLAPSE_T, NYT_AK, REGION_STATS, fmt_pt, prose):
    _r = REGION_STATS
    prose(f'''
    ## Two states kept flying

    Alaska Airlines said in a statement that flights within Alaska and inter-island flights in Hawaii were not affected
    by the ground stop, [The New York Times reported]({NYT_AK}). The tracking data agrees. Between {fmt_pt(COLLAPSE_T)} and the lift,
    airline departures in **Alaska ran at {_r["Alaska"]["pct"]}%** of the previous day's level for the same hours and
    **Hawaii at {_r["Hawaii"]["pct"]}%**. In the lower 48 states the figure was **{_r["Lower 48"]["pct"]}%**.

    Hawaiian Airlines' Boeing 717s kept shuttling between the islands, and international flights by Japan Airlines,
    ANA, Korean Air, Qantas and Philippine Airlines kept leaving Honolulu. In Alaska, Alaska Airlines' in-state jets,
    regional carriers such as Bering Air and Ravn, and the cargo flights that stop in Anchorage kept flying.
    ''')
    return


@app.cell(hide_code=True)
def _(
    EVENTS,
    PERIOD_LABEL,
    REGION_STATS,
    T0,
    T_END,
    alt,
    np,
    pd,
    tk_all,
    to_pt,
):
    _d = tk_all[tk_all.region.isin(["Lower 48", "Alaska", "Hawaii"]) & (tk_all.t < (T_END - 900) // 1800 * 1800)]
    _bins = np.arange(T0, (T_END - 900) // 1800 * 1800, 1800)
    _d = (_d.assign(b=_d.t // 1800 * 1800).groupby(["region", "b", "period"]).size()
          .reindex(pd.MultiIndex.from_product([["Lower 48", "Alaska", "Hawaii"], _bins, ["event", "baseline"]],
                                              names=["region", "b", "period"]), fill_value=0).rename("n").reset_index())
    _d["time_pt"] = to_pt(_d.b + 900)
    _d["day"] = _d.period.map(PERIOD_LABEL)
    _panels = []
    for _name in ["Lower 48", "Alaska", "Hawaii"]:
        _p = alt.Chart(_d[_d.region == _name]).mark_line(strokeWidth=2.2, point=alt.OverlayMarkDef(size=18)).encode(
            x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M", tickCount=4)),
            y=alt.Y("n:Q", title="airline departures / 30 min" if _name == "Lower 48" else None, scale=alt.Scale(zero=True)),
            color=alt.Color("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=["#1c7ed6", "#adb5bd"])),
            strokeDash=alt.StrokeDash("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=[[1, 0], [4, 3]])),
            tooltip=["day:N", alt.Tooltip("time_pt:T", format="%-I:%M %p"), "n:Q"])
        _rules = [alt.Chart(pd.DataFrame([e])).mark_rule(color=e["color"], strokeDash=[5, 3]).encode(x="t:T")
                  for e in EVENTS.to_dict("records")]
        _pct = REGION_STATS[_name]["pct"]
        _panels.append(alt.layer(_p, *_rules).properties(width=280, height=170, title=alt.Title(
            _name, subtitle=f"during the stop: {_pct}% of Nov. 12" if _pct is not None else "", fontSize=13)))
    states_chart = alt.hconcat(*_panels).resolve_scale(y="independent").properties(title=alt.Title(
        "Alaska and Hawaii barely noticed", subtitle="Airline departures per 30 minutes; solid = Nov. 13, dashed = Nov. 12"))
    states_chart
    return


@app.cell(hide_code=True)
def _(
    LH_AIRPORTS,
    LH_FIRST_HOUR,
    LH_LAST_HOUR,
    LH_RESUME_T,
    LH_STATS,
    LH_TOTAL,
    NYT_INTL,
    fmt_pt,
    prose,
):
    _lh_pct = LH_STATS["pct"]
    _wb = lambda n: f"{n} wide-body" if n == 1 else f"{n} wide-bodies"
    _share = round(100 * LH_LAST_HOUR[0] / LH_LAST_HOUR[1]) if LH_LAST_HOUR[1] else None
    _share_txt = ("about the usual number" if _share is not None and _share >= 85 else
                  f"about {_share}% of the {LH_LAST_HOUR[1]} that left the day before" if _share is not None else "")
    _apts = ", ".join(LH_AIRPORTS[:-1]) + (f" and {LH_AIRPORTS[-1]}" if len(LH_AIRPORTS) > 1 else "".join(LH_AIRPORTS))
    prose(f'''
    ## Long-haul flights got out

    The halt was not total. Some international flights were departing U.S. airports, including Honolulu and San
    Francisco for Asia, and several left Kennedy for Europe, [The New York Times reported]({NYT_INTL}). The FAA had not
    said which international flights were cleared to go. Wikipedia's account of the day says Pacific-bound flights from
    San Francisco were cleared about two hours after the advisory, and some transatlantic flights from the East Coast
    were allowed to leave.

    The data shows them clearly in the wide-body jets that fly long international routes. In the hour after the collapse,
    just **{_wb(LH_FIRST_HOUR[0])}** left mainland airports, against {LH_FIRST_HOUR[1]} the day before. Then they started
    coming back{f": from about **{fmt_pt(LH_RESUME_T)}** Pacific," if LH_RESUME_T else ","} the evening bank of flights to
    Europe and Asia began to leave. In the latest hour of data, **{LH_LAST_HOUR[0]}** departed, {_share_txt},
    led by {_apts}. Since the collapse, {_wb(LH_TOTAL)} have left the lower 48.
    ''')
    return


@app.cell(hide_code=True)
def _(
    PERIODS,
    PERIOD_LABEL,
    T0,
    T_END,
    alt,
    lh_tk,
    np,
    pd,
    to_pt,
    with_events,
):
    _bins = np.arange(T0, (T_END - 900) // 1800 * 1800, 1800)
    _d = (lh_tk.assign(b=lh_tk.t // 1800 * 1800).groupby(["b", "period"]).size()
          .reindex(pd.MultiIndex.from_product([_bins, PERIODS], names=["b", "period"]), fill_value=0).rename("n").reset_index())
    _d["time_pt"] = to_pt(_d.b + 900)
    _d["day"] = _d.period.map(PERIOD_LABEL)
    intl_chart = with_events(alt.Chart(_d).mark_line(strokeWidth=2.2, point=alt.OverlayMarkDef(size=20)).encode(
        x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")),
        y=alt.Y("n:Q", title="wide-body departures / 30 min"),
        color=alt.Color("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=["#1c7ed6", "#adb5bd"])),
        strokeDash=alt.StrokeDash("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=[[1, 0], [4, 3]])),
        tooltip=["day:N", alt.Tooltip("time_pt:T", format="%-I:%M %p"), "n:Q"])).properties(
        width="container", height=240, title=alt.Title("Wide-bodies dipped, then the long-haul bank left",
                                                       subtitle="Wide-body airline departures from the lower 48 per 30 minutes; solid = Nov. 13, dashed = Nov. 12"))
    intl_chart
    return


@app.cell(hide_code=True)
def _(CNN_ORIGIN, GATEWAYS, GW_PCT, TRICKLE, prose):
    _g = GATEWAYS.set_index("apt")
    _none = [a for a in GATEWAYS[GATEWAYS.kind == "inland hub"].apt if _g.loc[a, "nov13"] == 0][:4]
    _top = GATEWAYS[GATEWAYS.kind == "coastal gateway"].sort_values("nov13", ascending=False).head(3)
    prose(f'''
    Where the flights left from mattered. A long-haul flight from a coastal gateway reaches oceanic airspace within
    minutes. Oceanic airspace is managed through a separate, largely text-based system, as the head of the air traffic
    controllers' union explained on [CNN]({CNN_ORIGIN}). A flight from an inland hub first has to cross the en-route
    centers that were failing. During the stop, coastal gateways sent off **{GW_PCT.get("coastal gateway", 0)}%** of
    their usual wide-body departures
    ({", ".join(f"{a} {int(_g.loc[a, 'nov13'])} vs. {int(_g.loc[a, 'nov12'])}" for a in _top.apt)}), and inland hubs
    **{GW_PCT.get("inland hub", 0)}%**{f"; {', '.join(_none)} sent none" if _none else ""}.

    Those long-haul flights, plus flights within Alaska and Hawaii, kept the departure line in the chart at the top
    of the page off zero: of the {TRICKLE["n"]:,} airline departures from U.S. airports during the stop,
    {TRICKLE["akhi"]}% were in Alaska or Hawaii and {TRICKLE["wide48"]}% were wide-bodies from the lower 48.
    ''')
    return


@app.cell(hide_code=True)
def _(GATEWAYS, alt):
    _d = GATEWAYS.head(16).melt(id_vars=["apt", "kind"], value_vars=["nov13", "nov12"], var_name="day", value_name="n")
    _d["day"] = _d.day.map({"nov13": "Nov. 13, during the stop", "nov12": "Nov. 12, same hours"})
    _order = GATEWAYS.head(16).sort_values(["kind", "nov12"], ascending=[True, False]).apt.tolist()
    gateway_chart = alt.Chart(_d).mark_bar().encode(
        y=alt.Y("apt:N", sort=_order, title=None),
        x=alt.X("n:Q", title="wide-body departures"),
        yOffset=alt.YOffset("day:N", sort=["Nov. 13, during the stop", "Nov. 12, same hours"]),
        color=alt.Color("kind:N", title=None, scale=alt.Scale(domain=["coastal gateway", "inland hub"], range=["#1c7ed6", "#e8590c"]),
                        legend=alt.Legend(orient="top")),
        opacity=alt.Opacity("day:N", sort=["Nov. 13, during the stop", "Nov. 12, same hours"], scale=alt.Scale(range=[1, 0.3]),
                            legend=alt.Legend(orient="top", title=None)),
        tooltip=["apt:N", "kind:N", "day:N", "n:Q"]).properties(width="container", height=alt.Step(11), title=alt.Title(
        "Coastal gateways kept sending long-haul flights; inland hubs mostly didn't",
        subtitle="Wide-body airline departures between the collapse and the lift, vs. the same hours on Nov. 12"))
    gateway_chart
    return


@app.cell(hide_code=True)
def _(AIRSPACE, ROUTES, alt, pd):
    _feats = alt.Data(values=AIRSPACE)
    _states = alt.topo_feature("https://cdn.jsdelivr.net/npm/us-atlas@3.0.1/states-10m.json", "states")
    _bbox = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}, "geometry": {
        "type": "Polygon", "coordinates": [[[-135, 18], [-135, 55], [-55, 55], [-55, 18], [-135, 18]][::-1]]}}]}
    _proj = dict(type="mercator", center=[-100, 44], scale=620)
    _centers = alt.Chart(_feats).mark_geoshape(fill="#e8590c", fillOpacity=0.10, stroke="#e8590c", strokeOpacity=0.55, strokeWidth=0.8)
    _st = alt.Chart(_states).mark_geoshape(fill=None, stroke="#6c757d", strokeWidth=0.4)
    _lab = alt.Chart(alt.Data(values=[{"id": f["properties"]["id"], "lon": f["properties"]["lon"], "lat": f["properties"]["lat"]}
                                      for f in AIRSPACE if f["properties"].get("lon")])).mark_text(
        color="#e8590c", fontSize=9, opacity=0.8).encode(longitude="lon:Q", latitude="lat:Q", text="id:N")
    _rows = [{"route": f'{r["cs"]} from {r["apt"]}', "kind": r["kind"], "i": i, "lon": p[0], "lat": p[1]}
             for r in ROUTES for i, p in enumerate(r["path"])]
    _paths = alt.Chart(pd.DataFrame(_rows)).mark_line(strokeWidth=2.2).encode(
        longitude="lon:Q", latitude="lat:Q", detail="route:N", order="i:Q",
        color=alt.Color("kind:N", title=None, legend=alt.Legend(orient="bottom"),
                        scale=alt.Scale(domain=["left during the stop (coastal)", "same hour on Nov. 12 (inland, held on Nov. 13)"],
                                        range=["#4dabf7", "#ff6b6b"])),
        strokeDash=alt.StrokeDash("kind:N", legend=None, scale=alt.Scale(
            domain=["left during the stop (coastal)", "same hour on Nov. 12 (inland, held on Nov. 13)"], range=[[1, 0], [5, 3]])),
        tooltip=["route:N", "kind:N"]) if _rows else alt.Chart(pd.DataFrame({"lon": [], "lat": []})).mark_line()
    _ends = pd.DataFrame([{"route": f'{r["cs"]} from {r["apt"]}', "lon": r["path"][0][0], "lat": r["path"][0][1], "apt": r["apt"]} for r in ROUTES])
    _dots = alt.Chart(_ends).mark_text(fontSize=11, fontWeight="bold", color="#f1f3f5", dy=-9).encode(
        longitude="lon:Q", latitude="lat:Q", text="apt:N") if len(_ends) else alt.Chart(pd.DataFrame({"lon": []})).mark_point()
    airspace_map = alt.layer(_centers, _st, _lab, _paths, _dots).project(**_proj).properties(
        width="container", height=440, title=alt.Title(
            "Inland long-haul flights must cross the failing en-route centers first",
            subtitle="Shaded: the 20 lower-48 air route traffic control centers. Example wide-body routes, first 4 hours after takeoff"))
    airspace_map
    return


@app.cell(hide_code=True)
def _(GLOBAL_NEWS, NEIGHBOR_STATS, NYT_LIVE, prose):
    _n = NEIGHBOR_STATS
    prose(f'''
    ## The neighbors stopped flying to the U.S.

    The FAA controls only U.S. airspace, but the stop reached across both borders. Canadian airports suspended
    U.S.-bound flights while domestic Canadian flights carried on, [Global News reported]({GLOBAL_NEWS}).
    And the FAA asked Mexico's federal aviation agency to keep all aircraft at Mexican airports with scheduled
    flights to the United States on the ground, the Mexican agency said, [according to The New York Times]({NYT_LIVE}).

    The data shows the same split. Departures from Canadian airports that went on to enter U.S. airspace fell from
    about **{_n[("Canada", True)]["before"]:.0f} per half hour to {_n[("Canada", True)]["after"]:.0f}**, while
    flights that stayed out of the U.S. ran at **{_n[("Canada", False)]["pct"]}%** of the previous day's level. Mexico
    points the same way, with far fewer flights in the data: U.S.-bound departures went from {_n[("Mexico", True)]["before"]:.0f} to
    {_n[("Mexico", True)]["after"]:.0f} per half hour, and other flights ran at {_n[("Mexico", False)]["pct"]}% of normal.
    The volunteer receivers that feed this data cover far less of Mexico than of the U.S. and Canada, so the Mexican
    numbers are small.
    ''')
    return


@app.cell(hide_code=True)
def _(EVENTS, NB_END, PERIOD_LABEL, T0, alt, nb_tk, np, pd, to_pt):
    _d = nb_tk[nb_tk.t < NB_END // 1800 * 1800]
    _d = _d.assign(b=_d.t // 1800 * 1800, dest=np.where(_d.to_us, "into U.S. airspace", "elsewhere"))
    _bins = np.arange(T0, NB_END // 1800 * 1800, 1800)
    _d = (_d.groupby(["country", "dest", "b", "period"]).size()
          .reindex(pd.MultiIndex.from_product([["Canada", "Mexico"], ["into U.S. airspace", "elsewhere"], _bins, ["event", "baseline"]],
                                              names=["country", "dest", "b", "period"]), fill_value=0).rename("n").reset_index())
    _d["time_pt"] = to_pt(_d.b + 900)
    _d["day"] = _d.period.map(PERIOD_LABEL)
    _panels = []
    for _name in ["Canada", "Mexico"]:
        _p = alt.Chart(_d[_d.country == _name]).mark_line(strokeWidth=2.2, point=alt.OverlayMarkDef(size=18)).encode(
            x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M", tickCount=5)),
            y=alt.Y("n:Q", title="airline departures / 30 min" if _name == "Canada" else None),
            color=alt.Color("dest:N", title="flights that went", sort=["into U.S. airspace", "elsewhere"],
                            scale=alt.Scale(domain=["into U.S. airspace", "elsewhere"], range=["#e03131", "#2f9e44"])),
            strokeDash=alt.StrokeDash("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=[[1, 0], [4, 3]])),
            detail="day:N",
            tooltip=["dest:N", "day:N", alt.Tooltip("time_pt:T", format="%-I:%M %p"), "n:Q"])
        _rules = [alt.Chart(pd.DataFrame([e])).mark_rule(color=e["color"], strokeDash=[5, 3]).encode(x="t:T")
                  for e in EVENTS.to_dict("records")]
        _panels.append(alt.layer(_p, *_rules).properties(width=430, height=200, title=alt.Title(_name, fontSize=13)))
    neighbors_chart = alt.hconcat(*_panels).resolve_scale(y="independent", color="shared").properties(title=alt.Title(
        "Canada and Mexico: U.S.-bound departures stopped, the rest kept going",
        subtitle="Airline departures per 30 minutes; solid = Nov. 13, dashed = Nov. 12"))
    neighbors_chart
    return


@app.cell(hide_code=True)
def _(AUS_TARMAC, CNN_ORIGIN, TARMAC, prose):
    _top = TARMAC.head(3)
    _aus = AUS_TARMAC
    prose(f'''
    ## Where the planes piled up

    With nothing taking off and flights still landing, airports filled up. Airlines warned that some were running out of
    gates and taxiway space, and one airline source told CNN that Austin might be the first to saturate
    ([CNN]({CNN_ORIGIN})). Counting aircraft on the ground with their transponders on (mostly planes taxiing or waiting,
    since parked planes often switch theirs off) shows modest build-ups rather than dramatic ones. The largest were at
    {", ".join(f"**{r.apt}** ({r.ratio:.1f} times its morning level)" for r in _top.itertuples())}.
    {f"Austin was at {_aus['ratio']:.1f} times its morning level, so it does not stand out in this data." if _aus else ""}
    This measure is noisy: it depends on which receivers can hear aircraft on the ground at each airport.
    ''') if len(TARMAC) else prose("## Where the planes piled up\\n\\nNot enough data.")
    return


@app.cell(hide_code=True)
def _(
    GROUND,
    PERIODS,
    PERIOD_LABEL,
    T0,
    TARMAC,
    T_END,
    alt,
    fmt_pt,
    pd,
    to_pt,
    with_events,
):
    _d = TARMAC.head(12).copy()
    _d["when"] = _d.peak_t.map(fmt_pt)
    _bars = alt.Chart(_d).mark_bar(color="#e8590c").encode(
        y=alt.Y("apt:N", sort="-x", title=None), x=alt.X("ratio:Q", title="× the airport's own morning level"),
        tooltip=["apt:N", alt.Tooltip("peak:Q", title="peak on ground"), alt.Tooltip("when:N", title="at (PT)"),
                 alt.Tooltip("normal:Q", title="normal", format=".0f"), alt.Tooltip("ratio:Q", format=".1f")])
    _txt = _bars.mark_text(align="left", dx=4, color="#adb5bd", fontSize=11).encode(text=alt.Text("peak:Q"))
    _left = alt.layer(_bars, _txt).properties(width=300, height=alt.Step(18), title=alt.Title(
        "Where the planes piled up", subtitle="Aircraft on the ground (transponder on), average during the stop vs. the same morning; label = peak"))
    _a = TARMAC.apt.iloc[0] if len(TARMAC) else "ORD"
    _s = pd.concat([GROUND.loc[(p, _a)].rename("n").to_frame().assign(day=PERIOD_LABEL[p]) for p in PERIODS
                    if (p, _a) in GROUND.index]).rename_axis("t").reset_index()
    _s = _s[(_s.t >= T0) & (_s.t <= T_END)]
    _s["time_pt"] = to_pt(_s.t)
    _right = with_events(alt.Chart(_s).mark_line(strokeWidth=2).encode(
        x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")), y=alt.Y("n:Q", title="aircraft on the ground"),
        color=alt.Color("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=["#e8590c", "#adb5bd"])),
        strokeDash=alt.StrokeDash("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=[[1, 0], [4, 3]])),
        tooltip=["day:N", alt.Tooltip("time_pt:T", format="%-I:%M %p"), "n:Q"])).properties(width=400, height=260, title=alt.Title(
        f"{_a}: aircraft on the ground", subtitle="solid = Nov. 13, dashed = Nov. 12 (transponder on)"))
    tarmac_chart = alt.hconcat(_left, _right)
    tarmac_chart
    return


@app.cell(hide_code=True)
def _(part):
    part(3, "The return", "The ban is lifted and the sky refills")
    return


@app.cell(hide_code=True)
def _(
    AIR_NOW_PCT,
    DEP_NOW_PCT,
    EAST_WB,
    GAP_MIN,
    LAG_MIN,
    LIFTED,
    LIFT_SRC,
    LIFT_T,
    RECOVERY_T,
    T_END,
    ZONE_RECOVERY,
    fmt_pt,
    prose,
):
    _rec = (f"Departures stayed at the ground-stop trickle for about **{LAG_MIN} minutes** and only began climbing at "
            f"**{fmt_pt(RECOVERY_T)}**, the mirror image of the afternoon, when departures stopped "
            f"{GAP_MIN} minutes before the order." if RECOVERY_T and LAG_MIN is not None and LAG_MIN > 0 else
            f"Departures began climbing at **{fmt_pt(RECOVERY_T)}**." if RECOVERY_T else
            "Departures have not picked up yet in the data.")
    _zname = {"East": "the East", "West": "the West", "Central": "the central states", "Mountain": "the mountain states"}
    _zr = sorted([(t, _zname[z]) for z, t in ZONE_RECOVERY.items() if t], key=lambda x: x[0])
    _zone_txt = ""
    if _zr:
        _first_t, _first = _zr[0]
        _zone_txt = (
            f"{_first[0].upper() + _first[1:]} came back first, at {fmt_pt(_first_t)}"
            + (f", {round((LIFT_T - _first_t) / 60)} minutes before the lift was announced" if _first_t < LIFT_T else "")
            + (f"; {EAST_WB[0]} of its first {EAST_WB[1]} airline departures were wide-bodies, the jets used on long international routes"
               if _first == "the East" and EAST_WB[1] else "") + ". "
            + ("Then " + ", ".join(f"{z} ({fmt_pt(t)})" for t, z in _zr[1:-1])
               + (" and " if len(_zr) > 2 else "") + f"{_zr[-1][1]} ({fmt_pt(_zr[-1][0])})." if len(_zr) > 1 else ""))
    prose(f'''
    ## The lift

    The FAA lifted the nationwide ground stop at 8:15 p.m. Eastern (5:15 p.m. Pacific),
    [Al Jazeera reported]({LIFT_SRC}), after about four hours and 20 minutes. The sky did not refill at once. {_rec}

    {_zone_txt}

    By {fmt_pt(T_END)} Pacific, the latest data, airline departures were running at **{DEP_NOW_PCT}%** of the previous
    day's level and the number of aircraft in the air at **{AIR_NOW_PCT}%**. Airlines warned that delays and cancellations
    would continue as they got aircraft and crews back into position.
    ''') if LIFTED else prose('''
    ## The lift

    The FAA lifted the ground stop at 5:15 p.m. Pacific. The flight data here does not reach that time yet.
    ''')
    return


@app.cell(hide_code=True)
def _(
    LAG_MIN,
    LIFT,
    LIFT_T,
    PERIOD_LABEL,
    PT,
    RECOVERY_T,
    T_END,
    alt,
    dt,
    pd,
    rec_bs,
    rec_ev,
    to_pt,
    with_events,
):
    _lo, _hi = LIFT_T - 45 * 60, min(T_END - 900, LIFT_T + 100 * 60)
    _sm = lambda s: s.rolling(5, center=True, min_periods=3).mean()       # 5-minute average smooths feed gaps
    _c = pd.concat([_sm(rec_ev).rename("n").to_frame().assign(day=PERIOD_LABEL["event"]),
                    _sm(rec_bs).rename("n").to_frame().assign(day=PERIOD_LABEL["baseline"])]).rename_axis("t").reset_index()
    _c = _c[(_c.t >= _lo) & (_c.t <= _hi)]
    _c["time_pt"] = to_pt(_c.t)
    _layers = []
    if RECOVERY_T and RECOVERY_T > LIFT_T:
        _gap = pd.DataFrame([{"a": LIFT, "b": dt.datetime.fromtimestamp(RECOVERY_T, PT).replace(tzinfo=None),
                              "label": f"{LAG_MIN}-minute lag"}])
        _layers += [alt.Chart(_gap).mark_rect(color="#2f9e44", opacity=0.10).encode(x="a:T", x2="b:T"),
                    alt.Chart(_gap.assign(mid=_gap.a + (_gap.b - _gap.a) / 2)).mark_text(
                        color="#2f9e44", fontSize=12, fontWeight="bold", baseline="bottom").encode(x="mid:T", y=alt.value(40), text="label:N")]
    _lines = alt.Chart(_c).mark_line(strokeWidth=2.2, interpolate="monotone").encode(
        x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")),
        y=alt.Y("n:Q", title="airline takeoffs per minute (5-min avg)"),
        color=alt.Color("day:N", sort=list(PERIOD_LABEL.values()), scale=alt.Scale(range=["#1c7ed6", "#adb5bd"])),
        strokeDash=alt.StrokeDash("day:N", sort=list(PERIOD_LABEL.values()), legend=None, scale=alt.Scale(range=[[1, 0], [4, 3]])),
        tooltip=[alt.Tooltip("time_pt:T", format="%-I:%M %p", title="PT"), "day:N", alt.Tooltip("n:Q", title="takeoffs/min", format=".1f")])
    restart_chart = with_events(alt.layer(*_layers, _lines), lo=_lo, hi=_hi).properties(
        width="container", height=260,
        title=alt.Title("Departures restarted after the lift, not with it",
                        subtitle="Airline takeoffs per minute across the U.S. (5-minute average), Pacific time · blue: Nov. 13 · dashed grey: Nov. 12"))
    restart_chart
    return


@app.cell(hide_code=True)
def _(BACKLOG_PCT, EVE_ONSCHED_PCT, LIFT_T, PEAK_T, T_END, fmt_pt, prose):
    prose(f'''
    ## Why departures overshot, then settled

    After the restart, departures climbed quickly, peaked around {fmt_pt(PEAK_T) if PEAK_T else "–"} and then fell back.
    Matching flight numbers against a normal Friday, Nov. 6, explains the shape. About **{BACKLOG_PCT}%** of the airline
    departures after the lift were flights that normally leave during the afternoon: the held backlog, released in a
    wave. Underneath it, the regular evening schedule was thin. Only about **{EVE_ONSCHED_PCT}%** of the flights that
    normally leave between {fmt_pt(LIFT_T)} and {fmt_pt(T_END - 1800)} left within an hour of their usual time. As the
    backlog drained, departures settled at that lower level.
    ''')
    return


@app.cell(hide_code=True)
def _(BACKLOG, BACKLOG_KINDS, alt, to_pt, week_moves, with_events):
    _b = BACKLOG.assign(b=BACKLOG.t // 900 * 900).groupby(["b", "kind"]).size().rename("n").reset_index()
    _b["time_pt"] = to_pt(_b.b + 450)
    _wkq = _wk15 = week_moves[(week_moves.kind == "takeoff") & (week_moves.category == "Airline") & (week_moves.country == "US")
                             & (week_moves.t >= BACKLOG.t.min() if len(BACKLOG) else True)]
    _wkq = _wkq.groupby(_wkq.t // 900 * 900).size().rename("n").reset_index().rename(columns={"t": "b"})
    _wkq["time_pt"] = to_pt(_wkq.b + 450)
    _wkq = _wkq[_wkq.b <= _b.b.max()] if len(_b) else _wkq
    _area = alt.Chart(_b).mark_area(opacity=0.9, interpolate="monotone").encode(
        x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")),
        y=alt.Y("n:Q", stack="zero", title="airline departures / 15 min"),
        color=alt.Color("kind:N", title=None, sort=BACKLOG_KINDS, legend=alt.Legend(orient="top"),
                        scale=alt.Scale(domain=BACKLOG_KINDS, range=["#e8590c", "#fab005", "#1c7ed6", "#868e96"])),
        order=alt.Order("kind_order:Q"),
        tooltip=["kind:N", alt.Tooltip("time_pt:T", format="%-I:%M %p"), "n:Q"]).transform_calculate(
        kind_order=f"indexof({BACKLOG_KINDS}, datum.kind)")
    _ref = alt.Chart(_wkq).mark_line(strokeDash=[1, 3], color="#9aa5b1", strokeWidth=1.6).encode(
        x="time_pt:T", y="n:Q", tooltip=[alt.Tooltip("n:Q", title="Nov. 6 departures")])
    backlog_chart = with_events(alt.layer(_area, _ref), lo=int(BACKLOG.t.min()) if len(BACKLOG) else None).properties(
        width="container", height=260, title=alt.Title(
            "The backlog left in a wave on top of a thin evening schedule",
            subtitle="Airline departures after the lift, by how each flight number compares with Nov. 6 (estimated) · dotted: all departures on Nov. 6"))
    backlog_chart
    return


@app.cell(hide_code=True)
def _(
    EST_MISSING,
    EVE_SEEN_PCT,
    FLOOR,
    NYT_LIVE,
    STOP_DELAY_H,
    STOP_FLEW,
    STOP_MISSING,
    STOP_N,
    T_END,
    fmt_pt,
    prose,
):
    _f = FLOOR
    prose(f'''
    ## What happened to the afternoon's flights

    The flight-tracking data has no airline schedules, so this section uses a normal Friday as a stand-in: a flight
    number that left at 2:10 p.m. on Nov. 6 is treated as scheduled for about 2:10 p.m. on Nov. 13, and then looked for
    on Nov. 13. It is an estimate. Schedules change from week to week, and some flights are missing from the data. On
    the normal morning of Nov. 13, before the stop, {_f["on time (±15 min)"]:.0f}% of flight numbers left within 15
    minutes of their Nov. 6 time and {_f["not seen departing"]:.0f}% were not seen at all. That is the noise floor for
    the numbers below.

    Of the **{STOP_N:,}** flights "scheduled" to leave lower-48 airports during the stop, **{STOP_FLEW:,}** left later, a median
    **{STOP_DELAY_H:.1f} hours** late. **{STOP_MISSING:,}** had not been seen departing by {fmt_pt(T_END)} Pacific.
    Allowing for the normal-morning noise floor, that suggests roughly **{EST_MISSING:,}** of them were cancelled or
    still waiting. For the whole day, Cirium counted more than 8,200 cancelled flights, over 31% of Friday's U.S.
    schedule ([The New York Times]({NYT_LIVE})). For the evening after the lift, only {EVE_SEEN_PCT}% of scheduled flight numbers had been seen
    departing by {fmt_pt(T_END)} Pacific.
    ''') if STOP_DELAY_H is not None else prose("## What happened to the afternoon's flights\\n\\nNot enough data yet.")
    return


@app.cell(hide_code=True)
def _(MATCH, STATUSES, T0, T_END, alt, pd, to_pt, with_events):
    _m = MATCH[(MATCH.sched_t >= T0 + 900) & (MATCH.sched_t <= T_END - 1800)]
    _s = (_m.assign(b=_m.sched_t // 1800 * 1800).groupby(["b", "status"]).size()
          .unstack(fill_value=0).reindex(columns=STATUSES, fill_value=0))
    _sh = _s.div(_s.sum(axis=1), axis=0) * 100
    _top = _sh.cumsum(axis=1)
    _rows = []
    for _b in _sh.index:
        for _st in STATUSES:
            _rows.append({"b": _b, "status": _st, "y0": _top.loc[_b, _st] - _sh.loc[_b, _st], "y1": _top.loc[_b, _st],
                          "share": _sh.loc[_b, _st], "n": int(_s.loc[_b, _st])})
    _r = pd.DataFrame(_rows)
    _r["x0"], _r["x1"] = to_pt(_r.b + 90), to_pt(_r.b + 1710)
    sched_chart = with_events(alt.Chart(_r).mark_rect().encode(
        x=alt.X("x0:T", title="scheduled departure (Nov. 6 time, Pacific)", axis=alt.Axis(format="%-I:%M")), x2="x1:T",
        y=alt.Y("y0:Q", title="% of scheduled flights", scale=alt.Scale(domain=[0, 100])), y2="y1:Q",
        color=alt.Color("status:N", title=None, sort=STATUSES, legend=alt.Legend(orient="top"),
                        scale=alt.Scale(domain=STATUSES, range=["#2f9e44", "#fab005", "#e8590c", "#868e96"])),
        tooltip=["status:N", alt.Tooltip("x0:T", format="%-I:%M %p", title="scheduled from"), "n:Q",
                 alt.Tooltip("share:Q", format=".0f", title="%")])).properties(width="container", height=240, title=alt.Title(
        "What happened to each scheduled departure (estimated)",
        subtitle="Airline flight numbers that left lower-48 airports at this time on Nov. 6, and what the same flight number did on Nov. 13"))
    sched_chart
    return


@app.cell(hide_code=True)
def _(COLLAPSE_T, LIFT_T, MATCH, T0, T_END, alt):
    _d = MATCH[(MATCH.sched_t >= (COLLAPSE_T or T0)) & (MATCH.sched_t < min(LIFT_T, T_END)) & (MATCH.actual_t >= (COLLAPSE_T or T0))]
    _d = _d.assign(h=(_d.delay_min / 60).clip(lower=0, upper=8.99))
    delay_chart = alt.Chart(_d).mark_bar(color="#e8590c").encode(
        x=alt.X("h:Q", bin=alt.Bin(step=0.5, extent=[0, 9]), title="hours late (8+ grouped)"),
        y=alt.Y("count():Q", title="flights"),
        tooltip=[alt.Tooltip("count():Q", title="flights")]).properties(width="container", height=200, title=alt.Title(
        "How late the afternoon's flights left",
        subtitle="Lower-48 flights normally departing during the stop that left after the collapse (estimated from Nov. 6 flight numbers)"))
    delay_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html('<div class="er-part"><div class="er-part-n">In context</div>'
            '<div class="er-part-t">How rare is this?</div>'
            '<div class="er-part-d">Nationwide ground stops, from 9/11 to today</div></div>')
    return


@app.cell(hide_code=True)
def _(prose):
    prose('''
    Nationwide ground stops are rare. By [Wikipedia's count](https://en.wikipedia.org/wiki/2026_US_ground_stop),
    Nov. 13 was only the third in U.S. history; some outlets counted it as the second since 9/11.

    | Date | What happened | What stopped | How long |
    |---|---|---|---|
    | Sept. 11, 2001 | Terrorist hijackings | All civil traffic: departures halted, and every aircraft in the air ordered to land | About two days; commercial flights resumed Sept. 13 |
    | Jan. 11, 2023 | Failure of the NOTAM system that publishes safety notices to pilots, after a contractor deleted files | Domestic departures | About 1.5 hours, until 9 a.m. Eastern |
    | **Nov. 13, 2026** | **Communications failure affecting the FAA's en-route control centers** | **Departures, with exceptions for Alaska, Hawaii and some international flights** | **About 4 hours 20 minutes, 3:54 to 8:15 p.m. Eastern** |

    The first was different in kind. After the hijackings on Sept. 11, 2001, controllers brought down every aircraft in
    the sky: 4,638 commercial and private planes were landed and accounted for within about three hours. The second, on
    Jan. 11, 2023, halted domestic departures for about an hour and a half while the FAA restored the NOTAM system.

    Friday's stop sat between the two. Like 2023, it halted departures and let flights already aloft finish their trips.
    But it lasted more than twice as long, and it was declared in the middle of a busy afternoon rather than early in
    the morning. Its cause, a communications failure affecting the en-route centers that handle aircraft at cruise
    altitude, was still under investigation.

    Smaller, airline-specific stops have become more common. Carriers asked the FAA to hold their own fleets after
    technology failures at United in September 2023, at American, Delta, United and Allegiant during the CrowdStrike
    outage of July 2024, at American on Christmas Eve 2024, and twice at Alaska Airlines in 2025.

    <small>Sources: [Wikipedia: 2026 US ground stop](https://en.wikipedia.org/wiki/2026_US_ground_stop) ·
    [Wikipedia: 2023 FAA system outage](https://en.wikipedia.org/wiki/2023_FAA_system_outage) ·
    [Every US nationwide ground stop, from 9/11 to today](https://brendonbeebe.substack.com/p/every-us-nationwide-ground-stop-from) ·
    [NPR on the 2023 outage](https://www.npr.org/2023/01/11/1148340708/faa-notam-ground-stop-flight-delay) ·
    [Snopes on "first since 9/11"](https://www.snopes.com/fact-check/faa-orders-flights-grounded-first-time-since-911/)</small>
    ''')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"How we did this": mo.Html(f"""<div class="er-method">
    <h3>Data</h3>
    <p>Positions come from <a href="https://adsb.lol">adsb.lol</a>, an open, unfiltered network of volunteer ADS-B receivers.
    It publishes a snapshot of every aircraft it hears every 10 seconds, in one file per half hour, usually 30 to 60 minutes after the half hour ends.
    This page downloads those files when it runs and keeps one position per aircraft per minute. Each position is assigned to
    the U.S., Canada or Mexico using <a href="https://github.com/topojson/world-atlas">Natural Earth borders</a>, extended
    about 100 km offshore. "Over the U.S." includes Alaska and Hawaii. The page compares Nov. 13 with the same clock hours
    on Nov. 12. Aircraft types come from the
    <a href="https://github.com/wiedehopf/tar1090-db">tar1090 aircraft database</a>.</p>
    <h3>Definitions</h3>
    <p><b>Takeoff:</b> an aircraft's track goes from on the ground to airborne, or a track first appears in the air below 2,500 feet.
    <b>Airline:</b> an airline-style callsign (three-letter operator code plus flight number) on a jet or turboprop, or any
    medium or heavy jet. This includes regional and cargo carriers. Piston aircraft are excluded even with an operator
    code: flight schools such as the University of North Dakota fly under such codes, and their top-of-the-hour training
    departures otherwise look like an airline spike.
    <b>Wide-body:</b> Boeing 747/767/777/787, Airbus A330/A340/A350/A380 or MD-11, the aircraft used on most long international
    routes. Some fly domestic routes too.
    <b>Wyoming:</b> the state's borders are lines of latitude and longitude, so a box is its exact outline.
    <b>Airport stop time:</b> an airport's last airline departure before 12:53 p.m. Pacific (the collapse plus 15 minutes),
    shown only for airports where at least six departures would normally have left between that time and 12:53. Takeoffs are assigned to the nearest airport with
    scheduled service within about 10 km (<a href="https://ourairports.com/data/">OurAirports</a>).
    <b>Aircraft on the ground:</b> positions reported as on the ground within about 4 km of an airport, every two minutes,
    compared with the same airport between 10 a.m. and 12:38 p.m. that day (receiver coverage at the ground differs a lot between days),
    smoothed with a 10-minute running median to remove brief bursts in the feed.
    Parked aircraft often switch transponders off, so this mostly counts aircraft taxiing or waiting.
    <b>Airspace:</b> simplified en-route center boundaries from the
    <a href="https://github.com/vatsimnetwork/vatspy-data-project">VATSpy data project</a>, for illustration only.
    <b>Cross-check:</b> an independent analysis posted during the stop, using
    <a href="https://opensky-network.org">OpenSky Network</a> and adsb.lol live data
    (<a href="https://x.com/jon_vs_moloch/status/2121395654354170192">post</a>), counted 1,083, 1,035 and 990 aircraft airborne
    at 6:36, 6:42 and 6:49 p.m. Eastern; this data gives 1,060, 1,016 and 980 over the U.S. at the same moments, and the same
    airport counts within a few aircraft. That post describes all en-route centers failing at once; this data shows
    Chicago going quiet about 20 minutes before the rest of the country, and Alaska and Hawaii continuing to fly.
    <b>Schedule estimate:</b> there is no airline schedule in ADS-B data, so each U.S. airline flight number's departure
    time on Nov. 6 (a normal Friday) stands in for its schedule. Each Nov. 6 departure is matched to the first departure of
    the same flight number on Nov. 13 between 90 minutes early and 12 hours late (Nov. 6's own delays make some flights
    look early). Fractional and charter operators without fixed schedules are left out. Flight numbers come from the callsign the
    aircraft was broadcasting at the time. The shares on the normal morning of Nov. 13 show how noisy this is.
    <b>Recovery time:</b> the first minute, from half an hour before the lift, after which airline takeoffs run at
    at least twice the ground-stop rate for 20 minutes straight.
    <b>Collapse time:</b> the first minute after 11 a.m. Pacific when airline takeoffs over the next three minutes average less
    than 40% of the preceding half hour's rate. The same test is applied to each region.
    <b>Into U.S. airspace:</b> a departure from Canada or Mexico whose aircraft appears over the U.S. within four hours. This
    also catches some Canadian domestic routes that cut across U.S. airspace. Coverage of Mexico is much thinner than of the U.S.
    and Canada.</p>
    <h3>Caveats</h3>
    <p>Receiver coverage is incomplete, especially at low altitudes and in remote areas, so absolute counts are undercounts. The
    comparisons (before vs after, Nov. 13 vs Nov. 12) are more reliable than the totals. The 2:54 p.m. Central
    ground-stop time is as reported by
    <a href="https://www.news9.com/oklahoma-city-news/faa-reportedly-issues-nationwide-ground-stop">News9</a>; other outlets give
    only "Friday afternoon", and we could not find an official FAA timeline.</p>
    <h3>Reporting</h3>
    <p><a href="https://www.cbsnews.com/news/faa-issues-nationwide-ground-stop/">CBS News</a> ·
    <a href="https://www.cnbc.com/2026/11/13/faa-ground-stop.html">CNBC</a> ·
    <a href="https://www.cnn.com/2026/11/13/us/live-news/flights-ground-stop-faa">CNN</a> ·
    <a href="https://www.news9.com/oklahoma-city-news/faa-reportedly-issues-nationwide-ground-stop">News9</a> ·
    <a href="https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa">The New York Times</a> ·
    <a href="https://globalnews.ca/news/12150274/faa-usa-ground-stop-order/">Global News</a> ·
    <a href="https://www.aljazeera.com/news/2026/11/13/us-grounds-all-flights-after-communication-issue">Al Jazeera</a> ·
    <a href="https://www.nbcwashington.com/news/national-international/faa-ground-stop-nationwide-us-airports/4182917/">NBC Washington</a> ·
    <a href="https://en.wikipedia.org/wiki/2026_US_ground_stop">Wikipedia</a> ·
    <a href="https://www.youtube.com/watch?v=XNzzfW6Ki2I">CNN (live coverage)</a> ·
    <a href="https://www.youtube.com/watch?v=VJ9BRW0LtOg">CNN (origin and stranded passengers)</a> ·
    <a href="https://x.com/jon_vs_moloch/status/2121395654354170192">parallel ADS-B analysis</a></p>
    </div>""")})
    return


@app.cell(hide_code=True)
def _(mo, prose):
    mo.vstack([mo.md("---"), prose("""
    *This report is a [marimo](https://marimo.io) notebook
    ([source](https://github.com/ktaletsk/261113-airplanes-grounded)). Every number and chart is computed from the data
    shown at the top of the page, from a fixed snapshot of the flight-tracking data.*
    """, cls="er-note")])
    return


@app.cell(hide_code=True)
def _(PT, dt):
    WINDOW_START = dt.datetime(2026, 11, 13, 18, 0, tzinfo=dt.timezone.utc)   # 10:00 PT on the ground-stop day
    LOAD_START = WINDOW_START - dt.timedelta(hours=2)    # 2 h of lead-in so early departures can be matched to flight numbers
    MAX_HOURS = 24                       # stop downloading this many hours after WINDOW_START
    BASELINE_SHIFT = 86400               # compare with the same clock time one day earlier
    SHIFTS = {"event": 0, "baseline": BASELINE_SHIFT, "week": 7 * 86400}   # "week" = Nov 6, a normal Friday
    WEEK_LABEL = "Nov 6 (a normal Friday)"
    WORKERS = 6                          # parallel downloads (be gentle with adsb.lol)
    PERIOD_LABEL = {"event": "Nov 13 (ground stop)", "baseline": "Nov 12 (day before)"}
    CATS = ["Airline", "Business jet", "General aviation", "Helicopter", "Other"]

    # FAA nationwide ground stop took effect 2:54 p.m. Central (News9). The departure collapse is detected from the data.
    GROUND_STOP = dt.datetime(2026, 11, 13, 12, 54)          # naive PT
    GROUND_STOP_T = int(GROUND_STOP.replace(tzinfo=PT).timestamp())
    # FAA lifted the stop at 8:15 p.m. Eastern (Al Jazeera, NBC); departures' restart is detected from the data
    LIFT = dt.datetime(2026, 11, 13, 17, 15)               # naive PT
    LIFT_T = int(LIFT.replace(tzinfo=PT).timestamp())
    HUBS = {  # major US airports (lat, lon) for the hub comparison
        "Atlanta (ATL)": (33.64, -84.43), "Dallas–Fort Worth area": (32.90, -97.04), "Denver (DEN)": (39.86, -104.67),
        "Chicago O'Hare (ORD)": (41.98, -87.90), "Los Angeles (LAX)": (33.94, -118.41), "Charlotte (CLT)": (35.21, -80.94),
        "Las Vegas (LAS)": (36.08, -115.15), "Phoenix (PHX)": (33.43, -112.01), "Orlando (MCO)": (28.43, -81.31),
        "Seattle (SEA)": (47.45, -122.31), "Houston (IAH)": (29.98, -95.34), "Newark (EWR)": (40.69, -74.17),
        "New York (JFK, LGA)": (40.64, -73.78), "San Francisco (SFO)": (37.62, -122.38), "Miami (MIA)": (25.79, -80.29),
        "Minneapolis (MSP)": (44.88, -93.22), "Detroit (DTW)": (42.21, -83.35), "Boston (BOS)": (42.36, -71.01),
        "Washington Dulles (IAD)": (38.95, -77.46), "Philadelphia (PHL)": (39.87, -75.24),
    }

    # The published notebook is static: it always opens the snapshot in public/bundle.npz.
    # Rebuild that snapshot with scripts/update_snapshot.sh (sets EMPTY_SKIES_EXPORT and runs the raw-data pipeline).
    return (
        BASELINE_SHIFT,
        CATS,
        GROUND_STOP,
        GROUND_STOP_T,
        HUBS,
        LIFT,
        LIFT_T,
        LOAD_START,
        MAX_HOURS,
        PERIOD_LABEL,
        SHIFTS,
        WINDOW_START,
        WORKERS,
    )


@app.cell(hide_code=True)
def _():
    import marimo as mo
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
    alt.data_transformers.disable_max_rows()


    @alt.theme.register("report", enable=True)
    def _report_theme():
        return alt.theme.ThemeConfig({"config": {
            "font": "Inter, -apple-system, Segoe UI, sans-serif",
            "view": {"stroke": None},
            "axis": {"labelFontSize": 11, "titleFontSize": 11, "titleFontWeight": 500, "gridOpacity": 0.35,
                     "domain": False, "tickColor": "#888", "labelColor": "#777", "titleColor": "#777"},
            "title": {"fontSize": 16, "fontWeight": 700, "anchor": "start", "subtitleFontSize": 12.5,
                      "subtitleColor": "#888", "offset": 12},
            "legend": {"orient": "top", "labelFontSize": 11.5, "title": None, "symbolStrokeWidth": 3},
        }})

    return (
        PT,
        Path,
        ThreadPoolExecutor,
        WASM,
        ZoneInfo,
        alt,
        anywidget,
        as_completed,
        dt,
        gzip,
        io,
        json,
        mo,
        np,
        os,
        pd,
        re,
        time,
        traitlets,
        urllib,
    )


@app.cell(hide_code=True)
def _(mo):
    def part(n, title, dek):
        return mo.Html(f'<div class="er-part"><div class="er-part-n">Part {n}</div>'
                       f'<div class="er-part-t">{title}</div><div class="er-part-d">{dek}</div></div>')

    return (part,)


@app.cell(hide_code=True)
def _(
    COUNTRY_GRID,
    PERIODS,
    PERIOD_LABEL,
    PRE,
    T0,
    T_END,
    country_of,
    movements,
    region_of,
    snap,
    to_pt,
):
    # airborne aircraft per (aligned) minute over the US, by period and category; takeoffs/landings
    if PRE is None:
        _air = snap[(snap.alt_ft >= 0) & (snap.country == "US")]
        counts_all = _air.groupby(["period", "category", "t"]).size().rename("n").reset_index()
        moves_full = movements(snap)
        moves_full["country"] = country_of(moves_full.lat.values, moves_full.lon.values, COUNTRY_GRID)
        moves_full["region"] = region_of(moves_full.country.values, moves_full.lat.values, moves_full.lon.values)
    else:                                   # snapshot: computed upstream from full 1-minute tracks
        counts_all, moves_full = PRE["counts"], PRE["moves"]
    _win = lambda d: d[(d.t >= T0) & (d.t <= T_END)].copy()
    week_counts = _win(counts_all[counts_all.period == "week"])
    counts = _win(counts_all[counts_all.period.isin(PERIODS)])
    counts["time_pt"] = to_pt(counts.t)
    total = counts.groupby(["period", "t", "time_pt"]).n.sum().reset_index()
    total["label"] = total.period.map(PERIOD_LABEL)
    week_total = week_counts.groupby("t").n.sum()

    # ignore the first and last 15 min, where tracks are cut by the window edges
    moves_all = moves_full[moves_full.period.isin(PERIODS)]
    week_moves = moves_full[(moves_full.period == "week") & (moves_full.t >= T0 + 900) & (moves_full.t <= T_END - 900)]
    moves = moves_all[(moves_all.t >= T0 + 900) & (moves_all.t <= T_END - 900)].copy()
    moves["bin"] = moves.t // 300 * 300
    moves["time_pt"] = to_pt(moves["bin"])
    return (
        counts,
        counts_all,
        moves,
        moves_all,
        moves_full,
        total,
        week_moves,
        week_total,
    )


@app.cell(hide_code=True)
def _(
    GROUND_STOP,
    GROUND_STOP_T,
    HUBS,
    LIFT,
    LIFT_T,
    PT,
    T0,
    T_END,
    counts,
    dt,
    find_collapse,
    fmt_pt,
    moves,
    np,
    pd,
    total,
):
    _tk = moves[(moves.kind == "takeoff") & (moves.country == "US")]
    _air_tk = _tk[_tk.category == "Airline"]
    _idx = np.arange(T0 + 900, T_END - 900 + 1, 60)


    def _per_min(df):
        return df.groupby(df.t // 60 * 60).size().reindex(_idx, fill_value=0)


    tk_event, tk_base = _per_min(_air_tk[_air_tk.period == "event"]), _per_min(_air_tk[_air_tk.period == "baseline"])
    COLLAPSE_T, BEFORE_RATE = find_collapse(tk_event, T0 + 3600)
    _after = tk_event[(tk_event.index >= (COLLAPSE_T or 0) + 120) & (tk_event.index < (COLLAPSE_T or 0) + 1800)]
    AFTER_RATE = float(_after.mean()) if COLLAPSE_T and len(_after) else None
    GAP_MIN = round((GROUND_STOP_T - COLLAPSE_T) / 60) if COLLAPSE_T else None

    # the same test, region by region (rough time-zone longitude bands)
    _zones = pd.cut(_air_tk.lon, [-180, -115, -102, -87, -60], labels=["West", "Mountain", "Central", "East"]).where(
        _air_tk.region == "Lower 48")
    _air_tk = _air_tk.assign(zone=_zones)
    ZONE_COLLAPSE = {}
    for _z in ["West", "Mountain", "Central", "East"]:
        _s = _per_min(_air_tk[(_air_tk.period == "event") & (_air_tk.zone == _z)])
        ZONE_COLLAPSE[_z] = find_collapse(_s, T0 + 3600, fwd=5)[0]

    # hub-by-hub departures in the 30 minutes before vs the 30 minutes after the collapse
    _hub_names = list(HUBS)
    _hl = np.array([HUBS[h] for h in _hub_names])
    _ev = _air_tk[_air_tk.period == "event"]
    _d = np.hypot(_ev.lat.values[:, None] - _hl[:, 0], (_ev.lon.values[:, None] - _hl[:, 1]) * np.cos(np.radians(_hl[:, 0])))
    _ev = _ev.assign(hub=np.where(_d.min(axis=1) < 0.3, np.array(_hub_names)[_d.argmin(axis=1)], None))
    if COLLAPSE_T:
        _b = _ev[(_ev.t >= COLLAPSE_T - 1800) & (_ev.t < COLLAPSE_T)].hub.value_counts()
        _a = _ev[(_ev.t >= COLLAPSE_T + 120) & (_ev.t < COLLAPSE_T + 1920)].hub.value_counts()
        hubs = pd.DataFrame({"before": _b, "after": _a}).reindex(_hub_names).fillna(0).astype(int)
        hubs = hubs.rename_axis("hub").reset_index().sort_values("before", ascending=False)
    else:
        hubs = pd.DataFrame(columns=["hub", "before", "after"])

    # the sky: airborne just before the collapse, and now
    _tot = total.set_index(["period", "t"]).n
    _ref_t = (COLLAPSE_T or T0) // 60 * 60
    AIR_BEFORE = int(_tot.get(("event", _ref_t), 0))
    TOT_EV, TOT_BS = _tot["event"], _tot["baseline"]
    _low = TOT_EV[TOT_EV.index >= (COLLAPSE_T or T0)]
    AIR_MIN_T, AIR_MIN = int(_low.idxmin()), int(_low.min())
    AIR_MIN_BASE = int(TOT_BS.asof(AIR_MIN_T))
    _lat = counts[counts.t == AIR_MIN_T].pivot_table(index="category", columns="period", values="n", observed=True)
    CAT_NOW = (100 * _lat["event"] / _lat["baseline"]).round().dropna().astype(int).to_dict() if "baseline" in _lat else {}

    EVENTS = pd.DataFrame(
        ([{"t": dt.datetime.fromtimestamp(COLLAPSE_T, PT).replace(tzinfo=None), "label": f"departures collapse {fmt_pt(COLLAPSE_T)} ",
           "color": "#f08c00", "align": "right", "hud": f"Departures collapsing ({fmt_pt(COLLAPSE_T)} PT)"}] if COLLAPSE_T else [])
        + [{"t": GROUND_STOP, "label": " FAA ground stop 12:54 p.m. PT", "color": "#e03131", "align": "left",
            "hud": "FAA nationwide ground stop in effect"}]
        + ([{"t": LIFT, "label": " stop lifted 5:15 p.m.", "color": "#2f9e44", "align": "left",
             "hud": "Ground stop lifted (5:15 p.m. PT)"}] if LIFT_T <= T_END else []))
    return (
        AFTER_RATE,
        AIR_BEFORE,
        AIR_MIN,
        AIR_MIN_BASE,
        AIR_MIN_T,
        BEFORE_RATE,
        CAT_NOW,
        COLLAPSE_T,
        EVENTS,
        GAP_MIN,
        TOT_BS,
        TOT_EV,
        ZONE_COLLAPSE,
        hubs,
        tk_base,
        tk_event,
    )


@app.cell(hide_code=True)
def _(COLLAPSE_T, LIFT_T, T0, T_END, moves, pd, snap):
    NYT_AK = "https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa/cb2ab5a3-dcca-5a17-adfc-cc78cd6f1f2f"
    NYT_LIVE = "https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa"
    GLOBAL_NEWS = "https://globalnews.ca/news/12150274/faa-usa-ground-stop-order/"
    _tk_all = moves[(moves.kind == "takeoff") & (moves.category == "Airline")]
    _c = COLLAPSE_T or T0


    def _rate(d, lo, hi):
        # departures per 30 minutes in [lo, hi)
        return len(d[(d.t >= lo) & (d.t < hi)]) / max(1e-9, (hi - lo) / 1800)


    def rate_stats(d, hi):
        ev, bs = d[d.period == "event"], d[d.period == "baseline"]
        out = {"before": _rate(ev, _c - 3600, _c), "after": _rate(ev, _c + 120, hi), "base_after": _rate(bs, _c + 120, hi)}
        out["pct"] = round(100 * out["after"] / out["base_after"]) if out["base_after"] else None
        return out


    STOP_END = min(T_END - 900, LIFT_T)                # compare the ground-stop window only
    REGION_STATS = {r: rate_stats(_tk_all[_tk_all.region == r], STOP_END) for r in ["Lower 48", "Alaska", "Hawaii"]}

    # Canada / Mexico: did the aircraft enter US airspace within 4 hours of takeoff?
    NB_END = min(T_END - 3600, LIFT_T)           # ground-stop window; leave time for departures to reach the border
    _nb = _tk_all[_tk_all.country.isin(["Canada", "Mexico"])]
    _us_pos = snap.loc[snap.country == "US", ["hex", "minute"]]
    _f = _nb[["hex", "minute"]].merge(_us_pos, on="hex", suffixes=("", "_us"))
    _f = _f[(_f.minute_us > _f.minute) & (_f.minute_us <= _f.minute + 4 * 3600)]
    nb_tk = _nb.assign(to_us=_nb.set_index(["hex", "minute"]).index.isin(pd.MultiIndex.from_frame(_f[["hex", "minute"]])))
    NEIGHBOR_STATS = {(c, u): rate_stats(nb_tk[(nb_tk.country == c) & (nb_tk.to_us == u)], NB_END)
                      for c in ["Canada", "Mexico"] for u in [True, False]}
    tk_all = _tk_all
    return (
        GLOBAL_NEWS,
        NB_END,
        NEIGHBOR_STATS,
        NYT_AK,
        NYT_LIVE,
        REGION_STATS,
        STOP_END,
        nb_tk,
        rate_stats,
        tk_all,
    )


@app.cell(hide_code=True)
def _(
    COLLAPSE_T,
    HUBS,
    PERIODS,
    STOP_END,
    T0,
    T_END,
    aircraft,
    np,
    pd,
    rate_stats,
    snap,
    tk_all,
):
    NYT_INTL = "https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa/1f19bdff-736c-5ab5-bceb-19df5ab3be0e"
    # Wyoming is a lat/lon rectangle, so a box is its exact border
    _wy = snap[(snap.alt_ft >= 0) & snap.lat.between(41.0, 45.0) & snap.lon.between(-111.056, -104.052)]
    _wn = _wy.groupby(["period", "t"]).size()
    _grid = {p: np.sort(snap.loc[snap.period == p, "t"].unique()) for p in PERIODS}
    wy_series = {p: (_wn[p] if p in _wn.index.get_level_values(0) else pd.Series(dtype=int)).reindex(_grid[p], fill_value=0)
                 for p in PERIODS}
    _ev = wy_series["event"]
    _after = _ev[_ev.index >= (COLLAPSE_T or T0)]
    WY_ZERO_T = int(_after.index[_after.values == 0][0]) if (_after.values == 0).any() else None
    WY_NOON = int(_ev.get(T0 + 7200, 0))
    WY_BASE_AT = int(wy_series["baseline"].asof(WY_ZERO_T)) if WY_ZERO_T else None
    WY_MIN = int(_after.min()) if len(_after) else None

    # long-haul (wide-body) airline departures from the lower 48
    _wide = r"^(B74|B77|B78|B76|A33|A34|A35|A38|MD11)"
    _types = aircraft.drop_duplicates("hex").set_index("hex")["type"]
    lh_tk = tk_all[(tk_all.region == "Lower 48") & tk_all.hex.map(_types).fillna("").astype(str).str.match(_wide)]
    LH_STATS = rate_stats(lh_tk, STOP_END)
    _c = COLLAPSE_T or T0
    _lh_ev = lh_tk[(lh_tk.period == "event") & (lh_tk.t >= _c)]
    _win = lambda d, lo, hi: int(((d.t >= lo) & (d.t < hi)).sum())
    LH_FIRST_HOUR = (_win(_lh_ev, _c, _c + 3600), _win(lh_tk[lh_tk.period == "baseline"], _c, _c + 3600))
    LH_LAST_HOUR = (_win(_lh_ev, T_END - 900 - 3600, T_END - 900),
                    _win(lh_tk[lh_tk.period == "baseline"], T_END - 900 - 3600, T_END - 900))
    LH_TOTAL = int(((_lh_ev.t >= _c + 120) & (_lh_ev.t <= T_END - 900)).sum())
    _bins = _lh_ev.assign(b=_lh_ev.t // 1800 * 1800).groupby("b").size()
    _bb = lh_tk[lh_tk.period == "baseline"].assign(b=lambda d: d.t // 1800 * 1800).groupby("b").size()
    _res = [b for b in _bins.index if b > _c and _bb.get(b, 0) >= 5 and _bins[b] >= 0.5 * _bb.get(b, 0)]
    LH_RESUME_T = int(_res[0]) if _res else None
    _hn = list(HUBS); _hl = np.array([HUBS[h] for h in _hn])
    _lp = _lh_ev[_lh_ev.t >= (LH_RESUME_T or _c)]
    _d = np.hypot(_lp.lat.values[:, None] - _hl[:, 0], (_lp.lon.values[:, None] - _hl[:, 1]) * np.cos(np.radians(_hl[:, 0])))
    _apt = pd.Series(np.where(_d.min(axis=1) < 0.3, np.array(_hn)[_d.argmin(axis=1)], None)).dropna()
    LH_AIRPORTS = [a.split(" (")[0] if "(" in a else a for a in _apt.value_counts().head(5).index]
    return (
        LH_AIRPORTS,
        LH_FIRST_HOUR,
        LH_LAST_HOUR,
        LH_RESUME_T,
        LH_STATS,
        LH_TOTAL,
        NYT_INTL,
        WY_BASE_AT,
        WY_MIN,
        WY_NOON,
        WY_ZERO_T,
        lh_tk,
        wy_series,
    )


@app.cell(hide_code=True)
def _(COLLAPSE_T, LIFT_T, T0, TOT_BS, TOT_EV, T_END, aircraft, moves, np, pd):
    LIFT_SRC = "https://www.aljazeera.com/news/2026/11/13/us-grounds-all-flights-after-communication-issue"
    # minute-by-minute US airline takeoffs, Nov. 13 and the day before
    _tk = moves[(moves.kind == "takeoff") & (moves.category == "Airline") & (moves.country == "US")]
    _idx = np.arange(T0 + 900, T_END - 900 + 1, 60)
    _pm = lambda d: d.groupby(d.t // 60 * 60).size().reindex(_idx, fill_value=0)
    rec_ev, rec_bs = _pm(_tk[_tk.period == "event"]), _pm(_tk[_tk.period == "baseline"])
    LIFTED = LIFT_T <= T_END
    _stop = rec_ev[(rec_ev.index >= (COLLAPSE_T or T0) + 900) & (rec_ev.index < min(LIFT_T, T_END))]
    STOP_RATE = float(_stop.mean()) if len(_stop) else None
    # recovery = first minute (from 30 min before the lift) after which departures run at >= 2x the ground-stop
    # rate for 20 minutes straight
    RECOVERY_T = None
    if STOP_RATE and LIFTED:
        _fwd = rec_ev.rolling(10).mean().shift(-9)
        for _t in rec_ev.index[rec_ev.index >= LIFT_T - 1800]:
            if _fwd.get(_t, np.nan) >= 2 * STOP_RATE and _fwd.get(_t + 600, np.nan) >= 2 * STOP_RATE:
                RECOVERY_T = int(_t)
                break
    LAG_MIN = round((RECOVERY_T - LIFT_T) / 60) if RECOVERY_T else None
    _w = lambda s: s[s.index >= _idx[-1] - 1799].sum()
    DEP_NOW = (_w(rec_ev) / 30, _w(rec_bs) / 30)
    DEP_NOW_PCT = round(100 * DEP_NOW[0] / DEP_NOW[1]) if DEP_NOW[1] else None
    AIR_NOW = int(TOT_EV.get(T_END, 0))
    AIR_NOW_PCT = round(100 * AIR_NOW / TOT_BS.get(T_END, np.nan)) if TOT_BS.get(T_END) else None

    # restart time by longitude band (same test, per region)
    _ztk = _tk[_tk.region == "Lower 48"]
    _zones = pd.cut(_ztk.lon, [-180, -115, -102, -87, -60], labels=["West", "Mountain", "Central", "East"])
    ZONE_RECOVERY = {}
    for _z in ["West", "Mountain", "Central", "East"]:
        _s = _pm(_ztk[(_ztk.period == "event") & (_zones == _z)])
        _sr = _s[(_s.index >= (COLLAPSE_T or T0) + 900) & (_s.index < min(LIFT_T, T_END))].mean()
        _thr = max(2 * _sr, 0.5)
        _f = _s.rolling(10).mean().shift(-9)
        ZONE_RECOVERY[_z] = next((int(_t) for _t in _s.index[_s.index >= LIFT_T - 1800]
                                  if _f.get(_t, np.nan) >= _thr and _f.get(_t + 600, np.nan) >= _thr), None) if LIFTED else None
    # wide-body share of the East's first 20 minutes of restarted departures
    _et = ZONE_RECOVERY.get("East")
    _types = aircraft.drop_duplicates("hex").set_index("hex")["type"]
    _first = _ztk[(_ztk.period == "event") & (_zones == "East") & (_ztk.t >= (_et or 0)) & (_ztk.t < (_et or 0) + 1200)] if _et else _ztk.iloc[:0]
    EAST_WB = (int(_first.hex.map(_types).fillna("").astype(str).str.match(r"^(B74|B77|B78|B76|A33|A34|A35|A38|MD11)").sum()), len(_first))
    return (
        AIR_NOW_PCT,
        DEP_NOW_PCT,
        EAST_WB,
        LAG_MIN,
        LIFTED,
        LIFT_SRC,
        RECOVERY_T,
        ZONE_RECOVERY,
        rec_bs,
        rec_ev,
    )


@app.cell(hide_code=True)
def _(COLLAPSE_T, LIFT_T, T0, T_END, moves_full, np, pd, week_moves):
    DAY3 = {"event": "Nov. 13", "baseline": "Nov. 12 (day before)", "week": "Nov. 6 (a normal Friday)"}
    _NOSCHED = r"^(EJA|LXJ|XOJ|JTL|FFL|TWY|PCM|SVW|EJM|JRE|VJA|GPD|PRD|CNS|KOW|NJE|EDG|WUP|XSR|JTZ)"   # fractional / charter
    _isair = lambda m: m[(m.kind == "takeoff") & (m.category == "Airline") & (m.country == "US")
                         & m.cs.astype(object).fillna("").astype(str).str.match(r"^[A-Z]{3}\d")
                         & ~m.cs.astype(object).fillna("").astype(str).str.match(_NOSCHED)]
    SCHED = _isair(week_moves[week_moves.region == "Lower 48"])[["cs", "t", "region"]].sort_values("t")
    _ev_full = moves_full[(moves_full.period == "event") & (moves_full.t <= T_END - 900)]   # includes the 2-hour lead-in
    ACT = _isair(_ev_full[_ev_full.region == "Lower 48"])[["cs", "t", "region"]].sort_values("t")
    _EARLY, _LATE = 90 * 60, 12 * 3600
    # match each Nov. 6 departure to the earliest free departure of the same flight number in [-90 min, +12 h];
    # a departure goes to the earliest schedule that claims it (vectorized greedy, converges in a few rounds)
    _S = SCHED[["cs", "t"]].rename(columns={"t": "sched_t"}).reset_index(drop=True)
    _A = ACT[["cs", "t"]].rename(columns={"t": "actual_t"}).reset_index(drop=True)
    _cand = _S.merge(_A, on="cs")
    _cand = _cand[(_cand.actual_t >= _cand.sched_t - _EARLY) & (_cand.actual_t <= _cand.sched_t + _LATE)].sort_values(
        ["cs", "sched_t", "actual_t"])
    _got = []
    while len(_cand):
        _first = _cand.drop_duplicates(["cs", "sched_t"]).drop_duplicates(["cs", "actual_t"])
        _got.append(_first)
        _ks = pd.MultiIndex.from_frame(_first[["cs", "sched_t"]]); _ka = pd.MultiIndex.from_frame(_first[["cs", "actual_t"]])
        _cand = _cand[~pd.MultiIndex.from_frame(_cand[["cs", "sched_t"]]).isin(_ks)
                      & ~pd.MultiIndex.from_frame(_cand[["cs", "actual_t"]]).isin(_ka)]
    _rows = _S.merge(pd.concat(_got) if _got else _S.iloc[:0].assign(actual_t=np.nan), on=["cs", "sched_t"], how="left")
    MATCH = _rows[["cs", "sched_t", "actual_t"]].copy()
    MATCH["delay_min"] = (MATCH.actual_t - MATCH.sched_t) / 60
    MATCH["status"] = np.select(
        [MATCH.actual_t.isna(), MATCH.delay_min <= 15, MATCH.delay_min <= 120],
        ["not seen departing", "on time (±15 min)", "delayed under 2 h"], "delayed 2 h or more")
    STATUSES = ["on time (±15 min)", "delayed under 2 h", "delayed 2 h or more", "not seen departing"]

    def _shares(d):
        return d.status.value_counts(normalize=True).reindex(STATUSES, fill_value=0) * 100

    _c = COLLAPSE_T or T0
    FLOOR = _shares(MATCH[(MATCH.sched_t >= T0 + 900) & (MATCH.sched_t < _c - 3600)])      # a normal morning
    _stop = MATCH[(MATCH.sched_t >= _c) & (MATCH.sched_t < min(LIFT_T, T_END)) & ~(MATCH.actual_t < _c)]
    _flew = _stop[_stop.actual_t.notna()]
    STOP_N, STOP_FLEW = len(_stop), len(_flew)
    STOP_DELAY_H = float(_flew.delay_min.median() / 60) if len(_flew) else None
    STOP_MISSING = int(_stop.actual_t.isna().sum())
    EST_MISSING = max(0, round(STOP_MISSING - FLOOR["not seen departing"] / 100 * STOP_N))

    # who flew after the lift: held backlog vs regular evening flights
    _after = ACT[ACT.t >= min(LIFT_T, T_END) - 1800][["cs", "t"]]
    _bk = _after.merge(MATCH.dropna(subset=["actual_t"]).drop_duplicates(["cs", "actual_t"]),
                       left_on=["cs", "t"], right_on=["cs", "actual_t"], how="left")
    BACKLOG = _after.assign(kind=np.select(
        [_bk.sched_t.isna().values, ((_bk.sched_t >= _c) & (_bk.sched_t < LIFT_T)).values, ((_bk.t - _bk.sched_t) <= 3600).values],
        ["no match on Nov. 6", "held from the stop", "roughly on schedule"], "delayed evening flight"))
    BACKLOG_KINDS = ["held from the stop", "delayed evening flight", "roughly on schedule", "no match on Nov. 6"]
    BACKLOG_PCT = round(100 * (BACKLOG.kind == "held from the stop").mean()) if len(BACKLOG) else None
    _q = BACKLOG.groupby(BACKLOG.t // 900 * 900).size()
    PEAK_T = int(_q.idxmax()) if len(_q) else None
    _eve = MATCH[(MATCH.sched_t >= LIFT_T) & (MATCH.sched_t <= T_END - 1800)]
    EVE_N = len(_eve)
    EVE_ONSCHED_PCT = round(100 * ((_eve.actual_t.notna()) & (_eve.delay_min <= 60)).mean()) if EVE_N else None
    EVE_SEEN_PCT = round(100 * _eve.actual_t.notna().mean()) if EVE_N else None
    return (
        BACKLOG,
        BACKLOG_KINDS,
        BACKLOG_PCT,
        DAY3,
        EST_MISSING,
        EVE_ONSCHED_PCT,
        EVE_SEEN_PCT,
        FLOOR,
        MATCH,
        PEAK_T,
        STATUSES,
        STOP_DELAY_H,
        STOP_FLEW,
        STOP_MISSING,
        STOP_N,
    )


@app.cell(hide_code=True)
def _(
    AIRPORTS,
    COLLAPSE_T,
    GROUND_STOP_T,
    LIFT_T,
    T0,
    T_END,
    aircraft,
    moves_all,
    nearest_airport,
    np,
    pd,
    snap,
):
    CNN_ORIGIN = "https://www.youtube.com/watch?v=VJ9BRW0LtOg"
    CNN_LIVE = "https://www.youtube.com/watch?v=XNzzfW6Ki2I"
    NYT_CANCEL = "https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa"
    _c = COLLAPSE_T or T0
    _W = r"^(B74|B77|B78|B76|A33|A34|A35|A38|MD11)"
    _types = aircraft.drop_duplicates("hex").set_index("hex")["type"]
    _atk = moves_all[(moves_all.kind == "takeoff") & (moves_all.category == "Airline") & (moves_all.region == "Lower 48")].copy()
    _atk["apt"] = nearest_airport(_atk.lat.values, _atk.lon.values, AIRPORTS)
    _atk["wide"] = (_atk.hex.map(_types).fillna("").astype(str).str.match(_W)
                    & ~_atk.cs.astype(object).fillna("").astype(str).str.match(r"^(FDX|UPS|ABX|ATN)"))   # domestic cargo networks
    APT_TK = _atk
    _ev, _bs = _atk[_atk.period == "event"], _atk[_atk.period == "baseline"]
    _names = AIRPORTS.drop_duplicates("code").set_index("code").name

    # 1) when departures stopped at each busy airport: its last airline departure before the collapse + 15 minutes,
    #    kept only where at least 6 departures would normally have left between then and collapse + 15 minutes
    _end = _c + 900
    _rows = []
    for _a, _g in _ev[_ev.apt.notna()].groupby("apt"):
        _b = _bs[_bs.apt == _a]
        _busy = int(((_b.t >= _c - 5400) & (_b.t < _c + 1800)).sum())        # 2 normal hours around the collapse
        _tt = _g.t.values[(_g.t.values >= _c - 3600) & (_g.t.values <= _end)]
        if _busy < 20 or not len(_tt):
            continue
        _stop = int(_tt.max())
        _exp = int(((_b.t > _stop) & (_b.t <= _end)).sum())
        _rows.append({"apt": _a, "stop": _stop, "per_hr": _busy / 2, "missed": _exp})
    APT_ALL = pd.DataFrame(_rows)
    APT_STOP = (APT_ALL[(APT_ALL.missed >= 6) | (APT_ALL.apt == "MDW")].sort_values("stop").reset_index(drop=True)
                if len(APT_ALL) else APT_ALL)                  # Midway kept: named by airline sources as the origin
    APT_STOP["vs_collapse"] = (APT_STOP.stop - _c) / 60
    APT_STOP = APT_STOP.merge(AIRPORTS.drop_duplicates("code")[["code", "lat", "lon"]], left_on="apt", right_on="code", how="left")
    FIRST_APT = APT_STOP.iloc[0].to_dict() if len(APT_STOP) else None
    APT_Q = (int(APT_STOP.stop.quantile(.25)), int(APT_STOP.stop.median()), int(APT_STOP.stop.quantile(.75))) if len(APT_STOP) else None
    _stop_of = APT_STOP.set_index("apt").stop
    ORD_STOP, MDW_STOP = _stop_of.get("ORD"), _stop_of.get("MDW")
    ORD_MISSED = int(APT_STOP.set_index("apt").missed.get("ORD", 0))
    MDW_RANK = (APT_STOP.apt.tolist().index("MDW") + 1) if "MDW" in APT_STOP.apt.values else None
    _busiest = APT_STOP.sort_values("per_hr", ascending=False).apt.head(10).tolist()
    GRID_APTS = APT_STOP[APT_STOP.apt.isin(set(_busiest) | {"ORD", "MDW"} | set(APT_STOP.apt.head(4)))].apt.tolist()

    # 3) long-haul gateways during the stop: coastal vs inland
    COASTAL = {"BOS", "JFK", "EWR", "LGA", "PHL", "IAD", "BWI", "MIA", "FLL", "SFO", "LAX", "SEA", "SAN", "OAK", "SJC", "PDX", "TPA", "MCO"}
    _lo_, _hi_ = _c + 600, min(LIFT_T, T_END)
    _wev = _ev[_ev.wide & (_ev.t >= _lo_) & (_ev.t < _hi_)]
    _wbs = _bs[_bs.wide & (_bs.t >= _lo_) & (_bs.t < _hi_)]
    GATEWAYS = pd.DataFrame({"nov13": _wev.groupby("apt").size(), "nov12": _wbs.groupby("apt").size()}).fillna(0).astype(int)
    GATEWAYS = GATEWAYS[GATEWAYS.nov12 >= 5].sort_values("nov12", ascending=False)
    GATEWAYS["first"] = _wev.groupby("apt").t.min().reindex(GATEWAYS.index)
    GATEWAYS["kind"] = np.where(GATEWAYS.index.isin(COASTAL), "coastal gateway", "inland hub")
    GATEWAYS = GATEWAYS.rename_axis("apt").reset_index()
    _gk = GATEWAYS.groupby("kind")[["nov13", "nov12"]].sum()
    GW_PCT = {k: round(100 * _gk.loc[k, "nov13"] / _gk.loc[k, "nov12"]) for k in _gk.index if _gk.loc[k, "nov12"]}

    # what kept the departure line off zero during the stop
    _stop_all = moves_all[(moves_all.kind == "takeoff") & (moves_all.category == "Airline") & (moves_all.country == "US")
                          & (moves_all.period == "event") & (moves_all.t >= _c + 900) & (moves_all.t < _hi_)]
    _wide_all = _stop_all.hex.map(_types).fillna("").astype(str).str.match(_W)
    TRICKLE = {"n": len(_stop_all),
               "akhi": round(100 * _stop_all.region.isin(["Alaska", "Hawaii"]).mean()) if len(_stop_all) else 0,
               "wide48": round(100 * (_wide_all & (_stop_all.region == "Lower 48")).mean()) if len(_stop_all) else 0}

    # example routes for the airspace map: coastal wide-bodies that left during the stop; inland ones from the day before
    def _track(per, hx, t0, hours=4):
        p = snap[(snap.period == per) & (snap.hex == hx) & (snap.t >= t0) & (snap.t <= t0 + hours * 3600)].sort_values("t")
        return p[["lon", "lat"]].values.tolist()
    _routes = []
    for _a in ["SFO", "LAX", "JFK", "BOS"]:
        for _, r in _wev[_wev.apt == _a].sort_values("t").head(1).iterrows():
            _routes.append({"apt": _a, "cs": r.cs, "kind": "left during the stop (coastal)", "path": _track("event", r.hex, r.t)})
    for _a in ["ORD", "DFW", "IAH", "DEN"]:
        for _, r in _wbs[(_wbs.apt == _a) & ~_wbs.hex.isin(_wev.hex)].sort_values("t").head(1).iterrows():
            _routes.append({"apt": _a, "cs": r.cs, "kind": "same hour on Nov. 12 (inland, held on Nov. 13)", "path": _track("baseline", r.hex, r.t)})
    ROUTES = [r for r in _routes if len(r["path"]) >= 5]

    # 4) tarmac: aircraft on the ground (transponder on) near airports
    _gp = snap[(snap.alt_ft < 0) & (snap.country == "US")]
    _gp = _gp.assign(apt=nearest_airport(_gp.lat.values, _gp.lon.values, AIRPORTS, maxd=0.04)).dropna(subset=["apt"])
    GROUND = (_gp.groupby(["period", "apt", "t"]).size().rename("n")
              .groupby(level=[0, 1], group_keys=False).apply(lambda x: x.rolling(5, center=True, min_periods=3).median()))
    _rows = []
    for _a in GROUND.loc["event"].index.get_level_values(0).unique():
        _e = GROUND.loc[("event", _a)]
        _b = GROUND.loc[("baseline", _a)] if ("baseline", _a) in GROUND.index else pd.Series(dtype=float)
        # baseline = the same airport on the morning of Nov. 13 (10 a.m. to the collapse): same receivers, normal operations
        _es, _bsn = _e[(_e.index >= GROUND_STOP_T) & (_e.index < _hi_)], _e[(_e.index >= T0) & (_e.index < _c)]
        if len(_es) and len(_bsn) and _bsn.mean() >= 5:
            _rows.append({"apt": _a, "peak": int(_es.max()), "peak_t": int(_es.idxmax()), "normal": float(_bsn.mean()),
                          "ratio": float(_es.mean() / _bsn.mean()), "peak_ratio": float(_es.max() / _bsn.mean())})
    TARMAC = pd.DataFrame(_rows).sort_values("ratio", ascending=False).reset_index(drop=True)
    _tm = TARMAC.set_index("apt")
    AUS_TARMAC = _tm.loc["AUS"].to_dict() if "AUS" in _tm.index else None
    return (
        APT_Q,
        APT_STOP,
        APT_TK,
        AUS_TARMAC,
        CNN_ORIGIN,
        FIRST_APT,
        GATEWAYS,
        GRID_APTS,
        GROUND,
        GW_PCT,
        MDW_STOP,
        ORD_MISSED,
        ORD_STOP,
        ROUTES,
        TARMAC,
        TRICKLE,
    )


@app.cell(hide_code=True)
def _(GROUND_STOP_T, LIFT_T, PERIODS, T_END, moves_all, snap):
    OSINT_POST = "https://x.com/jon_vs_moloch/status/2121395654354170192"
    _lo_, _hi_ = GROUND_STOP_T + 1800, min(LIFT_T, T_END)
    _bj = moves_all[(moves_all.kind == "takeoff") & (moves_all.category == "Business jet") & (moves_all.region == "Lower 48")]
    BJ_TK = {p: int(((_bj.period == p) & (_bj.t >= _lo_) & (_bj.t < _hi_)).sum()) for p in PERIODS}
    def _hi_share(cat, p):
        y = snap[(snap.period == p) & (snap.category == cat) & (snap.region == "Lower 48") & (snap.alt_ft > 0)
                 & (snap.t >= _lo_) & (snap.t < _hi_)]
        return round(100 * (y.alt_ft >= 18000).mean()) if len(y) else None
    BJ_HIGH = {p: _hi_share("Business jet", p) for p in PERIODS}
    GA_HIGH = {p: _hi_share("General aviation", p) for p in PERIODS}
    return BJ_HIGH, BJ_TK, GA_HIGH, OSINT_POST


@app.cell(hide_code=True)
def _(
    AIRPORTS,
    AIRSPACE,
    Path,
    T0,
    T_END,
    WASM,
    aircraft,
    counts_all,
    missing,
    moves_full,
    os,
    pack_bundle,
    snap,
    time,
):
    # GitHub Actions sets EMPTY_SKIES_EXPORT=public/bundle.npz to build the snapshot for the browser version
    EXPORT_TO = os.environ.get("EMPTY_SKIES_EXPORT", "")
    if EXPORT_TO and not WASM:
        _p = Path(EXPORT_TO)
        _p.parent.mkdir(parents=True, exist_ok=True)
        pack_bundle(_p, snap, aircraft, counts_all, moves_full,
                    {"T_END": T_END, "missing": missing, "built": int(time.time())}, t0=T0,
                    airports=AIRPORTS, airspace=AIRSPACE)
        print(f"wrote {_p} ({_p.stat().st_size / 1e6:.1f} MB)")
    return


@app.cell(hide_code=True)
def _(EVENTS, PT, alt, dt, pd):
    def with_events(chart, lo=None, hi=None):
        """Layer the EVENTS markers (dashed rule + label) on a chart whose x is time_pt; lo/hi (unix) limit which show."""
        layers = [chart]
        _lo = dt.datetime.fromtimestamp(lo, PT).replace(tzinfo=None) if lo else None
        _hi = dt.datetime.fromtimestamp(hi, PT).replace(tzinfo=None) if hi else None
        for e in EVENTS.to_dict("records"):
            if (_lo and e["t"] < _lo) or (_hi and e["t"] > _hi):
                continue
            _d = pd.DataFrame([e])
            layers.append(alt.Chart(_d).mark_rule(color=e["color"], strokeWidth=1.5, strokeDash=[5, 3]).encode(x="t:T"))
            layers.append(alt.Chart(_d).mark_text(color=e["color"], align=e["align"], baseline="top", fontSize=11, fontWeight="bold")
                          .encode(x="t:T", y=alt.value(4), text="label:N"))
        return alt.layer(*layers)

    return (with_events,)


@app.cell(hide_code=True)
def _(
    AIR_MIN_T,
    BASELINE_SHIFT,
    CATS,
    EVENTS,
    FLIGHTMAP_CSS,
    FLIGHTMAP_JS,
    MAP_STEP,
    PT,
    T0,
    T_END,
    aircraft,
    anywidget,
    np,
    snap,
    traitlets,
):
    class FlightMap(anywidget.AnyWidget):
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
        _all = snap[(snap.period == period) & (snap.t >= T0) & (snap.t <= T_END)]
        s = _all[_all.category.isin(cats)]
        by_min = {m: g for m, g in s.groupby("minute")}
        mins = sorted(_all.minute.unique())          # slider range from all data, so an empty selection still shows the map
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
        _start = AIR_MIN_T - (BASELINE_SHIFT if period == "baseline" else 0)
        w.minute = int(min(mins, key=lambda m: abs(m - _start)))
        send()
        return w

    return (make_flightmap,)


@app.cell(hide_code=True)
def _(CATS, PT, SHIFTS, dt, gzip, io, json, mo, np, pd, re, time, urllib):
    # ---- adsb.lol readsb heatmap decoding -------------------------------------------------------------
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
        calls = pd.DataFrame({"t": slice_t[sid[is_cs]], "hex": hexv[is_cs],
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
        pos = pos.sort_values("t").drop_duplicates(["hex", "minute"], keep="last")
        calls = calls[calls.callsign != ""].sort_values("t")
        # flight number at that moment: nearest callsign broadcast by the same aircraft (aircraft fly several legs a day)
        pos = pd.merge_asof(pos, calls.rename(columns={"callsign": "cs"}), on="t", by="hex",
                            direction="nearest", tolerance=900).drop(columns="t")
        return pos, calls.drop(columns="t").drop_duplicates("hex", keep="last")


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
        # airline-style callsign on a jet or turboprop (flight schools fly pistons under operator codes)
        cat[cs.str.match(AIRLINE_CS) & ~cs.str.match(bizjet_ops) & ~d.str[0].eq("H") & ~d.str[2].eq("P")] = "Airline"
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
            out.append(df.loc[m, ["minute", "t", "period", "hex", "category", "lat", "lon", "cs"]].assign(kind=kind))
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
    ALL_PERIODS = ["event", "baseline", "week"]
    COUNTRIES, REGIONS = ["US", "Canada", "Mexico"], ["Lower 48", "Alaska", "Hawaii", "Canada", "Mexico"]


    def _codes(values, cats):
        return pd.Categorical(pd.Series(values).astype(str), categories=cats).codes.astype(np.int8)


    def pack_bundle(path, snap, aircraft, counts, moves_all, meta, steps=None, t0=None, airports=None, airspace=None):
        """Compact snapshot for the browser build. Map positions are kept every steps[period] minutes,
        quantized (~100-200 m) and delta-encoded along each aircraft's track; the per-minute counts and
        takeoff/landing events (which need full 1-minute tracks) are shipped precomputed."""
        steps = steps or {"event": 2, "baseline": 4}
        keep = np.zeros(len(snap), dtype=bool)
        _t0 = t0 if t0 is not None else -np.inf
        for per, st in steps.items():
            keep |= (snap.period.values == per) & (snap.minute.values % (60 * st) == 0) & (snap.t.values >= _t0)
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
            "c_period": _codes(counts.period, ALL_PERIODS), "c_cat": _codes(counts.category, CATS),
            "c_t": (counts.t // 60).astype(np.int32), "c_n": counts.n.astype(np.int32),
            "m_period": _codes(m.period, ALL_PERIODS), "m_min": (m.minute // 60).astype(np.int32), "m_hex": m.hex.astype(np.int32),
            "m_cat": _codes(m.category, CATS), "m_lat": m.lat.astype(np.float32), "m_lon": m.lon.astype(np.float32),
            "m_kind": _codes(m.kind, KINDS), "m_country": _codes(m.country, COUNTRIES), "m_region": _codes(m.region, REGIONS),
            "m_csv": np.asarray(_csv := sorted(set(m.cs.dropna().astype(str))), dtype="U8"),
            "m_cs": pd.Categorical(m.cs.astype(object), categories=_csv).codes.astype(np.int32),
            "meta": np.frombuffer(json.dumps({**meta, "map_step": steps, "airspace": airspace or []}).encode(), dtype=np.uint8),
            "ap_code": np.asarray(airports.code.tolist() if airports is not None else [], dtype="U4"),
            "ap_name": np.asarray(airports.name.str[:60].tolist() if airports is not None else [], dtype="U60"),
            "ap_lat": np.asarray(airports.lat if airports is not None else [], dtype=np.float32),
            "ap_lon": np.asarray(airports.lon if airports is not None else [], dtype=np.float32),
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
        snap["t"] = snap.minute + snap.period.map(SHIFTS).astype(np.int64)
        aircraft = pd.DataFrame({"hex": z["a_hex"], "callsign": z["a_cs"].astype(object), "type": z["a_type"].astype(object),
                                 "category": pick(z["a_cat"], CATS)})
        counts = pd.DataFrame({"period": pick(z["c_period"], ALL_PERIODS), "category": pick(z["c_cat"], CATS),
                               "t": z["c_t"].astype(np.int64) * 60, "n": z["c_n"]})
        m_period = pick(z["m_period"], ALL_PERIODS)
        m_minute = z["m_min"].astype(np.int64) * 60
        moves_all = pd.DataFrame({
            "minute": m_minute, "t": m_minute + pd.Series(m_period).map(SHIFTS).values.astype(np.int64), "period": m_period,
            "hex": z["m_hex"], "category": pick(z["m_cat"], CATS), "lat": z["m_lat"], "lon": z["m_lon"],
            "kind": pick(z["m_kind"], KINDS), "country": pick(z["m_country"], COUNTRIES), "region": pick(z["m_region"], REGIONS),
            "cs": np.where(z["m_cs"] >= 0, np.append(z["m_csv"], "").astype(object)[z["m_cs"]], None),
        })
        airports = pd.DataFrame({"code": z["ap_code"].astype(str), "name": z["ap_name"].astype(str),
                                 "lat": z["ap_lat"], "lon": z["ap_lon"]}) if "ap_code" in z.files else pd.DataFrame(
            columns=["code", "name", "lat", "lon"])
        return snap, aircraft, {"counts": counts, "moves": moves_all, "airports": airports}, meta


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


    AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    AIRSPACE_URL = "https://raw.githubusercontent.com/vatsimnetwork/vatspy-data-project/master/Boundaries.geojson"


    @mo.persistent_cache
    def load_airports():
        """US airports with scheduled service (OurAirports): IATA code, name, position."""
        a = pd.read_csv(io.BytesIO(local_or_fetch("airports.csv", AIRPORTS_URL)), low_memory=False,
                        usecols=["type", "name", "latitude_deg", "longitude_deg", "iso_country", "scheduled_service", "iata_code"])
        a = a[(a.iso_country == "US") & a.type.isin(["large_airport", "medium_airport"])
              & (a.scheduled_service == "yes") & a.iata_code.notna()]
        return pd.DataFrame({"code": a.iata_code.values.astype(str), "name": a.name.values.astype(str),
                             "lat": a.latitude_deg.values.astype(np.float32), "lon": a.longitude_deg.values.astype(np.float32)})


    @mo.persistent_cache
    def load_airspace():
        """Simplified boundaries of the lower-48 en-route centers (ARTCCs) from the VATSpy data project, as GeoJSON features."""
        d = json.loads(local_or_fetch("airspace.geojson", AIRSPACE_URL))
        feats = []
        for f in d["features"]:
            i, oce = str(f["properties"].get("id", "")), str(f["properties"].get("oceanic")) == "1"
            if not i.startswith("KZ") or "-" in i or oce or i == "KZAK":
                continue
            polys = f["geometry"]["coordinates"] if f["geometry"]["type"] == "MultiPolygon" else [f["geometry"]["coordinates"]]
            out = []
            for poly in polys:
                rings = []
                for k, ring in enumerate(poly):
                    r = [[round(x, 2), round(y, 2)] for x, y in ring[::max(1, len(ring) // 300)]]
                    if r[0] != r[-1]:
                        r.append(r[0])
                    if len(r) < 4:
                        continue
                    area = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(r, r[1:]))
                    if (k == 0 and area > 0) or (k > 0 and area < 0):     # d3 wants clockwise exteriors
                        r = r[::-1]
                    rings.append(r)
                if rings:
                    out.append(rings)
            feats.append({"type": "Feature", "properties": {"id": i[1:], "lon": f["properties"].get("label_lon"),
                                                             "lat": f["properties"].get("label_lat")},
                          "geometry": {"type": "MultiPolygon", "coordinates": out}})
        return feats


    def nearest_airport(lat, lon, airports, maxd=0.09):
        """IATA code of the nearest airport within maxd degrees (None otherwise)."""
        la, lo = airports.lat.values.astype(float), airports.lon.values.astype(float)
        lat, lon = np.asarray(lat, float), np.asarray(lon, float)
        out = np.full(len(lat), None, dtype=object)
        for i in range(0, len(lat), 20000):
            d = np.hypot(lat[i:i + 20000, None] - la, (lon[i:i + 20000, None] - lo) * np.cos(np.radians(la)))
            j = d.argmin(1)
            ok = d[np.arange(len(j)), j] < maxd
            out[i:i + 20000][ok] = airports.code.values[j[ok]]
        return out


    def to_pt(unix):
        """unix seconds -> naive Pacific datetimes (what the charts use)."""
        return pd.to_datetime(unix, unit="s", utc=True).dt.tz_convert(PT).dt.tz_localize(None)


    def fmt_pt(unix):
        """unix seconds -> '12:38 p.m.' (Pacific)."""
        d = dt.datetime.fromtimestamp(int(unix), PT)
        return f"{d:%-I:%M} {'a.m.' if d.hour < 12 else 'p.m.'}"


    def find_collapse(s, search_from, pre=30 * 60, fwd=3, frac=0.4):
        """First minute t >= search_from where the mean of the next `fwd` minutes falls below `frac` x the mean
        of the preceding `pre` seconds. s: per-minute counts indexed by unix minute. Returns (t, pre_rate) or (None, None)."""
        v, idx = s.values.astype(float), s.index.values
        for i in np.nonzero(idx >= search_from)[0]:
            if i + fwd > len(v):
                break
            prev = v[(idx >= idx[i] - pre) & (idx < idx[i])]
            if len(prev) >= pre // 60 * 0.8 and prev.mean() > 0 and v[i:i + fwd].mean() < frac * prev.mean():
                return int(idx[i]), float(prev.mean())
        return None, None

    return (
        ALL_PERIODS,
        BUNDLE_URL,
        Blocked,
        NotPublished,
        PERIODS,
        add_heading,
        categorize,
        country_grid,
        country_of,
        find_collapse,
        fmt_pt,
        load_airports,
        load_airspace,
        load_bundle,
        load_slot,
        load_type_db,
        movements,
        nearest_airport,
        pack_bundle,
        read_bundle,
        region_of,
        to_pt,
    )


@app.cell(hide_code=True)
def _():
    # Front end of the FlightMap widget (anywidget ESM + CSS), embedded so the notebook is a single file.
    FLIGHTMAP_JS = r'''// Flightradar-style canvas map for anywidget. Python owns the data; JS owns view, slider and playback.
    const TILE = 256;
    const TILE_URL = (z, x, y) => `https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/${z}/${y}/${x}`;
    const STATES_URL = "https://cdn.jsdelivr.net/npm/us-atlas@3.0.1/states-10m.json";
    const TOPO_URL = "https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/+esm";
    // one silhouette per category (index matches CATS: Airline, Business jet, General aviation, Helicopter, Other)
    const GLYPH_D = [
      "M0,-9 L1.4,-5 L1.4,-1.5 L8,2.5 L8,4 L1.4,2 L1,6 L3.5,8 L3.5,9 L0,8 L-3.5,9 L-3.5,8 L-1,6 L-1.4,2 L-8,4 L-8,2.5 L-1.4,-1.5 L-1.4,-5 Z",
      "M0,-8 L0.7,-5 L0.7,0 L5.5,3.5 L5.5,4.5 L0.7,2.6 L0.7,5 L3,6.6 L3,7.6 L0,7 L-3,7.6 L-3,6.6 L-0.7,5 L-0.7,2.6 L-5.5,4.5 L-5.5,3.5 L-0.7,0 L-0.7,-5 Z",
      "M0,-7 L0.8,-6 L0.8,-3.2 L7.5,-2.8 L7.5,-1.2 L0.8,-0.9 L0.6,4 L3,5 L3,6.2 L0,5.7 L-3,6.2 L-3,5 L-0.6,4 L-0.8,-0.9 L-7.5,-1.2 L-7.5,-2.8 L-0.8,-3.2 L-0.8,-6 Z",
      "M0,-3.2 C1.6,-3.2 2,-1.5 2,0 C2,1.6 1.2,2.6 0.5,2.8 L0.4,7 L1.8,7.3 L1.8,8 L-1.8,8 L-1.8,7.3 L-0.4,7 L-0.5,2.8 C-1.2,2.6 -2,1.6 -2,0 C-2,-1.5 -1.6,-3.2 0,-3.2 Z",
      "M0,-4.5 L3.2,0 L0,4.5 L-3.2,0 Z",
    ];
    const GLYPHS = GLYPH_D.map((d) => new Path2D(d));
    const GLYPH_SCALE = [1, 0.85, 0.8, 0.95, 0.9];
    const ROTOR = new Path2D("M0,0 m-6,0 a6,6 0 1,0 12,0 a6,6 0 1,0 -12,0");
    const glyphSvg = (k) => `<svg width="18" height="18" viewBox="-10 -10 20 20" style="vertical-align:-4px;margin-right:6px">` +
      (k === 3 ? `<path d="M0,0 m-6,0 a6,6 0 1,0 12,0 a6,6 0 1,0 -12,0" fill="none" stroke="currentColor" stroke-width="1.2"/>` : "") +
      `<path d="${GLYPH_D[k]}" fill="currentColor"/></svg>`;
    const fmtPT = new Intl.DateTimeFormat("en-US", { timeZone: "America/Los_Angeles", hour: "2-digit", minute: "2-digit", hour12: false });
    const fmtUTC = new Intl.DateTimeFormat("en-US", { timeZone: "UTC", hour: "2-digit", minute: "2-digit", hour12: false });
    const fmtDay = new Intl.DateTimeFormat("en-US", { timeZone: "America/Los_Angeles", weekday: "short", month: "short", day: "numeric" });

    // altitude -> color (ground grey, low green, mid yellow, cruise orange-red)
    function altColor(a) {
      if (a < 0) return "#7a8794";
      const stops = [[0, [80, 220, 120]], [10000, [180, 230, 60]], [25000, [255, 216, 74]], [40000, [255, 120, 60]]];
      for (let i = 1; i < stops.length; i++) {
        if (a <= stops[i][0]) {
          const [a0, c0] = stops[i - 1], [a1, c1] = stops[i], t = (a - a0) / (a1 - a0);
          return `rgb(${c0.map((v, k) => Math.round(v + t * (c1[k] - v))).join(",")})`;
        }
      }
      return "rgb(255,120,60)";
    }
    const lon2x = (lon, z) => ((lon + 180) / 360) * TILE * 2 ** z;
    const lat2y = (lat, z) => {
      const s = Math.sin((lat * Math.PI) / 180);
      return (0.5 - Math.log((1 + s) / (1 - s)) / (4 * Math.PI)) * TILE * 2 ** z;
    };
    const x2lon = (x, z) => (x / (TILE * 2 ** z)) * 360 - 180;
    const y2lat = (y, z) => {
      const n = Math.PI - (2 * Math.PI * y) / (TILE * 2 ** z);
      return (180 / Math.PI) * Math.atan(Math.sinh(n));
    };

    function render({ model, el }) {
      el.innerHTML = `
        <div class="fm-root">
          <canvas class="fm-map"></canvas>
          <div class="fm-hud"><div class="fm-day"></div><div class="fm-clock">--:--</div><div class="fm-utc"></div>
            <div class="fm-count"></div><div class="fm-sub"></div><div class="fm-event"></div></div>
          <div class="fm-legend">
            <div><span class="sw" style="background:#7a8794"></span>on ground</div>
            <div><span class="sw" style="background:rgb(80,220,120)"></span>&lt; 10,000 ft</div>
            <div><span class="sw" style="background:rgb(255,216,74)"></span>~25,000 ft</div>
            <div><span class="sw" style="background:rgb(255,120,60)"></span>40,000 ft +</div>
            <div style="opacity:.75"><span class="sw" style="background:rgb(255,216,74);opacity:.35"></span>faded: Canada, Mexico</div>
            <div class="fm-glyphs"></div>
            <div style="opacity:.6;margin-top:4px;font-size:10px">Basemap © Esri · states: US Census</div>
          </div>
          <canvas class="fm-spark"></canvas>
          <div class="fm-tip"></div>
          <div class="fm-bar">
            <button class="fm-play" title="play / pause">▶</button>
            <button class="fm-ghost fm-back" title="−10 min">−10</button>
            <input type="range" class="fm-slider">
            <button class="fm-ghost fm-fwd" title="+10 min">+10</button>
            <select class="fm-speed" title="minutes per step">
              <option value="1">1 min/step</option><option value="2" selected>2 min/step</option>
              <option value="5">5 min/step</option><option value="10">10 min/step</option></select>
          </div>
        </div>`;
      const root = el.querySelector(".fm-root");
      const cv = el.querySelector(".fm-map"), ctx = cv.getContext("2d");
      const spark = el.querySelector(".fm-spark"), sctx = spark.getContext("2d");
      const tip = el.querySelector(".fm-tip"), slider = el.querySelector(".fm-slider");
      const playBtn = el.querySelector(".fm-play"), speedSel = el.querySelector(".fm-speed");
      const $ = (s) => el.querySelector(s);

      // view state: center in lon/lat + fractional zoom
      let view = { lon: -96.5, lat: 38.5, z: 4 }, W = 0, H = 0, dpr = 1, fitted = false;
      const tiles = new Map();
      let states = null; // array of rings [[lon,lat],...]
      (async () => {
        try {
          const topo = await import(TOPO_URL);
          const us = await (await fetch(STATES_URL)).json();
          const g = topo.mesh(us, us.objects.states);
          states = g.coordinates; dirty = true;
        } catch (e) { console.warn("state outlines unavailable", e); }
      })();
      let frame = model.get("frame"), aircraft = model.get("aircraft"), pts = [];
      let playing = false, lastReq = 0, dirty = true;

      function resize() {
        const r = root.getBoundingClientRect();
        dpr = window.devicePixelRatio || 1; W = r.width; H = r.height;
        cv.width = W * dpr; cv.height = H * dpr;
        spark.width = spark.clientWidth * dpr; spark.height = spark.clientHeight * dpr;
        if (!fitted && W > 0) { // fit CONUS
          view.z = Math.max(2, Math.min(7, Math.log2((W / TILE) * (360 / 62))));
          fitted = true;
        }
        dirty = true;
      }
      new ResizeObserver(resize).observe(root);

      function getTile(z, x, y) {
        const n = 2 ** z; x = ((x % n) + n) % n;
        if (y < 0 || y >= n) return null;
        const k = `${z}/${x}/${y}`;
        let t = tiles.get(k);
        if (!t) {
          t = new Image(); t.onload = () => (dirty = true); t.src = TILE_URL(z, x, y);
          tiles.set(k, t);
          if (tiles.size > 600) tiles.delete(tiles.keys().next().value);
        }
        return t.complete && t.naturalWidth ? t : null;
      }

      function draw() {
        if (!W) return;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.fillStyle = "#1b1d21"; ctx.fillRect(0, 0, W, H);
        const zi = Math.max(0, Math.min(18, Math.round(view.z))), sc = 2 ** (view.z - zi);
        const cx = lon2x(view.lon, zi), cy = lat2y(view.lat, zi);
        const x0 = cx - W / 2 / sc, y0 = cy - H / 2 / sc;
        for (let tx = Math.floor(x0 / TILE); tx <= Math.floor((x0 + W / sc) / TILE); tx++)
          for (let ty = Math.floor(y0 / TILE); ty <= Math.floor((y0 + H / sc) / TILE); ty++) {
            const t = getTile(zi, tx, ty);
            if (t) ctx.drawImage(t, (tx * TILE - x0) * sc, (ty * TILE - y0) * sc, TILE * sc + 0.5, TILE * sc + 0.5);
          }
        if (states) {
          const Z = view.z, X0 = lon2x(view.lon, Z) - W / 2, Y0 = lat2y(view.lat, Z) - H / 2;
          ctx.beginPath();
          for (const line of states) line.forEach(([lo, la], k) => {
            const x = lon2x(lo, Z) - X0, y = lat2y(la, Z) - Y0; k ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
          ctx.strokeStyle = "rgba(170,185,200,.35)"; ctx.lineWidth = 0.8; ctx.stroke();
        }
        // aircraft
        pts = [];
        const f = frame;
        if (f && f.n) {
          const s = Math.max(0.42, Math.min(1.3, 0.5 + (view.z - 4.5) * 0.2));
          const Z = view.z, X0 = lon2x(view.lon, Z) - W / 2, Y0 = lat2y(view.lat, Z) - H / 2;
          // ground first, then airborne sorted low->high so cruise traffic sits on top
          const order = [...f.alt.keys()].sort((a, b) => f.alt[a] - f.alt[b]);
          for (const i of order) {
            const x = lon2x(f.lon[i], Z) - X0, y = lat2y(f.lat[i], Z) - Y0;
            if (x < -10 || y < -10 || x > W + 10 || y > H + 10) continue;
            pts.push([x, y, i]);
            ctx.save(); ctx.translate(x, y); ctx.rotate((f.hdg[i] * Math.PI) / 180);
            const ground = f.alt[i] < 0;
            const info = aircraft[f.hex[i]], k = info ? info[2] : 4;
            const gs = (ground ? s * 0.6 : s) * GLYPH_SCALE[k];
            ctx.scale(gs, gs);
            ctx.globalAlpha = f.us && !f.us[i] ? 0.35 : 1;
            const col = altColor(f.alt[i]);
            if (k === 3) { ctx.strokeStyle = col; ctx.lineWidth = 1.1 / gs * s; ctx.stroke(ROTOR); }
            ctx.fillStyle = col; ctx.fill(GLYPHS[k]);
            ctx.restore();
          }
        }
        ctx.globalAlpha = 1;
        drawSpark();
      }

      function drawSpark() {
        const ser = model.get("series"), [b0, b1] = model.get("bounds");
        const w = spark.width, h = spark.height;
        sctx.clearRect(0, 0, w, h);
        if (!ser || ser.length < 2) return;
        const mx = Math.max(...ser.map((d) => d[1]));
        const X = (t) => ((t - b0) / Math.max(1, b1 - b0)) * w, Y = (v) => h - (v / mx) * (h - 4 * dpr);
        sctx.beginPath(); sctx.moveTo(X(ser[0][0]), h);
        for (const [t, v] of ser) sctx.lineTo(X(t), Y(v));
        sctx.lineTo(X(ser[ser.length - 1][0]), h); sctx.closePath();
        sctx.fillStyle = "rgba(255,216,74,.18)"; sctx.fill();
        sctx.beginPath(); ser.forEach(([t, v], k) => (k ? sctx.lineTo(X(t), Y(v)) : sctx.moveTo(X(t), Y(v))));
        sctx.strokeStyle = "rgba(255,216,74,.85)"; sctx.lineWidth = 1.5 * dpr; sctx.stroke();
        sctx.font = `${10 * dpr}px ui-sans-serif, sans-serif`; sctx.textBaseline = "top";
        for (const [t, label, color] of model.get("events")) {
          if (t < b0 || t > b1) continue;
          sctx.fillStyle = color; sctx.fillRect(X(t) - dpr, 0, 2 * dpr, h);
        }
        const m = model.get("minute");
        sctx.fillStyle = "#fff"; sctx.fillRect(X(m) - dpr, 0, 2 * dpr, h);
      }

      function loop() { if (dirty) { dirty = false; draw(); } requestAnimationFrame(loop); }
      requestAnimationFrame(loop);

      function setBounds() {
        const [b0, b1, st] = model.get("bounds");
        slider.min = b0; slider.max = b1; slider.step = st; slider.value = model.get("minute");
        dirty = true;
      }
      function hud() {
        const m = model.get("minute"), d = new Date(m * 1000), f = frame || {};
        $(".fm-day").textContent = fmtDay.format(d);
        $(".fm-clock").textContent = fmtPT.format(d) + " PT";
        $(".fm-utc").textContent = fmtUTC.format(d) + " UTC";
        let nAir = 0, nGround = 0;
        if (f.alt) f.alt.forEach((a, i) => { if (!f.us || f.us[i]) { if (a >= 0) nAir++; else nGround++; } });
        $(".fm-count").textContent = `${nAir.toLocaleString()} airborne over the U.S.`;
        $(".fm-sub").textContent = f.alt ? `${nGround.toLocaleString()} on the ground (transponder on)` : "";
        const past = model.get("events").filter(([t]) => t <= m);
        const ev = $(".fm-event"), last = past[past.length - 1];
        ev.textContent = last ? last[3] : ""; ev.style.color = last ? last[2] : "";
      }
      function setMinute(m) {
        const [b0, b1] = model.get("bounds");
        m = Math.max(b0, Math.min(b1, m));
        lastReq = performance.now();
        model.set("minute", m); model.save_changes();
        slider.value = m; hud(); dirty = true;
      }

      model.on("change:frame", () => {
        frame = model.get("frame"); hud(); dirty = true;
        if (playing) {
          const [, b1] = model.get("bounds"), step = 60 * +speedSel.value;
          if (model.get("minute") >= b1) { togglePlay(false); return; }
          const wait = Math.max(0, 110 - (performance.now() - lastReq));
          setTimeout(() => playing && setMinute(model.get("minute") + step), wait);
        }
      });
      model.on("change:aircraft", () => (aircraft = model.get("aircraft")));
      model.on("change:bounds", setBounds);
      model.on("change:series", () => (dirty = true));
      model.on("change:minute", () => { slider.value = model.get("minute"); hud(); dirty = true; });

      function togglePlay(on = !playing) {
        playing = on; playBtn.textContent = on ? "❚❚" : "▶";
        if (on) {
          const [b0, b1] = model.get("bounds");
          setMinute(model.get("minute") >= b1 ? b0 : model.get("minute") + 60 * +speedSel.value);
        }
      }
      playBtn.onclick = () => togglePlay();
      $(".fm-back").onclick = () => setMinute(model.get("minute") - 600);
      $(".fm-fwd").onclick = () => setMinute(model.get("minute") + 600);
      slider.oninput = () => setMinute(+slider.value);

      // pan / zoom
      let drag = null;
      cv.addEventListener("pointerdown", (e) => { drag = { x: e.clientX, y: e.clientY, lon: view.lon, lat: view.lat }; cv.setPointerCapture(e.pointerId); });
      cv.addEventListener("pointerup", () => (drag = null));
      cv.addEventListener("pointermove", (e) => {
        const r = cv.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
        if (drag) {
          const Z = view.z;
          view.lon = x2lon(lon2x(drag.lon, Z) - (e.clientX - drag.x), Z);
          view.lat = Math.max(-80, Math.min(80, y2lat(lat2y(drag.lat, Z) - (e.clientY - drag.y), Z)));
          tip.style.display = "none"; dirty = true; return;
        }
        let best = null, bd = 64;
        for (const [x, y, i] of pts) { const d = (x - mx) ** 2 + (y - my) ** 2; if (d < bd) { bd = d; best = i; } }
        if (best === null) { tip.style.display = "none"; return; }
        const f = frame, hx = f.hex[best], info = aircraft[hx] || ["", "", 4];
        const cats = model.get("categories");
        tip.innerHTML = `<b>${info[0] || hx}</b> ${info[1] || ""} · ${cats[info[2]] || ""}<br>` +
          (f.alt[best] < 0 ? "on ground" : `${f.alt[best].toLocaleString()} ft`) + ` · ${f.gs[best]} kt · ${f.hdg[best]}°<br>` +
          `<span style="opacity:.6">${hx}</span>`;
        tip.style.display = "block";
        tip.style.left = Math.min(mx + 14, W - 200) + "px"; tip.style.top = (my + 14) + "px";
      });
      cv.addEventListener("pointerleave", () => (tip.style.display = "none"));
      cv.addEventListener("wheel", (e) => {
        e.preventDefault();
        const r = cv.getBoundingClientRect(), mx = e.clientX - r.left - W / 2, my = e.clientY - r.top - H / 2;
        const Z = view.z, nz = Math.max(2, Math.min(12, Z - e.deltaY * 0.0025));
        const lon = x2lon(lon2x(view.lon, Z) + mx, Z), lat = y2lat(lat2y(view.lat, Z) + my, Z);
        view.z = nz;
        view.lon = x2lon(lon2x(lon, nz) - mx, nz); view.lat = y2lat(lat2y(lat, nz) - my, nz);
        dirty = true;
      }, { passive: false });

      const glyphLegend = () => {
        $(".fm-glyphs").innerHTML = model.get("categories").map((c, k) => `<div>${glyphSvg(k)}${c}</div>`).join("");
      };
      model.on("change:categories", glyphLegend);
      glyphLegend();
      setBounds(); hud();
      return () => { playing = false; };
    }

    export default { render };
    '''

    FLIGHTMAP_CSS = r'''.fm-root { position: relative; width: 100%; height: 620px; background: #1b1d21; border-radius: 8px; overflow: hidden;
      font-family: ui-sans-serif, -apple-system, "Segoe UI", sans-serif; color: #dfe7ef; user-select: none; }
    .fm-root canvas.fm-map { position: absolute; inset: 0; width: 100%; height: 100%; cursor: grab; }
    .fm-root canvas.fm-map:active { cursor: grabbing; }
    .fm-hud { position: absolute; top: 10px; left: 12px; background: rgba(8, 16, 26, .82); padding: 8px 12px; border-radius: 6px;
      font-size: 13px; line-height: 1.45; pointer-events: none; }
    .fm-hud .fm-clock { font-size: 22px; font-weight: 600; font-variant-numeric: tabular-nums; color: #fff; }
    .fm-hud .fm-count { font-size: 15px; color: #ffd84a; font-variant-numeric: tabular-nums; }
    .fm-legend { position: absolute; top: 10px; right: 12px; background: rgba(8, 16, 26, .82); padding: 8px 12px; border-radius: 6px;
      font-size: 12px; line-height: 1.6; }
    .fm-legend span.sw { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 6px; vertical-align: -1px; }
    .fm-bar { position: absolute; left: 0; right: 0; bottom: 0; display: flex; align-items: center; gap: 10px; padding: 10px 14px;
      background: linear-gradient(transparent, rgba(5, 10, 18, .95) 40%); }
    .fm-bar button { background: #1f6feb; color: #fff; border: 0; border-radius: 5px; padding: 5px 10px; font-size: 13px; cursor: pointer;
      min-width: 34px; }
    .fm-bar button.fm-ghost { background: #253445; }
    .fm-bar input[type=range] { flex: 1; accent-color: #ffd84a; }
    .fm-bar select { background: #253445; color: #dfe7ef; border: 0; border-radius: 5px; padding: 4px; font-size: 12px; }
    .fm-root canvas.fm-spark { position: absolute; left: 14px; bottom: 52px; width: calc(100% - 28px); height: 44px; pointer-events: none; }
    .fm-tip { position: absolute; pointer-events: none; background: rgba(8, 16, 26, .92); border: 1px solid #34495e; border-radius: 5px;
      padding: 5px 8px; font-size: 12px; white-space: nowrap; display: none; }
    .fm-hud .fm-event { font-weight: 600; margin-top: 2px; }
    .fm-hud .fm-event:empty { display: none; }
    .fm-legend .fm-glyphs { margin-top: 6px; padding-top: 6px; border-top: 1px solid rgba(255,255,255,.15); }
    .fm-legend .fm-glyphs div { display: flex; align-items: center; gap: 2px; }
    .fm-legend .fm-glyphs svg { display: inline-block; flex: none; }
    '''
    return FLIGHTMAP_CSS, FLIGHTMAP_JS


if __name__ == "__main__":
    app.run()
