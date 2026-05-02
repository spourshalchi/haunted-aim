# Sounds folder

Drop the four classic AIM `.wav` files in here, named exactly as below. Until you do, the app runs silently (no errors).

| Filename       | Original AIM event           | When it plays in this app                |
|----------------|-------------------------------|------------------------------------------|
| `signon.wav`   | Door open / buddy signs on    | When the ghost first appears             |
| `signoff.wav`  | Door close / buddy signs off  | When the conversation ends               |
| `imrcv.wav`    | Incoming IM "bloop"           | Each ghost message                       |
| `imsend.wav`   | Outgoing IM swoosh            | Each player choice                       |

## Where to find them

These are the iconic late-90s/early-00s AIM sounds. Search for "AIM sound effects pack" — they're widely archived. The original filenames in AIM 5.x were `imrcv.wav`, `imsend.wav`, `dooropen.wav`, `doorslam.wav` — rename `dooropen` → `signon` and `doorslam` → `signoff` to match the table above.

## Notes

- Keep file sizes small (under ~50 KB each) so they load instantly on the iPad over cellular.
- iOS Safari blocks audio until the first tap. The app handles this by unlocking audio when the player taps "Sign On" — you don't need to do anything.
- If you want different sound mappings, edit the `CONFIG.sounds` block near the top of `index.html`.
