"""Read and write the local .env file. Tokens live here and nowhere else."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def load_env():
    values = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            values[key.strip()] = val.strip().strip('"').strip("'")
    # Real environment variables win over the file.
    for key in list(values):
        if key in os.environ:
            values[key] = os.environ[key]
    return values


def update_env(updates):
    """Set keys in .env, keeping every other line, and lock the file to the owner."""
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    remaining = dict(updates)
    out = []
    for line in lines:
        key = line.split("=", 1)[0].strip()
        if key in remaining and not line.lstrip().startswith("#"):
            out.append(f"{key}={remaining.pop(key)}")
        else:
            out.append(line)
    for key, val in remaining.items():
        out.append(f"{key}={val}")
    ENV_PATH.write_text("\n".join(out) + "\n")
    os.chmod(ENV_PATH, 0o600)


def require(env, *keys):
    missing = [k for k in keys if not env.get(k)]
    if missing:
        raise SystemExit(
            f"Missing {', '.join(missing)} in {ENV_PATH}. "
            "Copy .env.example to .env and fill it in (see stress_report/README.md)."
        )
