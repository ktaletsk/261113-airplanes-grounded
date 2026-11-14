// Flightradar-style canvas map for anywidget. Python owns the data; JS owns view, slider and playback.
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
