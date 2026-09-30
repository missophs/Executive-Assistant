#!/usr/bin/env python3
"""Ellie morning email: one send, replacing 'Melissa Daily Briefing' (missophs/daily-briefing) and
the old paused 'Ellie — Morning Standup' cloud routine. Reads the vault (read-only, the phone sync
does the filing), triages the inbox and rescues from Trash the same way phone_sync.py does, reads
the 7-day calendar, and sends one email built by morning_briefing_email.py.

Env: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN, ANTHROPIC_API_KEY (optional —
falls back to no AI triage/rescue if missing, same as phone_sync.py). DRY_RUN=1 writes
morning-preview.html instead of sending and changes nothing in Gmail.
`python scripts/morning_briefing.py alert` sends the plain-text failure notice the workflow uses.
"""
import base64, json, os, re, sys
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from briefing_cards import REVIEW_CATS, calendar_action_cards, rich_events
from morning_briefing_email import CATS, build_morning

NY = ZoneInfo("America/New_York")
DRY = os.environ.get("DRY_RUN") == "1"
ME = "melissaw212@gmail.com"
STATE = ".morning-briefing-state.json"  # separate from .ellie-state.json (phone_sync.py's) so the two workflows never race on the same file
now = datetime.now(NY)
today = now.strftime("%Y-%m-%d")

creds = Credentials(None, refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"], client_id=os.environ["GOOGLE_CLIENT_ID"],
                    client_secret=os.environ["GOOGLE_CLIENT_SECRET"], token_uri="https://oauth2.googleapis.com/token")
gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)
cal = build("calendar", "v3", credentials=creds, cache_discovery=False)


def send(subject: str, body: str, subtype: str) -> None:
    msg = MIMEText(body, subtype, "utf-8")
    msg["To"], msg["From"], msg["Subject"] = ME, ME, subject
    gmail.users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}).execute()


if sys.argv[1:] == ["alert"]:
    send("ALERT: Ellie morning email FAILED - nothing sent",
         "The Ellie morning-briefing workflow failed. Your morning email was NOT delivered.\n\nRun log:\n"
         "https://github.com/missophs/Executive-Assistant/actions/workflows/morning-briefing.yml\n\n"
         "Likely causes: Google token expired (run scripts/get_google_token.py and update the 3 Google secrets), "
         "or a Gmail/Calendar API error. The Melissa Daily Briefing email (missophs/daily-briefing) is unaffected.\n", "plain")
    sys.exit(0)


def read(path: str) -> str:
    return open(path, encoding="utf-8").read()


def bullets(md: str, heading: str) -> list[str]:
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    return [l[2:].strip().lower() for l in (m.group(1).splitlines() if m else []) if l.startswith("- ") and l[2:].strip()]


def section(md: str, prefix: str) -> list[str]:
    m = re.search(rf"^## {re.escape(prefix)}[^\n]*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    lines = m.group(1).splitlines() if m else []
    return [re.sub(r"^\[[ x]\] ", "", l[2:]).strip() for l in lines if l.startswith("- ") and "(none" not in l]


state = json.load(open(STATE)) if os.path.exists(STATE) else {}
usage = {"in": 0, "out": 0}


def ask_haiku(prompt: str, max_tokens: int) -> str:
    import urllib.request
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", method="POST", data=json.dumps({
        "model": "claude-haiku-4-5-20251001", "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"})
    resp = json.load(urllib.request.urlopen(req, timeout=60))
    usage["in"] += resp["usage"]["input_tokens"]
    usage["out"] += resp["usage"]["output_tokens"]
    return resp["content"][0]["text"]


# --- vault
board = read("Task Board.md")
apps = read("Applications.md")
memory = read("Memory.md")
rules = read("routines/trash-rules.md")

protected = bullets(rules, "PROTECTED (never trash)")
never_subj = bullets(rules, "NEVER TRASH if subject/snippet mentions")
always_l = bullets(rules, "ALWAYS TRASH (sender contains)")
dnr_m = re.search(r"^## Do Not Rescue[^\n]*\n(.*?)(?=^## |\Z)", memory, re.M | re.S)
do_not_rescue = [c[0].lower() for l in (dnr_m.group(1).splitlines() if dnr_m else []) if l.startswith("|")
                 for c in [[x.strip() for x in l.strip().strip("|").split("|")]] if c and c[0] not in ("Sender / domain", "---") and not c[0].startswith("-")]

# --- inbox triage + full-day review (own cache; deliberately not phone_sync.py's .ellie-state.json — see STATE comment above)
# Every email from the last day (inbox, archived, Trash, Spam) is sorted into one category so the email can account for all of them.
mail_cache = state.setdefault("mail", {})  # thread id -> [needs, line, reply, why, category]
allmail: list[tuple[str, str, str, str, str]] = []  # (thread id, from, subject, snippet, location)
kept: list[tuple[str, str, str, str, str]] = []  # the inbox subset, same shape
protected_ids: set[str] = set()
for t in gmail.users().threads().list(userId="me", maxResults=100, q="in:anywhere newer_than:1d -in:sent -in:drafts -from:me").execute().get("threads", []):
    th = gmail.users().threads().get(userId="me", id=t["id"], format="metadata", metadataHeaders=["From", "Subject"]).execute()
    hd = {h["name"]: h["value"] for h in th["messages"][0]["payload"]["headers"]}
    frm, subj = hd.get("From", "").lower(), hd.get("Subject", "")
    labels = set(th["messages"][-1].get("labelIds", []))
    loc = "trash" if "TRASH" in labels else "spam" if "SPAM" in labels else "inbox" if "INBOX" in labels else "other"
    row = (t["id"], hd.get("From", ""), subj, th["messages"][0].get("snippet", ""), loc)
    allmail.append(row)
    if loc != "inbox":
        continue
    hay = f"{subj} {row[3]}".lower()
    if any(p in frm for p in protected) or any(n in hay for n in never_subj):
        protected_ids.add(t["id"])
        kept.append(row)
        continue
    if any(a in frm for a in always_l):
        continue  # deterministic always-trash senders are handled by the wrap-up/phone-sync triage already; this email only reports, it never trashes a protected/never list
    kept.append(row)

fresh = [k for k in allmail if len(mail_cache.get(k[0], [])) < 5 or (mail_cache[k[0]][4] in REVIEW_CATS and len(mail_cache[k[0]]) < 7)]  # review mail also needs next step + due
if fresh and os.environ.get("ANTHROPIC_API_KEY"):
    where = {"inbox": "in inbox", "trash": "in Trash", "spam": "in Spam", "other": "archived"}
    for i in range(0, len(fresh), 40):
        chunk = fresh[i:i + 40]
        try:
            out = ask_haiku(f"Today is {today}. Melissa is a senior HR executive job searching. For each email return a JSON array, same order: "
                            '{"i":<n>,"needs":true|false,"reply":true|false,"cat":"<one category>","line":"one plain line, max 14 words, what it is and any amount or deadline",'
                            '"why":"if reply=true, one short line on why a reply is owed and to whom, else empty",'
                            '"next":"if cat is Financial / Billing, Security / Risk or Medical / Health: the concrete next step in one sentence (what to open, click, pay, save or confirm), else empty",'
                            '"due":"if cat is one of those: when it is due, e.g. Today, This week, Within 7 days, By Friday, October 30, 2026 (use a real deadline from the email if it has one), else empty"}. '
                            "Financial / Billing also covers bank, card, brokerage and investment notices, tax and statement mail, and orders, returns or deliveries with a deadline. "
                            f"cat must be exactly one of: {' | '.join(CATS)}. Phishing / Scam = fake or spoofed senders, fake payment or account threats. Security / Risk = REAL alerts from her banks, accounts or logins. "
                            "needs=true ONLY when a real person is waiting on her, a recruiter or interviewer wrote directly, there is a hard deadline, or a security or money problem, and the email is in her inbox. Automated job alerts, job digests, newsletters, receipts, statements, promos and deposits are needs=false. "
                            "reply=true ONLY when a real person (recruiter, interviewer, hiring manager, networking contact) is owed a reply from Melissa and no automated sender, and the email is in her inbox. Never invent facts. JSON only.\n\n" +
                            "\n".join(f"{n}. ({where[k[4]]}) From: {k[1][:60]} | Subject: {k[2][:90]} | {k[3][:160]}" for n, k in enumerate(chunk, 1)), 4000)
            for r in json.loads(out[out.index("["):out.rindex("]") + 1]):
                if 1 <= r.get("i", 0) <= len(chunk):
                    k = chunk[r["i"] - 1]
                    inbox_ = k[4] == "inbox"
                    mail_cache[k[0]] = [bool(r.get("needs")) and inbox_, str(r.get("line", ""))[:140], bool(r.get("reply")) and inbox_,
                                        str(r.get("why", ""))[:160], r.get("cat") if r.get("cat") in CATS else "Other",
                                        str(r.get("next", ""))[:200], str(r.get("due", ""))[:60]]
        except Exception as exc:
            print("AI mail triage failed:", exc)
for k in allmail:
    c = mail_cache.get(k[0])
    if not c:
        mail_cache[k[0]] = [False, "", False, "", "Other"]
    elif len(c) < 5:
        c.append("Other")
inbox_rows = [(mail_cache[k[0]][0], re.sub(r"<.*?>|\"", "", k[1]).split("@")[0][:40], k[2][:80], mail_cache[k[0]][1] or k[3][:120]) for k in kept]
inbox_rows.sort(key=lambda r: not r[0])
draft_candidates = [(re.sub(r"<.*?>|\"", "", k[1]).split("@")[0][:40], k[2][:100], mail_cache[k[0]][3])
                    for k in kept if mail_cache[k[0]][2] and k[0] not in protected_ids][:5]
for k in list(mail_cache)[:-300]:
    del mail_cache[k]

# --- rescue from trash: same high bar as phone_sync.py. Report only — this email never trashes.
rescued: list[tuple[str, str]] = []
rescued_ids: set[str] = set()
judged = set(state.get("trashjudged", []))
try:
    cands = []
    for t in gmail.users().threads().list(userId="me", maxResults=50, q='in:trash newer_than:3d (interview OR invitation OR calendly OR schedule OR scheduling OR availability OR "next steps" OR offer OR recruiter OR "speak with" OR hiring OR "your application")').execute().get("threads", []):
        if t["id"] in judged:
            continue
        th = gmail.users().threads().get(userId="me", id=t["id"], format="metadata", metadataHeaders=["From", "Subject", "List-Unsubscribe"]).execute()
        hd = {h_["name"]: h_["value"] for h_ in th["messages"][0]["payload"]["headers"]}
        frm = hd.get("From", "")
        judged.add(t["id"])
        if any(x in frm.lower() for x in ("no-reply", "noreply", "donotreply", "do-not-reply")) or "List-Unsubscribe" in hd or any(d in frm.lower() for d in do_not_rescue if d) or any(a in frm.lower() for a in always_l):
            continue
        cands.append((t["id"], frm, hd.get("Subject", ""), th["messages"][0].get("snippet", "")))
    if cands and os.environ.get("ANTHROPIC_API_KEY"):
        out = ask_haiku(f"Today is {today}. Melissa is a senior HR executive job searching. These emails are in her Trash. For each return a JSON array, same order: "
                        '{"i":<n>,"rescue":true|false}. rescue=true ONLY when a real person (recruiter, interviewer, hiring manager, networking contact) or a real applicant-tracking system wrote to her specifically about a real role, application, interview or meeting involving her. '
                        "rescue=false for marketing, newsletters, bulk job digests, retail, receipts, automated acknowledgments, spam, or anything you are unsure about. JSON only.\n\n" +
                        "\n".join(f"{n}. From: {f[:60]} | Subject: {sb[:90]} | {sn[:160]}" for n, (_, f, sb, sn) in enumerate(cands, 1)), 800)
        for r in json.loads(out[out.index("["):out.rindex("]") + 1]):
            if r.get("rescue") is True and 1 <= r.get("i", 0) <= len(cands):
                k = cands[r["i"] - 1]
                if not DRY:
                    gmail.users().threads().modify(userId="me", id=k[0], body={"addLabelIds": ["INBOX", "STARRED", "IMPORTANT"], "removeLabelIds": ["TRASH"]}).execute()
                rescued_ids.add(k[0])
                rescued.append((re.sub(r".*<|>.*", "", k[1]).strip() or k[1], k[2]))
except Exception as exc:
    print("trash rescue failed:", exc)
state["trashjudged"] = sorted(judged)[-300:]

# --- financial / security / medical / order mail that landed in Trash: Ellie brings it back herself (Melissa, 2026-09-30: "ellie should be doing that").
# Never the same thread twice (if she trashes it again that is her call), never Do Not Rescue / always-trash senders, never the Phishing category.
fin_done = set(state.get("fin_rescued", []))
for k in allmail:
    c = mail_cache[k[0]]
    if (k[4] == "trash" and len(c) >= 5 and c[4] in REVIEW_CATS and k[0] not in fin_done and k[0] not in rescued_ids
            and not any(d in k[1].lower() for d in do_not_rescue + always_l if d)):
        if not DRY:
            gmail.users().threads().modify(userId="me", id=k[0], body={"addLabelIds": ["INBOX", "STARRED", "IMPORTANT"], "removeLabelIds": ["TRASH"]}).execute()
        fin_done.add(k[0])
        rescued_ids.add(k[0])
        rescued.append((re.sub(r".*<|>.*", "", k[1]).strip() or k[1], k[2]))
state["fin_rescued"] = sorted(fin_done)[-300:]

# --- calendar, 7 days, every day shown (same shape the old Melissa Daily Briefing used), plus
# overlap detection and RSVP-needed flags (ported from missophs/daily-briefing, missing here before 2026-09-27)
day0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
events = cal.events().list(calendarId="primary", timeMin=day0.isoformat(), timeMax=(day0 + timedelta(days=7)).isoformat(),
                           singleEvents=True, orderBy="startTime", timeZone="America/New_York").execute().get("items", [])
cal_cards = calendar_action_cards(events, now)  # RSVP pending + declined invites, shown under Action Required
by_day: dict[str, list[dict]] = {}
seen_ev: set[tuple[str, str]] = set()  # same start + same title = one appointment entered twice (e.g. Walgreens with two address spellings)
for e in events:
    s = e["start"].get("dateTime")
    key = (s or e["start"].get("date", ""), e.get("summary", "(no title)").strip().lower())
    if key in seen_ev:
        continue
    seen_ev.add(key)
    summary = e.get("summary", "(no title)")
    if e.get("location"):
        summary += f" ({e['location']})"
    rsvp = any(a.get("self") and a.get("responseStatus") == "needsAction" for a in e.get("attendees", []))
    if s:
        d = datetime.fromisoformat(s).astimezone(NY)
        end_s = e.get("end", {}).get("dateTime")
        d_end = datetime.fromisoformat(end_s).astimezone(NY) if end_s else d
        by_day.setdefault(d.strftime("%Y-%m-%d"), []).append(
            {"start": d, "end": d_end, "when": d.strftime("%-I:%M%p").lower(), "what": summary, "rsvp": rsvp, "conflict": False})
    else:
        d = datetime.fromisoformat(e["start"]["date"])
        by_day.setdefault(d.strftime("%Y-%m-%d"), []).append(
            {"start": None, "end": None, "when": "all day", "what": summary, "rsvp": rsvp, "conflict": False})

for day_events in by_day.values():
    timed = sorted((ev for ev in day_events if ev["start"] is not None), key=lambda ev: ev["start"])
    for i in range(len(timed) - 1):
        if timed[i]["end"] and timed[i + 1]["start"] < timed[i]["end"]:
            timed[i]["conflict"] = True
            timed[i + 1]["conflict"] = True

calendar_days = []
rsvp_needed: list[tuple[str, str]] = []
for i in range(7):
    d = day0 + timedelta(days=i)
    day_events = by_day.get(d.strftime("%Y-%m-%d"), [])
    for ev in day_events:
        if ev["rsvp"]:
            rsvp_needed.append((d.strftime("%a %-m/%-d"), ev["what"]))
    calendar_days.append({"label": d.strftime("%a %-m/%-d"),
                          "events": [(ev["when"], ev["what"], ev["conflict"], ev["rsvp"]) for ev in day_events]})

# --- calendar in the Daily Briefing layout (status, host, Zoom, Prep, named conflicts). Prep lines: one cached Haiku call for new events in the next 3 days.
prep_cache = state.setdefault("prep", {})  # event id -> one-line prep, only from the event's own title/description/location
need_prep = [e for e in events if e.get("id") and e["id"] not in prep_cache and e.get("status") != "cancelled"
             and datetime.fromisoformat(e["start"].get("dateTime") or e["start"]["date"] + "T00:00:00+00:00").astimezone(NY) < day0 + timedelta(days=3)]
if need_prep and os.environ.get("ANTHROPIC_API_KEY"):
    try:
        out = ask_haiku("For each calendar event give ONE practical prep line, max 22 words, using ONLY its title, description and location (what to bring, confirm or read). "
                        'If the event gives nothing to prepare, return "". Never invent people, places, facts or documents. Return a JSON array, same order: {"i":<n>,"prep":"..."} JSON only.\n\n' +
                        "\n".join(f"{n}. {e.get('summary', '')} | {(e.get('description') or '')[:200]} | {e.get('location', '')}" for n, e in enumerate(need_prep, 1)), 1500)
        for r in json.loads(out[out.index("["):out.rindex("]") + 1]):
            if 1 <= r.get("i", 0) <= len(need_prep):
                prep_cache[need_prep[r["i"] - 1]["id"]] = str(r.get("prep", ""))[:200]
    except Exception as exc:
        print("prep lines failed:", exc)
for k in list(prep_cache)[:-200]:
    del prep_cache[k]
rich = rich_events(events, now, prep_cache)
cal_rich = [((day0 + timedelta(days=i)).strftime("%A, %B %-d, %Y"), i == 0, rich.get((day0 + timedelta(days=i)).strftime("%Y-%m-%d"), [])) for i in range(7)]

# --- prepare: interviews/screens/prep-worthy events in the next 7 days, checklist from the vault only
PREP_WORDS = re.compile(r"\b(interview|screen|phone screen|video screen|panel|call with|meeting with|appointment|prep)\b", re.I)
apps_rows = [[x.strip() for x in l.strip().strip("|").split("|")] for l in apps.splitlines() if l.startswith("|") and not l.startswith("|---")]
apps_rows = [c for c in apps_rows if len(c) >= 7 and c[0] not in ("Company", "---")]
prepare_items: list[tuple[str, str, list[str]]] = []
for i, day in enumerate(calendar_days):
    rel = "TODAY" if i == 0 else f"TOMORROW ({day['label'].split()[-1]})" if i == 1 else day["label"]
    for when, what, conflict, rsvp in day["events"]:
        if not (i < 2 or PREP_WORDS.search(what)):  # today and tomorrow: every event gets a card; later days only prep-worthy ones
            continue
        match = next((c for c in apps_rows if c[0].lower() and c[0].lower() in what.lower()), None)
        checklist = ([f"Stage / last contact: {match[2]}, {match[4]}", f"What you owe them: {match[5][:200]}", f"Contact: {match[6]}"] if match else [])
        if conflict:
            checklist.append("⚠️ Potential time conflict — review timing before it starts")
        if rsvp:
            checklist.append("RSVP still needed")
        prepare_items.append((rel, f"{what} @ {when}" if when != "all day" else f"{what} (all day)", checklist or ["Nothing extra in the vault for this one"]))
if os.path.isdir("Meetings"):
    for fn in sorted(os.listdir("Meetings")):
        m = re.match(r"(\d{4}-\d{2}-\d{2}) (.+)\.md$", fn)
        if m and today <= m.group(1) <= (now + timedelta(days=7)).strftime("%Y-%m-%d"):
            lines = [l.strip("- ").strip() for l in read(f"Meetings/{fn}").splitlines() if l.strip().startswith("-")][:6]
            prepare_items.append((m.group(1), m.group(2), lines or ["not in vault"]))
prepare_items.sort(key=lambda p: p[0])

# --- top 3 & follow up
WAITING_MAX_DAYS = 5  # items older than this stop being reported (Melissa, 2026-09-27) — still tracked in Memory.md, just not surfaced
focus = section(board, "🔥 Today") + section(board, "⏭ This Week")
waiting_board = [(x.split(" — ")[0][:80], " — ".join(x.split(" — ")[1:]), 0) for x in section(board, "⏳ Waiting On")]
fu_m = re.search(r"^## Follow-Ups[^\n]*\n(.*?)(?=^## |\Z)", memory, re.M | re.S)
waiting_fu = []
for l in (fu_m.group(1).splitlines() if fu_m else []):
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    if l.startswith("|") and len(c) >= 4 and c[0] not in ("Item", "---"):
        try:
            days_since = (now.date() - datetime.strptime(c[2], "%Y-%m-%d").date()).days
        except ValueError:
            days_since = 0
        if days_since <= WAITING_MAX_DAYS:
            waiting_fu.append((c[1], f"{c[0]} — {c[3][:160]}", days_since))
waiting = sorted(waiting_board + waiting_fu, key=lambda w: -w[2])

# --- action required: every board item with an explicit due date, not just the top 3 (ported from
# missophs/daily-briefing's Action Required cards, missing here before 2026-09-27)
due_re = re.compile(r"due (\d{4}-\d{2}-\d{2})")
action_items = sorted(
    (t for t in focus + section(board, "📋 Backlog") if due_re.search(t)),
    key=lambda t: due_re.search(t).group(1))

role_count = len({c[0] for c in apps_rows if c[2] != "Closed"})
awaiting_count = len(waiting)
open_count = len(focus) + len(section(board, "📋 Backlog"))

mail_records = [{"frm": re.sub(r"<.*?>|\"", "", k[1]).strip()[:40] or k[1][:40], "subj": k[2][:90], "line": mail_cache[k[0]][1], "cat": mail_cache[k[0]][4],
                 "loc": "rescued" if k[0] in rescued_ids else k[4], "needs": mail_cache[k[0]][0],
                 "next": mail_cache[k[0]][5] if len(mail_cache[k[0]]) > 5 else "", "due": mail_cache[k[0]][6] if len(mail_cache[k[0]]) > 6 else ""} for k in allmail]
state["review"] = {"date": today, "mail": [m for m in mail_records if m["cat"] in REVIEW_CATS and m["loc"] in ("inbox", "rescued", "trash")]}  # wrap_up.py reads this
FIT = {"Offer": "High", "Final": "High", "Interview": "High", "Screen": "Medium", "Applied": "Low"}  # ponytail: fit is by stage only, no real scoring
pipeline = [(f"{c[0]} - {c[1]}", f"{c[2]} · last contact {c[4]}: {c[5].replace('**', '')[:140]}", FIT[c[2]])
            for c in sorted((c for c in apps_rows if c[2] in FIT), key=lambda c: list(FIT).index(c[2]))]

subject, body = build_morning(now, calendar_days, rescued, [], inbox_rows, prepare_items, draft_candidates, focus, waiting,
                              role_count, awaiting_count, open_count, action_items, rsvp_needed, mail_records, pipeline, cal_cards, cal_rich)
state["drafts"] = {"date": today, "items": [list(d) for d in draft_candidates]}  # wrap_up.py shows the same list
assert body.startswith("<table") and "$(" not in body and "/tmp/" not in body, "bad email body"

if DRY:
    open("morning-preview.html", "w", encoding="utf-8").write(body)
    print(f"DRY RUN: subject={subject!r} inbox={len(inbox_rows)} rescued={len(rescued)} drafts={len(draft_candidates)} "
          f"prepare={len(prepare_items)} focus={len(focus)} waiting={len(waiting)} roles={role_count} "
          f"action_items={len(action_items)} rsvp_needed={len(rsvp_needed)} mail={len(mail_records)} pipeline={len(pipeline)} ai_tokens={usage}")
    for r in inbox_rows:
        print("  inbox:", r)
    for r in rescued:
        print("  rescued:", r)
    for r in draft_candidates:
        print("  draft candidate:", r)
    for r in prepare_items:
        print("  prepare:", r)
    for d in calendar_days:
        print("  calendar:", d)
    sys.exit(0)

dup = gmail.users().messages().list(userId="me", q=f'in:sent newer_than:1d subject:"{subject}"').execute().get("messages")
if dup:
    print("Morning email already sent today, not sending again.")
    sys.exit(0)
send(subject, body, "html")
json.dump(state, open(STATE, "w"))
print(f"Morning email sent to {ME}: {subject}")
print(f"ai tokens: {usage}")
