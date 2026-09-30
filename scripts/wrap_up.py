#!/usr/bin/env python3
"""Ellie end-of-day wrap-up email. Read-only on the vault (the phone sync does the filing); sends one email to Melissa.

Env: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN. DRY_RUN=1 writes wrapup-preview.html instead of sending.
`python scripts/wrap_up.py alert` sends the plain-text failure notice the workflow uses.
"""
import base64, json, os, re, sys
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from briefing_cards import action_card, calendar_action_cards, summary_cards, triage_rows
from wrapup_email import _parse, build_wrapup

NY = ZoneInfo("America/New_York")
ME = "melissaw212@gmail.com"
DRY = os.environ.get("DRY_RUN") == "1"
now = datetime.now(NY)
today = now.strftime("%Y-%m-%d")

creds = Credentials(None, refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"], client_id=os.environ["GOOGLE_CLIENT_ID"],
                    client_secret=os.environ["GOOGLE_CLIENT_SECRET"], token_uri="https://oauth2.googleapis.com/token")
gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)


def send(subject: str, body: str, subtype: str) -> None:
    msg = MIMEText(body, subtype, "utf-8")
    msg["To"], msg["From"], msg["Subject"] = ME, ME, subject
    gmail.users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}).execute()


if sys.argv[1:] == ["alert"]:
    send("ALERT: Ellie wrap-up FAILED - no wrap-up sent",
         "The Ellie wrap-up workflow failed. Your wrap-up was NOT delivered.\n\nRun log:\nhttps://github.com/missophs/Executive-Assistant/actions/workflows/wrap-up.yml\n\n"
         "Likely causes: Google token expired (run scripts/get_google_token.py and update the 3 Google secrets), or a Gmail/Calendar API error.\n", "plain")
    sys.exit(0)

board = open("Task Board.md", encoding="utf-8").read()


def section(prefix: str) -> list[str]:
    m = re.search(rf"^## {re.escape(prefix)}[^\n]*\n(.*?)(?=^## |\Z)", board, re.M | re.S)
    lines = m.group(1).splitlines() if m else []
    return [re.sub(r"^\[[ x]\] ", "", l[2:]).strip() for l in lines if l.startswith("- ") and "(none" not in l]


done_today = [l for l in section("✅ Done") if today in l]
focus = section("🔥 Today") + section("⏭ This Week")
n_backlog = len(section("📋 Backlog"))

# everything put into Ellie today: board captures, Applications/Memory lines the sync writes as "- <date>: text"
filed = [re.sub(r"^\[[ x]\] ", "", l[2:]).split(" — ")[0].strip() for l in board.splitlines() if l.startswith("- ") and f"captured {today}" in l]
for name in ("Applications.md", "Memory.md"):
    filed += [m.group(1).strip() for l in open(name, encoding="utf-8").read().splitlines() for m in [re.match(rf"- {today}: (.+)", l)] if m]
filed = list(dict.fromkeys(filed))


def when(e: dict) -> str:
    s = e["start"].get("dateTime")
    d = datetime.fromisoformat(s).astimezone(NY) if s else datetime.fromisoformat(e["start"]["date"])
    return f"{d.strftime('%a %-m/%-d')} · {d.strftime('%-I:%M%p').lower() if s else 'all day'}"


day0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
try:
    cal = build("calendar", "v3", credentials=creds, cache_discovery=False)
    ahead = cal.events().list(calendarId="primary", timeMin=(day0 + timedelta(days=1)).isoformat(), timeMax=(day0 + timedelta(days=8)).isoformat(),
                              singleEvents=True, orderBy="startTime", timeZone="America/New_York").execute().get("items", [])
    week = [(when(e), e.get("summary", "(no title)")) for e in ahead]
    new = cal.events().list(calendarId="primary", updatedMin=day0.isoformat(), maxResults=100, timeZone="America/New_York").execute().get("items", [])
    # ponytail: "created today, no attendees" = added by her or Ellie, not an invite she received
    cal_added = [f"{e.get('summary', '(no title)')} — {when(e)}" for e in new if e.get("status") != "cancelled" and not e.get("attendees")
                 and datetime.fromisoformat(e["created"].replace("Z", "+00:00")).astimezone(NY).strftime("%Y-%m-%d") == today]
except Exception as exc:  # never claim "clear" when the check failed
    print("calendar failed:", exc)
    week, cal_added = None, []

WAITING_MAX_DAYS = 5  # items older than this stop being reported (Melissa, 2026-09-27) — still tracked in Memory.md, just not surfaced
waiting = [(x.split(" — ")[0][:80], " — ".join(x.split(" — ")[1:])) for x in section("⏳ Waiting On")]
fu = re.search(r"^## Follow-Ups[^\n]*\n(.*?)(?=^## |\Z)", open("Memory.md", encoding="utf-8").read(), re.M | re.S)
for l in (fu.group(1).splitlines() if fu else []):
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    if l.startswith("|") and len(c) >= 4 and c[0] not in ("Item", "---"):
        try:
            age = (now.date() - datetime.strptime(c[2], "%Y-%m-%d").date()).days
        except ValueError:
            age = 0
        if age <= WAITING_MAX_DAYS:
            waiting.append((c[1], f"since {c[2]} — {c[3]}"))

week_end = (now + timedelta(days=7)).strftime("%Y-%m-%d")
reminders = sorted((m.group(1), re.sub(r"^- \[ \] ", "", l).split(" — ")[0]) for l in board.splitlines() if l.startswith("- [ ]")
                   for m in [re.search(r"due (\d{4}-\d{2}-\d{2})", l)] if m and today <= m.group(1) <= week_end)

STAGES = ["Offer", "Final", "Interview", "Screen"]  # open roles with a human in the loop; "Applied" rows are noise here
rows = []
for l in open("Applications.md", encoding="utf-8").read().splitlines():
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    if l.startswith("|") and len(c) >= 6 and c[2] in STAGES:
        rows.append((STAGES.index(c[2]), f"{c[0]} - {c[1]}", f"{c[2]} · last contact {c[4]}: {c[5].replace('**', '')}"))
pipeline = [(t, d) for _, t, d in sorted(rows)]

# --- Inbox Triage / Executive Summary / Action Required (same format as the 7am Daily Briefing, Melissa 2026-09-30)
st = json.load(open(".ellie-state.json")) if os.path.exists(".ellie-state.json") else {}
wrap = st.get("wrap", {}) if st.get("wrap", {}).get("date") == today else {}  # written by the 4:30 phone sync; stale = not today's
mail_rows = [tuple(r) for r in wrap.get("rows", [])]
try:
    n_bin = sum(gmail.users().messages().list(userId="me", q=f"in:{box} newer_than:1d", maxResults=100).execute().get("resultSizeEstimate", 0) for box in ("trash", "spam"))
    cal_events = cal.events().list(calendarId="primary", timeMin=now.isoformat(), timeMax=(day0 + timedelta(days=8)).isoformat(), singleEvents=True,
                                   orderBy="startTime", timeZone="America/New_York").execute().get("items", [])
    cal_cards = calendar_action_cards(cal_events, now)
except Exception as exc:
    print("triage/calendar extras failed:", exc)
    n_bin, cal_cards = 0, []
n_auto = len(wrap.get("trashed", []))
triage = triage_rows([tuple(r) for r in wrap.get("rescued", [])], mail_rows, [(n_auto, "unimportant or always-trash senders")], max(0, n_bin - n_auto)) if (mail_rows or n_bin or n_auto) else None
needs = [r for r in mail_rows if r[0]]
due_soon = [(a, due, why) for t in focus for a, why, due, _ in [_parse(t)] if due and due <= week_end]
risk = (f"{len(needs)} inbox item{'s' if len(needs) != 1 else ''} need your call: {needs[0][1]} — {needs[0][3]}." if needs else "Nothing in your inbox needs you right now.") + \
    f" {n_auto} email{'s' if n_auto != 1 else ''} auto-trashed today."
job = f"{pipeline[0][0]} — {pipeline[0][1]}" if pipeline else "No role at screen stage or later right now."
tmr = [w for w in (week or []) if w[0].startswith((now + timedelta(days=1)).strftime('%a %-m/%-d'))]
cal_txt = (f"Tomorrow: " + " → ".join(f"{w.split(' · ')[-1]} {s}" for w, s in tmr[:6]) + ". " if tmr else "Nothing on the calendar tomorrow. ") + \
    (f"Next deadline: {due_soon[0][0]} (due {due_soon[0][1]})." if due_soon else "")
summary = summary_cards(risk, job, cal_txt.strip())
actions = cal_cards + [action_card("🔵" if due > today else "🔴", a, "Task Board", why or "Open task on your board.", "Finish it or tell Ellie it is done.", due,
                                   "#FF3B3B" if due <= today else "#FFAA00") for a, due, why in due_soon[:8]]
subject, body = build_wrapup(now, done_today, filed, cal_added, focus, n_backlog, waiting, reminders, pipeline, week, triage, summary, actions or None)
assert body.startswith("<table") and "$(" not in body and "/tmp/" not in body, "bad email body"

if DRY:
    open("wrapup-preview.html", "w", encoding="utf-8").write(body)
    print(f"DRY RUN: subject={subject!r} done={len(done_today)} focus={len(focus)} backlog={n_backlog} filed={len(filed)} added={cal_added} week={week}")
    sys.exit(0)

dup = gmail.users().messages().list(userId="me", q=f'in:sent newer_than:1d subject:"{subject}"').execute().get("messages")
if dup:
    print("Wrap-up already sent today, not sending again.")
    sys.exit(0)
send(subject, body, "html")
print(f"Wrap-up sent to {ME}: {subject}")
