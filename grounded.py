# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
#     "pandas",
#     "altair",
#     "anywidget",
#     "traitlets",
#     "tzdata==2026.6",
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
      .er-hero h1 { font-family: 'Source Serif 4', Georgia, serif; font-weight: 800; font-size: clamp(44px, 7vw, 76px);
                    line-height: 1.0; letter-spacing: -.02em; margin: 10px 0 14px; }
      .er-dek { font-family: 'Source Serif 4', Georgia, serif; font-size: 23px; line-height: 1.4; opacity: .85; margin: 0 0 18px; }
      .er-byline { font: 500 13px Inter, sans-serif; opacity: .6; border-top: 1px solid rgba(127,127,127,.3); padding-top: 12px; }
      .er-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 18px; padding: 14px 0 6px; }
      .er-stat .v { font: 700 34px/1.1 Inter, sans-serif; letter-spacing: -.02em; font-variant-numeric: tabular-nums; }
      .er-stat .v.hot { color: #e03131; } .er-stat .v.warm { color: #f08c00; }
      .er-stat .l { font: 400 13.5px/1.35 Inter, sans-serif; opacity: .7; margin-top: 4px; }
        .er-note p, .er-note em { font-family: Inter, sans-serif !important; font-size: 12.5px !important; }
      .er-note { font: 400 12.5px/1.5 Inter, sans-serif; opacity: .6; max-width: 720px; margin: 4px auto 0; }
      .er-method { font: 400 14.5px/1.6 Inter, sans-serif; }
      .er-method h3 { font-size: 15px; margin: 1.2em 0 .3em; }
    </style>
    """)
    return (prose,)


@app.cell(hide_code=True)
def _(COLLAPSE_T, GAP_MIN, T_END, WASM, fmt_pt, mo):
    mo.Html(f"""
    <div class="er-hero">
      <div class="er-kicker">Flight-tracking analysis · Nov. 13, 2026</div>
      <h1>Empty skies</h1>
      <p class="er-dek">Departures from U.S. airports stopped almost all at once at {fmt_pt(COLLAPSE_T) if COLLAPSE_T else "midday"} Pacific,
      {f"{GAP_MIN} minutes" if GAP_MIN else "shortly"} before the FAA's nationwide ground stop officially took effect.
      Then the sky slowly emptied.</p>
      <div class="er-byline">Data: adsb.lol open ADS-B network · Live analysis, last data point
      {fmt_pt(T_END)} PT · {"Snapshot rebuilt about every 30 minutes" if WASM else "Updated each time this notebook runs"}</div>
    </div>""")
    return


@app.cell(hide_code=True)
def _(
    AFTER_RATE,
    AIR_BEFORE,
    AIR_NOW,
    BEFORE_RATE,
    COLLAPSE_T,
    GAP_MIN,
    fmt_pt,
    mo,
):
    _stat = lambda v, l, cls="": f'<div class="er-stat"><div class="v {cls}">{v}</div><div class="l">{l}</div></div>'
    mo.Html('<div class="er-stats">'
            + _stat(fmt_pt(COLLAPSE_T).split()[0] if COLLAPSE_T else "–", "p.m. Pacific: airline takeoffs fall off a cliff", "warm")
            + _stat(f"{GAP_MIN} min" if GAP_MIN else "–", "before the FAA ground stop took effect (2:54 p.m. Central)", "hot")
            + _stat(f"{BEFORE_RATE:.0f} → {AFTER_RATE:.0f}" if AFTER_RATE is not None else "–", "airline takeoffs per minute, before → after")
            + _stat(f"−{100 * (1 - AIR_NOW / AIR_BEFORE):.0f}%" if AIR_BEFORE else "–",
                    f"aircraft airborne over the U.S. since the collapse ({AIR_BEFORE:,} → {AIR_NOW:,})")
            + '</div>')
    return


@app.cell(hide_code=True)
def _(
    AFTER_RATE,
    AIR_BEFORE,
    AIR_NOW,
    AIR_NOW_BASE,
    BEFORE_RATE,
    COLLAPSE_T,
    GAP_MIN,
    T_END,
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
    aircraft over the country fell steadily, from **{AIR_BEFORE:,}** at the moment of the collapse to **{AIR_NOW:,}**
    at {fmt_pt(T_END)} Pacific. A day earlier at the same time, {AIR_NOW_BASE:,} aircraft were airborne.
    """)
    return


@app.cell(hide_code=True)
def _(COLLAPSE_T, GAP_MIN, fmt_pt, prose):
    prose(f"""
    ## The cliff came first

    Counting airline takeoffs minute by minute makes the timing plain. The rate did not taper off as you might expect if
    airlines were holding flights at the gate one by one. It fell off a cliff, from the high 30s per minute to single
    digits, between {fmt_pt(COLLAPSE_T)} and {fmt_pt(COLLAPSE_T + 120)}. The official ground-stop time comes
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
    cliff_chart = with_events(alt.layer(_band, _lines, _gap_txt)).properties(
        width="container", height=280,
        title=alt.Title("Airline takeoffs stopped before the ground stop was declared",
                        subtitle="Airline takeoffs per minute across the U.S., Pacific time · blue: Nov. 13 · dashed grey: Nov. 12"))
    cliff_chart
    return


@app.cell(hide_code=True)
def _(ZONE_COLLAPSE, fmt_pt, prose):
    _z = {k: (fmt_pt(v) if v else "—") for k, v in ZONE_COLLAPSE.items()}
    prose(f"""
    ## Everywhere at once

    The halt did not roll across the country as a wave. Splitting departures into rough time-zone bands, the same
    test finds the collapse at **{_z["East"]}** in the East, **{_z["Central"]}** in the Central band, **{_z["Mountain"]}**
    in the Mountain band and **{_z["West"]}** in the West (all Pacific time), within a few minutes of each other.
    At the biggest hubs, the half hour after the cliff looked like an airport closed for the night.
    """)
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
                  for e in EVENTS.to_dict("records")]
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
def _(COLLAPSE_T, NYT_AK, REGION_STATS, fmt_pt, prose):
    _r = REGION_STATS
    prose(f'''
    ## Two states kept flying

    Alaska Airlines said in a statement that flights within Alaska and inter-island flights in Hawaii were not affected
    by the ground stop, [The New York Times reported]({NYT_AK}). The tracking data agrees. After {fmt_pt(COLLAPSE_T)},
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
            _name, subtitle=f"after the collapse: {_pct}% of Nov. 12" if _pct is not None else "", fontSize=13)))
    states_chart = alt.hconcat(*_panels).resolve_scale(y="independent").properties(title=alt.Title(
        "Alaska and Hawaii barely noticed", subtitle="Airline departures per 30 minutes; solid = Nov. 13, dashed = Nov. 12"))
    states_chart
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
def _(prose):
    prose("""
    ## Watch the sky empty

    Every aircraft broadcasting its position over the U.S., one frame per minute. Press play, or drag the slider back to
    late morning to see an ordinary Friday. Aircraft are colored by altitude; grey ones are on the ground with transponders
    on. Canadian and Mexican traffic is shown faded. Hover over a plane for its callsign and type.
    """)
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
def _(CAT_NOW, T_END, fmt_pt, prose):
    _cat = ", ".join(f"{k.lower()} {v}%" for k, v in sorted(CAT_NOW.items(), key=lambda kv: -kv[1]))
    prose(f"""
    ## Who is still flying

    Airline traffic fell furthest, and the mix of what remains aloft shows it. At {fmt_pt(T_END)} Pacific, compared
    with the same time a day earlier, airborne traffic by category stood at: {_cat}. Helicopters (police, medical, news)
    and small private planes make up a growing share of what is still flying.
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
    <b>Airline:</b> an airline-style callsign (three-letter operator code plus flight number) or a medium or heavy jet. This
    includes regional and cargo carriers, and a few flight schools that use operator codes.
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
    <a href="https://globalnews.ca/news/12150274/faa-usa-ground-stop-order/">Global News</a></p>
    </div>""")})
    return


@app.cell(hide_code=True)
def _(PT, dt, mo):
    WINDOW_START = dt.datetime(2026, 11, 13, 18, 0, tzinfo=dt.timezone.utc)   # 10:00 PT on the ground-stop day
    MAX_HOURS = 24                       # stop downloading this many hours after WINDOW_START
    BASELINE_SHIFT = 86400               # compare with the same clock time one day earlier
    WORKERS = 6                          # parallel downloads (be gentle with adsb.lol)
    PERIOD_LABEL = {"event": "Nov 13 (ground stop)", "baseline": "Nov 12 (day before)"}
    CATS = ["Airline", "Business jet", "General aviation", "Helicopter", "Other"]

    # FAA nationwide ground stop took effect 2:54 p.m. Central (News9). The departure collapse is detected from the data.
    GROUND_STOP = dt.datetime(2026, 11, 13, 12, 54)          # naive PT
    GROUND_STOP_T = int(GROUND_STOP.replace(tzinfo=PT).timestamp())
    HUBS = {  # major US airports (lat, lon) for the hub comparison
        "Atlanta (ATL)": (33.64, -84.43), "Dallas–Fort Worth area": (32.90, -97.04), "Denver (DEN)": (39.86, -104.67),
        "Chicago O'Hare (ORD)": (41.98, -87.90), "Los Angeles (LAX)": (33.94, -118.41), "Charlotte (CLT)": (35.21, -80.94),
        "Las Vegas (LAS)": (36.08, -115.15), "Phoenix (PHX)": (33.43, -112.01), "Orlando (MCO)": (28.43, -81.31),
        "Seattle (SEA)": (47.45, -122.31), "Houston (IAH)": (29.98, -95.34), "Newark (EWR)": (40.69, -74.17),
        "New York (JFK, LGA)": (40.64, -73.78), "San Francisco (SFO)": (37.62, -122.38), "Miami (MIA)": (25.79, -80.29),
        "Minneapolis (MSP)": (44.88, -93.22), "Detroit (DTW)": (42.21, -83.35), "Boston (BOS)": (42.36, -71.01),
    }

    refresh_btn = mo.ui.run_button(label="Load newest data", kind="neutral")
    refresh_btn
    return (
        BASELINE_SHIFT,
        CATS,
        GROUND_STOP,
        GROUND_STOP_T,
        HUBS,
        MAX_HOURS,
        PERIOD_LABEL,
        WINDOW_START,
        WORKERS,
        refresh_btn,
    )


@app.cell(hide_code=True)
async def _(
    BASELINE_SHIFT,
    MAX_HOURS,
    NotPublished,
    PT,
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
    load_bundle,
    load_slot,
    load_type_db,
    mo,
    np,
    pd,
    refresh_btn,
    region_of,
    time,
):
    refresh_btn  # re-run this cell (and everything below) when the button is pressed
    T0 = int(WINDOW_START.timestamp())

    if WASM:
        # browser build: the compact snapshot that GitHub Actions rebuilds and publishes next to the page
        snap, aircraft, PRE, _meta = await load_bundle(mo.notebook_location() / "public" / "bundle.npz")
        missing, T_END, MAP_STEP, DATA_BUILT = _meta["missing"], _meta["T_END"], _meta["map_step"], _meta["built"]
    else:
        _now = dt.datetime.now(dt.timezone.utc)
        _end = min(_now, WINDOW_START + dt.timedelta(hours=MAX_HOURS))
        _jobs = []
        _t = WINDOW_START
        while _t < _end:
            _jobs += [("event", _t), ("baseline", _t - dt.timedelta(seconds=BASELINE_SHIFT))]
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
        snap["t"] = snap.minute + np.where(snap.period == "baseline", BASELINE_SHIFT, 0)   # aligned clock (event day)

        _cs = pd.concat(_calls).drop_duplicates("hex", keep="last")
        aircraft = (pd.DataFrame({"hex": snap.hex.unique()}).merge(_cs, on="hex", how="left")
                    .merge(type_db, on="hex", how="left"))
        aircraft["category"] = categorize(aircraft.callsign, aircraft.desc, aircraft.wtc)
        snap = add_heading(snap.merge(aircraft[["hex", "category"]], on="hex", how="left"))
        PRE, MAP_STEP, DATA_BUILT = None, {"event": 1, "baseline": 1}, int(time.time())
        T_END = int(snap[snap.period == "event"].t.max())

    _last = dt.datetime.fromtimestamp(T_END, PT)
    mo.md(f"Loaded **{len(snap):,}** aircraft positions for **{snap.hex.nunique():,}** aircraft. "
          f"Ground-stop day data runs **10:00 → {_last:%H:%M} PT** ({dt.datetime.fromtimestamp(T_END, dt.timezone.utc):%H:%M UTC}); "
          + (f"snapshot built {dt.datetime.fromtimestamp(DATA_BUILT, PT):%b %-d, %H:%M PT}." if WASM
             else f"loaded at {dt.datetime.now(PT):%H:%M PT}.")
          + (f"  \n<small>Not published yet / unavailable: {', '.join(sorted(missing))}</small>" if missing else ""))
    return COUNTRY_GRID, MAP_STEP, PRE, T0, T_END, aircraft, missing, snap


@app.cell(hide_code=True)
def _(mo, prose):
    mo.vstack([mo.md("---"), prose("""
    *This report is a [marimo](https://marimo.io) notebook. The numbers and charts are recomputed from the newest
    available data each time it runs. Use the button to pull in data published since the page loaded.*
    """, cls="er-note")])
    return


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
def _(
    COUNTRY_GRID,
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
    moves["time_pt"] = to_pt(moves["bin"])
    return counts, moves, moves_all, total


@app.cell(hide_code=True)
def _(
    GROUND_STOP,
    GROUND_STOP_T,
    HUBS,
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
    AIR_NOW = int(_tot.get(("event", T_END), 0))
    AIR_NOW_BASE = int(_tot.get(("baseline", T_END), 0))
    _lat = counts[counts.t == T_END].pivot_table(index="category", columns="period", values="n", observed=True)
    CAT_NOW = (100 * _lat["event"] / _lat["baseline"]).round().dropna().astype(int).to_dict() if "baseline" in _lat else {}

    EVENTS = pd.DataFrame(
        ([{"t": dt.datetime.fromtimestamp(COLLAPSE_T, PT).replace(tzinfo=None), "label": f"departures collapse {fmt_pt(COLLAPSE_T)} ",
           "color": "#f08c00", "align": "right", "hud": f"Departures collapsing ({fmt_pt(COLLAPSE_T)} PT)"}] if COLLAPSE_T else [])
        + [{"t": GROUND_STOP, "label": " FAA ground stop 12:54 p.m. PT", "color": "#e03131", "align": "left",
            "hud": "FAA nationwide ground stop in effect"}])
    return (
        AFTER_RATE,
        AIR_BEFORE,
        AIR_NOW,
        AIR_NOW_BASE,
        BEFORE_RATE,
        CAT_NOW,
        COLLAPSE_T,
        EVENTS,
        GAP_MIN,
        ZONE_COLLAPSE,
        hubs,
        tk_base,
        tk_event,
    )


@app.cell(hide_code=True)
def _(COLLAPSE_T, T0, T_END, moves, pd, snap):
    NYT_AK = "https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa/cb2ab5a3-dcca-5a17-adfc-cc78cd6f1f2f"
    NYT_LIVE = "https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa"
    GLOBAL_NEWS = "https://globalnews.ca/news/12150274/faa-usa-ground-stop-order/"
    _tk_all = moves[(moves.kind == "takeoff") & (moves.category == "Airline")]
    _c = COLLAPSE_T or T0


    def _rate(d, lo, hi):
        # departures per 30 minutes in [lo, hi)
        return len(d[(d.t >= lo) & (d.t < hi)]) / max(1e-9, (hi - lo) / 1800)


    def _stats(d, hi):
        ev, bs = d[d.period == "event"], d[d.period == "baseline"]
        out = {"before": _rate(ev, _c - 3600, _c), "after": _rate(ev, _c + 120, hi), "base_after": _rate(bs, _c + 120, hi)}
        out["pct"] = round(100 * out["after"] / out["base_after"]) if out["base_after"] else None
        return out


    REGION_STATS = {r: _stats(_tk_all[_tk_all.region == r], T_END - 900) for r in ["Lower 48", "Alaska", "Hawaii"]}

    # Canada / Mexico: did the aircraft enter US airspace within 4 hours of takeoff?
    NB_END = T_END - 3600                      # leave an hour for late departures to reach the border
    _nb = _tk_all[_tk_all.country.isin(["Canada", "Mexico"])]
    _us_pos = snap.loc[snap.country == "US", ["hex", "minute"]]
    _f = _nb[["hex", "minute"]].merge(_us_pos, on="hex", suffixes=("", "_us"))
    _f = _f[(_f.minute_us > _f.minute) & (_f.minute_us <= _f.minute + 4 * 3600)]
    nb_tk = _nb.assign(to_us=_nb.set_index(["hex", "minute"]).index.isin(pd.MultiIndex.from_frame(_f[["hex", "minute"]])))
    NEIGHBOR_STATS = {(c, u): _stats(nb_tk[(nb_tk.country == c) & (nb_tk.to_us == u)], NB_END)
                      for c in ["Canada", "Mexico"] for u in [True, False]}
    tk_all = _tk_all
    return (
        GLOBAL_NEWS,
        NB_END,
        NEIGHBOR_STATS,
        NYT_AK,
        NYT_LIVE,
        REGION_STATS,
        nb_tk,
        tk_all,
    )


@app.cell(hide_code=True)
def _(
    Path,
    T_END,
    WASM,
    aircraft,
    counts,
    missing,
    moves_all,
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
        pack_bundle(_p, snap, aircraft, counts, moves_all,
                    {"T_END": T_END, "missing": missing, "built": int(time.time())})
        print(f"wrote {_p} ({_p.stat().st_size / 1e6:.1f} MB)")
    return


@app.cell(hide_code=True)
def _(EVENTS, alt, pd):
    def with_events(chart):
        """Layer the EVENTS markers (dashed rule + label) on a chart whose x is time_pt."""
        layers = [chart]
        for e in EVENTS.to_dict("records"):
            _d = pd.DataFrame([e])
            layers.append(alt.Chart(_d).mark_rule(color=e["color"], strokeWidth=1.5, strokeDash=[5, 3]).encode(x="t:T"))
            layers.append(alt.Chart(_d).mark_text(color=e["color"], align=e["align"], baseline="top", fontSize=11, fontWeight="bold")
                          .encode(x="t:T", y=alt.value(4), text="label:N"))
        return alt.layer(*layers)

    return (with_events,)


@app.cell(hide_code=True)
def _(
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
        return w

    return (make_flightmap,)


@app.cell(hide_code=True)
def _(
    BASELINE_SHIFT,
    CATS,
    PT,
    dt,
    gzip,
    io,
    json,
    mo,
    np,
    pd,
    re,
    time,
    urllib,
):
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


    def fetch(url, timeout=180, tries=3):
        for i in range(tries):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                    return r.read()
            except urllib.error.HTTPError as e:
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
            out.append(df.loc[m, ["minute", "t", "period", "hex", "category", "lat", "lon"]].assign(kind=kind))
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


    async def load_bundle(url):
        """Browser build: fetch the snapshot that GitHub Actions publishes next to the page."""
        from pyodide.http import pyfetch
        resp = await pyfetch(f"{url}?v={int(time.time() // 300)}")
        if not resp.ok:
            raise RuntimeError(f"could not load {url}: HTTP {resp.status}")
        return unpack_bundle(await resp.bytes())


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
        NotPublished,
        add_heading,
        categorize,
        country_grid,
        country_of,
        find_collapse,
        fmt_pt,
        load_bundle,
        load_slot,
        load_type_db,
        movements,
        pack_bundle,
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
    const PLANE = new Path2D("M0,-9 L1.4,-5 L1.4,-1.5 L8,2.5 L8,4 L1.4,2 L1,6 L3.5,8 L3.5,9 L0,8 L-3.5,9 L-3.5,8 L-1,6 L-1.4,2 L-8,4 L-8,2.5 L-1.4,-1.5 L-1.4,-5 Z");
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
            ctx.scale(ground ? s * 0.6 : s, ground ? s * 0.6 : s);
            ctx.globalAlpha = f.us && !f.us[i] ? 0.35 : 1;
            ctx.fillStyle = altColor(f.alt[i]); ctx.fill(PLANE);
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
    '''
    return FLIGHTMAP_CSS, FLIGHTMAP_JS


if __name__ == "__main__":
    app.run()
