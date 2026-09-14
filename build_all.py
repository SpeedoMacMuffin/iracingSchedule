import json, sys
OUT = next((a for a in sys.argv[1:] if not a.startswith('--')), 'index.html')
STANDALONE = '--standalone' in sys.argv   # full HTML document (GitHub Pages / local file); default output is meant for the Claude artifact wrapper
data = json.load(open('schedule.json'))

SPECIAL = [
 ('2026-01-09','2026-01-10','Roar','Daytona International Speedway','LMP3, GT4, Touring',None),
 ('2026-01-16','2026-01-18','Daytona 24','Daytona International Speedway','GTP, LMP2, GT3','Team Event'),
 ('2026-02-11','2026-02-18','Daytona 500','Daytona International Speedway','NASCAR Cup',None),
 ('2026-02-20','2026-02-22','Bathurst 12','Mount Panorama Circuit','GT3, GT4','Team Event'),
 ('2026-03-27','2026-03-29','Sebring 12','Sebring International Raceway','GTP, LMP2, GT3','Team Event'),
 ('2026-04-10','2026-04-11','IMSA Classic 500','WeatherTech Raceway Laguna Seca','Nissan GTP, Audi 90','Team Event'),
 ('2026-05-01','2026-05-03','Nürburgring 24h','Nürburgring - Gesamtstrecke 24h','GT3, Pcup, GT4, Touring','Team Event'),
 ('2026-05-05','2026-05-11','Indy 500 - Fixed','Indianapolis Motor Speedway','Dallara IR-18',None),
 ('2026-05-12','2026-05-18','Indy 500 - Open','Indianapolis Motor Speedway','Dallara IR-18',None),
 ('2026-05-20','2026-05-25','World 600','Charlotte Motor Speedway','NASCAR Cup',None),
 ('2026-05-29','2026-05-31','4 Hours at Thruxton','Thruxton Circuit','Touring Cars',None),
 ('2026-06-19','2026-06-21','Watkins Glen 6 Hour','Watkins Glen International','GTP, LMP2, GT3','Team Event'),
 ('2026-06-30','2026-07-06','Firecracker 400','Daytona International Speedway 2007','1987 NASCAR Cup',None),
 ('2026-07-10','2026-07-12','Spa 24','Circuit de Spa-Francorchamps','GT3','Team Event'),
 ('2026-07-22','2026-07-27','Brickyard 400','Indianapolis Motor Speedway','NASCAR Cup',None),
 ('2026-07-24','2026-07-26','6 Hours of Road America','Road America','GTP, LMP2, GT3','Team Event'),
 ('2026-08-04','2026-08-09','Knoxville Nationals','Knoxville Raceway','410 Winged Sprint Car','Super Session'),
 ('2026-08-14','2026-08-15','Portimao 1000km','Algarve International Circuit','HPD, GT1, GT2',None),
 ('2026-08-25','2026-08-30','Crandon Championship','Crandon International Raceway','Pro 4, Pro 2, Rally, Cross Car','Super Session'),
 ('2026-09-02','2026-09-07','Southern 500','Darlington Raceway','NASCAR Cup',None),
 ('2026-09-10','2026-09-15','Suzuka 1000km','Suzuka Circuit','GT3','Team Event'),
 ('2026-09-18','2026-09-20','Britcar 24','Silverstone','GT3, GT4','Team Event'),
 ('2026-09-25','2026-09-27','Petit Le Mans','Michelin Raceway Road Atlanta','GTP, LMP2, GT3','Team Event'),
 ('2026-10-02','2026-10-04','Bathurst 1000','Mount Panorama Circuit','Supercars','Team Event'),
 ('2026-10-16','2026-10-18','8 Hours of Indianapolis','Indianapolis Motor Speedway','GT3','Team Event'),
 ('2026-10-30','2026-10-31','iRacing FF1600 Festival','Brands Hatch','FF1600',None),
 ('2026-11-04','2026-11-09','Homestead Championship','Homestead Miami Speedway','NASCAR Cup',None),
 ('2026-11-13','2026-11-15','SFL Mountain Showdown','Mount Panorama Circuit','Super Formula Light',None),
 ('2026-11-17','2026-11-21','iRacing Runoffs','Road America','6 classes','Super Session'),
 ('2026-11-27','2026-11-29','Creventic 992 Endurance Cup','Circuit de Spa-Francorchamps','Porsche Cup 992.2',None),
 ('2026-12-02','2026-12-07','Winter Derby','Five Flags Speedway','Super Late Model',None),
 ('2026-12-15','2026-12-20','Chili Bowl','Chili Bowl','Dirt Midget','Super Session'),
 ('2026-12-18','2026-12-19','THE Production Car Challenge','Virginia International Raceway','PCC class',None),
]
data['special'] = [{'s': s, 'e': e, 'name': n, 'track': t, 'cars': c, 'tag': g} for s, e, n, t, c, g in SPECIAL]
payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
page = r'''<title>2026 S4 Schedule</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap">
<style>
:root {
  --bg: #eef0f3; --ink: #15181d; --muted: #5b6470; --rule: #d5dae1; --rule-soft: #e3e7ec; --tag-bg: #e2e6eb; --tag-ink: #3a424d; --place: #2f4a6d; --hot: #dcebe1;
  --cR: #d23b2e; --cD: #f0921e; --cC: #f2c51d; --cB: #1e8e4c; --cA: #2367b3;
  --onR: #fff; --onD: #15181d; --onC: #15181d; --onB: #fff; --onA: #fff;
  font-size: clamp(9px, 1.4vh, 16px);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --bg: #14171c; --ink: #e8ebef; --muted: #98a1ad; --rule: #333a44; --rule-soft: #262c35; --tag-bg: #2a313b; --tag-ink: #c3cad3; --place: #9fbadf; --hot: #1d2f25; }
}
:root[data-theme="dark"] { --bg: #14171c; --ink: #e8ebef; --muted: #98a1ad; --rule: #333a44; --rule-soft: #262c35; --tag-bg: #2a313b; --tag-ink: #c3cad3; --place: #9fbadf; --hot: #1d2f25; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 1rem/1.3 "Barlow", "Helvetica Neue", Arial, sans-serif; padding-block: .8rem .6rem; padding-inline: clamp(16px, 1.6vw, 32px); font-variant-numeric: tabular-nums; }
.cond, .brand, .cats button, .weeks, h1, h2, .nm, .side, .tag, .eyebrow, .dates { font-family: "Barlow Condensed", "Arial Narrow", sans-serif; }
button { color: inherit; }
button:focus-visible { outline: 2px solid var(--cA); outline-offset: 2px; }
.bar { display: flex; flex-wrap: wrap; align-items: center; gap: .3rem 1.4rem; margin-bottom: .5rem; }
.brand { font-weight: 600; font-size: 1.05rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.cats { display: flex; flex-wrap: wrap; gap: .1rem; }
.cats button { font-weight: 600; font-size: 1.1rem; letter-spacing: .04em; text-transform: uppercase; padding: .15rem .55rem; border: 0; border-bottom: 2px solid transparent; background: none; color: var(--muted); cursor: pointer; }
.cats button:hover { color: var(--ink); }
.cats button[aria-pressed="true"] { color: var(--ink); border-bottom-color: var(--ink); }
.weeks { margin-left: auto; display: flex; align-items: center; gap: .2rem; }
.weeks .lbl { font-weight: 600; font-size: .85rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin-right: .3rem; }
.weeks button { position: relative; width: 1.9rem; height: 1.9rem; border: 1px solid var(--rule); background: transparent; font-weight: 600; font-size: 1rem; border-radius: 3px; cursor: pointer; }
.weeks button:hover { border-color: var(--muted); }
.weeks button[aria-pressed="true"] { background: var(--ink); color: var(--bg); border-color: var(--ink); }
.weeks button.now::after { content: ""; position: absolute; left: 50%; bottom: -.45rem; width: .35rem; height: .35rem; margin-left: -.175rem; border-radius: 50%; background: var(--cB); }
header .title { display: flex; flex-wrap: wrap; align-items: baseline; gap: .2rem 1.2rem; border-bottom: 2px solid var(--ink); padding-bottom: .4rem; margin-bottom: .7rem; }
h1 { font-weight: 700; font-size: 1.9rem; line-height: 1; margin: 0; letter-spacing: -.01em; }
.dates { font-weight: 500; font-size: 1.25rem; color: var(--muted); }
.eyebrow { font-weight: 600; font-size: 1.05rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.lede { margin-left: auto; color: var(--muted); font-size: .9rem; }
.cols { columns: 3; column-gap: 2rem; column-rule: 1px solid var(--rule); }
h2 { display: flex; align-items: center; gap: .5rem; margin: 0 0 .3rem; padding-top: .5rem; font-weight: 600; font-size: 1.25rem; letter-spacing: .03em; text-transform: uppercase; break-after: avoid; break-inside: avoid; }
h2:first-child { padding-top: 0; }
.count { font-size: .85rem; font-weight: 500; color: var(--muted); }
.badge { display: inline-grid; place-items: center; width: 1.5rem; height: 1.5rem; border-radius: 3px; font-weight: 700; font-size: 1rem; }
.cR { background: var(--cR); color: var(--onR); } .cD { background: var(--cD); color: var(--onD); } .cC { background: var(--cC); color: var(--onC); } .cB { background: var(--cB); color: var(--onB); } .cA { background: var(--cA); color: var(--onA); }
.row { break-inside: avoid; display: flex; align-items: flex-start; gap: .8rem; padding: .28rem 0; border-top: 1px solid var(--rule-soft); }
.main { flex: 1; min-width: 0; }
.nm { font-weight: 600; font-size: 1.25rem; line-height: 1.15; letter-spacing: .005em; }
.trk { color: var(--place); font-weight: 400; font-size: .98rem; line-height: 1.25; }
.car { color: var(--ink); font-weight: 500; }
.side { flex: none; text-align: right; font-weight: 500; font-size: .9rem; line-height: 1.35; color: var(--muted); white-space: nowrap; padding-top: .1rem; }
.tag { font-weight: 600; font-size: .75rem; letter-spacing: .06em; text-transform: uppercase; background: var(--tag-bg); color: var(--tag-ink); padding: 0 .35rem; border-radius: 2px; margin-left: .4rem; vertical-align: .1em; }
.off .nm { color: var(--muted); font-weight: 500; }
.off .trk { color: var(--muted); font-size: .9rem; }
.empty { color: var(--muted); padding: 1rem 0; }
.cols > .row:first-child { border-top: 0; }
.cats .sep { width: 1px; height: 1.2rem; background: var(--rule); margin: 0 .5rem; align-self: center; }
.ev .date { flex: none; min-width: 6rem; font-family: "Barlow Condensed", "Arial Narrow", sans-serif; font-weight: 700; font-size: 1.05rem; line-height: 1.2; padding-top: .12rem; white-space: nowrap; }
.ev .side { white-space: normal; max-width: 11rem; }
.ev.past { color: var(--muted); }
.ev.past .nm, .ev.past .trk, .ev.past .date { color: var(--muted); font-weight: 500; }
.ev.hot { background: var(--hot); box-shadow: 0 0 0 .35rem var(--hot); border-top-color: transparent; }
.tag.now { background: var(--cB); color: #fff; }
@media (max-width: 1000px) { .cols { columns: 2; } .weeks { margin-left: 0; } }
@media (max-width: 640px) {
  :root { font-size: 15px; }
  .cols { columns: 1; }
  .lede { display: none; }
  .bar { gap: .5rem .8rem; }
  .cats button { padding: .45rem .6rem; font-size: 1.05rem; }
  .cats .sep { display: none; }
  .weeks { margin-left: 0; flex-wrap: wrap; gap: .3rem; }
  .weeks .lbl { flex-basis: 100%; margin: 0; }
  .weeks button { width: 2.6rem; height: 2.4rem; font-size: 1.1rem; }
  .weeks button.now::after { bottom: .2rem; }
  h1 { font-size: 2.2rem; }
  .row { flex-wrap: wrap; gap: .15rem .8rem; padding: .5rem 0; }
  .side { flex-basis: 100%; text-align: left; white-space: normal; padding-top: 0; display: flex; flex-wrap: wrap; gap: 0 .3rem; }
  .side div + div::before { content: "· "; }
  .ev .side { margin-left: calc(6rem + .8rem); max-width: none; }
  .ev.hot { box-shadow: 0 0 0 .5rem var(--hot); }
}
</style>
<header>
  <div class="bar">
    <div class="brand">iRacing 2026 Season 4</div>
    <nav class="cats" id="cats" aria-label="Category"></nav>
    <nav class="weeks" id="weeks" aria-label="Week"><span class="lbl">Week</span></nav>
  </div>
  <div class="title">
    <h1 id="h1">Week 1</h1>
    <div class="dates" id="dates"></div>
    <div class="eyebrow" id="catname"></div>
    <div class="lede" id="lede"></div>
  </div>
</header>
<div class="cols" id="cols"></div>
<script type="application/json" id="data">__DATA__</script>
<script>
(function () {
  const DATA = JSON.parse(document.getElementById('data').textContent);
  const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const addDays = (iso, n) => { const d = new Date(iso + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
  const fmtDay = iso => `${+iso.slice(8, 10)} ${MONTHS[+iso.slice(5, 7) - 1]}`;
  const fmtDM = iso => `${iso.slice(8, 10)}.${iso.slice(5, 7)}.`;
  const weekRange = w => { const s = addDays(DATA.seasonStart, 7 * (w - 1)); return [s, addDays(s, 6)]; };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const today = new Date().toISOString().slice(0, 10);
  let thisWeek = null;
  for (let w = 1; w <= DATA.weeks; w++) { const [s, e] = weekRange(w); if (today >= s && today <= e) thisWeek = w; }
  const state = { cat: 'sports-car', week: thisWeek || (today < DATA.seasonStart ? 1 : DATA.weeks) };

  function readHash() {
    const m = location.hash.match(/^#([a-z-]+)\/(\d+)$/);
    if (!m || !(m[1] === 'special-events' || DATA.categories.some(c => c.key === m[1]))) return;
    state.cat = m[1]; state.week = Math.min(Math.max(+m[2], 1), DATA.weeks);
  }
  function writeHash() { history.replaceState(null, '', `#${state.cat}/${state.week}`); }
  function set(patch) { Object.assign(state, patch); writeHash(); render(); }

  const catsEl = document.getElementById('cats');
  const SPECIAL_KEY = 'special-events';
  catsEl.innerHTML = DATA.categories.map(c => `<button type="button" data-cat="${c.key}">${esc(c.label)}</button>`).join('')
    + `<span class="sep"></span><button type="button" data-cat="${SPECIAL_KEY}">Special Events</button>`;
  catsEl.addEventListener('click', e => { const b = e.target.closest('button'); if (b) set({ cat: b.dataset.cat }); });
  const weeksEl = document.getElementById('weeks');
  for (let w = 1; w <= DATA.weeks; w++) {
    const [s, e] = weekRange(w);
    weeksEl.insertAdjacentHTML('beforeend', `<button type="button" data-week="${w}" class="${w === thisWeek ? 'now' : ''}" title="${fmtDay(s)} – ${fmtDay(e)}${w === thisWeek ? ' (this week)' : ''}">${w}</button>`);
  }
  weeksEl.addEventListener('click', e => { const b = e.target.closest('button'); if (b) set({ week: +b.dataset.week }); });
  document.addEventListener('keydown', e => {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === 'ArrowRight' && state.week < DATA.weeks) set({ week: state.week + 1 });
    if (e.key === 'ArrowLeft' && state.week > 1) set({ week: state.week - 1 });
  });
  window.addEventListener('hashchange', () => { readHash(); render(); });

  const fmtRange = (s, e) => s.slice(5, 7) === e.slice(5, 7) ? `${+s.slice(8, 10)} – ${fmtDay(e)}` : `${fmtDay(s)} – ${fmtDay(e)}`;
  function renderSpecial(ws, we) {
    let hot = 0;
    const rows = DATA.special.map(ev => {
      const status = ev.e < ws ? 'past' : (ev.s <= we ? 'hot' : '');
      if (status === 'hot') hot++;
      const tags = (ev.tag ? `<span class="tag">${esc(ev.tag)}</span>` : '') + (status === 'hot' ? '<span class="tag now">This week</span>' : '');
      return `<div class="row ev ${status}"><div class="date">${fmtRange(ev.s, ev.e)}</div><div class="main"><div><span class="nm">${esc(ev.name)}</span>${tags}</div><div class="trk">${esc(ev.track)}</div></div><div class="side"><div>${esc(ev.cars)}</div></div></div>`;
    });
    document.getElementById('cols').innerHTML = rows.join('');
    document.getElementById('lede').textContent = `${hot} special event${hot === 1 ? '' : 's'} overlap${hot === 1 ? 's' : ''} this week. Full 2026 calendar; past events greyed out. ← → change week.`;
  }
  function render() {
    const cat = DATA.categories.find(c => c.key === state.cat);
    const [ws, we] = weekRange(state.week);
    catsEl.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.cat === state.cat)));
    weeksEl.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.week === state.week)));
    document.getElementById('h1').textContent = `Week ${state.week}`;
    document.getElementById('dates').textContent = `${fmtDay(ws)} – ${fmtDay(we)} ${we.slice(0, 4)}`;
    document.getElementById('catname').textContent = cat ? cat.label : 'Special Events';
    if (!cat) return renderSpecial(ws, we);
    let racing = 0, off = 0, html = '';
    for (const k of cat.classes) {
      const rows = [];
      for (const s of k.series) {
        const tags = s.tags.map(t => `<span class="tag">${t}</span>`).join('');
        const name = `<span class="nm">${esc(s.name)}${tags}</span>`;
        const inWin = s.weeks.filter(w => w.d >= ws && w.d <= we);
        if (inWin.length) {
          racing++;
          const w = inWin[0];
          const tracks = [...new Set(inWin.map(x => x.track))].join(' / ');
          const l1 = [w.t != null ? `${w.t} °C` : null, w.r].filter(Boolean).join(' · ');
          const l2 = [w.s, w.sim ? `sim ${w.sim}` : null].filter(Boolean).join(' · ');
          const car = w.car ? ` <span class="car">· ${esc(w.car)}</span>` : '';
          rows.push(`<div class="row"><div class="main"><div>${name}</div><div class="trk">${esc(tracks)}${car}</div></div><div class="side"><div>${esc(l1)}</div><div>${esc(l2)}</div></div></div>`);
        } else {
          const next = s.weeks.filter(w => w.d > we).sort((a, b) => a.d < b.d ? -1 : 1)[0];
          if (!next) continue; // season over for this series
          off++;
          rows.push(`<div class="row off"><div class="main"><div>${name}</div><div class="trk">No round this week · next ${fmtDM(next.d)}</div></div></div>`);
        }
      }
      if (!rows.length) continue;
      html += `<h2><span class="badge c${k.cls}">${k.cls}</span>${k.label}<span class="count">${rows.length}</span></h2>${rows.join('')}`;
    }
    document.getElementById('cols').innerHTML = html || '<div class="empty">Nothing scheduled in this category for this week.</div>';
    document.getElementById('lede').textContent = `${racing} series on track${off ? `, ${off} without a round` : ''}. Temperatures are air temp at session start; “sim” is the in-game time of day. ← → change week.`;
    document.title = `2026 S4 Schedule`;
  }
  readHash(); writeHash(); render();
})();
</script>
'''.replace('__DATA__', payload)
if STANDALONE:
    head, body = page.split('</style>\n', 1)
    page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="color-scheme" content="light dark">\n'
            + head + '</style>\n</head>\n<body>\n' + body + '</body>\n</html>\n')
open(OUT, 'w').write(page)
print(OUT, len(page), 'bytes', '(standalone)' if STANDALONE else '(artifact fragment)')
