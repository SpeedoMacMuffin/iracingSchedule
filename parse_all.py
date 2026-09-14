import re, json, sys
TXT = sys.argv[1] if len(sys.argv) > 1 else '2026s4.txt'   # output of: pdftotext -layout <schedule.pdf> 2026s4.txt
lines = open(TXT).read().replace('\x0c','').split('\n')
CATS = ['OVAL','SPORTS CAR','FORMULA CAR','DIRT OVAL','DIRT ROAD','UNRANKED']
LABEL = {'OVAL':'Oval','SPORTS CAR':'Sports Car','FORMULA CAR':'Formula Car','DIRT OVAL':'Dirt Oval','DIRT ROAD':'Dirt Road','UNRANKED':'Unranked'}
start = next(i for i,l in enumerate(lines) if l.strip()=='OVAL' and i > 100)
sec = lines[start:]
def is_pageno(s): return re.match(r'^\s*\d+\s*$', s) is not None
def is_struct(h): return h.strip() in CATS or re.match(r'^[RDCBA] Class Series \(', h) is not None

series = []; cat = cls = None; cur = None; i = 0
while i < len(sec):
    ln = sec[i]
    if ln.strip() in CATS and ln.startswith(ln.strip()): cat = ln.strip()
    m = re.match(r'^([RDCBA]) Class Series \(', ln)
    if m: cls = m.group(1)
    wm = re.match(r'^Week (\d+) \((\d{4}-\d{2}-\d{2})\)', ln)
    if wm:
        if cur is None or wm.group(1) == '1' or int(wm.group(1)) <= cur['weeks'][-1]['week']:
            hdr = []; j = i - 1
            while j >= 0:
                h = sec[j]
                if h.strip()=='' or re.match(r'^\s+\S', h) or is_pageno(h) or is_struct(h) or re.match(r'^Week \d+', h): break
                hdr.insert(0, h.rstrip()); j -= 1
            cur = {'cat': cat, 'cls': cls, 'header': hdr, 'weeks': []}
            series.append(cur)
        entry = [ln.rstrip()]; k = i + 1
        while k < len(sec):
            s = sec[k]
            if s.strip()=='' or is_pageno(s): k += 1; continue
            if re.match(r'^\S', s): break
            entry.append(s.rstrip()); k += 1
        cur['weeks'].append({'week': int(wm.group(1)), 'date': wm.group(2), 'lines': entry})
        i = k; continue
    i += 1

problems = []
SETTINGS_WORDS = {'Detached','Rolling','Standing','Local','Cautions','Qual','Grid','Min','Max','Drive','Full','Single','Double','Constant','advisory','enforced','cautions','start','scrutiny'}
EXTRA = []
def parse_entry(e, sname, weekly_cars=False, cars=''):
    first = e['lines'][0]
    posB = re.match(r'^Week \d+ \(\d{4}-\d{2}-\d{2}\)\s+', first).end()
    wm = re.search(r'(\d+°F/\d+°C|Constant weather)', first)
    if not wm:
        problems.append(f'no weather: {sname} wk{e["week"]}: {first[:100]}'); return None
    posC = wm.start()
    lm = re.search(r'\s(\d+)( mins| laps)?\s*$', first)
    hm = re.search(r'\s[A-Z]:\d+L\s*$', first)
    posD = lm.start(1) if lm else (hm.start()+1 if hm else len(first))
    unit = (lm.group(2) or '').strip() if lm else 'x'
    colB = [first[posB:posC].strip()]; colC = [first[posC:posD].strip()]
    mid = (posB + posC) // 2
    for s in e['lines'][1:]:
        if re.match(r'^\s*[A-Za-z0-9 .\-\']+: (fuel|-?\d+kg|pwr|\d+ tire)', s): continue
        toks = []
        for m in re.finditer(r'\S+(?: \S+)*', s):
            tok, pos, end = m.group(0), m.start(), m.end()
            if pos < mid and end > posC + 2:   # straddles column B/C boundary: cut at the weather column
                cut = posC
                while cut > pos and s[cut-1] != ' ': cut -= 1          # never cut inside a word
                left = s[pos:cut].split()
                while left and left[-1].rstrip(',') in SETTINGS_WORDS:  # settings words belong to the right side
                    cut = s.rfind(left[-1], pos, cut); left.pop()
                toks.append((s[pos:cut].strip(), pos)); toks.append((s[cut:end].strip(), posC))
            else: toks.append((tok, pos))
        for tok, pos in toks:
            if not tok or re.match(r'^[A-Z]:\d+L$', tok) or tok in ('mins', 'laps'): continue
            if not unit and re.search(r' (mins|laps)$', tok): tok = tok.rsplit(' ', 1)[0]; unit = 'x'
            (colB if pos < mid else colC).append(tok)
    car_parts = []
    if weekly_cars:
        # car names for the week sit under the track (column B, before the session datetime)
        car_parts = [b for b in colB[1:] if b and not re.match(r'^\(\d{4}-', b)]
        colB = colB[:1] + [b for b in colB[1:] if re.match(r'^\(\d{4}-', b)]
    sim = None; track_parts = []
    for n_, b in enumerate(colB):
        if not b: continue
        sm = re.match(r'^\((\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})(?: \S+)?\)$', b)
        if sm: sim = sm.group(2)
        elif n_ > 0 and len(b) >= 3 and b in cars: car_parts.append(b); EXTRA.append((sname, e['week'], b, 'car'))
        else:
            if n_ > 0: EXTRA.append((sname, e['week'], b, 'track'))
            track_parts.append(b)
    settings = ' '.join(x for x in colC if x)
    temp = None; rain = None
    tm = re.search(r'/(\d+)°C', settings)
    if tm: temp = int(tm.group(1))
    rm = re.search(r'Rain chance ([^,]+?)(?:,|$)', settings)
    if rm:
        r = rm.group(1).strip()
        r = 'dry' if r == 'None' else r
        r = re.sub(r'^(\d+)%$', r'\1% rain', r)
        r = re.sub(r'^(\d+)% \((\d+)% before session\)$', r'\1% rain, \2% before', r)
        r = re.sub(r'^(\d+)% \(None before session\)$', r'\1% rain, dry before', r)
        r = r.replace('Slight (None before session)', 'slight rain')
        rain = r
    elif settings.startswith('Constant weather'): rain = 'constant weather'
    else: problems.append(f'no rain: {sname} wk{e["week"]}: {settings[:80]}')
    sm_ = re.search(r'\b(Standing|Rolling)\b', settings); st = sm_.group(1) if sm_ else None
    if st is None: problems.append(f'no start: {sname} wk{e["week"]}: {settings[:80]}')
    out_ = {'w': e['week'], 'd': e['date'], 'track': ' '.join(track_parts), 't': temp, 'r': rain, 's': st, 'sim': sim}
    if car_parts: out_['car'] = re.sub(r'\s+', ' ', ' '.join(car_parts))
    return out_

def short_name(n):
    n = re.sub(r'\s*-?\s*2026 Season( 4)?\s*(-\s*)?', ' ', n).strip(' -')
    return re.sub(r'\s{2,}', ' ', n)

SEASON_START = '2026-09-15'   # Tuesday of week 1 -- change per season
out = {'seasonStart': SEASON_START, 'weeks': 12, 'categories': []}
for c in CATS:
    catobj = {'key': c.lower().replace(' ', '-'), 'label': LABEL[c], 'classes': []}
    for cls, clabel in [('R','Rookie'),('D','Class D'),('C','Class C'),('B','Class B'),('A','Class A')]:
        ss = [s for s in series if s['cat']==c and s['cls']==cls]
        if not ss: continue
        items = []
        for s in ss:
            hdr = s['header']
            if not hdr: problems.append(f'no header: {c} {cls} first week line {s["weeks"][0]["lines"][0][:60]}'); continue
            name = hdr[0]
            lic_i = next((i for i,h in enumerate(hdr) if re.search(r'\(\d\.\d\) --> ', h)), None)
            lic = hdr[lic_i] if lic_i is not None else ''
            cadence = hdr[lic_i+1] if lic_i is not None and lic_i+1 < len(hdr) else ''
            tags = []
            if re.search(r'\bFixed\b', name): tags.append('Fixed')
            if 'Team racing' in lic: tags.append('Team')
            weekly = any(h.startswith('See race week') for h in hdr)
            cars = ' '.join(h.strip() for h in hdr[1:lic_i]) if lic_i else ''
            weeks = [w for w in (parse_entry(e, name, weekly, cars) for e in s['weeks']) if w]
            items.append({'name': short_name(name), 'full': name, 'tags': tags, 'cadence': cadence, 'weeks': weeks})
        catobj['classes'].append({'cls': cls, 'label': clabel, 'series': items})
    out['categories'].append(catobj)
json.dump(out, open('schedule.json','w'), ensure_ascii=False)
for c in out['categories']:
    n = sum(len(k['series']) for k in c['classes']); print(c['label'], n, 'series;', {k['cls']: len(k['series']) for k in c['classes']})
print('total', sum(len(k['series']) for c in out['categories'] for k in c['classes']))
from collections import Counter; print('problems:', len(problems), dict(Counter(p.split(':')[0] for p in problems))); print('\n'.join(problems[:12]))

from collections import Counter
print('extra under-track tokens:'); [print(' ', k, v) for k, v in Counter((x[0][:40], x[2], x[3]) for x in EXTRA).items()]
