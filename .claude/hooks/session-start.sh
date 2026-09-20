#!/bin/bash
# SessionStart hook — installs what this repo needs in Claude Code on the web.
#
# The /watch skill (.claude/skills/watch/) shells out to ffmpeg, ffprobe and
# yt-dlp. Its own scripts/setup.py auto-installs those via Homebrew on macOS,
# but on Linux it only *prints* the commands — so in a remote container the
# binaries are never actually installed and /watch fails at its preflight.
# This hook installs them, so every web session starts ready to run /watch.
#
# Idempotent: every step is guarded and safe to re-run.
set -euo pipefail

# Local machines manage their own toolchain; only set up remote containers.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

log() { echo "[session-start] $*"; }

# --- /watch: ffmpeg + ffprobe -------------------------------------------------
if command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1; then
  log "ffmpeg/ffprobe already present"
else
  log "installing ffmpeg…"
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg
  log "ffmpeg $(ffmpeg -version | head -1 | awk '{print $3}') installed"
fi

# --- /watch: yt-dlp -----------------------------------------------------------
if command -v yt-dlp >/dev/null 2>&1; then
  log "yt-dlp already present"
else
  log "installing yt-dlp…"
  pip3 install --quiet --break-system-packages yt-dlp
  log "yt-dlp $(yt-dlp --version) installed"
fi

# --- node dependencies --------------------------------------------------------
# Puppeteer downloads its own Chrome on install; the container already ships
# Chromium at $PLAYWRIGHT_BROWSERS_PATH, and disk here is a fixed allowance, so
# skip the redundant download and point Puppeteer at the preinstalled binary.
if [ -f "${CLAUDE_PROJECT_DIR:-.}/package.json" ]; then
  cd "${CLAUDE_PROJECT_DIR:-.}"
  CHROMIUM_BIN="${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}/chromium"
  if [ -x "$CHROMIUM_BIN" ]; then
    export PUPPETEER_SKIP_DOWNLOAD=true
    export PUPPETEER_EXECUTABLE_PATH="$CHROMIUM_BIN"
    if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
      echo "export PUPPETEER_EXECUTABLE_PATH=\"$CHROMIUM_BIN\"" >> "$CLAUDE_ENV_FILE"
      echo "export PUPPETEER_SKIP_DOWNLOAD=true" >> "$CLAUDE_ENV_FILE"
    fi
  fi
  if [ -d node_modules ]; then
    log "node_modules already present"
  else
    log "installing node dependencies…"
    npm install --no-audit --no-fund --loglevel=error
    log "node dependencies installed"
  fi
fi

log "ready"
