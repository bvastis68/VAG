# /watch — vendored skill

Upstream: https://github.com/taoufik123-collab/claude-watch (MIT, by taoufik), tag `v0.2.0`.

## Why this is vendored here

The copy of this skill synced from claude.ai contained **only `SKILL.md`** — none of the
nine scripts under `scripts/` that `SKILL.md` invokes. Every step of the pipeline shells
out to those files:

```
python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py" --check   # Step 0
python3 "${CLAUDE_SKILL_DIR}/scripts/watch.py" ...       # Step 2
```

With the scripts absent, `/watch` fails on its first command. Vendoring the complete
runtime into the repo makes `/watch` work in any session opened on this project,
independent of what the claude.ai skill sync happens to carry.

## Contents

`SKILL.md` plus the nine runtime scripts named in its "Bundled scripts" section:
`watch.py`, `download.py`, `frames.py`, `pacing.py`, `hook.py`, `report.py`,
`transcribe.py`, `whisper.py`, `setup.py`.

Pure stdlib — no pip install step. External binaries (`ffmpeg`, `ffprobe`, `yt-dlp`) are
handled by `scripts/setup.py`.

## Fixing the other surfaces

- **Claude Code (plugin):** `/plugin marketplace add taoufik123-collab/claude-watch`
  then `/plugin install watch@claude-watch`. This also installs the `SessionStart` hook
  and the `/watch` command, which a vendored skill does not carry.
- **claude.ai (web):** upload the packaged `watch.skill` bundle — not a bare `SKILL.md` —
  under Settings → Capabilities → Skills. Build it from a clean checkout of upstream with
  `bash scripts/build-skill.sh`, which writes `dist/watch.skill`.
