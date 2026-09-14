# iRacing schedule browser

Builds a single self-contained HTML page from the official iRacing season schedule PDF:
category tabs (Oval, Sports Car, Formula Car, Dirt Oval, Dirt Road, Unranked), a week 1–12 picker,
and a Special Events tab. Fits one desktop screen; type scales with window height.

## Rebuild

    pdftotext -layout ~/Downloads/2026s4.pdf 2026s4.txt
    python3 parse_all.py 2026s4.txt        # -> schedule.json (prints per-category counts and parse problems)
    python3 build_all.py index.html --standalone   # full HTML document for GitHub Pages / opening from disk
    python3 build_all.py 2026s4-schedule.html     # fragment without <html>/<head>, for the Claude artifact wrapper

Requires `poppler` (pdftotext) and Python 3, no other dependencies.

## GitHub Pages

Push this folder to a public repo and enable Pages (Settings → Pages → deploy from branch, root). `index.html` is served as is;
no build step is needed. Google Fonts are loaded from fonts.googleapis.com, everything else is inline.

## New season checklist

- `parse_all.py`: set `SEASON_START` to the Tuesday of week 1.
- `build_all.py`: replace the `SPECIAL` list (read from the yearly Special Events poster; dates, track, car classes, Team Event / Super Session tag).
- Run the parser and check its output: `problems: 0` and the "extra under-track tokens" list should only contain
  track-name fragments (e.g. "Prix", "Oval", "Course Long"). Anything else means a layout change in the PDF.

## Parsing notes

- Series names are prefixed with a form-feed character in the pdftotext output; it is stripped up front.
- Columns are sliced by character position from the "Week N" line (track / weather+settings / length).
  Continuation lines are split on 2+ spaces and assigned by position; tokens straddling the boundary are cut at a word boundary.
- Dirt oval rows carry heat/consolation/feature lap counts (`H:8L`, `C:10L`, `F:50L`) in the length column; they are skipped.
- Series whose car changes weekly (header says "See race week for cars in use that week", e.g. Ring Meister, Outlaw Micro Showdown)
  list the car under the track; it is captured as `car` and shown after the track.
- Year-long series (NASCAR iRacing Series, NEC, DTM, Creventic, ...) number rounds differently; the page matches rounds to
  season weeks by date and shows "No round this week · next dd.mm." when there is none.
