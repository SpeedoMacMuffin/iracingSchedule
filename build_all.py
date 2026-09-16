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
 ('2026-09-10','2026-09-14','Suzuka 1000km','Suzuka Circuit','GT3','Team Event'),   # poster says 10-15, but iRacing's dates were wrong: it ended before week 1
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
page = r"""<title>2026 S4 Schedule</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap">
<style>
:root {
  color-scheme: dark;
  --bg: #14171c; --surface: #1c2027; --hover: #242a33; --ink: #eef1f4; --muted: #b3bcc7; --rule: #3a424d; --rule-soft: #2a313a; --tag-bg: #2f3742; --tag-ink: #d5dbe2; --place: #a9c4e6; --hot: #1f3a2b;
  --cR: #d23b2e; --cD: #f0921e; --cC: #f2c51d; --cB: #1e8e4c; --cA: #2367b3;
  --onR: #fff; --onD: #15181d; --onC: #15181d; --onB: #fff; --onA: #fff;
  --mR: #8a3029; --mD: #9c651f; --mC: #9c821f; --mB: #1e6a3e; --mA: #234c7c;   /* class colours blended toward the ground, for row rules */
  font-size: clamp(12px, 1.4vh, 16px);
}
:root[data-theme="light"] {
  color-scheme: light;
  --bg: #eef0f3; --surface: #ffffff; --hover: #e4e8ed; --ink: #15181d; --muted: #3f4750; --rule: #cfd5dc; --rule-soft: #dfe3e8; --tag-bg: #dde2e8; --tag-ink: #2f3740; --place: #29405f; --hot: #d9eadf;
  --mR: #dc8a84; --mD: #eab876; --mC: #ecd377; --mB: #79b693; --mA: #7ca3cf;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 1rem/1.3 "Barlow", "Helvetica Neue", Arial, sans-serif; padding-block: .8rem .6rem; padding-inline: clamp(16px, 1.6vw, 32px); font-variant-numeric: tabular-nums; }
.brand, .cats button, .weeks, h1, h2, h3, .nm, .tag, .eyebrow, .dates, .view, .cardnav, .dtitle, .cal .wk, .cal .ln { font-family: "Barlow Condensed", "Arial Narrow", sans-serif; }
button { color: inherit; font: inherit; }
button:focus-visible, [tabindex]:focus-visible { outline: 2px solid var(--cA); outline-offset: 2px; }
.bar { display: flex; flex-wrap: wrap; align-items: center; gap: .3rem 1.4rem; margin-bottom: .5rem; }
.brand { font-weight: 600; font-size: 1.05rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.cats { display: flex; flex-wrap: wrap; gap: .1rem; }
.cats button { font-weight: 600; font-size: 1.1rem; letter-spacing: .04em; text-transform: uppercase; padding: .15rem .55rem; border: 0; border-bottom: 2px solid transparent; background: none; color: var(--muted); cursor: pointer; }
.cats button:hover { color: var(--ink); }
.cats button[aria-pressed="true"] { color: var(--ink); border-bottom-color: var(--ink); }
.cats .pill { display: inline-grid; place-items: center; min-width: 1.15rem; height: 1.15rem; padding: 0 .3rem; margin-left: .4rem; border-radius: .6rem; background: var(--cB); color: #fff; font-size: .75rem; font-weight: 700; letter-spacing: 0; vertical-align: .1em; }
.cats .sep { width: 1px; height: 1.2rem; background: var(--rule); margin: 0 .5rem; align-self: center; }
.weeks { margin-left: auto; display: flex; align-items: center; gap: .2rem; }
.weeks .lbl { font-weight: 600; font-size: .85rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin-right: .3rem; }
.weeks button { position: relative; width: 1.9rem; height: 1.9rem; border: 1px solid var(--rule); background: transparent; font-weight: 600; font-size: 1rem; border-radius: 3px; cursor: pointer; }
.weeks button:hover { border-color: var(--muted); }
.weeks button[aria-pressed="true"] { background: var(--ink); color: var(--bg); border-color: var(--ink); }
.weeks button.now::after { content: ""; position: absolute; left: 50%; bottom: -.45rem; width: .35rem; height: .35rem; margin-left: -.175rem; border-radius: 50%; background: var(--cB); }
.view { display: inline-flex; margin-left: .9rem; border: 1px solid var(--rule); border-radius: 3px; overflow: hidden; }
.weeks .view button { width: auto; height: 1.9rem; border: 0; border-radius: 0; padding: 0 .55rem; font-size: .85rem; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
.weeks .view button[aria-pressed="true"] { background: var(--ink); color: var(--bg); }
.weeks .theme { margin-left: .5rem; font-size: 1.05rem; }
.title { display: flex; flex-wrap: wrap; align-items: baseline; gap: .2rem 1.2rem; border-bottom: 2px solid var(--ink); padding-bottom: .4rem; margin-bottom: .7rem; }
h1 { font-weight: 700; font-size: 1.9rem; line-height: 1; margin: 0; letter-spacing: -.01em; }
.dates { font-weight: 500; font-size: 1.25rem; color: var(--muted); }
.eyebrow { font-weight: 600; font-size: 1.05rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.lede { margin-left: auto; color: var(--muted); font-size: .95rem; font-weight: 500; }
.cols { columns: 3; column-gap: 2rem; column-rule: 1px solid var(--rule); }
h2 { display: flex; align-items: center; gap: .5rem; margin: 0 0 .3rem; padding-top: .5rem; font-weight: 600; font-size: 1.25rem; letter-spacing: .03em; text-transform: uppercase; break-after: avoid; break-inside: avoid; }
h2:first-child { padding-top: 0; }
.count { font-size: .9rem; font-weight: 500; color: var(--muted); }
.badge { display: inline-grid; place-items: center; width: 1.5rem; height: 1.5rem; border-radius: 3px; font-weight: 700; font-size: 1rem; }
.cR { background: var(--cR); color: var(--onR); } .cD { background: var(--cD); color: var(--onD); } .cC { background: var(--cC); color: var(--onC); } .cB { background: var(--cB); color: var(--onB); } .cA { background: var(--cA); color: var(--onA); }
.row { break-inside: avoid; display: flex; align-items: flex-start; gap: .8rem; padding: .28rem 0 .28rem .55rem; border-top: 1px solid var(--rule-soft); border-left: 2px solid transparent; }
.row.clk { cursor: pointer; }
.row.clk:hover { background: var(--hover); }
.row.clk:focus-visible { outline-offset: -2px; }
.wx { color: var(--ink); }
.main { flex: 1; min-width: 0; }
.nm { font-weight: 600; font-size: 1.25rem; line-height: 1.15; letter-spacing: .005em; }
.trk { color: var(--place); font-weight: 500; font-size: 1rem; line-height: 1.3; }
.car { color: var(--ink); font-weight: 500; }
.side { flex: none; text-align: right; font-weight: 500; font-size: 1rem; line-height: 1.3; color: var(--muted); white-space: nowrap; padding-top: .1rem; }
.tag { font-weight: 600; font-size: .8rem; letter-spacing: .06em; text-transform: uppercase; background: var(--tag-bg); color: var(--tag-ink); padding: 0 .35rem; border-radius: 2px; margin-left: .4rem; vertical-align: .1em; }
.tag.now { background: var(--cB); color: #fff; }
.off .nm { color: var(--muted); font-weight: 500; }
.off .trk { color: var(--muted); font-size: .95rem; }
.empty { color: var(--muted); padding: 1rem 0; }
.cols > .row:first-child { border-top: 0; }
/* cards view */
.cardnav { display: flex; align-items: center; gap: .7rem; margin-bottom: .9rem; flex-wrap: wrap; }
.cardnav .cls { display: flex; gap: .35rem; }
.cardnav .cls button { border: 2px solid transparent; background: none; padding: 0; border-radius: 5px; cursor: pointer; opacity: .5; line-height: 0; }
.cardnav .cls button:hover { opacity: .85; }
.cardnav .cls button[aria-pressed="true"] { opacity: 1; border-color: var(--ink); }
.cardnav .cls .badge { width: 1.8rem; height: 1.8rem; font-size: 1.15rem; }
.cardnav .arrow { width: 2rem; height: 2rem; border: 1px solid var(--rule); background: transparent; border-radius: 3px; cursor: pointer; font-size: 1.3rem; line-height: 1; padding: 0 0 .15rem; }
.cardnav .arrow:disabled { opacity: .3; cursor: default; }
.cardnav h2 { padding: 0; margin: 0 0 0 .4rem; font-size: 1.5rem; }
.cardnav .hint { margin-left: auto; color: var(--muted); font-size: .9rem; font-weight: 500; }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(17rem, 1fr)); gap: .8rem; }
.card { background: var(--surface); border: 1px solid var(--rule); border-left-width: 3px; border-radius: 5px; padding: .7rem .9rem .75rem; display: flex; flex-direction: column; gap: .15rem; cursor: pointer; }
.card:hover { border-color: var(--muted); }
.card .nm { font-size: 1.35rem; }
.card .trk { font-size: 1.02rem; }
.card .cars { color: var(--muted); font-size: 1rem; font-weight: 500; }
.card .meta { color: var(--muted); font-size: 1rem; font-weight: 500; margin-top: .35rem; display: flex; flex-wrap: wrap; gap: 0 .7rem; line-height: 1.4; }
.card .len { margin-left: auto; color: var(--ink); font-weight: 600; }
.card.off .nm, .card.off .trk { color: var(--muted); font-weight: 500; }
.kR { border-left-color: var(--mR); } .kD { border-left-color: var(--mD); } .kC { border-left-color: var(--mC); } .kB { border-left-color: var(--mB); } .kA { border-left-color: var(--mA); }
.off.kR, .off.kD, .off.kC, .off.kB, .off.kA { border-left-color: var(--rule); }
/* special events */
.ev { padding-left: 0; border-left: 0; }
.ev .date { flex: none; min-width: 6.4rem; font-family: "Barlow Condensed", "Arial Narrow", sans-serif; font-weight: 700; font-size: 1.05rem; line-height: 1.2; padding-top: .12rem; white-space: nowrap; }
.ev .side { white-space: normal; max-width: 11rem; }
.ev.past { color: var(--muted); }
.ev.past .nm, .ev.past .trk, .ev.past .date { color: var(--muted); font-weight: 500; }
.ev.hot { background: var(--hot); box-shadow: 0 0 0 .35rem var(--hot); border-top-color: transparent; }
/* detail panel */
dialog.detail { border: 0; padding: 0; background: var(--surface); color: var(--ink); width: min(32rem, 100vw); max-width: 100vw; height: 100dvh; max-height: 100dvh; margin: 0 0 0 auto; box-shadow: -8px 0 30px rgba(0, 0, 0, .18); }
dialog.detail::backdrop { background: rgba(10, 12, 16, .4); }
.dhead { display: flex; align-items: flex-start; gap: .7rem; padding: 1rem 1.1rem .8rem; border-bottom: 2px solid var(--ink); position: sticky; top: 0; background: var(--surface); z-index: 1; }
.dhead .badge { width: 2rem; height: 2rem; font-size: 1.25rem; flex: none; margin-top: .15rem; }
.dtitle { font-weight: 700; font-size: 1.6rem; line-height: 1.1; text-wrap: balance; }
.dsub { color: var(--muted); font-size: .95rem; font-weight: 500; margin: .2rem 0 0; }
.dclose { margin-left: auto; flex: none; width: 2.2rem; height: 2.2rem; border: 1px solid var(--rule); background: transparent; border-radius: 3px; font-size: 1.4rem; line-height: 1; cursor: pointer; }
.dbody { padding: .2rem 1.1rem 1.4rem; }
.dbody h3 { font-weight: 600; font-size: 1rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 1.1rem 0 .4rem; }
.dbody p { margin: 0; font-size: 1rem; }
.kv { display: grid; grid-template-columns: 7.5rem 1fr; gap: .3rem .8rem; font-size: 1rem; margin: 0; }
.kv dt { color: var(--muted); font-weight: 500; }
.kv dd { margin: 0; }
.cal { list-style: none; margin: 0; padding: 0; font-size: 1rem; }
.cal li { display: grid; grid-template-columns: 2.4rem 4rem 1fr auto; gap: .6rem; padding: .3rem .5rem; margin: 0 -.5rem; border-top: 1px solid var(--rule-soft); align-items: baseline; }
.cal li.cur { background: var(--hot); border-radius: 3px; border-top-color: transparent; }
.cal .wk { font-weight: 700; color: var(--muted); }
.cal .dt { font-weight: 500; color: var(--muted); }
.cal .tr { font-weight: 500; }
.cal .tr { color: var(--place); }
.cal .ln { font-weight: 600; white-space: nowrap; }
@media (max-width: 1000px) { .cols { columns: 2; } .weeks { margin-left: 0; } }
@media (max-width: 640px) {
  :root { font-size: 15px; }
  .cols { columns: 1; }
  .lede { display: none; }
  header { position: sticky; top: 0; z-index: 2; background: var(--bg); margin-inline: -16px; padding: .5rem 16px .6rem; box-shadow: 0 1px 0 var(--rule); }
  .bar { gap: .5rem .8rem; margin-bottom: 0; }
  .brand, .weeks .lbl { display: none; }
  .title { margin-top: .8rem; }
  .cats button { padding: .45rem .6rem; font-size: 1.05rem; }
  .cats .sep { display: none; }
  .weeks { margin-left: 0; flex-wrap: wrap; gap: .3rem; }
  .weeks button { width: 2.6rem; height: 2.4rem; font-size: 1.1rem; }
  .weeks .view { margin-left: auto; }
  .weeks .view button { height: 2.4rem; padding: 0 .7rem; font-size: .95rem; }
  .weeks button.now::after { bottom: .2rem; }
  h1 { font-size: 2.2rem; }
  .row { flex-wrap: wrap; gap: .15rem .8rem; padding-block: .5rem; }
  .side { flex-basis: 100%; text-align: left; white-space: normal; padding-top: 0; display: flex; flex-wrap: wrap; gap: 0 .3rem; }
  .side div + div::before { content: "· "; }
  .ev .side { margin-left: calc(6.4rem + .8rem); max-width: none; }
  .ev.hot { box-shadow: 0 0 0 .5rem var(--hot); }
  .cardnav .hint { display: none; }
  dialog.detail { width: 100vw; }
  .kv { grid-template-columns: 6.5rem 1fr; }
}
</style>
<script>(function(){var t='dark';try{t=localStorage.getItem('theme')==='light'?'light':'dark';}catch(e){}document.documentElement.setAttribute('data-theme',t);})();</script>
<header>
  <div class="bar">
    <div class="brand">iRacing 2026 Season 4</div>
    <nav class="cats" id="cats" aria-label="Category"></nav>
    <nav class="weeks" id="weeks" aria-label="Week"><span class="lbl">Week</span></nav>
  </div>
</header>
<div class="title">
  <h1 id="h1">Week 1</h1>
  <div class="dates" id="dates"></div>
  <div class="eyebrow" id="catname"></div>
  <div class="lede" id="lede"></div>
</div>
<div class="cols" id="cols"></div>
<div id="cardsview" hidden><div class="cardnav" id="cardnav"></div><div class="cards" id="cards"></div></div>
<dialog class="detail" id="detail" aria-label="Series details"></dialog>
<script type="application/json" id="data">__DATA__</script>
<script>
(function () {
  const DATA = JSON.parse(document.getElementById('data').textContent);
  const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const SPECIAL_KEY = 'special-events';
  const addDays = (iso, n) => { const d = new Date(iso + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
  const fmtDay = iso => `${+iso.slice(8, 10)} ${MONTHS[+iso.slice(5, 7) - 1]}`;
  const fmtDM = iso => `${iso.slice(8, 10)}.${iso.slice(5, 7)}.`;
  const weekRange = w => { const s = addDays(DATA.seasonStart, 7 * (w - 1)); return [s, addDays(s, 6)]; };
  const weekOf = iso => Math.floor((new Date(iso + 'T00:00:00Z') - new Date(DATA.seasonStart + 'T00:00:00Z')) / 604800000) + 1;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const today = new Date().toISOString().slice(0, 10);
  let thisWeek = null;
  for (let w = 1; w <= DATA.weeks; w++) { const [s, e] = weekRange(w); if (today >= s && today <= e) thisWeek = w; }
  const state = { cat: 'sports-car', week: thisWeek || (today < DATA.seasonStart ? 1 : DATA.weeks), view: 'list', cls: null };

  // index every series so rows and cards can open its detail panel
  const byId = new Map();
  DATA.categories.forEach(c => c.classes.forEach(k => k.series.forEach((s, i) => {
    s.id = `${c.key}:${k.cls}:${i}`; s.cls = k.cls; s.clsLabel = k.label; s.catLabel = c.label; byId.set(s.id, s);
  })));

  function readHash() {
    const m = location.hash.match(/^#([a-z-]+)\/(\d+)(?:\/cards(?:\/([RDCBA]))?)?$/);
    if (!m || !(m[1] === SPECIAL_KEY || DATA.categories.some(c => c.key === m[1]))) return;
    state.cat = m[1]; state.week = Math.min(Math.max(+m[2], 1), DATA.weeks);
    state.view = m[3] !== undefined || /\/cards$/.test(location.hash) ? 'cards' : 'list';
    if (m[3]) state.cls = m[3];
  }
  function writeHash() {
    const cards = state.view === 'cards' && state.cat !== SPECIAL_KEY;
    history.replaceState(null, '', `#${state.cat}/${state.week}${cards ? `/cards/${state.cls || ''}` : ''}`);
  }
  function set(patch) { Object.assign(state, patch); writeHash(); render(); }

  const catsEl = document.getElementById('cats');
  catsEl.innerHTML = DATA.categories.map(c => `<button type="button" data-cat="${c.key}">${esc(c.label)}</button>`).join('')
    + `<span class="sep"></span><button type="button" data-cat="${SPECIAL_KEY}">Special Events</button>`;
  catsEl.addEventListener('click', e => { const b = e.target.closest('button'); if (b) set({ cat: b.dataset.cat }); });
  const weeksEl = document.getElementById('weeks');
  for (let w = 1; w <= DATA.weeks; w++) {
    const [s, e] = weekRange(w);
    weeksEl.insertAdjacentHTML('beforeend', `<button type="button" data-week="${w}" class="${w === thisWeek ? 'now' : ''}" title="${fmtDay(s)} – ${fmtDay(e)}${w === thisWeek ? ' (this week)' : ''}">${w}</button>`);
  }
  weeksEl.insertAdjacentHTML('beforeend', `<div class="view" id="view" role="group" aria-label="View"><button type="button" data-view="list">List</button><button type="button" data-view="cards">Cards</button></div><button type="button" class="theme" id="theme"></button>`);
  const themeBtn = document.getElementById('theme');
  function paintTheme() { const light = document.documentElement.getAttribute('data-theme') === 'light'; themeBtn.textContent = light ? '☾' : '☀'; themeBtn.setAttribute('aria-label', light ? 'Switch to dark mode' : 'Switch to light mode'); themeBtn.title = themeBtn.getAttribute('aria-label'); }
  paintTheme();
  weeksEl.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.week) set({ week: +b.dataset.week });
    else if (b.dataset.view) set({ view: b.dataset.view });
    else if (b.id === 'theme') { const next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light'; document.documentElement.setAttribute('data-theme', next); try { localStorage.setItem('theme', next); } catch (e) {} paintTheme(); }
  });
  document.addEventListener('keydown', e => {
    if (e.altKey || e.ctrlKey || e.metaKey || document.getElementById('detail').open) return;
    if (e.key === 'ArrowRight' && state.week < DATA.weeks) set({ week: state.week + 1 });
    if (e.key === 'ArrowLeft' && state.week > 1) set({ week: state.week - 1 });
  });
  window.addEventListener('hashchange', () => { readHash(); render(); });

  const colsEl = document.getElementById('cols'), cardsView = document.getElementById('cardsview'), navEl = document.getElementById('cardnav'), cardsEl = document.getElementById('cards');
  const wxTxt = w => [w.t != null ? `${w.t} °C` : null, w.r].filter(Boolean).join(' · ');
  const runTxt = w => [w.s, w.sim ? `sim ${w.sim}` : null].filter(Boolean).join(' · ');
  const tagsOf = s => s.tags.map(t => `<span class="tag">${t}</span>`).join('');
  const shortCars = c => { const p = c.split(',').map(x => x.trim()).filter(Boolean); return p.length <= 2 ? p.join(' / ') : `${p[0]} +${p.length - 1} more`; };

  // which round of a series falls into the selected week; null when the series' season is over
  function resolve(s, ws, we) {
    const inWin = s.weeks.filter(w => w.d >= ws && w.d <= we);
    if (inWin.length) return { s, round: inWin[0], tracks: [...new Set(inWin.map(x => x.track))].join(' / ') };
    const next = s.weeks.filter(w => w.d > we).sort((a, b) => a.d < b.d ? -1 : 1)[0];
    return next ? { s, round: null, next } : null;
  }

  let currentModel = [];
  function render() {
    const cat = DATA.categories.find(c => c.key === state.cat);
    const [ws, we] = weekRange(state.week);
    const hotEv = DATA.special.filter(ev => ev.e >= ws && ev.s <= we);
    const sb = catsEl.querySelector(`button[data-cat="${SPECIAL_KEY}"]`);
    sb.innerHTML = 'Special Events' + (hotEv.length ? `<span class="pill" aria-label="${hotEv.length} this week">${hotEv.length}</span>` : '');
    sb.title = hotEv.length ? `This week: ${hotEv.map(e => e.name).join(', ')}` : 'No special event this week';
    catsEl.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.cat === state.cat)));
    weeksEl.querySelectorAll('button[data-week]').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.week === state.week)));
    const viewEl = document.getElementById('view');
    viewEl.hidden = !cat;
    viewEl.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.view === state.view)));
    document.getElementById('h1').textContent = `Week ${state.week}`;
    document.getElementById('dates').textContent = `${fmtDay(ws)} – ${fmtDay(we)} ${we.slice(0, 4)}`;
    document.getElementById('catname').textContent = cat ? cat.label : 'Special Events';
    if (!cat) { colsEl.hidden = false; cardsView.hidden = true; return renderSpecial(ws, we); }
    currentModel = cat.classes.map(k => ({ cls: k.cls, label: k.label, items: k.series.map(s => resolve(s, ws, we)).filter(Boolean) })).filter(k => k.items.length);
    const racing = currentModel.reduce((n, k) => n + k.items.filter(i => i.round).length, 0);
    const off = currentModel.reduce((n, k) => n + k.items.filter(i => !i.round).length, 0);
    const cards = state.view === 'cards';
    colsEl.hidden = cards; cardsView.hidden = !cards;
    if (cards) renderCards(); else renderList();
    document.getElementById('lede').textContent = `${racing} series on track${off ? `, ${off} without a round` : ''}. Click a series for details. Air temp at session start; “sim” is in-game time of day; ↻ per race: forecast regenerated for every race. ← → change week.`;
  }

  function renderList() {
    let html = '';
    for (const k of currentModel) {
      const rows = k.items.map(it => {
        const s = it.s, name = `<span class="nm">${esc(s.name)}${tagsOf(s)}</span>`;
        if (!it.round) return `<div class="row off clk k${k.cls}" data-id="${s.id}" role="button" tabindex="0"><div class="main"><div>${name}</div><div class="trk">No round this week · next ${fmtDM(it.next.d)}</div></div></div>`;
        const w = it.round, car = w.car ? ` <span class="car">· ${esc(w.car)}</span>` : '';
        const wx = w.wx ? ' · <span class="wx" title="Forecast regenerated for each race">↻ per race</span>' : '';
        return `<div class="row clk k${k.cls}" data-id="${s.id}" role="button" tabindex="0"><div class="main"><div>${name}</div><div class="trk">${esc(it.tracks)}${car}</div></div><div class="side"><div>${esc(wxTxt(w))}</div><div>${esc(runTxt(w))}${wx}</div></div></div>`;
      });
      html += `<h2><span class="badge c${k.cls}">${k.cls}</span>${k.label}<span class="count">${rows.length}</span></h2>${rows.join('')}`;
    }
    colsEl.innerHTML = html || '<div class="empty">Nothing scheduled in this category for this week.</div>';
  }

  function renderCards() {
    if (!currentModel.length) { navEl.innerHTML = ''; cardsEl.innerHTML = '<div class="empty">Nothing scheduled in this category for this week.</div>'; return; }
    if (!currentModel.some(k => k.cls === state.cls)) { state.cls = currentModel[0].cls; writeHash(); }
    const idx = currentModel.findIndex(k => k.cls === state.cls), k = currentModel[idx];
    navEl.innerHTML = `<button type="button" class="arrow" data-dir="-1" aria-label="Previous class" ${idx === 0 ? 'disabled' : ''}>‹</button>`
      + `<div class="cls">${currentModel.map(m => `<button type="button" data-cls="${m.cls}" aria-pressed="${m.cls === state.cls}" aria-label="${m.label}" title="${m.label} · ${m.items.length}"><span class="badge c${m.cls}">${m.cls}</span></button>`).join('')}</div>`
      + `<button type="button" class="arrow" data-dir="1" aria-label="Next class" ${idx === currentModel.length - 1 ? 'disabled' : ''}>›</button>`
      + `<h2>${k.label}<span class="count">${k.items.length} series</span></h2><span class="hint">Click a card for details · swipe or use the arrows to change class</span>`;
    cardsEl.innerHTML = k.items.map(it => {
      const s = it.s, name = `<span class="nm">${esc(s.name)}${tagsOf(s)}</span>`;
      if (!it.round) return `<div class="card off k${k.cls}" data-id="${s.id}" role="button" tabindex="0">${name}<span class="trk">No round this week · next ${fmtDM(it.next.d)}</span></div>`;
      const w = it.round, cars = s.weekly ? (w.car || '') : shortCars(s.cars || '');
      const wx = w.wx ? ' · <span class="wx" title="Forecast regenerated for each race">↻ per race</span>' : '';
      return `<div class="card k${k.cls}" data-id="${s.id}" role="button" tabindex="0">${name}<span class="trk">${esc(it.tracks)}</span>${cars ? `<span class="cars">${esc(cars)}</span>` : ''}<div class="meta"><span>${esc(wxTxt(w))}${wx}</span><span>${esc(runTxt(w))}</span>${w.len ? `<span class="len">${esc(w.len)}</span>` : ''}</div></div>`;
    }).join('');
  }
  navEl.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || b.disabled) return;
    if (b.dataset.cls) set({ cls: b.dataset.cls });
    else if (b.dataset.dir) { const i = currentModel.findIndex(k => k.cls === state.cls) + (+b.dataset.dir); if (currentModel[i]) set({ cls: currentModel[i].cls }); }
  });
  let touchX = null, touchY = null;
  cardsView.addEventListener('touchstart', e => { touchX = e.changedTouches[0].clientX; touchY = e.changedTouches[0].clientY; }, { passive: true });
  cardsView.addEventListener('touchend', e => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX, dy = e.changedTouches[0].clientY - touchY; touchX = touchY = null;
    if (Math.abs(dx) < 60 || Math.abs(dy) > 50) return;
    const i = currentModel.findIndex(k => k.cls === state.cls) + (dx < 0 ? 1 : -1);
    if (currentModel[i]) set({ cls: currentModel[i].cls });
  }, { passive: true });

  const fmtRange = (s, e) => s.slice(5, 7) === e.slice(5, 7) ? `${+s.slice(8, 10)} – ${fmtDay(e)}` : `${fmtDay(s)} – ${fmtDay(e)}`;
  function renderSpecial(ws, we) {
    let hot = 0;
    const rows = DATA.special.map(ev => {
      const status = ev.e < ws ? 'past' : (ev.s <= we ? 'hot' : '');
      if (status === 'hot') hot++;
      const tags = (ev.tag ? `<span class="tag">${esc(ev.tag)}</span>` : '') + (status === 'hot' ? '<span class="tag now">This week</span>' : '');
      return `<div class="row ev ${status}"><div class="date">${fmtRange(ev.s, ev.e)}</div><div class="main"><div><span class="nm">${esc(ev.name)}</span>${tags}</div><div class="trk">${esc(ev.track)}</div></div><div class="side"><div>${esc(ev.cars)}</div></div></div>`;
    });
    colsEl.innerHTML = rows.join('');
    document.getElementById('lede').textContent = `${hot} special event${hot === 1 ? '' : 's'} overlap${hot === 1 ? 's' : ''} this week. Full 2026 calendar; past events greyed out. ← → change week.`;
  }

  // detail panel
  const dlg = document.getElementById('detail');
  let opener = null;
  const kv = rows => `<dl class="kv">${rows.filter(([, v]) => v != null && v !== '').map(([k, v]) => `<dt>${k}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
  function openDetail(id, from) {
    const s = byId.get(id); if (!s) return;
    const [ws, we] = weekRange(state.week), it = resolve(s, ws, we), w = it && it.round;
    let html = `<div class="dhead"><span class="badge c${s.cls}">${s.cls}</span><div><div class="dtitle">${esc(s.full)}</div><p class="dsub">${esc(s.catLabel)} · ${esc(s.clsLabel)}${s.lic ? ` · ${esc(s.lic)}` : ''}${tagsOf(s)}</p></div><button type="button" class="dclose" aria-label="Close">×</button></div><div class="dbody">`;
    html += `<h3>Week ${state.week} · ${fmtDay(ws)} – ${fmtDay(we)}</h3>`;
    if (w) {
      html += kv([
        ['Track', it.tracks],
        ['Race', w.len],
        ['Weather', wxTxt(w) + (w.wx ? ' · forecast regenerated for each race' : '')],
        ['Start', [w.s ? `${w.s} start` : null, w.grid ? 'grid by class' : null].filter(Boolean).join(', ')],
        ['Cautions', w.caut],
        ['Qualifying', [w.dq ? 'detached' : null, w.qual ? `scrutiny ${w.qual.toLowerCase()}` : null].filter(Boolean).join(', ')],
        ['Sim time', w.sim],
        ['Drivers', w.drv],
      ]);
    } else if (it && it.next) html += `<p class="dsub">No round this week. Next round on ${fmtDay(it.next.d)} at ${esc(it.next.track)}.</p>`;
    else html += `<p class="dsub">No further rounds this season.</p>`;
    const cars = s.weekly ? (w && w.car ? `${w.car} (this week; the car changes every week)` : 'Changes every week') : s.cars;
    html += `<h3>Cars</h3><p>${esc(cars || '—')}</p>`;
    html += `<h3>Session rules</h3>${kv([['Races', s.cadence], ['Min entries', s.min], ['Split at', s.split], ['Drop weeks', s.drops], ['Incidents', s.pen], ['Rule set', s.rules]])}`;
    const seasonEnd = addDays(DATA.seasonStart, 7 * DATA.weeks - 1);
    const inSeason = s.weeks.filter(x => x.d >= DATA.seasonStart && x.d <= seasonEnd), outside = s.weeks.length - inSeason.length;
    html += `<h3>Season calendar</h3><ol class="cal">${inSeason.map(x => { const wk = weekOf(x.d); return `<li class="${wk === state.week ? 'cur' : ''}"><span class="wk">W${wk}</span><span class="dt">${fmtDay(x.d)}</span><span class="tr">${esc(x.track)}${x.car ? ` · ${esc(x.car)}` : ''}</span><span class="ln">${esc(x.len || '')}</span></li>`; }).join('')}</ol>`;
    if (!inSeason.length) html += `<p class="dsub">No rounds inside Season 4.</p>`;
    if (outside) html += `<p class="dsub">${outside} more round${outside === 1 ? '' : 's'} outside Season 4.</p>`;
    html += `</div>`;
    dlg.innerHTML = html; opener = from || null;
    dlg.showModal(); dlg.querySelector('.dclose').focus();
  }
  const onActivate = e => {
    const el = e.target.closest('[data-id]'); if (!el) return;
    if (e.type === 'keydown') { if (e.key !== 'Enter' && e.key !== ' ') return; e.preventDefault(); }
    openDetail(el.dataset.id, el);
  };
  [colsEl, cardsEl].forEach(el => { el.addEventListener('click', onActivate); el.addEventListener('keydown', onActivate); });
  dlg.addEventListener('click', e => { if (e.target === dlg || e.target.closest('.dclose')) dlg.close(); });
  dlg.addEventListener('close', () => { if (opener && document.contains(opener)) opener.focus(); });

  readHash(); writeHash(); render();
})();
</script>
""".replace('__DATA__', payload)
if STANDALONE:
    head, body = page.split('</style>\n', 1)
    page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="color-scheme" content="dark light">\n'
            + head + '</style>\n</head>\n<body>\n' + body + '</body>\n</html>\n')
open(OUT, 'w').write(page)
print(OUT, len(page), 'bytes', '(standalone)' if STANDALONE else '(artifact fragment)')
