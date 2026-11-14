# Run inside the marimo kernel (marimo-pair execute-code) to (re)build grounded.py as the "Empty skies" report.
# Reuses the data/widget cells from build_notebook_live.py and adds the narrative, findings and report charts.
from pathlib import Path

_src = ((Path(mo.notebook_dir()) / "scripts" / "build_notebook_live.py").read_text()
        .split("\nORDER = ")[0])
exec(_src)          # defines C (data/widget cells), JS, CSS, cm

# ---------------------------------------------------------------- tweaks to the reused cells
C["imports"] += r'''


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
    }})'''

C["config"] = C["config"].replace(r'''# key moments (PT, naive). FAA time per News9 (2:54 pm CT); the departure collapse is measured from this data.
EVENTS = pd.DataFrame([
    {"t": dt.datetime(2026, 11, 13, 12, 35), "label": "departures collapse 12:35 ", "color": "#f5a623", "align": "right",
     "hud": "Departures collapsing (12:35 PT)"},
    {"t": dt.datetime(2026, 11, 13, 12, 54), "label": " FAA ground stop 12:54 PT (2:54 CT)", "color": "#ff4d4f", "align": "left",
     "hud": "FAA nationwide ground stop in effect"},
])
''', r'''# FAA nationwide ground stop took effect 2:54 p.m. Central (News9). The departure collapse is detected from the data.
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
''')

C["helpers"] = C["helpers"].replace(
    '''out.append(df.loc[m, ["minute", "t", "period", "hex", "category"]].assign(kind=kind))''',
    '''out.append(df.loc[m, ["minute", "t", "period", "hex", "category", "lat", "lon"]].assign(kind=kind))''')
C["helpers"] += r'''


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
    return None, None'''

C["derive"] = C["derive"].replace('mo.md(f"Derived per-minute counts and **{len(moves):,}** takeoff/landing events.")', "")

C["load"] = C["load"].replace(
    'with mo.status.progress_bar(total=len(_jobs) + 1, title="Downloading ADS-B snapshots from adsb.lol",',
    'with mo.status.progress_bar(total=len(_jobs) + 1, title="Fetching the latest flight-tracking data from adsb.lol",')

# ---------------------------------------------------------------- findings (all numbers in the text come from here)
C["findings"] = r'''_tk = moves[(moves.kind == "takeoff") & (moves.country == "US")]
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
         "hud": "Ground stop lifted (5:15 p.m. PT)"}] if LIFT_T <= T_END else []))'''

# ---------------------------------------------------------------- styling + narrative
C["style"] = r'''def prose(text, cls="er-prose"):
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
  .er-databar { max-width: 720px; margin: 0 auto; display: flex; align-items: center; gap: 16px;
                font: 400 13px/1.45 Inter, sans-serif; padding: 10px 14px; border-radius: 8px;
                background: rgba(127,127,127,.10); }
  .er-databar span { flex: 1; opacity: .8; }
  .er-databar button { flex-shrink: 0; white-space: nowrap; }
  .er-databar-note { max-width: 720px; margin: 8px auto 0; }
  .er-method h3 { font-size: 15px; margin: 1.2em 0 .3em; }
</style>
""")'''


C["stats"] = r'''_stat = lambda v, l, cls="": f'<div class="er-stat"><div class="v {cls}">{v}</div><div class="l">{l}</div></div>'
mo.Html('<div class="er-stats">'
        + _stat(fmt_pt(COLLAPSE_T).split()[0] if COLLAPSE_T else "–", "p.m. Pacific: airline takeoffs fall off a cliff", "warm")
        + _stat(f"{GAP_MIN} min" if GAP_MIN else "–", "before the FAA ground stop took effect (2:54 p.m. Central)", "hot")
        + _stat(f"{BEFORE_RATE:.0f} → {AFTER_RATE:.0f}" if AFTER_RATE is not None else "–", "airline takeoffs per minute, before → after")
        + _stat(f"−{100 * (1 - AIR_MIN / AIR_BEFORE):.0f}%" if AIR_BEFORE else "–",
                f"aircraft airborne over the U.S., collapse to low point ({AIR_BEFORE:,} → {AIR_MIN:,})")
        + '</div>')'''

C["lede"] = r'''prose(f"""
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
""")'''

C["s_cliff"] = r'''prose(f"""
## The cliff came first

Counting airline takeoffs minute by minute makes the timing plain. The rate did not taper off as you might expect if
airlines were holding flights at the gate one by one. It fell off a cliff, from about {BEFORE_RATE:.0f} a minute to {AFTER_RATE:.0f},
between {fmt_pt(COLLAPSE_T)} and {fmt_pt(COLLAPSE_T + 120)}. The official ground-stop time comes
{GAP_MIN} minutes later, in the shaded gap below.

Early reports cited the 2:54 p.m. Central time. The data suggests departures were already being held in practice
before the formal nationwide order. One possibility is that facilities hit by the communications outage stopped
releasing flights on their own first. We could not find an official FAA timeline that settles it.
""")'''

C["cliff_chart"] = r'''_lo, _hi = (COLLAPSE_T or T0) - 45 * 60, min(T_END - 900, (COLLAPSE_T or T0) + 40 * 60)
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
cliff_chart'''

C["s_where"] = r'''_z = {k: (fmt_pt(v) if v else "—") for k, v in ZONE_COLLAPSE.items()}
prose(f"""
## Everywhere at once

The halt did not roll across the country as a wave. Splitting departures into rough time-zone bands, the same
test finds the collapse at **{_z["East"]}** in the East, **{_z["Central"]}** in the Central band, **{_z["Mountain"]}**
in the Mountain band and **{_z["West"]}** in the West (all Pacific time), within a few minutes of each other.
At the biggest hubs, the half hour after the cliff looked like an airport closed for the night.
""")'''

C["zones_chart"] = r'''_zt = moves[(moves.kind == "takeoff") & (moves.category == "Airline") & (moves.region == "Lower 48")].copy()
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
zones_chart'''

C["hubs_chart"] = r'''_h = hubs[hubs.before > 0].melt(id_vars="hub", value_vars=["before", "after"], var_name="when", value_name="n")
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
hubs_chart'''

C["s_map"] = r'''prose("""
## Watch the sky empty

Every aircraft broadcasting its position over the U.S., one frame per minute. Press play, or drag the slider back to
late morning to see an ordinary Friday. Aircraft are colored by altitude; grey ones are on the ground with transponders
on. Canadian and Mexican traffic is shown faded. Hover over a plane for its callsign and type.
{f"Drag the slider to {fmt_pt(WY_ZERO_T)} and look at Wyoming." if WY_ZERO_T else ""}
""")'''

C["s_landings"] = r'''prose(f"""
## Landings kept coming

Takeoffs and landings normally track each other closely. That's how the number of aircraft aloft stays roughly
level through the afternoon. After {fmt_pt(COLLAPSE_T)} the two lines split: takeoffs dropped to near zero, while
landings continued at close to their usual pace as flights already en route reached their destinations. The gap
between the lines is the sky draining.
""")'''

C["s_alt"] = r'''prose("""
## The middle of the sky emptied first

Sorting airborne aircraft by altitude shows the order the sky emptied in. The layers between 15,000 and 35,000 feet,
where jets climb out after takeoff, thinned fastest because nothing new was climbing through them. Two layers held
up longer: cruise altitudes above 35,000 feet, where long flights already en route kept going, and the lowest band
under 5,000 feet, which is mostly small private planes and helicopters.
""")'''

C["s_who"] = r'''_cat = ", ".join(f"{k.lower()} {v}%" for k, v in sorted(CAT_NOW.items(), key=lambda kv: -kv[1]))
prose(f"""
## Who kept flying

Airline traffic fell furthest, and the mix of what stayed aloft shows it. At the low point, {fmt_pt(AIR_MIN_T)} Pacific,
compared with the same time a day earlier, airborne traffic by category stood at: {_cat}. Helicopters (police,
medical, news) and small private planes made up a growing share of what was still flying.
""")'''

C["method"] = r'''mo.accordion({"How we did this": mo.Html(f"""<div class="er-method">
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
<a href="https://www.nbcwashington.com/news/national-international/faa-ground-stop-nationwide-us-airports/4182917/">NBC Washington</a></p>
</div>""")})'''

C["s_end"] = r'''mo.vstack([mo.md("---"), prose("""
*This report is a [marimo](https://marimo.io) notebook
([source](https://github.com/ktaletsk/261113-airplanes-grounded)). Every number and chart is computed from the data
shown at the top of the page; use the button there to fetch the newest data from adsb.lol and recompute everything.*
""", cls="er-note")])'''

# config cell outputs the refresh button; place it near the end with the data-status line


C["airborne_chart"] = C["airborne_chart"].replace(
    'title="Aircraft airborne over the US: ground-stop day vs the day before (same clock time)")',
    'title=alt.Title("The sky drained for hours", subtitle="Aircraft airborne over the U.S. each minute, Pacific time"))')
C["airborne_chart"] = C["airborne_chart"].replace('axis=alt.Axis(format="%H:%M")', 'axis=alt.Axis(format="%-I:%M")').replace(
    'title="time (PT)"', "title=None")
C["moves_chart"] = C["moves_chart"].replace(
    'title="Takeoffs vs landings per 5 min (all US)")',
    'title=alt.Title("Takeoffs stopped; landings didn\'t", subtitle="All U.S. takeoffs and landings per 5 minutes, Pacific time · solid: Nov. 13 · dashed: Nov. 12"))')
C["moves_chart"] = C["moves_chart"].replace(
    """legend=alt.Legend(labelExpr="datum.value == 'event' ? 'Nov 13' : 'Nov 12'")""",
    "legend=None")
assert "legend=None" in C["moves_chart"]
C["moves_chart"] = C["moves_chart"].replace('axis=alt.Axis(format="%H:%M")', 'axis=alt.Axis(format="%-I:%M")').replace(
    'title="time (PT)"', "title=None")
C["category_chart"] = C["category_chart"].replace(
    'title="Who is still flying? Airborne by category vs the day before")',
    'title=alt.Title("What is left in the air", subtitle="Aircraft airborne by category, as a share of the same time a day earlier"))')
C["category_chart"] = C["category_chart"].replace('axis=alt.Axis(format="%H:%M")', 'axis=alt.Axis(format="%-I:%M")').replace(
    'title="time (PT)"', "title=None")
C["alt_chart"] = (C["alt_chart"].replace("width=520", "width=430")
                  .replace('title="Airborne by altitude band (ground-stop day)")', 'title=alt.Title("Airborne by altitude", subtitle="Nov. 13, Pacific time"))')
                  .replace('title="Which layers empty first?")', 'title=alt.Title("Which layers emptied first", subtitle="Each band as % of its 10 a.m.–noon average"))')
                  .replace('axis=alt.Axis(format="%H:%M")', 'axis=alt.Axis(format="%-I:%M", tickCount=6)').replace('title="time (PT)"', "title=None"))
C["title"] = None


# ---------------------------------------------------------------- Alaska / Hawaii and the neighbours
NYT_AK = "https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa/cb2ab5a3-dcca-5a17-adfc-cc78cd6f1f2f"
NYT_LIVE = "https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa"
GLOBAL_NEWS = "https://globalnews.ca/news/12150274/faa-usa-ground-stop-order/"

C["findings2"] = r"""_tk_all = moves[(moves.kind == "takeoff") & (moves.category == "Airline")]
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
tk_all = _tk_all"""

C["s_states"] = r"""_r = REGION_STATS
prose(f'''
## Two states kept flying

Alaska Airlines said in a statement that flights within Alaska and inter-island flights in Hawaii were not affected
by the ground stop, [The New York Times reported]({NYT_AK}). The tracking data agrees. Between {fmt_pt(COLLAPSE_T)} and the lift,
airline departures in **Alaska ran at {_r["Alaska"]["pct"]}%** of the previous day's level for the same hours and
**Hawaii at {_r["Hawaii"]["pct"]}%**. In the lower 48 states the figure was **{_r["Lower 48"]["pct"]}%**.

Hawaiian Airlines' Boeing 717s kept shuttling between the islands, and international flights by Japan Airlines,
ANA, Korean Air, Qantas and Philippine Airlines kept leaving Honolulu. In Alaska, Alaska Airlines' in-state jets,
regional carriers such as Bering Air and Ravn, and the cargo flights that stop in Anchorage kept flying.
''')"""

C["states_chart"] = r"""_d = tk_all[tk_all.region.isin(["Lower 48", "Alaska", "Hawaii"]) & (tk_all.t < (T_END - 900) // 1800 * 1800)]
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
states_chart"""

C["s_neighbors"] = r"""_n = NEIGHBOR_STATS
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
''')"""

C["neighbors_chart"] = r"""_d = nb_tk[nb_tk.t < NB_END // 1800 * 1800]
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
neighbors_chart"""

C["findings2"] = f'NYT_AK = "{NYT_AK}"\nNYT_LIVE = "{NYT_LIVE}"\nGLOBAL_NEWS = "{GLOBAL_NEWS}"\n' + C["findings2"]
assert "country_grid" in C["helpers"] and '"us": (g.country' in C["widget"]


# ---------------------------------------------------------------- Wyoming moment + long-haul departures
NYT_INTL = "https://www.nytimes.com/live/2026/11/13/us/ground-stop-nationwide-flights-faa/1f19bdff-736c-5ab5-bceb-19df5ab3be0e"

C["findings3"] = r"""# Wyoming is a lat/lon rectangle, so a box is its exact border
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
LH_AIRPORTS = [a.split(" (")[0] if "(" in a else a for a in _apt.value_counts().head(5).index]"""

C["s_wyoming"] = r"""prose(f'''
## An empty state

One moment on the map sums it up. At **{fmt_pt(WY_ZERO_T)} Pacific**, not a single aircraft was visible in the sky
over Wyoming. At noon there had been {WY_NOON}. At the same time a day earlier there were {WY_BASE_AT}.
Receiver coverage is thin at low altitude over the rural West, so a small plane flying low could be missed. The jets
at cruise altitude that normally cross the state all day are hard to miss.
''') if WY_ZERO_T else prose(f'''
## An emptying state

Over Wyoming, the number of aircraft in the air fell from {WY_NOON} at noon to as few as {WY_MIN}.
''')"""

C["wy_chart"] = r"""_d = pd.concat([wy_series[p].rename("n").to_frame().assign(day=PERIOD_LABEL[p]) for p in PERIODS]).rename_axis("t").reset_index()
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
wy_chart"""

C["s_intl"] = r"""_lh_pct = LH_STATS["pct"]
_wb = lambda n: f"{n} wide-body" if n == 1 else f"{n} wide-bodies"
_share = round(100 * LH_LAST_HOUR[0] / LH_LAST_HOUR[1]) if LH_LAST_HOUR[1] else None
_share_txt = ("about the usual number" if _share is not None and _share >= 85 else
              f"about {_share}% of the {LH_LAST_HOUR[1]} that left the day before" if _share is not None else "")
_apts = ", ".join(LH_AIRPORTS[:-1]) + (f" and {LH_AIRPORTS[-1]}" if len(LH_AIRPORTS) > 1 else "".join(LH_AIRPORTS))
prose(f'''
## Long-haul flights got out

The halt was not total. Some international flights were departing U.S. airports, including Honolulu and San
Francisco for Asia, and several left Kennedy for Europe, [The New York Times reported]({NYT_INTL}). The FAA had not
said which international flights were cleared to go.

The data shows them clearly in the wide-body jets that fly long international routes. In the hour after the collapse,
just **{_wb(LH_FIRST_HOUR[0])}** left mainland airports, against {LH_FIRST_HOUR[1]} the day before. Then they started
coming back{f": from about **{fmt_pt(LH_RESUME_T)}** Pacific," if LH_RESUME_T else ","} the evening bank of flights to
Europe and Asia began to leave. In the latest hour of data, **{LH_LAST_HOUR[0]}** departed, {_share_txt},
led by {_apts}. Since the collapse, {_wb(LH_TOTAL)} have left the lower 48.
''')"""

C["intl_chart"] = r"""_bins = np.arange(T0, (T_END - 900) // 1800 * 1800, 1800)
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
intl_chart"""

C["header"] = r'''_ser = total[total.period == "event"].set_index("t").n.sort_index()
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
</div>""")'''

C["findings3"] = f'NYT_INTL = "{NYT_INTL}"\n' + C["findings3"]


# ---------------------------------------------------------------- recovery tracker
LIFT_SRC = "https://www.aljazeera.com/news/2026/11/13/us-grounds-all-flights-after-communication-issue"

C["findings4"] = r"""# minute-by-minute US airline takeoffs, Nov. 13 and the day before
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
AIR_NOW_PCT = round(100 * AIR_NOW / TOT_BS.get(T_END, np.nan)) if TOT_BS.get(T_END) else None"""

C["recovery_stats"] = r"""_stat = lambda v, l, cls="": f'<div class="er-stat"><div class="v {cls}">{v}</div><div class="l">{l}</div></div>'
_lift_v = fmt_pt(LIFT_T).split()[0]
mo.Html('<div class="er-stats">'
        + _stat(_lift_v, "p.m. Pacific: FAA lifts the ground stop (8:15 p.m. Eastern)", "good")
        + _stat(f"{DEP_NOW_PCT}%" if DEP_NOW_PCT is not None else "–",
                f"airline departures in the last half hour of data, vs. the day before ({DEP_NOW[0]:.0f} vs {DEP_NOW[1]:.0f} a minute)")
        + _stat(f"{AIR_NOW_PCT}%" if AIR_NOW_PCT is not None else "–",
                f"aircraft in the air over the U.S. at {fmt_pt(T_END)}, vs. the day before ({AIR_NOW:,})")
        + _stat(f"{AIR_MIN:,}", f"aircraft in the air at the low point, {fmt_pt(AIR_MIN_T)} (normally {AIR_MIN_BASE:,})", "hot")
        + '</div>')"""

C["s_recovery"] = r"""_rec = (f"Departures stayed at the ground-stop trickle for about **{LAG_MIN} minutes** and only began climbing at "
        f"**{fmt_pt(RECOVERY_T)}**, the mirror image of the afternoon, when departures stopped "
        f"{GAP_MIN} minutes before the order." if RECOVERY_T and LAG_MIN is not None and LAG_MIN > 0 else
        f"Departures began climbing at **{fmt_pt(RECOVERY_T)}**." if RECOVERY_T else
        "Departures have not picked up yet in the data.")
prose(f'''
## The recovery

The FAA lifted the nationwide ground stop at 8:15 p.m. Eastern (5:15 p.m. Pacific),
[Al Jazeera reported]({LIFT_SRC}), after about four hours and 20 minutes. The sky did not refill at once. {_rec}
The number of aircraft in the air bottomed out at **{AIR_MIN:,}** at {fmt_pt(AIR_MIN_T)}, when about
{AIR_MIN_BASE:,} would normally be flying.

As of {fmt_pt(T_END)} Pacific, the latest data, airline departures were running at **{DEP_NOW_PCT}%** of the
previous day's level and the number of aircraft in the air at **{AIR_NOW_PCT}%**. This page updates as new data
comes in. The rest of the story below is how the sky emptied.
''') if LIFTED else prose('''
## The recovery

The FAA lifted the ground stop at 5:15 p.m. Pacific. The flight data here does not reach that time yet.
''')"""

C["recovery_chart"] = r"""_r30 = lambda s: s.rolling(30, min_periods=10).sum()
_dep = pd.DataFrame({"t": rec_ev.index, "pct": 100 * _r30(rec_ev).values / _r30(rec_bs).replace(0, np.nan).values,
                     "series": "airline departures"})
_te = TOT_EV[TOT_EV.index >= T0]
_air = pd.DataFrame({"t": _te.index, "pct": 100 * _te.values / TOT_BS.reindex(_te.index).values,
                     "series": "aircraft in the air"})
_d = pd.concat([_dep, _air]).dropna()
_d["time_pt"] = to_pt(_d.t)
recovery_chart = with_events(alt.Chart(_d).mark_line(strokeWidth=2.4).encode(
    x=alt.X("time_pt:T", title=None, axis=alt.Axis(format="%-I:%M")),
    y=alt.Y("pct:Q", title="% of the day before", scale=alt.Scale(domain=[0, 115])),
    color=alt.Color("series:N", sort=["airline departures", "aircraft in the air"],
                    scale=alt.Scale(range=["#1c7ed6", "#f08c00"])),
    tooltip=["series:N", alt.Tooltip("time_pt:T", format="%-I:%M %p"), alt.Tooltip("pct:Q", format=".0f")])).properties(
    width="container", height=260, title=alt.Title("The day in one chart",
                                                   subtitle="U.S. airline departures (30-minute window) and aircraft in the air, as a share of the day before; Pacific time"))
recovery_chart"""

C["s_collapse_head"] = r"""prose('''
## How the sky emptied
''')"""

C["findings4"] = f'LIFT_SRC = "{LIFT_SRC}"\n' + C["findings4"]
C["s_recovery"] = C["s_recovery"]


# ---------------------------------------------------------------- three-part structure
C["part_fn"] = r"""def part(n, title, dek):
    return mo.Html(f'<div class="er-part"><div class="er-part-n">Part {n}</div>'
                   f'<div class="er-part-t">{title}</div><div class="er-part-d">{dek}</div></div>')"""

C["summary_stats"] = r"""_stat = lambda v, l, cls="": f'<div class="er-stat"><div class="v {cls}">{v}</div><div class="l">{l}</div></div>'
mo.Html('<div class="er-stats">'
        + _stat(fmt_pt(COLLAPSE_T).split()[0] if COLLAPSE_T else "–",
                f"p.m. PT: airline departures collapse, {GAP_MIN} minutes before the FAA's ground stop", "warm")
        + _stat(f"{AIR_MIN:,}", f"aircraft over the U.S. at the low point, {fmt_pt(AIR_MIN_T)} (normally {AIR_MIN_BASE:,})", "hot")
        + (_stat(fmt_pt(LIFT_T).split()[0], f"p.m. PT: the stop is lifted; departures restart {LAG_MIN} minutes later"
                 if LAG_MIN is not None else "p.m. PT: the stop is lifted", "good") if LIFTED else "")
        + _stat(f"{DEP_NOW_PCT}%" if DEP_NOW_PCT is not None else "–",
                f"of normal airline departures in the latest data ({fmt_pt(T_END)})")
        + '</div>')"""

C["s_intro"] = r"""prose(f'''
The two lines above tell the whole story. At {fmt_pt(COLLAPSE_T)} Pacific, U.S. airline departures (blue) fell
off a cliff. The number of aircraft in the air (orange) drained for hours as flights already aloft landed, bottoming
out at {AIR_MIN:,} at {fmt_pt(AIR_MIN_T)}{f" After the FAA lifted the stop at {fmt_pt(LIFT_T)}, both began to climb." if LIFTED else ""}

This page tells it in three parts: how the sky emptied, what kept flying when it was nearly empty, and how it came back.
''')"""

C["part1"] = r"""part(1, "The stop", "Departures halt, and the sky drains")"""
C["part2"] = r"""part(2, "At the bottom", "What kept flying, and what didn't")"""
C["part3"] = r"""part(3, "The return", "The ban is lifted and the sky refills")"""

C["s_map2"] = r"""prose(f'''
## Replay the day

Every aircraft broadcasting its position over the U.S., one frame per minute, from 10 a.m. to {fmt_pt(T_END)} Pacific.
The map opens at the low point. Drag the slider back to {fmt_pt(COLLAPSE_T)} to watch departures stop,
{f"to {fmt_pt(WY_ZERO_T)} to see Wyoming empty, " if WY_ZERO_T else ""}{f"and past {fmt_pt(LIFT_T)} to watch the sky refill" if LIFTED else ""}.
Aircraft are colored by altitude; grey ones are on the ground with transponders on. Canadian and Mexican traffic is
faded. Hover over a plane for its callsign and type.
''')"""

C["s_recovery2"] = r"""_rec = (f"Departures stayed at the ground-stop trickle for about **{LAG_MIN} minutes** and only began climbing at "
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
''')"""

C["restart_chart"] = r"""_lo, _hi = LIFT_T - 45 * 60, min(T_END - 900, LIFT_T + 100 * 60)
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
restart_chart"""


C["findings4"] += '\n\n# restart time by longitude band (same test, per region)\n_ztk = _tk[_tk.region == "Lower 48"]\n_zones = pd.cut(_ztk.lon, [-180, -115, -102, -87, -60], labels=["West", "Mountain", "Central", "East"])\nZONE_RECOVERY = {}\nfor _z in ["West", "Mountain", "Central", "East"]:\n    _s = _pm(_ztk[(_ztk.period == "event") & (_zones == _z)])\n    _sr = _s[(_s.index >= (COLLAPSE_T or T0) + 900) & (_s.index < min(LIFT_T, T_END))].mean()\n    _thr = max(2 * _sr, 0.5)\n    _f = _s.rolling(10).mean().shift(-9)\n    ZONE_RECOVERY[_z] = next((int(_t) for _t in _s.index[_s.index >= LIFT_T - 1800]\n                              if _f.get(_t, np.nan) >= _thr and _f.get(_t + 600, np.nan) >= _thr), None) if LIFTED else None\n# wide-body share of the East\'s first 20 minutes of restarted departures\n_et = ZONE_RECOVERY.get("East")\n_types = aircraft.drop_duplicates("hex").set_index("hex")["type"]\n_first = _ztk[(_ztk.period == "event") & (_zones == "East") & (_ztk.t >= (_et or 0)) & (_ztk.t < (_et or 0) + 1200)] if _et else _ztk.iloc[:0]\nEAST_WB = (int(_first.hex.map(_types).fillna("").astype(str).str.match(r"^(B74|B77|B78|B76|A33|A34|A35|A38|MD11)").sum()), len(_first))'

for _k, _needle in [("config", "GROUND_STOP_T"), ("helpers", '"lat", "lon"]].assign'), ("config", "CATS ="),
                    ("config", 'Fetch newest data'), ("load", "Fetching the latest")]:
    assert _needle in C[_k], (_k, _needle)
assert "EVENTS = pd.DataFrame" not in C["config"]

ORDER = ["style", "header", "load", "summary_stats", "recovery_chart", "s_intro",
         "part1", "lede", "s_cliff", "cliff_chart", "s_where", "zones_chart", "hubs_chart",
         "s_landings", "airborne_chart", "moves_chart", "s_alt", "alt_chart", "s_wyoming", "wy_chart",
         "s_map2", "map_controls", "map",
         "part2", "s_who", "category_chart", "s_states", "states_chart", "s_intl", "intl_chart",
         "s_neighbors", "neighbors_chart",
         "part3", "s_recovery2", "restart_chart",
         "method", "s_end", "config",
         "imports", "part_fn", "derive", "findings", "findings2", "findings3", "findings4", "export",
         "events_fn", "widget", "helpers", "assets"]

async with cm.get_context(skip_staleness_check=True) as ctx:
    cells = [c.id for c in ctx.cells]
    keep = cells[0]
    for cid in cells[1:]:
        ctx.delete_cell(cid)
    ctx.edit_cell(keep, code=C[ORDER[0]])
    prev, ids = keep, [keep]
    for k in ORDER[1:]:
        prev = ctx.create_cell(C[k], after=prev, hide_code=True)
        ids.append(prev)
print(dict(zip(ORDER, ids)))
