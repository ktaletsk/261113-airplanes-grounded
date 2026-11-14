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
HUBS = {  # major US airports (lat, lon) for the hub comparison
    "Atlanta (ATL)": (33.64, -84.43), "Dallas–Fort Worth area": (32.90, -97.04), "Denver (DEN)": (39.86, -104.67),
    "Chicago O'Hare (ORD)": (41.98, -87.90), "Los Angeles (LAX)": (33.94, -118.41), "Charlotte (CLT)": (35.21, -80.94),
    "Las Vegas (LAS)": (36.08, -115.15), "Phoenix (PHX)": (33.43, -112.01), "Orlando (MCO)": (28.43, -81.31),
    "Seattle (SEA)": (47.45, -122.31), "Houston (IAH)": (29.98, -95.34), "Newark (EWR)": (40.69, -74.17),
    "New York (JFK, LGA)": (40.64, -73.78), "San Francisco (SFO)": (37.62, -122.38), "Miami (MIA)": (25.79, -80.29),
    "Minneapolis (MSP)": (44.88, -93.22), "Detroit (DTW)": (42.21, -83.35), "Boston (BOS)": (42.36, -71.01),
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
AIR_NOW = int(_tot.get(("event", T_END), 0))
AIR_NOW_BASE = int(_tot.get(("baseline", T_END), 0))
_lat = counts[counts.t == T_END].pivot_table(index="category", columns="period", values="n", observed=True)
CAT_NOW = (100 * _lat["event"] / _lat["baseline"]).round().dropna().astype(int).to_dict() if "baseline" in _lat else {}

EVENTS = pd.DataFrame(
    ([{"t": dt.datetime.fromtimestamp(COLLAPSE_T, PT).replace(tzinfo=None), "label": f"departures collapse {fmt_pt(COLLAPSE_T)} ",
       "color": "#f08c00", "align": "right", "hud": f"Departures collapsing ({fmt_pt(COLLAPSE_T)} PT)"}] if COLLAPSE_T else [])
    + [{"t": GROUND_STOP, "label": " FAA ground stop 12:54 p.m. PT", "color": "#e03131", "align": "left",
        "hud": "FAA nationwide ground stop in effect"}])'''

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
  .er-databar { max-width: 720px; margin: 0 auto; display: flex; align-items: center; gap: 16px;
                font: 400 13px/1.45 Inter, sans-serif; padding: 10px 14px; border-radius: 8px;
                background: rgba(127,127,127,.10); }
  .er-databar span { flex: 1; opacity: .8; }
  .er-databar button { flex-shrink: 0; white-space: nowrap; }
  .er-databar-note { max-width: 720px; margin: 8px auto 0; }
  .er-method h3 { font-size: 15px; margin: 1.2em 0 .3em; }
</style>
""")'''

C["header"] = r'''mo.Html(f"""
<div class="er-hero">
  <div class="er-kicker">Flight-tracking analysis · Nov. 13, 2026</div>
  <h1>Empty skies</h1>
  <p class="er-dek">Departures from U.S. airports stopped almost all at once at {fmt_pt(COLLAPSE_T) if COLLAPSE_T else "midday"} Pacific,
  {f"{GAP_MIN} minutes" if GAP_MIN else "shortly"} before the FAA's nationwide ground stop officially took effect.
  Then the sky slowly emptied.</p>
  <div class="er-byline">Data: adsb.lol open ADS-B network · data through
  {fmt_pt(T_END)} PT</div>
</div>""")'''

C["stats"] = r'''_stat = lambda v, l, cls="": f'<div class="er-stat"><div class="v {cls}">{v}</div><div class="l">{l}</div></div>'
mo.Html('<div class="er-stats">'
        + _stat(fmt_pt(COLLAPSE_T).split()[0] if COLLAPSE_T else "–", "p.m. Pacific: airline takeoffs fall off a cliff", "warm")
        + _stat(f"{GAP_MIN} min" if GAP_MIN else "–", "before the FAA ground stop took effect (2:54 p.m. Central)", "hot")
        + _stat(f"{BEFORE_RATE:.0f} → {AFTER_RATE:.0f}" if AFTER_RATE is not None else "–", "airline takeoffs per minute, before → after")
        + _stat(f"−{100 * (1 - AIR_NOW / AIR_BEFORE):.0f}%" if AIR_BEFORE else "–",
                f"aircraft airborne over the U.S. since the collapse ({AIR_BEFORE:,} → {AIR_NOW:,})")
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
aircraft over the country fell steadily, from **{AIR_BEFORE:,}** at the moment of the collapse to **{AIR_NOW:,}**
at {fmt_pt(T_END)} Pacific. A day earlier at the same time, {AIR_NOW_BASE:,} aircraft were airborne.
""")'''

C["s_cliff"] = r'''prose(f"""
## The cliff came first

Counting airline takeoffs minute by minute makes the timing plain. The rate did not taper off as you might expect if
airlines were holding flights at the gate one by one. It fell off a cliff, from the high 30s per minute to single
digits, between {fmt_pt(COLLAPSE_T)} and {fmt_pt(COLLAPSE_T + 120)}. The official ground-stop time comes
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
cliff_chart = with_events(alt.layer(_band, _lines, _gap_txt)).properties(
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
              for e in EVENTS.to_dict("records")]
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
## Who is still flying

Airline traffic fell furthest, and the mix of what remains aloft shows it. At {fmt_pt(T_END)} Pacific, compared
with the same time a day earlier, airborne traffic by category stood at: {_cat}. Helicopters (police, medical, news)
and small private planes make up a growing share of what is still flying.
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
tk_all = _tk_all"""

C["s_states"] = r"""_r = REGION_STATS
prose(f'''
## Two states kept flying

Alaska Airlines said in a statement that flights within Alaska and inter-island flights in Hawaii were not affected
by the ground stop, [The New York Times reported]({NYT_AK}). The tracking data agrees. After {fmt_pt(COLLAPSE_T)},
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
        _name, subtitle=f"after the collapse: {_pct}% of Nov. 12" if _pct is not None else "", fontSize=13)))
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

for _k, _needle in [("config", "GROUND_STOP_T"), ("helpers", '"lat", "lon"]].assign'), ("config", "CATS ="),
                    ("config", 'Fetch newest data'), ("load", "Fetching the latest")]:
    assert _needle in C[_k], (_k, _needle)
assert "EVENTS = pd.DataFrame" not in C["config"]

ORDER = ["style", "header", "load", "stats", "lede", "s_cliff", "cliff_chart", "s_where", "zones_chart", "hubs_chart", "s_states", "states_chart", "s_neighbors", "neighbors_chart",
         "s_map", "map_controls", "map", "s_landings", "airborne_chart", "moves_chart", "s_alt", "alt_chart",
         "s_who", "category_chart", "method", "s_end", "config",
         "imports", "derive", "findings", "findings2", "export", "events_fn", "widget", "helpers", "assets"]

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
