"""Match WHOOP heart rate to calendar meetings and rank what stresses you most.

For each meeting: average heart rate during the meeting minus that day's WHOOP
resting heart rate. Grouped by meeting type and person/group, most stressful first.

Usage:
    python3 stress_report/report.py                       # uses the newest .ics in the repo folder
    python3 stress_report/report.py --ics calendar.ics --days 30 --min-meetings 2
"""
import argparse
import bisect
import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean

from envfile import DATA_DIR, OUTPUT_DIR, ROOT, load_env
from ics_parser import load_meetings

HERE = Path(__file__).resolve().parent
ROOM_MARKERS = ("resource.calendar.google.com", "@group.calendar.google.com")


def parse_ts(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


# ---------- inputs ----------

def load_whoop():
    def read(name):
        path = DATA_DIR / f"whoop_{name}.json"
        if not path.exists():
            raise SystemExit(f"Missing {path}. Run: python3 stress_report/whoop_pull.py")
        return json.loads(path.read_text())

    now = datetime.now(timezone.utc)
    cycles = sorted(
        (parse_ts(c["start"]), parse_ts(c["end"]) if c.get("end") else now, c["id"]) for c in read("cycles")
    )
    rhr_by_cycle = {
        r["cycle_id"]: r["score"]["resting_heart_rate"]
        for r in read("recoveries")
        if r.get("score_state") == "SCORED" and r.get("score")
    }
    workouts = [(parse_ts(w["start"]), parse_ts(w["end"])) for w in read("workouts") if w.get("end")]
    return cycles, rhr_by_cycle, workouts


def load_hr():
    path = DATA_DIR / "hr_samples.csv"
    if not path.exists():
        raise SystemExit(
            f"Missing {path}. WHOOP's API has no minute-level heart rate, so import it first:\n"
            "  python3 stress_report/import_hr.py apple_health_export/export.xml"
        )
    times, bpms = [], []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            times.append(parse_ts(row["timestamp_utc"]))
            bpms.append(float(row["bpm"]))
    return times, bpms


def find_ics(arg):
    if arg:
        return Path(arg)
    found = sorted(list(ROOT.glob("*.ics")) + list(HERE.glob("*.ics")), key=lambda p: p.stat().st_mtime)
    if not found:
        raise SystemExit(f"No .ics file found. Export Google Calendar and drop the .ics into {ROOT}")
    return found[-1]


# ---------- classification ----------

def domain(email):
    return email.rsplit("@", 1)[-1] if "@" in email else ""


def others_in(meeting, me):
    return [
        a for a in meeting.attendees
        if a.email not in me and not any(m in a.email for m in ROOM_MARKERS) and a.status != "DECLINED"
    ]


def classify(meeting, others, rules, internal_domains):
    title = meeting.summary.lower()
    other_domains = {domain(a.email) for a in others}
    for rule in rules["rules"]:
        if any(k in title for k in rule.get("keywords", [])) or other_domains & set(rule.get("domains", [])):
            return rule["type"]
    all_internal = internal_domains and other_domains <= internal_domains
    if all_internal:
        return rules["fallback_internal_1on1"] if len(others) == 1 else rules["fallback_internal_group"]
    return rules["fallback_external"]


def who(meeting, others):
    if len(others) == 1:
        return others[0].name
    return f"Group: {meeting.summary}"


# ---------- per-meeting math ----------

def cycle_for(ts, cycles):
    i = bisect.bisect_right([c[0] for c in cycles], ts) - 1
    if i >= 0 and cycles[i][0] <= ts < cycles[i][1]:
        return cycles[i][2]
    return None


def avg_hr(start, end, times, bpms):
    lo = bisect.bisect_left(times, start)
    hi = bisect.bisect_left(times, end)
    window = bpms[lo:hi]
    return (mean(window), len(window)) if window else (None, 0)


def overlaps(start, end, spans):
    return any(s < end and start < e for s, e in spans)


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ics", help="path to the Google Calendar .ics export")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--min-samples", type=int, default=5, help="heart-rate samples needed per meeting")
    ap.add_argument("--min-meetings", type=int, default=1, help="hide rows with fewer meetings")
    ap.add_argument("--include-solo", action="store_true", help="keep events with no other attendees")
    args = ap.parse_args()

    env = load_env()
    me = {e.strip().lower() for e in env.get("MY_EMAILS", "").split(",") if e.strip()}
    internal = {d.strip().lower() for d in env.get("INTERNAL_DOMAINS", "").split(",") if d.strip()}
    rules = json.loads((HERE / "meeting_types.json").read_text())

    cycles, rhr_by_cycle, workouts = load_whoop()
    times, bpms = load_hr()
    ics = find_ics(args.ics)

    window_end = datetime.now(timezone.utc)
    window_start = window_end - timedelta(days=args.days)
    meetings = load_meetings(ics, window_start, window_end)

    skipped = defaultdict(int)
    detail = []
    for m in sorted(meetings, key=lambda m: m.start):
        mine = [a for a in m.attendees if a.email in me]
        if any(a.status == "DECLINED" for a in mine):
            skipped["declined"] += 1
            continue
        others = others_in(m, me)
        if not others and not args.include_solo:
            skipped["no other attendees (focus/blocks)"] += 1
            continue
        if overlaps(m.start, m.end, workouts):
            skipped["overlaps a WHOOP workout"] += 1
            continue
        cycle_id = cycle_for(m.start, cycles)
        rhr = rhr_by_cycle.get(cycle_id)
        if rhr is None:
            skipped["no scored WHOOP recovery that day"] += 1
            continue
        hr, n = avg_hr(m.start, m.end, times, bpms)
        if n < args.min_samples:
            skipped["not enough heart-rate samples"] += 1
            continue
        detail.append({
            "date": m.start.astimezone().strftime("%Y-%m-%d %H:%M"),
            "title": m.summary,
            "type": classify(m, others, rules, internal),
            "who": who(m, others) if others else "Solo",
            "minutes": int((m.end - m.start).total_seconds() // 60),
            "avg_hr": round(hr, 1),
            "resting_hr": rhr,
            "change_bpm": round(hr - rhr, 1),
            "change_pct": round(100 * (hr - rhr) / rhr, 1),
            "samples": n,
        })

    if not detail:
        print("No meetings could be matched to heart-rate data.")
        for reason, count in skipped.items():
            print(f"  skipped {count:3d}: {reason}")
        return

    groups = defaultdict(list)
    for d in detail:
        groups[(d["type"], d["who"])].append(d)
    table = sorted(
        (
            {
                "type": t,
                "who": w,
                "change_bpm": round(mean(x["change_bpm"] for x in rows), 1),
                "change_pct": round(mean(x["change_pct"] for x in rows), 1),
                "meetings": len(rows),
            }
            for (t, w), rows in groups.items()
            if len(rows) >= args.min_meetings
        ),
        key=lambda r: r["change_bpm"],
        reverse=True,
    )

    by_type = defaultdict(list)
    for d in detail:
        by_type[d["type"]].append(d["change_bpm"])

    lines = [
        "# Meeting Stress Report",
        "",
        f"Window: last {args.days} days · Calendar: `{ics.name}` · Meetings matched: {len(detail)}",
        "",
        f"Heart-rate change = average HR during the meeting minus WHOOP resting HR for that day.",
        "",
        "| Rank | Meeting type | Person or group | Avg HR change | Meetings |",
        "|---:|---|---|---:|---:|",
    ]
    for i, r in enumerate(table, 1):
        lines.append(
            f"| {i} | {r['type']} | {r['who']} | {r['change_bpm']:+.1f} bpm ({r['change_pct']:+.0f}%) | {r['meetings']} |"
        )
    lines += ["", "## By meeting type", "", "| Meeting type | Avg HR change | Meetings |", "|---|---:|---:|"]
    for t, vals in sorted(by_type.items(), key=lambda kv: mean(kv[1]), reverse=True):
        lines.append(f"| {t} | {mean(vals):+.1f} bpm | {len(vals)} |")
    if skipped:
        lines += ["", "## Not counted", ""]
        lines += [f"- {count} {reason}" for reason, count in sorted(skipped.items(), key=lambda kv: -kv[1])]
    lines += [
        "",
        "_Heart rate rises with posture, caffeine, walking between rooms and time of day, not only stress. "
        "Treat single meetings as noise; look at rows with 3+ meetings._",
    ]
    report = "\n".join(lines) + "\n"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "stress_report.md").write_text(report)
    for name, rows in (("stress_by_group.csv", table), ("meetings_detail.csv", detail)):
        with open(OUTPUT_DIR / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    print(report)
    print(f"Saved: {OUTPUT_DIR / 'stress_report.md'}, stress_by_group.csv, meetings_detail.csv")


if __name__ == "__main__":
    main()
