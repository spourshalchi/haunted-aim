# Haunted AIM — D&D Campaign Prop

A retro 2000s AOL Instant Messenger window with a haunted "buddy" who talks to your D&D party. Built as a single static HTML file — designed for iPad/iPhone Safari, deployable on GitHub Pages.

## What's in here

```
DnDAimBot/
├── index.html        ← the entire app (HTML + CSS + JS)
├── sounds/           ← drop classic AIM .wav files here (see sounds/README.md)
└── README.md         ← this file
```

## Local preview

Just double-click `index.html`. **Note:** sounds won't play from `file://` on some browsers. To preview audio locally, run a tiny static server from this folder:

```bash
# Python 3
python -m http.server 8000
# then open http://localhost:8000 on your iPad (same Wi-Fi)
```

## Deploy to GitHub Pages

1. Create a new GitHub repo (e.g. `dnd-aim-bot`) and push these files to `main`.
2. Repo → **Settings** → **Pages** → Source: **Deploy from a branch** → Branch: **main**, folder: **/ (root)** → Save.
3. After ~30 seconds your site is live at `https://<your-username>.github.io/<repo-name>/`.
4. Open that URL in Safari on the iPad. Tap the **Share** icon → **Add to Home Screen** for a fullscreen, no-Safari-chrome experience at the table.

## Editing the dialogue

Open `index.html` and find the `DIALOGUE` block (near the top of the `<script>` section). Each node looks like:

```js
nodeKey: {
  ghost: ["first message", "second message", "..."],
  choices: [
    { text: "what the player taps", next: "anotherNodeKey" },
    { text: "another option", next: "yetAnotherKey" }
  ]
}
```

- The conversation always starts at the node named `start`.
- A node with `choices: []` ends the conversation (ghost signs off).
- `next` can point to any other node key — including looping back to earlier nodes.

## Editing the personas

At the top of the `<script>` block, the `CONFIG` object controls:

- `playerScreenName` — shown on player messages (e.g. `"TheParty"`)
- `ghostScreenName` — shown on ghost messages and in the title bar
- `typingSpeedMs` — fake "typing..." duration per character
- `ghostMessageGapMs` — pause between consecutive ghost lines
- `sounds` — file paths to the four AIM sounds

## iPad / iPhone notes

- Audio is unlocked when the player taps **Sign On** (iOS Safari requires a user gesture).
- The viewport is locked against pinch-zoom so the chat fills the screen.
- "Add to Home Screen" launches the app fullscreen with a black status bar — best presentation mode at the table.
- Tested layouts down to iPhone SE width.
