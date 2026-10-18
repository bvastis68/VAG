"""End-to-end check on synthetic data. Run: python3 -m unittest discover stress_report/tests"""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC))

from ics_parser import load_meetings  # noqa: E402

UTC = timezone.utc


def ics_time(dt):
    return dt.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


def build_ics(day0):
    """Weekly team huddle (one week moved, one cancelled), a client review, a declined call, a focus block."""
    huddle = day0.replace(hour=14)
    review = (day0 + timedelta(days=2)).replace(hour=15)
    declined = (day0 + timedelta(days=3)).replace(hour=16)
    moved_orig = huddle + timedelta(weeks=1)
    skipped = huddle + timedelta(weeks=2)
    me = "ATTENDEE;CN=Me;PARTSTAT=ACCEPTED:mailto:me@firm.com"
    return "\r\n".join([
        "BEGIN:VCALENDAR",
        "BEGIN:VEVENT", "UID:huddle", f"DTSTART:{ics_time(huddle)}", f"DTEND:{ics_time(huddle + timedelta(minutes=30))}",
        "RRULE:FREQ=WEEKLY;COUNT=4", f"EXDATE:{ics_time(skipped)}", "SUMMARY:Team Huddle", me,
        "ATTENDEE;CN=Sydney;PARTSTAT=ACCEPTED:mailto:sydney@firm.com",
        "ATTENDEE;CN=Jason;PARTSTAT=ACCEPTED:mailto:jason@firm.com", "END:VEVENT",
        "BEGIN:VEVENT", "UID:huddle", f"RECURRENCE-ID:{ics_time(moved_orig)}",
        f"DTSTART:{ics_time(moved_orig + timedelta(hours=1))}", f"DTEND:{ics_time(moved_orig + timedelta(hours=1, minutes=30))}",
        "SUMMARY:Team Huddle", me, "ATTENDEE;CN=Sydney;PARTSTAT=ACCEPTED:mailto:sydney@firm.com",
        "ATTENDEE;CN=Jason;PARTSTAT=ACCEPTED:mailto:jason@firm.com", "END:VEVENT",
        "BEGIN:VEVENT", "UID:review", f"DTSTART:{ics_time(review)}", "DURATION:PT1H",
        "SUMMARY:Annual portfolio review", me,
        'ATTENDEE;CN="Smith, Pat";PARTSTAT=ACCEPTED:mailto:pat@client.com', "END:VEVENT",
        "BEGIN:VEVENT", "UID:declined", f"DTSTART:{ics_time(declined)}", f"DTEND:{ics_time(declined + timedelta(hours=1))}",
        "SUMMARY:Vendor pitch", "ATTENDEE;CN=Me;PARTSTAT=DECLINED:mailto:me@firm.com",
        "ATTENDEE;CN=Vendor;PARTSTAT=ACCEPTED:mailto:v@vendor.com", "END:VEVENT",
        "BEGIN:VEVENT", "UID:focus", f"DTSTART:{ics_time(review + timedelta(hours=2))}",
        f"DTEND:{ics_time(review + timedelta(hours=3))}", "SUMMARY:Focus time", "END:VEVENT",
        "END:VCALENDAR",
    ])


class PipelineTest(unittest.TestCase):
    def test_recurrence_overrides_and_exdates(self):
        day0 = (datetime.now(UTC) - timedelta(days=25)).replace(minute=0, second=0, microsecond=0)
        with tempfile.NamedTemporaryFile("w", suffix=".ics", delete=False) as fh:
            fh.write(build_ics(day0))
        ms = load_meetings(fh.name, day0 - timedelta(days=1), datetime.now(UTC))
        huddles = sorted(m.start for m in ms if m.summary == "Team Huddle")
        self.assertEqual(len(huddles), 3)  # 4 weekly, 1 excluded, 1 moved (still counted once)
        self.assertIn(day0.replace(hour=15) + timedelta(weeks=1), huddles)
        review = next(m for m in ms if m.uid == "review")
        self.assertEqual(review.end - review.start, timedelta(hours=1))
        self.assertEqual(review.attendees[1].name, "Smith, Pat")

    def test_report_end_to_end(self):
        day0 = (datetime.now(UTC) - timedelta(days=25)).replace(minute=0, second=0, microsecond=0)
        review_start = (day0 + timedelta(days=2)).replace(hour=15)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pkg = root / "stress_report"
            subprocess.run(["cp", "-r", str(SRC), str(pkg)], check=True)
            data = pkg / "data"
            data.mkdir(exist_ok=True)
            (root / "cal.ics").write_text(build_ics(day0))
            (root / ".env").write_text("MY_EMAILS=me@firm.com\nINTERNAL_DOMAINS=firm.com\n")

            cycles, recoveries, samples = [], [], []
            for d in range(-1, 27):
                start = (day0 + timedelta(days=d)).replace(hour=4)
                cycles.append({"id": d + 100, "start": start.isoformat(), "end": (start + timedelta(days=1)).isoformat()})
                recoveries.append({"cycle_id": d + 100, "score_state": "SCORED", "score": {"resting_heart_rate": 55}})
            t = day0 - timedelta(days=1)
            while t < datetime.now(UTC):
                bpm = 65
                if review_start <= t < review_start + timedelta(hours=1):
                    bpm = 85
                samples.append((t.isoformat(), bpm))
                t += timedelta(minutes=1)
            (data / "whoop_cycles.json").write_text(json.dumps(cycles))
            (data / "whoop_recoveries.json").write_text(json.dumps(recoveries))
            (data / "whoop_workouts.json").write_text("[]")
            with open(data / "hr_samples.csv", "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["timestamp_utc", "bpm"])
                w.writerows(samples)

            out = subprocess.run(
                [sys.executable, str(pkg / "report.py"), "--ics", str(root / "cal.ics")],
                capture_output=True, text=True, check=True,
            ).stdout
            with open(pkg / "output" / "stress_by_group.csv", newline="") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(rows[0]["type"], "Client review")
            self.assertEqual(rows[0]["who"], "Smith, Pat")
            self.assertEqual(float(rows[0]["change_bpm"]), 30.0)
            self.assertEqual(rows[1]["who"], "Group: Team Huddle")
            self.assertEqual(int(rows[1]["meetings"]), 3)
            self.assertIn("1 declined", out)
            self.assertIn("1 no other attendees", out)


if __name__ == "__main__":
    unittest.main()
