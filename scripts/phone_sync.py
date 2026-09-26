#!/usr/bin/env python3
"""Ellie phone sync, no AI: empties captures, trashes per trash-rules.md, rebuilds the Drive `Ellie` board.

Env: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN. DRY_RUN=1 changes nothing outside the runner.
"""
import base64, hashlib, html, io, json, os, re, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

NY = ZoneInfo("America/New_York")
DRY = os.environ.get("DRY_RUN") == "1"
ME = "melissaw212@gmail.com"
PLACEHOLDER = "Type anything here."
STATE = ".ellie-state.json"
COLORS = {"red": "#c62828", "amber": "#b26a00", "blue": "#1c4dc4", "green": "#0c7351", "purple": "#6d21c9", "gray": "#6b6b6b"}
now = datetime.now(NY)
today = now.strftime("%Y-%m-%d")

creds = Credentials(None, refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"], client_id=os.environ["GOOGLE_CLIENT_ID"],
                    client_secret=os.environ["GOOGLE_CLIENT_SECRET"], token_uri="https://oauth2.googleapis.com/token")
gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)
drive = build("drive", "v3", credentials=creds, cache_discovery=False)
cal = build("calendar", "v3", credentials=creds, cache_discovery=False)


def read(path: str) -> str:
    return open(path, encoding="utf-8").read()


def bullets(md: str, heading: str) -> list[str]:
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    return [l[2:].strip().lower() for l in (m.group(1).splitlines() if m else []) if l.startswith("- ") and l[2:].strip()]


def body_text(msg: dict) -> str:
    parts, out = [msg["payload"]], []
    while parts:
        p = parts.pop()
        parts.extend(p.get("parts", []))
        if p.get("mimeType") == "text/plain" and p.get("body", {}).get("data"):
            out.append(base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8", "replace"))
    return "\n".join(out).strip() or msg.get("snippet", "")


state = json.load(open(STATE)) if os.path.exists(STATE) else {"seen": []}
seen = set(state["seen"])
captures: list[tuple[str, str]] = []  # (source id, text)

for q in (f"in:anywhere newer_than:1d from:{ME} to:{ME}", f"in:anywhere newer_than:1d from:{ME} to:melweiss212@gmail.com"):
    for m in gmail.users().messages().list(userId="me", q=q).execute().get("messages", []):
        if m["id"] in seen:
            continue
        full = gmail.users().messages().get(userId="me", id=m["id"], format="full").execute()
        subj = next((h["value"] for h in full["payload"]["headers"] if h["name"] == "Subject"), "")
        captures.append((m["id"], " ".join(f"{subj}. {body_text(full)}".split())))

tell = drive.files().list(q="name='Tell Ellie' and trashed=false", fields="files(id,parents,mimeType)").execute().get("files", [])
tell_text = ""
if tell:
    is_doc = tell[0]["mimeType"] == "application/vnd.google-apps.document"
    raw = (drive.files().export_media(fileId=tell[0]["id"], mimeType="text/plain") if is_doc
           else drive.files().get_media(fileId=tell[0]["id"])).execute()
    tell_text = raw.decode("utf-8", "replace").lstrip("\ufeff").strip()
    if tell_text and not tell_text.startswith(PLACEHOLDER):
        captures.append((f"drive-{tell[0]['id']}-{hashlib.md5(tell_text.encode()).hexdigest()[:8]}", " ".join(tell_text.split())))
    else:
        tell = []

# --- file captures into the vault
board = read("Task Board.md")
rules = read("routines/trash-rules.md")
added, always = [], []
for cid, text in captures:
    m = re.match(r"(?i)\s*(?:tell ellie:?\s*)?always trash\s+(\S+)", text)
    if m:
        always.append(m.group(1).lower())
    else:
        added.append(f"- [ ] {text[:400]} — captured {today} · #unsorted")
    seen.add(cid)
if added:
    block = "## 📥 Captured (unsorted)\n" + "\n".join(added) + "\n\n"
    board = board.replace("## 📋 Backlog", block + "## 📋 Backlog", 1) if "## 📥 Captured" not in board else \
        re.sub(r"(## 📥 Captured \(unsorted\)\n)", lambda m: m.group(1) + "\n".join(added) + "\n", board, count=1)
if always:
    rules = re.sub(r"(## ALWAYS TRASH[^\n]*\n\n)", lambda m: m.group(1) + "".join(f"- {a}\n" for a in always), rules, count=1)

# --- trash per rules (deterministic rules only; never permanent delete)
protected = bullets(rules, "PROTECTED (never trash)")
never_subj = bullets(rules, "NEVER TRASH if subject/snippet mentions")
always_l = bullets(rules, "ALWAYS TRASH (sender contains)") + always
trashed = []
for t in gmail.users().threads().list(userId="me", q="in:inbox newer_than:1d").execute().get("threads", []):
    th = gmail.users().threads().get(userId="me", id=t["id"], format="metadata", metadataHeaders=["From", "Subject"]).execute()
    hd = {h["name"]: h["value"] for h in th["messages"][0]["payload"]["headers"]}
    frm, subj = hd.get("From", "").lower(), hd.get("Subject", "")
    hay = f"{subj} {th['messages'][0].get('snippet', '')}".lower()
    if any(p in frm for p in protected) or any(n in hay for n in never_subj):
        continue
    if any(a in frm for a in always_l):
        trashed.append((hd.get("From", ""), subj))
        if not DRY:
            gmail.users().threads().trash(userId="me", id=t["id"]).execute()

# --- calendar, rest of the week
sunday = (now + timedelta(days=(6 - now.weekday()))).replace(hour=23, minute=59, second=59)
events = cal.events().list(calendarId="primary", timeMin=now.isoformat(), timeMax=sunday.isoformat(),
                           singleEvents=True, orderBy="startTime", timeZone="America/New_York").execute().get("items", [])
cal_lines = []
for e in events:
    s = e["start"].get("dateTime")
    if s:
        d = datetime.fromisoformat(s).astimezone(NY)
        cal_lines.append(f"{d.strftime('%a %-m/%-d')} {d.strftime('%-I:%M%p').lower()} - {e.get('summary', '(no title)')}")
    else:
        d = datetime.fromisoformat(e["start"]["date"])
        cal_lines.append(f"{d.strftime('%a %-m/%-d')} all day - {e.get('summary', '(no title)')}")


# --- board HTML
def h(text: str, color: str) -> str:
    return f'<h2 style="color:{COLORS[color]}">{html.escape(text)}</h2>'


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>" if items else "<p>None.</p>"


def section(md: str, prefix: str) -> list[str]:
    m = re.search(rf"^## {re.escape(prefix)}[^\n]*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    lines = m.group(1).splitlines() if m else []
    return [re.sub(r"^\[[ x]\] ", "", l[2:]).strip() for l in lines if l.startswith("- ") and "(none" not in l]


done_today = [l for l in section(board, "✅ Done") if today in l]
page = [f"<h1>ELLIE - LIVE BOARD</h1><p>Melissa Weiss, Senior HR executive, New York (US Eastern). Last updated: {now.strftime('%Y-%m-%d %-I:%M%p')} ET</p>",
        h("What happened today", "green"),
        ul([f"Filed {len(added)} new capture(s)"] + [f"Closed: {d}" for d in done_today] + ([f"Always-trash added: {', '.join(always)}"] if always else [])),
        h("On your calendar, rest of the week", "blue"), ul(cal_lines),
        h("Inbox trash (undo from Gmail Trash if wrong)", "red"), ul([f"{f} | {s}" for f, s in trashed]),
        h("Today", "red"), ul(section(board, "🔥 Today")),
        h("This week", "amber"), ul(section(board, "⏭ This Week")),
        h("Captured, not yet sorted", "purple"), ul(section(board, "📥 Captured")),
        h("Waiting on", "amber"), ul(section(board, "⏳ Waiting On")),
        h("Backlog", "gray"), ul(section(board, "📋 Backlog")),
        "<p>To close a task, tell Ellie: mark it done. To capture, write in the Tell Ellie file.</p>"]
doc = "<html><body>" + "".join(page) + "</body></html>"

if DRY:
    print(f"DRY RUN: captures={len(captures)} would_trash={len(trashed)} events={len(cal_lines)} board_chars={len(doc)}")
    for f, s in trashed:
        print("  would trash:", f, "|", s)
    print("\n".join(cal_lines))
    sys.exit(0)

# --- write vault, then Drive
open("Task Board.md", "w", encoding="utf-8").write(board)
open("routines/trash-rules.md", "w", encoding="utf-8").write(rules)
json.dump({"seen": sorted(seen)[-300:]}, open(STATE, "w"))


def replace_doc(name: str, content: str, text_mime: str, parents: list[str] | None = None) -> None:
    old = drive.files().list(q=f"name='{name}' and trashed=false", fields="files(id,parents)").execute().get("files", [])
    par = parents or (old[0].get("parents") if old else None)
    meta = {"name": name, **({"parents": par} if par else {})}
    if text_mime == "text/html":
        meta["mimeType"] = "application/vnd.google-apps.document"
    media = MediaIoBaseUpload(io.BytesIO(content.encode()), mimetype=text_mime)
    new = drive.files().create(body=meta, media_body=media, fields="id").execute()
    for o in old:
        drive.files().update(fileId=o["id"], body={"trashed": True}).execute()
    print(f"replaced {name}: new {new['id']}, trashed {len(old)}")


replace_doc("Ellie", doc, "text/html")
if tell:
    replace_doc("Tell Ellie", f"<p>{PLACEHOLDER} Ellie files it at 6:30am and 4:30pm ET.</p>", "text/html", tell[0].get("parents"))
print(f"done: captures={len(captures)} trashed={len(trashed)} events={len(cal_lines)}")
