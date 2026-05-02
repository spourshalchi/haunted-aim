# Campaign Props — Agent Guide

This repo holds a collection of single-page, themed, interactable webpages used as in-game props during D&D sessions, hosted on GitHub Pages. Players interact with them on an iPad at the table.

## Layout convention

Each prop is a **self-contained folder at the repo root**. No build step, no framework, no shared dependencies — every prop must be openable as raw HTML.

```
.
├── README.md           # human-facing overview
├── CLAUDE.md           # this file
├── index.html          # landing page listing all props
├── <prop-name>/
│   ├── index.html      # the entire prop (HTML + CSS + JS inline)
│   └── (assets/)       # sounds, images, etc.
└── split_sounds.py     # WAV-dump → individual clips utility
```

Prop folder names: lowercase, hyphen-separated, short noun (`aim`, `radio`, `seance`, `answering-machine`).

URL pattern: `https://spourshalchi.github.io/<repo>/<prop-name>/`.

## iPad/iOS gotchas — non-negotiable

The AIM prop demonstrates working solutions for all of these. **Read its `index.html` before writing a new prop's audio or interaction code.**

### Audio: Web Audio API only — never HTMLAudio.

iOS WebKit (which Chrome on iPad is forced to use too) silently drops overlapping short HTMLAudio clones. Symptom: rapid-fire sounds randomly fail to play, only on iPad. Use the Web Audio pattern:

- `fetch()` + `audioCtx.decodeAudioData()` once per sound at load → `AudioBuffer`
- Fire-and-forget `BufferSource` per `play()` call (auto-GC'd, supports concurrency)
- Single `audioCtx.resume()` during a user gesture unlocks the whole context

### Audio unlock requires a user gesture.

iOS blocks audio until the user taps. Gate the prop behind a thematic splash whose tap calls `audioCtx.resume()` and any unlock side effects. Even a "warmup loop" through HTMLAudio will leak audible chunks of every sound on the first tap — Web Audio's single `resume()` is silent.

### Required `<head>` meta tags for every prop:

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="<short prop name>">
<meta name="theme-color" content="<#hex>">
```

These let players Add to Home Screen and launch the prop fullscreen with no Safari chrome — the table-ready presentation mode.

### Layout & input.

- Tap targets ≥44px; no hover-only states (mobile Safari fakes hover and it gets weird).
- Use `100dvh` not `100vh` (Safari toolbar collapse changes vh mid-session).
- Honor `env(safe-area-inset-*)` for notched devices.
- Block pinch-zoom in JS (`touchmove` + `e.scale !== 1`).
- `overscroll-behavior: none` on `body` to kill the rubber-band scroll.
- `* { -webkit-tap-highlight-color: transparent; }` to kill the gray flash on tap.
- `-webkit-user-select: none` on UI chrome; allow `text` selection on prose so players can copy clues if useful.

## Style direction

Retro is the through-line. Pick a different era + UI metaphor per prop. Lean hard — atmosphere is the point.

| Built / Slot | Era + Metaphor                                          |
|--------------|---------------------------------------------------------|
| `aim`        | 2000s AOL Instant Messenger                             |
| (open)       | 1980s answering machine — red blinking light, tape hiss |
| (open)       | 1990s BBS terminal — green phosphor, modem handshake    |
| (open)       | Cold War radio scanner — static between bands, dial knob|
| (open)       | Victorian séance / Ouija — parchment, candle flicker    |
| (open)       | DOS dungeon text adventure — ASCII art, blocking input  |

Period-correct fonts, beveled chrome, scanlines, gradients. **Dialogue/clue text must stay legible** at table distance — ≥14px, high contrast — even when chrome is heavily atmospheric.

## Reusable patterns from the AIM prop

- **Branching dialogue tree** (`DIALOGUE` JSON → `runNode(key)`): copy-paste into any prop with a conversational entity. Replace nodes, keep the engine. Schema: `{ ghost: [lines], choices: [{text, next}] }`. `choices: []` means terminal node (signs off).
- **Sign-on splash** as audio-unlock gate: reuse the pattern, restyle the splash to match the new prop's era (sign-on screen → tape rewind → radio warmup → séance candle, etc).
- **Web Audio block** (preload + unlock + play): copy intact, only swap the `CONFIG.sounds` paths.

## Deployment

GitHub Pages, branch `main`, folder `/ (root)`. Set once at repo creation; nothing to do per-prop.

**Push to `main` → live in ~30–60 seconds.** No build, no CI.

## Local testing

`file://` does NOT work — `fetch()` and audio won't load. Always serve via HTTP:

```bash
python -m http.server 8000
# http://localhost:8000 in any browser
# http://<LAN-ip>:8000 from iPad on the same Wi-Fi
```

The audio bug above is invisible on desktop browsers. **Always test new props on an actual iPad over the LAN before a session, not just localhost.**

## Audio asset prep

If a sound source comes as one WAV dump with multiple clips:

```bash
python split_sounds.py
```

Detects silent gaps, outputs `sounds/clip_NN.wav`. Listen and rename to whatever the prop expects. Tweak the threshold knobs at the top of the script if splits are wrong. Update `INPUT_PATH` to point at the new prop's dump file before running.

## Adding a new prop — checklist

1. `mkdir <prop-name>/`
2. Create `<prop-name>/index.html` with the required meta tags
3. Copy AIM's Web Audio block + sign-on splash pattern if the prop needs sound — do not reinvent
4. Add `<prop-name>/<assets>/` for sounds, images, etc.
5. Add a tile to the root `index.html` linking to `/<prop-name>/`
6. Test locally on the iPad over LAN (not just desktop)
7. Commit + push to `main`; redeploy in ~1 min
8. Cache-bust on iPad: append `?v=<n>` to the URL or delete + re-add the home-screen icon

## Don't do this

- Use `<audio>` elements + `cloneNode()` for playback — see Audio gotcha
- Add a build step, framework, npm dependency, or transpiler
- Skip the iOS meta tags — Add to Home Screen breaks silently and the prop loses its app feel
- Test only on desktop and ship — the audio bug only manifests on iPad
- Use `file://` for local testing — `fetch()` and audio fail mysteriously
- Hardcode the repo name in prop code; only README/CLAUDE reference it (so the repo can be renamed cleanly)
