# Campaign — D&D Table Props

A growing collection of single-page, themed, interactable webpages used as in-game props during D&D sessions. Players touch them on an iPad at the table.

Hosted on GitHub Pages. Live at **https://spourshalchi.github.io/campaign/** (rename pending).

## What's in here

```
.
├── index.html        ← landing page (Programs menu)
├── aim/              ← Haunted AOL Instant Messenger prop
│   ├── index.html
│   └── sounds/
├── CLAUDE.md         ← agent guide for adding new props
├── README.md         ← this file
└── split_sounds.py   ← utility for splitting WAV dumps into clips
```

## Current props

| Prop | Path  | Vibe                                          |
|------|-------|-----------------------------------------------|
| AIM  | `aim/`| Haunted 2000s AOL Instant Messenger; branching dialogue with a "buddy" who knows things they shouldn't |

## Adding a new prop

See [CLAUDE.md](CLAUDE.md) for the full pattern + iPad/iOS gotchas. Short version:

1. `mkdir <prop-name>/`
2. Build `<prop-name>/index.html` (single self-contained file — HTML + CSS + JS + assets folder beside it)
3. Add a tile in the root `index.html` linking to `/<prop-name>/`
4. Test on the actual iPad (the audio bug from CLAUDE.md is invisible on desktop)
5. Push to `main`. GitHub Pages redeploys in ~30–60 seconds.

## Local preview

`file://` doesn't work — `fetch()` and audio are blocked. Always serve via HTTP:

```bash
python -m http.server 8000
# Open http://localhost:8000 in any browser
# Or http://<your-LAN-ip>:8000 from the iPad on the same Wi-Fi
```

## iPad setup at the table

1. In Safari on the iPad, open the live URL above
2. Tap **Share** → **Add to Home Screen** → **Add**
3. Launch from the home screen icon — fullscreen, no Safari chrome, looks like a real app
4. After any update push, cache-bust by appending `?v=<n>` to the URL or delete + re-add the icon

## Audio asset prep

If a sound source comes as one big WAV with multiple clips:

```bash
python split_sounds.py
```

Detects silent gaps and chops the file into numbered clips. Tweak the constants at the top of the script if it splits poorly. Update `INPUT_PATH` to point at the dump file for your new prop first.
