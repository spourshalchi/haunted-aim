"""
Split a single WAV file containing multiple AIM-style sound clips into
individual numbered .wav files by detecting silent gaps between them.

Usage (from the project root):
    python split_sounds.py

Output: sounds/clip_01.wav, sounds/clip_02.wav, ...
Then listen to each and rename to: signon.wav, signoff.wav, imrcv.wav, imsend.wav

Tweak the constants below if too few/many clips come out.
"""
import wave, array, os, sys

# ---------------- knobs ----------------
INPUT_PATH         = "sounds/aimsounds.wav.wav"
OUTPUT_DIR         = "sounds"
SILENCE_THRESHOLD  = 0.015   # fraction of full scale; lower = stricter silence
MIN_SILENCE_MS     = 150     # silent gap (ms) required to split clips
MIN_CLIP_MS        = 80      # ignore blips shorter than this
PAD_MS             = 40      # silence kept on each side of a clip
WINDOW_MS          = 10      # analysis window
# ---------------------------------------


def main():
    if not os.path.exists(INPUT_PATH):
        print(f"ERROR: input file not found: {INPUT_PATH}")
        sys.exit(1)

    with wave.open(INPUT_PATH, "rb") as w:
        nch = w.getnchannels()
        sw  = w.getsampwidth()
        fr  = w.getframerate()
        nf  = w.getnframes()
        raw = w.readframes(nf)

    print(f"Loaded: {INPUT_PATH}")
    print(f"  channels={nch}  sample_width={sw}B  rate={fr}Hz  frames={nf}  duration={nf/fr:.2f}s")

    if sw == 2:
        fmt, full, signed = "h", 32768, True
    elif sw == 1:
        fmt, full, signed = "B", 128, False
    else:
        print(f"ERROR: only 8-bit and 16-bit WAV supported (got {sw*8}-bit). "
              "Convert with another tool first.")
        sys.exit(1)

    samples = array.array(fmt, raw)
    if sys.byteorder != "little" and sw == 2:
        samples.byteswap()

    win_frames   = max(1, int(fr * WINDOW_MS / 1000))
    win_samples  = win_frames * nch
    threshold    = SILENCE_THRESHOLD * full

    peaks = []
    for i in range(0, len(samples), win_samples):
        chunk = samples[i:i + win_samples]
        if not chunk:
            peaks.append(0); continue
        if signed:
            peaks.append(max(abs(s) for s in chunk))
        else:
            peaks.append(max(abs(s - 128) for s in chunk))

    is_silent = [p < threshold for p in peaks]
    n = len(is_silent)
    min_gap   = max(1, MIN_SILENCE_MS // WINDOW_MS)
    min_clip  = max(1, MIN_CLIP_MS    // WINDOW_MS)
    pad       = max(0, PAD_MS         // WINDOW_MS)

    clips = []
    i = 0
    while i < n:
        while i < n and is_silent[i]:
            i += 1
        if i >= n:
            break
        start = i
        silence_run = 0
        last_sound = i
        while i < n:
            if is_silent[i]:
                silence_run += 1
                if silence_run >= min_gap:
                    break
            else:
                silence_run = 0
                last_sound = i
            i += 1
        end = last_sound + 1
        if end - start >= min_clip:
            clips.append((max(0, start - pad), min(n, end + pad)))

    if not clips:
        print("\nNo clips detected. Try lowering SILENCE_THRESHOLD or MIN_SILENCE_MS.")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\nFound {len(clips)} clips.\n")
    print(f"  {'file':<18} {'start':>8} {'dur (ms)':>10}")
    print(f"  {'-'*18} {'-'*8} {'-'*10}")

    for idx, (s_win, e_win) in enumerate(clips, start=1):
        s_frame = s_win * win_frames
        e_frame = e_win * win_frames
        s_samp  = s_frame * nch
        e_samp  = e_frame * nch
        chunk   = samples[s_samp:e_samp]

        if sys.byteorder != "little" and sw == 2:
            chunk = array.array(fmt, chunk)
            chunk.byteswap()

        out_path = os.path.join(OUTPUT_DIR, f"clip_{idx:02d}.wav")
        with wave.open(out_path, "wb") as w:
            w.setnchannels(nch)
            w.setsampwidth(sw)
            w.setframerate(fr)
            w.writeframes(chunk.tobytes())

        dur_ms   = (e_frame - s_frame) * 1000 / fr
        start_ms = s_frame * 1000 / fr
        print(f"  clip_{idx:02d}.wav   {start_ms:7.0f}ms  {dur_ms:9.0f}")

    print(f"\nDone. Listen to each clip in {OUTPUT_DIR}/ and rename the four you want to:")
    print("  signon.wav   signoff.wav   imrcv.wav   imsend.wav")


if __name__ == "__main__":
    main()
