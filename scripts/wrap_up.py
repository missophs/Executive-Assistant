#!/usr/bin/env python3
"""Ellie end-of-day wrap-up email. Read-only on the vault (the phone sync does the filing); sends one email to Melissa.

Env: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN. DRY_RUN=1 writes wrapup-preview.html instead of sending.
`python scripts/wrap_up.py alert` sends the plain-text failure notice the workflow uses.
"""
import base64, os, re, sys
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from wrapup_email import build_wrapup

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
n_open = sum(1 for l in board.splitlines() if l.startswith("- [ ]"))

t0 = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
try:
    cal = build("calendar", "v3", credentials=creds, cache_discovery=False)
    items = cal.events().list(calendarId="primary", timeMin=t0.isoformat(), timeMax=(t0 + timedelta(days=1)).isoformat(),
                              singleEvents=True, orderBy="startTime", timeZone="America/New_York").execute().get("items", [])
    tomorrow = [(datetime.fromisoformat(e["start"]["dateTime"]).astimezone(NY).strftime("%-I:%M%p").lower() if e["start"].get("dateTime") else "All day",
                 e.get("summary", "(no title)")) for e in items]
except Exception as exc:  # never claim "clear" when the check failed
    print("tomorrow calendar failed:", exc)
    tomorrow = None

subject, body = build_wrapup(now, done_today, [], focus, n_open, section("⏳ Waiting On"), tomorrow)
assert body.startswith("<table") and "$(" not in body and "/tmp/" not in body, "bad email body"

if DRY:
    open("wrapup-preview.html", "w", encoding="utf-8").write(body)
    print(f"DRY RUN: subject={subject!r} done={len(done_today)} focus={len(focus)} open={n_open} tomorrow={tomorrow}")
    sys.exit(0)

dup = gmail.users().messages().list(userId="me", q=f'in:sent newer_than:1d subject:"{subject}"').execute().get("messages")
if dup:
    print("Wrap-up already sent today, not sending again.")
    sys.exit(0)
send(subject, body, "html")
print(f"Wrap-up sent to {ME}: {subject}")
