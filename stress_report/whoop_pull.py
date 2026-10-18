"""Pull the last N days of WHOOP cycles, recoveries and workouts into stress_report/data/.

Usage:
    python3 stress_report/whoop_pull.py            # last 30 days
    python3 stress_report/whoop_pull.py --days 45
"""
import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

from envfile import DATA_DIR, load_env, require
from whoop_auth import refresh

API = "https://api.prod.whoop.com/developer"
ENDPOINTS = {
    "cycles": "/v2/cycle",
    "recoveries": "/v2/recovery",
    "workouts": "/v2/activity/workout",
}


def get(env, path, params):
    url = API + path + "?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {env['WHOOP_ACCESS_TOKEN']}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp), env
        except urllib.error.HTTPError as err:
            if err.code == 401 and attempt == 0:
                env = refresh(env)
                continue
            if err.code == 429:
                time.sleep(2 ** attempt)
                continue
            raise SystemExit(f"WHOOP GET {path} failed: HTTP {err.code} {err.read().decode()[:300]}")
    raise SystemExit(f"WHOOP GET {path} kept failing after retries.")


def pull_all(env, path, start, end):
    records, next_token = [], None
    while True:
        params = {"limit": 25, "start": start, "end": end}
        if next_token:
            params["nextToken"] = next_token
        page, env = get(env, path, params)
        records.extend(page.get("records", []))
        next_token = page.get("next_token")
        if not next_token:
            return records, env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    args = ap.parse_args()

    env = load_env()
    require(env, "WHOOP_CLIENT_ID", "WHOOP_CLIENT_SECRET")
    if not env.get("WHOOP_ACCESS_TOKEN"):
        raise SystemExit("No WHOOP token yet. Run: python3 stress_report/whoop_auth.py")
    if int(env.get("WHOOP_TOKEN_EXPIRES_AT") or 0) < time.time():
        env = refresh(env)

    now = datetime.now(timezone.utc)
    # One extra day so the first meeting day still has its overnight cycle.
    start = (now - timedelta(days=args.days + 1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name, path in ENDPOINTS.items():
        records, env = pull_all(env, path, start, end)
        (DATA_DIR / f"whoop_{name}.json").write_text(json.dumps(records, indent=1))
        print(f"{name:11s} {len(records):4d} records")

    print(f"Saved to {DATA_DIR}. Next: export heart-rate samples (see README), then run report.py")


if __name__ == "__main__":
    main()
