# Meeting Stress Report

Ranks your meetings by how much they raise your heart rate above your WHOOP resting baseline.

**Output:** meeting type · person or group · average HR change · number of meetings, most stressful first.

Everything runs on your laptop. The only network calls go to WHOOP's API, to pull your own data. Tokens, heart-rate data, your calendar and the report are all git-ignored.

---

## Read this first: WHOOP's API has no minute-by-minute heart rate

WHOOP's developer API gives **daily summaries only**: resting HR, HRV, average HR per day, sleep, workouts. It does not return a heart-rate reading for 10:00–10:45.

So the tool uses two sources:

| Need | Source |
|---|---|
| Resting baseline per day | WHOOP API (`/v2/recovery`): resting heart rate |
| Day boundaries | WHOOP API (`/v2/cycle`) |
| Workouts to exclude | WHOOP API (`/v2/activity/workout`) |
| Heart rate **during** each meeting | WHOOP's samples in an **Apple Health export**, or any `timestamp,bpm` CSV |

If your WHOOP isn't syncing to Apple Health, turn that on first (step 4) and give it a couple of weeks to build up history.

---

## Setup (about 15 minutes, one time)

### 1. Get the code onto your laptop

```bash
git clone https://github.com/bvastis68/VAG.git && cd VAG
git checkout claude/whoop-calendar-stress-report-rscbkx
python3 -m pip install -r stress_report/requirements.txt
cp .env.example .env
```

You need Python 3.9 or newer.

### 2. Create the WHOOP developer app

1. Go to **developer.whoop.com** and sign in with your WHOOP account.
2. Create a **Team** if asked (any name, e.g. "Personal").
3. **Create App**:
   - **Name:** `Personal Stress Report`
   - **Scopes:** tick `read:recovery`, `read:cycles`, `read:workout`, `read:sleep`, `read:profile`. Also tick `offline` if it's listed (it lets the script refresh access without signing in again).
   - **Redirect URL:** `http://localhost:8765/callback`
   - **Privacy policy URL** (if required): any URL you control. The app is only for you.
4. Save. Copy the **Client ID** and **Client Secret** into `.env`:
   ```
   WHOOP_CLIENT_ID=...
   WHOOP_CLIENT_SECRET=...
   ```
   Paste them into the file only. Never into a chat, email or Slack.

If the portal rejects an `http://localhost` redirect, register `https://localhost/callback`, set `WHOOP_REDIRECT_URI=https://localhost/callback` in `.env`, and use `--manual` in step 3.

### 3. Connect with OAuth

```bash
python3 stress_report/whoop_auth.py
```

Your browser opens WHOOP's consent page. Approve it. The script catches the redirect on `localhost`, swaps the code for tokens and writes them to `.env` with owner-only permissions (`chmod 600`).

With `--manual`: approve, then the browser shows a "can't connect" page. That's expected. Copy the full URL from the address bar and paste it into **the terminal prompt**, not a chat.

Tokens refresh automatically after that. Re-run this step only if you revoke access.

### 4. Turn on WHOOP → Apple Health (if not already on)

WHOOP app → **More → App Settings → Integrations → Apple Health** → allow WHOOP to write **Heart Rate**.

### 5. Fill in who you are

In `.env`:
```
MY_EMAILS=you@yourfirm.com,you@gmail.com
INTERNAL_DOMAINS=yourfirm.com
```
This lets the report skip meetings you declined and label internal versus external meetings.

---

## Each run

```bash
# 1. Pull 30 days of WHOOP baselines, cycles and workouts
python3 stress_report/whoop_pull.py

# 2. Heart-rate samples: iPhone Health app → profile picture → Export All Health Data.
#    AirDrop the zip to the laptop, unzip it into this folder, then:
python3 stress_report/import_hr.py apple_health_export/export.xml

# 3. Google Calendar: calendar.google.com → Settings → Import & export → Export.
#    Unzip and drop your main calendar's .ics into this folder, then:
python3 stress_report/report.py
```

`report.py` uses the newest `.ics` in the folder. Use `--ics path.ics` to pick one.

Useful flags:
- `--min-meetings 3`: hide one-off rows (single meetings are noisy)
- `--days 30`: analysis window
- `--include-solo`: keep calendar blocks that have no other attendees

Results are written to `stress_report/output/`:
- `stress_report.md`: the ranked table
- `stress_by_group.csv`: the same table, ready for Excel
- `meetings_detail.csv`: every meeting with its HR, baseline and change, so you can audit the numbers

---

## How it's calculated

- **Change** = average heart rate during the meeting − WHOOP resting heart rate for that day's cycle. Shown in bpm and %.
- **Person or group:** for a 1:1, the other person's name. For 3+ people, the meeting title. That way a recurring "Team Huddle" groups together.
- **Meeting type:** keyword and email-domain rules in `meeting_types.json`. Edit the rules to match how you title meetings. First matching rule wins.
- **Not counted** (and listed at the bottom of the report): meetings you declined, blocks with nobody else invited, all-day events, meetings that overlap a logged WHOOP workout, days with no scored recovery, and meetings with fewer than 5 heart-rate samples.

**Caveat:** heart rate also moves with caffeine, walking, standing to present and time of day. Trust rows with 3+ meetings. Treat a single meeting as an anecdote.

## Privacy

- `.env`, `*.ics`, the Apple Health export, `stress_report/data/` and `stress_report/output/` are all in `.gitignore`. Run `git status` before any commit to confirm.
- The scripts send nothing anywhere except WHOOP's own API (`api.prod.whoop.com`), to pull your data.
- To revoke access: delete the app at developer.whoop.com and clear the token lines in `.env`.

## Tests

```bash
python3 -m unittest discover -s stress_report/tests
```
Runs on synthetic data only.
