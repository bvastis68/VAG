"""Import minute-level heart-rate samples into stress_report/data/hr_samples.csv.

The WHOOP API only returns daily summaries, so per-meeting heart rate comes from
WHOOP's samples in an Apple Health export, or from any CSV of timestamp,bpm.

Usage:
    python3 stress_report/import_hr.py apple_health_export/export.xml
    python3 stress_report/import_hr.py my_hr.csv          # columns: timestamp,bpm (ISO 8601)
    python3 stress_report/import_hr.py export.xml --all-sources   # keep non-WHOOP samples too
"""
import argparse
import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

from envfile import DATA_DIR

HR_TYPE = "HKQuantityTypeIdentifierHeartRate"


def parse_apple_date(text):
    # Apple Health format: "2026-10-01 09:15:00 -0400"
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S %z")


def from_apple_health(path, since, all_sources):
    """Stream the XML (it can be several GB) and keep only heart-rate records."""
    for _, elem in ET.iterparse(path, events=("end",)):
        if elem.tag != "Record":
            continue
        if elem.get("type") == HR_TYPE:
            source = elem.get("sourceName", "")
            if all_sources or "whoop" in source.lower():
                ts = parse_apple_date(elem.get("startDate"))
                if ts >= since:
                    yield ts, float(elem.get("value"))
        elem.clear()


def from_csv(path, since):
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            ts = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
            if ts.tzinfo is None:
                ts = ts.astimezone()  # treat naive times as this laptop's local zone
            if ts >= since:
                yield ts, float(row["bpm"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="Apple Health export.xml or a timestamp,bpm CSV")
    ap.add_argument("--days", type=int, default=31)
    ap.add_argument("--all-sources", action="store_true", help="Apple Health: keep non-WHOOP heart-rate samples")
    args = ap.parse_args()

    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    if args.source.lower().endswith(".xml"):
        samples = from_apple_health(args.source, since, args.all_sources)
    else:
        samples = from_csv(args.source, since)

    rows = sorted((ts.astimezone(timezone.utc), bpm) for ts, bpm in samples)
    if not rows:
        hint = "" if args.all_sources else " Try --all-sources if WHOOP isn't listed as the source."
        raise SystemExit(f"No heart-rate samples found in the last {args.days} days.{hint}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / "hr_samples.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["timestamp_utc", "bpm"])
        for ts, bpm in rows:
            w.writerow([ts.isoformat(), bpm])
    span_days = (rows[-1][0] - rows[0][0]).total_seconds() / 86400
    print(f"Saved {len(rows):,} samples over {span_days:.1f} days to {out}")


if __name__ == "__main__":
    main()
