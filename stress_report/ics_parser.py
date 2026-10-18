"""Minimal .ics reader for a Google Calendar export: events, attendees, recurring series."""
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from dateutil.rrule import rrulestr


@dataclass
class Attendee:
    email: str
    name: str
    status: str  # ACCEPTED, DECLINED, TENTATIVE, NEEDS-ACTION


@dataclass
class Meeting:
    uid: str
    summary: str
    start: datetime  # always timezone-aware
    end: datetime
    attendees: list = field(default_factory=list)
    organizer: str = ""
    status: str = "CONFIRMED"


def _unfold(text):
    lines = []
    for raw in text.replace("\r\n", "\n").split("\n"):
        if raw[:1] in (" ", "\t") and lines:
            lines[-1] += raw[1:]
        else:
            lines.append(raw)
    return lines


def _split(line):
    """'DTSTART;TZID=America/Toronto:20261001T090000' -> ('DTSTART', {'TZID': ...}, value)."""
    head, value, in_quotes = line, "", False
    for i, ch in enumerate(line):
        if ch == '"':
            in_quotes = not in_quotes
        elif ch == ":" and not in_quotes:
            head, value = line[:i], line[i + 1:]
            break
    parts = head.split(";")
    params = {}
    for p in parts[1:]:
        k, _, v = p.partition("=")
        params[k.upper()] = v.strip('"')
    return parts[0].upper(), params, value


def _unescape(value):
    return value.replace("\\n", " ").replace("\\,", ",").replace("\\;", ";").replace("\\\\", "\\").strip()


def _parse_dt(value, params, default_tz):
    if params.get("VALUE") == "DATE" or (len(value) == 8 and value.isdigit()):
        return date(int(value[:4]), int(value[4:6]), int(value[6:8]))
    if value.endswith("Z"):
        return datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    naive = datetime.strptime(value, "%Y%m%dT%H%M%S")
    tz = params.get("TZID")
    try:
        return naive.replace(tzinfo=ZoneInfo(tz) if tz else default_tz)
    except Exception:
        return naive.replace(tzinfo=default_tz)


def _email(value):
    return value.split(":", 1)[1].strip().lower() if value.lower().startswith("mailto:") else value.strip().lower()


def _read_events(text, default_tz):
    events, cur = [], None
    for line in _unfold(text):
        if line == "BEGIN:VEVENT":
            cur = {"attendees": [], "exdates": [], "props": {}}
            continue
        if line == "END:VEVENT":
            events.append(cur)
            cur = None
            continue
        if cur is None or ":" not in line:
            continue
        name, params, value = _split(line)
        if name == "ATTENDEE":
            cur["attendees"].append(Attendee(
                email=_email(value),
                name=_unescape(params.get("CN", "")) or _email(value),
                status=params.get("PARTSTAT", "NEEDS-ACTION").upper(),
            ))
        elif name == "ORGANIZER":
            cur["props"]["ORGANIZER"] = _email(value)
        elif name == "EXDATE":
            for v in value.split(","):
                cur["exdates"].append(_parse_dt(v, params, default_tz))
        elif name in ("DTSTART", "DTEND", "RECURRENCE-ID"):
            cur["props"][name] = _parse_dt(value, params, default_tz)
        elif name == "DURATION":
            cur["props"][name] = value
        else:
            cur["props"][name] = value
    return events


def _duration(text):
    # Enough of RFC 5545 durations for calendar exports: PT1H30M, P1D, PT45M
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-P")
    days = hours = mins = secs = 0
    num, in_time = "", False
    for ch in text:
        if ch == "T":
            in_time = True
        elif ch.isdigit():
            num += ch
        else:
            n = int(num or 0)
            num = ""
            if ch == "W":
                days += 7 * n
            elif ch == "D":
                days += n
            elif ch == "H":
                hours += n
            elif ch == "M" and in_time:
                mins += n
            elif ch == "S":
                secs += n
    return sign * timedelta(days=days, hours=hours, minutes=mins, seconds=secs)


def load_meetings(path, window_start, window_end, default_tz=None):
    """Return timed meetings overlapping [window_start, window_end), recurring series expanded.

    All-day events are dropped: they aren't meetings.
    """
    default_tz = default_tz or datetime.now().astimezone().tzinfo
    with open(path, encoding="utf-8", errors="replace") as fh:
        raw = _read_events(fh.read(), default_tz)

    overrides = {}  # (uid, original start) -> event that replaces that occurrence
    for ev in raw:
        rid = ev["props"].get("RECURRENCE-ID")
        if isinstance(rid, datetime):
            overrides[(ev["props"].get("UID"), rid.astimezone(timezone.utc))] = ev

    meetings = []
    for ev in raw:
        p = ev["props"]
        start = p.get("DTSTART")
        if not isinstance(start, datetime):
            continue  # all-day or malformed
        if "DTEND" in p and isinstance(p["DTEND"], datetime):
            length = p["DTEND"] - start
        elif "DURATION" in p:
            length = _duration(p["DURATION"])
        else:
            length = timedelta(0)
        if length <= timedelta(0):
            continue

        uid = p.get("UID", "")
        if "RRULE" in p and "RECURRENCE-ID" not in p:
            rule = rrulestr(p["RRULE"], dtstart=start, unfold=True, forceset=True)
            for ex in ev["exdates"]:
                if isinstance(ex, datetime):
                    rule.exdate(ex)
            occurrences = rule.between(window_start - length, window_end, inc=True)
            for occ in occurrences:
                if (uid, occ.astimezone(timezone.utc)) in overrides:
                    continue  # the override event carries this occurrence
                meetings.append(_to_meeting(ev, occ, occ + length))
        else:
            end = start + length
            if end > window_start and start < window_end:
                meetings.append(_to_meeting(ev, start, end))
    return [m for m in meetings if m.status != "CANCELLED"]


def _to_meeting(ev, start, end):
    p = ev["props"]
    return Meeting(
        uid=p.get("UID", ""),
        summary=_unescape(p.get("SUMMARY", "(no title)")),
        start=start,
        end=end,
        attendees=list(ev["attendees"]),
        organizer=p.get("ORGANIZER", ""),
        status=p.get("STATUS", "CONFIRMED").upper(),
    )
