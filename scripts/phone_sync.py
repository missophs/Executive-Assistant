#!/usr/bin/env python3
"""Ellie phone sync, no AI: empties captures, trashes per trash-rules.md, rebuilds the Drive `Ellie` board.

Env: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN. DRY_RUN=1 changes nothing outside the runner.
"""
import base64, hashlib, html, io, json, os, re, sys
from datetime import datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from midday_email import build_midday
from prep_doc import build_prep, keywords, to_html

NY = ZoneInfo("America/New_York")
DRY = os.environ.get("DRY_RUN") == "1"
ME = "melissaw212@gmail.com"
OWN_MAIL = ("standup", "melissa daily briefing", "daily job search sweep", "vault write failed", "wrap-up", "wrap up", "midday", "ellie")  # Ellie's own emails to her
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
seen = set(state["seen"]) | set(re.findall(r"^([0-9a-f]{16}) \|", read("Memory.md"), re.M))  # ids the cloud routine already filed
captures: list[tuple[str, str]] = []  # (source id, text)

for q in (f"in:anywhere newer_than:1d from:{ME} to:{ME}", f"in:anywhere newer_than:1d from:{ME} to:melweiss212@gmail.com"):
    for m in gmail.users().messages().list(userId="me", q=q).execute().get("messages", []):
        if m["id"] in seen:
            continue
        full = gmail.users().messages().get(userId="me", id=m["id"], format="full").execute()
        subj = next((h["value"] for h in full["payload"]["headers"] if h["name"] == "Subject"), "")
        if subj.lower().startswith(OWN_MAIL):
            seen.add(m["id"])
            continue
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

if os.environ.get("LIGHT") == "1" and not captures:  # midday: one cheap look, stop if nothing new (no board rebuild, no AI)
    print("Midday: no new captures, nothing rebuilt.")
    sys.exit(0)

# --- file captures into the vault
board = read("Task Board.md")
rules = read("routines/trash-rules.md")
memory = read("Memory.md")
apps = read("Applications.md")
added: list[str] = []
always: list[str] = []
plan_log: list[str] = []
filed_notes: list[str] = []  # midday email: task/application/memory/link items filed this run
done_list: list[str] = []  # midday email: tasks closed out by a capture
needs_call: list[str] = []  # midday email: ambiguous captures she needs to resolve herself
usage = {"in": 0, "out": 0}


def add_after(md: str, heading: str, line: str) -> str:
    """Insert a bullet right under the heading that starts with `heading`; create the section if missing."""
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n", md, re.M)
    if not m:
        return md.rstrip() + f"\n\n## {heading}\n{line}\n"
    rest = md[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    end = m.end() + (nxt.start() if nxt else len(rest))
    section_txt = re.sub(r"^_\(none open\)_\n?", "", md[m.end():end], flags=re.M)
    return md[:m.end()] + line + "\n" + section_txt + md[end:]


def ask_haiku(prompt: str, max_tokens: int) -> str:
    import urllib.request
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", method="POST", data=json.dumps({
        "model": "claude-haiku-4-5-20251001", "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"})
    resp = json.load(urllib.request.urlopen(req, timeout=60))
    usage["in"] += resp["usage"]["input_tokens"]
    usage["out"] += resp["usage"]["output_tokens"]
    return resp["content"][0]["text"]


def classify(items: list[tuple[str, str]], open_tasks: list[str]) -> list[dict]:
    prompt = (f"Today is {now.strftime('%A')} {today} (America/New_York). Melissa, a senior HR executive job searching, sent these notes to her assistant.\n"
              "For EACH note return one JSON object in an array, same order: "
              '{"i":<note number>,"kind":"task|application|memory|link|done|calendar|prep|send|trash|unclear","text":"short clean version",'
              '"match":<open task number or null, for done>,"date":"YYYY-MM-DD or null","time":"HH:MM start or null","end":"HH:MM end or null","sender":"for trash"}.\n'
              'For calendar and for reminders, text is ONLY the short subject (e.g. "Mahjong", "Call New York City about documents"), never words like "add to calendar", "remind me" or "tomorrow".\n'
              "kind meanings: task=something to do or a reminder; application=company/role/recruiter/stage news; memory=person, preference or decision; "
              "link=bare link with no action; done=says something is finished, cancelled, or that she heard back from someone and no longer needs to wait "
              '(e.g. "Nasreen replied", "stop waiting on Chime", "mark the dentist done") — set match to the item number, whether it is a task or a waiting-on item below; '
              "calendar=explicit request to put something on the calendar (needs date); prep=asks for prep or a prep doc for an interview or meeting (e.g. prep for interview with Acme tomorrow; Prep: Acme Thursday) — set text to the company and date to the meeting day; send=asks Ellie to email or send her a document from Google Drive (e.g. send CAI talking points; email me the Cprime notes) — set text to the document name only; trash=always trash a sender; unclear=cannot tell. "
              "Never invent facts. Output only the JSON array.\n\nOPEN TASKS AND WAITING-ON ITEMS (say done to close either):\n" +
              "\n".join(f"{n}. {t[:110]}" for n, t in enumerate(open_tasks, 1)) + "\n\nNOTES:\n" +
              "\n".join(f"{n}. {t[:600]}" for n, (_, t) in enumerate(items, 1)))
    txt = ask_haiku(prompt, 1500)
    return json.loads(txt[txt.index("["):txt.rindex("]") + 1])


open_tasks = [l for l in board.splitlines() if l.startswith("- [ ]")]  # Task Board Waiting On items are checkboxes too, already included here

# Memory.md's Follow-Ups table is the other place a Waiting-On item lives (not a checkbox, so not in open_tasks
# above) — matchable by a "done" capture too: "Nasreen replied", "stop waiting on Chime".
fu_m0 = re.search(r"^## Follow-Ups[^\n]*\n(.*?)(?=^## |\Z)", memory, re.M | re.S)
waiting_fu_rows = [[x.strip() for x in l.strip().strip("|").split("|")] for l in (fu_m0.group(1).splitlines() if fu_m0 else []) if l.startswith("|")]
waiting_fu_rows = [c for c in waiting_fu_rows if len(c) >= 4 and c[0] not in ("Item", "---")]
waiting_labels = [f"Waiting on: {c[1]} — {c[0]}"[:110] for c in waiting_fu_rows]
matchable = open_tasks + waiting_labels

plan: list[dict] = []
if captures and os.environ.get("ANTHROPIC_API_KEY"):
    try:
        plan = classify(captures, matchable)
    except Exception as exc:  # fall back to unsorted so nothing is lost
        print("AI classify failed, filing unsorted:", exc)
if not plan:
    plan = [{"i": n, "kind": "unsorted", "text": t[:400]} for n, (_, t) in enumerate(captures, 1)]

for item in plan:
    kind, text = item.get("kind", "unclear"), (item.get("text") or "").strip()
    src = captures[item["i"] - 1][1] if 1 <= item.get("i", 0) <= len(captures) else text
    plan_log.append(f"{kind}: {text[:70]}")
    if kind in ("task", "application"):
        due = item.get("date") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(item.get("date"))) else None
        soon = due is not None and due <= (now + timedelta(days=7)).strftime("%Y-%m-%d")
        target = "🔥 Today" if (due == today or (item.get("priority") and not due)) else "⏭ This Week" if (soon or item.get("priority")) else "📋 Backlog"
        tag = "jobsearch" if kind == "application" else "task"
        board = add_after(board, target, f"- [ ] {text}{' — due ' + due if due else ''} — captured {today} · #{tag}{' · #priority' if item.get('priority') else ''}")
        if kind == "application":
            apps = apps.rstrip() + f"\n- {today}: {text}\n"
        added.append(text)
        filed_notes.append(text)
        if kind == "task" and due and due >= today and re.search(r"\bremind", src, re.I) and not DRY:  # dated "remind me" = calendar entry with a phone popup
            t0 = item.get("time") if re.fullmatch(r"\d{2}:\d{2}", str(item.get("time"))) else "09:00"
            start = datetime.fromisoformat(f"{due}T{t0}")
            dup = cal.events().list(calendarId="primary", timeMin=f"{due}T00:00:00-04:00", timeMax=f"{due}T23:59:59-04:00", singleEvents=True, timeZone="America/New_York").execute().get("items", [])
            if not any(e.get("summary", "").lower() == text.lower() for e in dup):
                cal.events().insert(calendarId="primary", body={"summary": text,
                    "start": {"dateTime": start.strftime("%Y-%m-%dT%H:%M:00"), "timeZone": "America/New_York"},
                    "end": {"dateTime": (start + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:00"), "timeZone": "America/New_York"},
                    "reminders": {"useDefault": False, "overrides": [{"method": "popup", "minutes": 10}]}}).execute()
                added.append(f"Calendar reminder: {text} {due} {t0}")
    elif kind == "memory":
        memory = add_after(memory, "Decisions & Context", f"- {today}: {text}")
        added.append(text)
        filed_notes.append(text)
    elif kind == "link":
        memory = add_after(memory, "Saved Links", f"- {today}: {text}")
        added.append(text)
        # Melissa, 2026-09-28: don't show bare links in the midday email — no title to show, just noise.
        # Still filed to Memory.md's Saved Links above for the record.
    elif kind == "done":
        n = item.get("match")
        if isinstance(n, int) and 1 <= n <= len(open_tasks) and open_tasks[n - 1] in board:
            board = board.replace(open_tasks[n - 1] + "\n", "", 1)
            text = re.sub(r"^- \[ \] ", "", open_tasks[n - 1])[:150]
        elif isinstance(n, int) and n > len(open_tasks):
            idx = n - 1 - len(open_tasks)
            if 0 <= idx < len(waiting_fu_rows):
                c = waiting_fu_rows[idx]
                m2 = re.search(r"^## Follow-Ups[^\n]*\n(.*?)(?=^## |\Z)", memory, re.M | re.S)
                if m2:
                    kept = [l for l in m2.group(1).splitlines() if not (l.startswith("|") and c[1] in l and c[0][:30] in l)]
                    memory = memory[:m2.start(1)] + "\n".join(kept) + ("\n" if kept else "") + memory[m2.end(1):]
                text = f"No longer waiting on {c[1]}"
        board = add_after(board, "✅ Done", f"- [x] {text} — done {today}")
        done_list.append(text)
    elif kind == "trash":
        always.append((item.get("sender") or text).lower())
    elif kind == "calendar" and item.get("date"):
        day = item["date"]
        t0 = item.get("time")
        existing = cal.events().list(calendarId="primary", timeMin=f"{day}T00:00:00-04:00", timeMax=f"{day}T23:59:59-04:00",
                                     singleEvents=True, timeZone="America/New_York").execute().get("items", [])
        if not any(e.get("summary", "").lower() == text.lower() for e in existing) and not DRY:
            if t0:
                end = f"{day}T{item['end']}:00" if re.fullmatch(r"\d{2}:\d{2}", str(item.get("end"))) else (datetime.fromisoformat(f"{day}T{t0}") + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:00")
                when = {"start": {"dateTime": f"{day}T{t0}:00", "timeZone": "America/New_York"},
                        "end": {"dateTime": end, "timeZone": "America/New_York"}}
            else:
                when = {"start": {"date": day}, "end": {"date": (datetime.fromisoformat(day) + timedelta(days=1)).strftime("%Y-%m-%d")}}
            body = {"summary": text, **when}
            if re.search(r"\bremind", src, re.I):  # a reminder is a short block with a phone popup, not an hour-long meeting
                if t0 and not re.fullmatch(r"\d{2}:\d{2}", str(item.get("end"))):
                    body["end"] = {"dateTime": (datetime.fromisoformat(f"{day}T{t0}") + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:00"), "timeZone": "America/New_York"}
                body["reminders"] = {"useDefault": False, "overrides": [{"method": "popup", "minutes": 10}]}
            cal.events().insert(calendarId="primary", body=body).execute()
        added.append(f"Calendar: {text} {day}")
        if item.get("priority"):  # a calendar block she also called a priority is a task too
            board = add_after(board, "🔥 Today" if day == today else "⏭ This Week", f"- [ ] {text} — due {day} — captured {today} · #task · #priority")
    elif kind == "prep":
        day = item.get("date") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(item.get("date"))) else (now + timedelta(days=1)).strftime("%Y-%m-%d")
        kws = [k.lower() for k in keywords(text)]
        evs = cal.events().list(calendarId="primary", timeMin=f"{day}T00:00:00-04:00", timeMax=f"{day}T23:59:59-04:00", singleEvents=True,
                                orderBy="startTime", timeZone="America/New_York").execute().get("items", [])
        ev = next((e for e in evs if any(k in (e.get("summary", "") + " " + e.get("description", "")).lower() for k in kws)), None)
        built = build_prep(text, day, ev, apps, memory)
        if built:
            os.makedirs("Meetings", exist_ok=True)
            if not DRY:
                open(f"Meetings/{day} {re.sub(r'[^A-Za-z0-9 &-]', '', built[0])}.md", "w", encoding="utf-8").write(built[1])
            if not DRY:  # the vault is private, so the prep doc has to reach her phone by email
                subj_p = f"Ellie - Prep - {built[0].removesuffix(' prep')} - {day}"
                if not gmail.users().messages().list(userId="me", q=f'in:sent newer_than:2d subject:"{subj_p}"').execute().get("messages"):
                    msg_p = MIMEText(to_html(built[1]), "html", "utf-8")
                    msg_p["To"], msg_p["From"], msg_p["Subject"] = ME, ME, subj_p
                    gmail.users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg_p.as_bytes()).decode()}).execute()
            added.append(f"Prep doc: {built[0]} ({day})")
            filed_notes.append(f"Prep doc ready: {built[0]} for {day} (in the Prepare section of your next morning email)")
        else:  # nothing in the vault or on the calendar for it: say so instead of guessing
            board = add_after(board, "Needs Melissa", f"- [ ] Prep requested: {text} — no calendar event or Applications row found; tell Ellie the company and time — {today}")
            needs_call.append(f"Prep for \"{text}\": couldn't find it on your calendar or in Applications. Reply with the company name and time.")
    elif kind == "send":  # email a Drive document to Melissa (she cannot open the vault, and the Drive app is slow on a phone)
        words = [w for w in keywords(text) if w.lower() not in ("send", "email", "document", "doc", "file", "drive", "google", "here", "it")]
        q_ = " and ".join(f"name contains '{w}'" for w in words) + " and trashed=false and mimeType!='application/vnd.google-apps.folder'"
        hits = drive.files().list(q=q_, orderBy="modifiedTime desc", pageSize=3, fields="files(id,name,mimeType,size)").execute().get("files", []) if words else []
        f0 = hits[0] if hits else None
        if f0 and f0["mimeType"] == "application/vnd.google-apps.document":
            body_ = drive.files().export_media(fileId=f0["id"], mimeType="text/html").execute()
            msg_s = MIMEText(body_.decode("utf-8", "replace"), "html", "utf-8")
        elif f0 and int(f0.get("size") or 0) <= 15_000_000:  # non-Doc files (docx, pdf) go as an attachment
            msg_s = MIMEMultipart()
            msg_s.attach(MIMEText(f"Attached: {f0['name']}", "plain", "utf-8"))
            part = MIMEApplication(drive.files().get_media(fileId=f0["id"]).execute(), Name=f0["name"])
            part["Content-Disposition"] = f'attachment; filename="{f0["name"]}"'
            msg_s.attach(part)
        else:
            msg_s = None
        if msg_s:
            if not DRY:
                msg_s["To"], msg_s["From"], msg_s["Subject"] = ME, ME, f"Ellie - Doc - {f0['name']}"
                gmail.users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg_s.as_bytes()).decode()}).execute()
            added.append(f"Emailed you: {f0['name']}")
            filed_notes.append(f"Emailed you the document: {f0['name']}" + (f" (other matches: {', '.join(x['name'] for x in hits[1:])})" if len(hits) > 1 else ""))
        else:  # no match: email her her recent docs so she can just text back a name
            recent = drive.files().list(q="trashed=false and mimeType!='application/vnd.google-apps.folder'", orderBy="modifiedTime desc", pageSize=10,
                                        fields="files(name)").execute().get("files", [])
            if not DRY:
                msg_s = MIMEText(f"<p>I couldn't find a Drive file matching \"{html.escape(text)}\". Your most recent documents:</p><ul>" +
                                 "".join(f"<li>{html.escape(r['name'])}</li>" for r in recent) + "</ul><p>Text me <b>send</b> and the name of one and I'll email it.</p>", "html", "utf-8")
                msg_s["To"], msg_s["From"], msg_s["Subject"] = ME, ME, "Ellie - Doc - which one?"
                gmail.users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg_s.as_bytes()).decode()}).execute()
            filed_notes.append(f"No Drive file matched \"{text}\" - emailed you a list of recent documents to pick from")
    else:  # unclear or unsorted
        board = add_after(board, "📥 Captured (unsorted)", f"- [ ] {src[:400]} — captured {today} · #unsorted")
        added.append(src[:80])
        needs_call.append(src[:200])
    if kind == "trash":
        plan_log[-1] += " (added to always-trash)"
for a_ in always:
    rules = re.sub(r"(## ALWAYS TRASH[^\n]*\n\n)", lambda m: m.group(1) + f"- {a_}\n", rules, count=1)
for cid, _ in captures:
    seen.add(cid)

# --- trash per rules (deterministic rules only; never permanent delete)
protected = bullets(rules, "PROTECTED (never trash)")
never_subj = bullets(rules, "NEVER TRASH if subject/snippet mentions")
always_l = bullets(rules, "ALWAYS TRASH (sender contains)") + always
trashed = []
kept: list[tuple[str, str, str, str]] = []  # (thread id, from, subject, snippet) left in the inbox
ourtrash = set(state.get("ourtrash", []))  # threads Ellie trashed herself: never rescued back
protected_ids: set[str] = set()  # threads the trash rules protect: the AI pass below may never trash these
for t in gmail.users().threads().list(userId="me", q="in:inbox newer_than:1d").execute().get("threads", []):
    th = gmail.users().threads().get(userId="me", id=t["id"], format="metadata", metadataHeaders=["From", "Subject"]).execute()
    hd = {h["name"]: h["value"] for h in th["messages"][0]["payload"]["headers"]}
    frm, subj = hd.get("From", "").lower(), hd.get("Subject", "")
    hay = f"{subj} {th['messages'][0].get('snippet', '')}".lower()
    if any(p in frm for p in protected) or any(n in hay for n in never_subj):
        protected_ids.add(t["id"])
        if not subj.lower().startswith(OWN_MAIL):
            kept.append((t["id"], hd.get("From", ""), subj, th["messages"][0].get("snippet", "")))
        continue
    if any(a in frm for a in always_l):
        trashed.append((hd.get("From", ""), subj))
        if not DRY:
            gmail.users().threads().trash(userId="me", id=t["id"]).execute()
            ourtrash.add(t["id"])
        continue
    if not subj.lower().startswith(OWN_MAIL):
        kept.append((t["id"], hd.get("From", ""), subj, th["messages"][0].get("snippet", "")))

# --- rescue from Trash: same bar as the morning briefing. High: a real person or real ATS about a real role/meeting, addressed to her, never bulk.
rescued: list[tuple[str, str]] = []
dnr_m = re.search(r"^## Do Not Rescue[^\n]*\n(.*?)(?=^## |\Z)", memory, re.M | re.S)
do_not_rescue = [c[0].lower() for l in (dnr_m.group(1).splitlines() if dnr_m else []) if l.startswith("|")
                 for c in [[x.strip() for x in l.strip().strip("|").split("|")]] if c and c[0] not in ("Sender / domain", "---") and not c[0].startswith("-")]
for tid in list(state.get("rescued", {})):  # a rescued thread back in Trash = she put it there on purpose: never rescue that sender again
    try:
        th = gmail.users().threads().get(userId="me", id=tid, format="metadata", metadataHeaders=["From", "Subject"]).execute()
        if "TRASH" in th["messages"][-1].get("labelIds", []) and "INBOX" not in th["messages"][-1].get("labelIds", []):
            frm = state["rescued"].pop(tid)
            if not DRY:
                memory = re.sub(r"(## Do Not Rescue[^\n]*\n.*?\n\|---[^\n]*\n(?:\|[^\n]*\n)*)", lambda m: m.group(1) + f"| {frm} | {today} | Rescued by Ellie, put back in Trash by Melissa |\n", memory, count=1, flags=re.S)
            do_not_rescue.append(frm.lower())
    except Exception:
        state["rescued"].pop(tid, None)
judged = set(state.get("trashjudged", []))
cands = []
try:
    for t in gmail.users().threads().list(userId="me", maxResults=50, q='in:trash newer_than:3d (interview OR invitation OR calendly OR schedule OR scheduling OR availability OR "next steps" OR offer OR recruiter OR "speak with" OR hiring OR "your application")').execute().get("threads", []):
        if t["id"] in ourtrash or t["id"] in judged:
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
                    state.setdefault("rescued", {})[k[0]] = re.sub(r".*<|>.*", "", k[1]).strip() or k[1]
                rescued.append((k[1], k[2]))
except Exception as exc:
    print("trash rescue failed:", exc)

# --- calendar, rest of the week
horizon = (now + timedelta(days=7)).replace(hour=23, minute=59, second=59)  # rolling 7 days: "until Sunday" hid Monday's events on a Saturday
events = cal.events().list(calendarId="primary", timeMin=now.isoformat(), timeMax=horizon.isoformat(),
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

DAY_COLORS = ["#1c4dc4", "#0c7351", "#6d21c9", "#b26a00", "#c62828", "#1c4dc4", "#0c7351"]  # cycles per calendar day, not weekday


def cal_html(lines: list[str]) -> str:
    """Group the flat 'Day date time - summary' lines by day, each day colored and separated by a rule
    (Melissa, 2026-09-28: calendar days should be in different colors and separated with lines)."""
    if not lines:
        return "<p>Nothing on the calendar in the next 7 days.</p>"
    days: list[tuple[str, list[str]]] = []
    for l in lines:
        day, date, rest = l.split(" ", 2)
        label = f"{day} {date}"
        if days and days[-1][0] == label:
            days[-1][1].append(rest)
        else:
            days.append((label, [rest]))
    out = []
    for i, (label, rest_lines) in enumerate(days):
        color = DAY_COLORS[i % len(DAY_COLORS)]
        out.append(f'<div style="border-left:4px solid {color};padding:4px 0 4px 10px;margin-top:8px;">'
                    f'<b style="color:{color}">{html.escape(label)}</b>'
                    + "".join(f"<br>{html.escape(r)}" for r in rest_lines) + "</div><hr style=\"border:none;border-top:1px solid #ddd;margin:4px 0;\">")
    return "".join(out)


# --- inbox triage: one Haiku line per NEW thread, cached by thread id
mail_cache = state.setdefault("mail", {})
fresh = [k for k in kept if k[0] not in mail_cache]
to_trash: list[tuple[str, str, str, str]] = []
if fresh and os.environ.get("ANTHROPIC_API_KEY"):
    try:
        out = ask_haiku(f"Today is {today}. Melissa is a senior HR executive job searching. For each inbox email return a JSON array, same order: "
                        '{"i":<n>,"needs":true|false,"trash":true|false,"line":"one plain line, max 14 words, what it is and any amount or deadline"}. '
                        "needs=true ONLY when a real person is waiting on her, a recruiter or interviewer wrote directly, there is a hard deadline, or a security or money problem. Automated job alerts, job digests, newsletters, receipts, statements, promos and deposits are needs=false. "
                        "trash=true ONLY for clearly unimportant bulk mail: marketing and promotions, product or feature announcements, newsletters, webinar or event promos, surveys, social-network notifications. "
                        "trash=false for anything from a real person, recruiters, job applications or acknowledgments, job alerts and digests, interviews, receipts, statements, banking, health or insurance, security alerts, government, or anything you are unsure about. Never invent facts. JSON only.\n\n" +
                        "\n".join(f"{n}. From: {f[:60]} | Subject: {sb[:90]} | {sn[:160]}" for n, (_, f, sb, sn) in enumerate(fresh, 1)), 1500)
        for r in json.loads(out[out.index("["):out.rindex("]") + 1]):
            if 1 <= r.get("i", 0) <= len(fresh):
                k = fresh[r["i"] - 1]
                mail_cache[k[0]] = [bool(r.get("needs")), str(r.get("line", ""))[:140]]
                if r.get("trash") is True and not r.get("needs") and k[0] not in protected_ids:
                    to_trash.append(k)
    except Exception as exc:
        print("AI mail triage failed:", exc)
for k in to_trash:  # Trash, never permanent delete: she can undo from Gmail Trash
    trashed.append((k[1], f"{k[2]} (Ellie judged unimportant)"))
    if not DRY:
        gmail.users().threads().trash(userId="me", id=k[0]).execute()
        ourtrash.add(k[0])
kept = [k for k in kept if k not in to_trash]
mail_rows = [(mail_cache[k[0]][0], re.sub(r"<.*?>|\"", "", k[1]).split("@")[0][:40], k[2][:80], mail_cache[k[0]][1]) for k in kept if k[0] in mail_cache]
mail_rows.sort(key=lambda r: not r[0])
for k in list(mail_cache)[:-200]:
    del mail_cache[k]

# --- reminders: open tasks dated in the next 7 days
week_end = (now + timedelta(days=7)).strftime("%Y-%m-%d")
reminders = sorted((m.group(1), re.sub(r"^- \[ \] ", "", l).split(" — ")[0]) for l in board.splitlines() if l.startswith("- [ ]")
                   for m in [re.search(r"due (\d{4}-\d{2}-\d{2})", l)] if m and today <= m.group(1) <= week_end)


# --- board HTML
def h(text: str, color: str) -> str:
    return f'<h2 style="color:{COLORS[color]}">{html.escape(text)}</h2>'


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>" if items else "<p>None.</p>"


def section(md: str, prefix: str) -> list[str]:
    m = re.search(rf"^## {re.escape(prefix)}[^\n]*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    lines = m.group(1).splitlines() if m else []
    return [re.sub(r"^\[[ x]\] ", "", l[2:]).strip() for l in lines if l.startswith("- ") and "(none" not in l]


def trunc(t: str, n: int = 240) -> str:
    t = t.replace("**", "").strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "..."


STAGE_ORDER = ["Offer", "Final", "Interview", "Screen", "Applied", "Researching"]


def pipeline(md: str) -> list[str]:
    rows = []
    for l in md.splitlines():
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if l.startswith("|") and len(c) >= 6 and c[2] in STAGE_ORDER:
            rows.append((STAGE_ORDER.index(c[2]), f"{c[0]} - {c[1]} - {c[2]} (last contact {c[4]}): {trunc(c[5], 200)}"))
    return [r for _, r in sorted(rows, key=lambda x: x[0])]


done_today = [l for l in section(board, "✅ Done") if today in l]
WAITING_MAX_DAYS = 5  # items older than this stop being reported (Melissa, 2026-09-27) — still tracked in Memory.md, just not surfaced
fu_m = re.search(r"^## Follow-Ups[^\n]*\n(.*?)(?=^## |\Z)", memory, re.M | re.S)  # the real waiting-on list lives in Memory.md, not the Task Board


def _fresh(since: str) -> bool:
    try:
        return (now.date() - datetime.strptime(since, "%Y-%m-%d").date()).days <= WAITING_MAX_DAYS
    except ValueError:
        return True


def _priority_fresh(bullet: str) -> bool:
    """Keep a Current Priorities bullet only if the most recent M/D date it mentions is within
    WAITING_MAX_DAYS (Melissa, 2026-09-28: only go back 5 days on priorities). No date found = stale, drop it."""
    dates = re.findall(r"\b(\d{1,2})/(\d{1,2})\b", bullet)
    if not dates:
        return False
    try:
        latest = max(datetime(now.year, int(mo), int(d)) for mo, d in dates)
    except ValueError:
        return False
    return (now.date() - latest.date()).days <= WAITING_MAX_DAYS


waiting_rows = section(board, "⏳ Waiting On") + [f"{c[1]} - {trunc(c[3], 160)} (since {c[2]})" for l in (fu_m.group(1).splitlines() if fu_m else [])
                                                 for c in [[x.strip() for x in l.strip().strip("|").split("|")]] if l.startswith("|") and len(c) >= 4 and c[0] not in ("Item", "---") and _fresh(c[2])]
page = [f"<h1>ELLIE - LIVE BOARD</h1><p>Melissa Weiss, Senior HR executive, New York (US Eastern). Last updated: {now.strftime('%Y-%m-%d %-I:%M%p')} ET</p>",
        h("What happened today", "green"),
        ul([f"Filed {len(added)} new capture(s)"] + [f"Rescued from Trash: {f} | {sb}" for f, sb in rescued] + [f"Closed: {d}" for d in done_today] + ([f"Always-trash added: {', '.join(always)}"] if always else [])),
        h("On your calendar, next 7 days", "blue"), cal_html(cal_lines),
        h("Reminders, next 7 days", "amber"), ul([f"{d}: {t}" for d, t in reminders]),
        h("Inbox: what needs you and what else is there", "blue"),
        ("<table border='1' cellpadding='4'><tr><th>Status</th><th>From</th><th>Subject</th><th>Summary</th></tr>" +
         "".join(f"<tr><td style='color:{COLORS['red' if n else 'gray']}'>{'NEEDS YOU' if n else 'INBOX'}</td><td>{html.escape(f)}</td><td>{html.escape(sb)}</td><td>{html.escape(ln)}</td></tr>"
                 for n, f, sb, ln in mail_rows) + "</table>") if mail_rows else "<p>Nothing new in the inbox.</p>",
        h("Rescued from Trash (Ellie thought you would want these; back in your inbox, starred)", "green"), ul([f"{f} | {sb}" for f, sb in rescued]),
        h("Inbox trash (undo from Gmail Trash if wrong)", "red"), ul([f"{f} | {s}" for f, s in trashed]),
        h("Current priorities", "green"), ul([trunc(x, 420) for x in section(memory, "Current Priorities") if _priority_fresh(x)][:5]),
        h("Today", "red"), ul(section(board, "🔥 Today")),
        h("This week", "amber"), ul(section(board, "⏭ This Week")),
        h("Captured, not yet sorted", "purple"), ul(section(board, "📥 Captured")),
        h("Application pipeline (open roles)", "green"), ul(pipeline(apps)),
        h("Waiting on", "amber"), ul(waiting_rows),
        h("People", "blue"), ul([trunc(x, 200) for x in section(memory, "People")[:30]]),
        h("Decisions & context", "purple"), ul([trunc(x, 260) for x in section(memory, "Decisions & Context")[:15]]),
        h("Backlog", "gray"), ul(section(board, "📋 Backlog")),
        h("Who you are", "purple"), ul([
            "You are Ellie, Melissa's executive assistant: professional, concise, direct, no fluff, bullets and next steps. Get her approval before drafting, sending, scheduling or changing anything external. Exception: calendar entries she asks for are pre-approved.",
            "To capture something she writes or dictates it into the Drive file Tell Ellie. To close a task she says mark it done and it clears at the next sync.",
            "When she asks where did we leave off on a topic: read this board first, then open the file named Where we left off - <Topic> (list below), then Tell Ellie and her self-sent mail for anything newer, and say which source each item came from."]),
        h("Which file to read", "gray"), ul([f"Where we left off - {t}: Ellie Files / {t}" for t in ("Job Search", "Meetings & Prep", "Reminders & Tasks", "Saved Links", "Ellie Setup", "Calendar")]),
        "<p>To close a task, tell Ellie: mark it done. To capture, write in the Tell Ellie file.</p>"]
doc = "<html><body>" + "".join(page) + "</body></html>"

# --- "Where we left off" topic files (rebuilt only when their content changed)
FOLDERS = {"Job Search": "1EJE9YAHK2pnaLZ8o-VkXF6g1bpq4ydtu", "Meetings & Prep": "1Y1DKfI-w471txK-t4Zlp6EhXYHW3J5Bm",
           "Reminders & Tasks": "1K8Aleb9OqEDmroWDQtuF2kbRZdEuXzI9", "Saved Links": "14nnStHuMg8uPtxvq53GY1UvxqSaMD7td",
           "Ellie Setup": "1hNbRyq0LmeudaDbPmqlqpSrNHluKfN9F", "Calendar": "1-9RxuHy0MaUD5rpb4I2-CjMixPt_Ghiv"}
COLOR_OF = {"Job Search": "green", "Meetings & Prep": "blue", "Reminders & Tasks": "amber", "Saved Links": "purple", "Ellie Setup": "gray", "Calendar": "blue"}
meet_files = sorted(f for f in os.listdir("Meetings") if f.endswith(".md")) if os.path.isdir("Meetings") else []
app_rows = [l for l in apps.splitlines() if l.startswith("|") and not l.startswith("|---")][:40]
app_notes = [trunc(l[2:], 200) for l in apps.splitlines() if l.startswith("- ")][-15:]  # application captures the sync appends
links = section(memory, "Saved Links")[:15]
topics = {
    "Job Search": (app_rows or ["No applications listed."]) + (["Recent notes:"] + app_notes if app_notes else []) + ["Waiting on:"] + waiting_rows
                  + ["Decisions & context:"] + [trunc(x, 200) for x in section(memory, "Decisions & Context")[:10]],
    "Meetings & Prep": [f"Prep doc: {f}" for f in meet_files[-10:]] + [x for x in section(board, "Needs Melissa") if "Prep requested" in x] or ["No prep docs yet."],
    "Reminders & Tasks": ["Today:"] + section(board, "🔥 Today") + ["This week:"] + section(board, "⏭ This Week") + ["Not yet sorted:"] + section(board, "📥 Captured"),
    "Saved Links": links or ["No saved links."],
    "Ellie Setup": [l for l in read("Standing Instructions.md").splitlines() if l.startswith("- ")][-25:],
    "Calendar": cal_lines or ["Nothing on the calendar in the next 7 days."],
}
topic_docs = {t: "<html><body>" + h(f"Where we left off - {t}", COLOR_OF[t]) + f"<p>Updated {now.strftime('%Y-%m-%d')}</p>" + ul(items) + "</body></html>"
              for t, items in topics.items()}

if DRY:
    print(f"DRY RUN: captures={len(captures)} would_trash={len(trashed)} kept={len(kept)} events={len(cal_lines)} board_chars={len(doc)}")
    for f, s in trashed:
        print("  would trash:", f, "|", s)
    for line in plan_log:
        print("  plan:", line)
    for r in mail_rows:
        print("  mail:", r)
    print("  reminders:", reminders)
    print("  ai tokens:", usage)
    print("  topic files:", {t: len(d) for t, d in topic_docs.items()})
    print("\n".join(cal_lines))
    sys.exit(0)

# --- write vault, then Drive
open("Task Board.md", "w", encoding="utf-8").write(board)
open("routines/trash-rules.md", "w", encoding="utf-8").write(rules)
open("Memory.md", "w", encoding="utf-8").write(memory)
open("Applications.md", "w", encoding="utf-8").write(apps)


def blk(title: str, items: list[str]) -> list[str]:
    return [f"## {title}"] + ([f"- {i}" for i in items] if items else ["- (none)"]) + [""]


open("Handoff.md", "w", encoding="utf-8").write("\n".join(
    [f"# Handoff - {now.strftime('%Y-%m-%d %-I:%M%p')} ET", "Read this first in a new chat. Rebuilt by scripts/phone_sync.py at every sync; do not hand-edit.", ""]
    + blk("Filed this run", added) + blk("Closed today", done_today) + blk("Open: Today", section(board, "🔥 Today")) + blk("Open: This week", section(board, "⏭ This Week"))
    + blk("Waiting on", waiting_rows) + blk("Calendar, next 7 days", cal_lines)
    + ["## Where things live",
       "- Vault: GitHub missophs/Executive-Assistant (Task Board.md, Applications.md, Memory.md, Standing Instructions.md, routines/README.md changelog).",
       "- Phone: Drive Ellie Files / Ellie (live board), Tell Ellie (capture), Where we left off - <Topic> files in the topic folders.",
       "- Email: wrap-up 4:45pm ET from this repo (wrap-up.yml); Melissa Daily Briefing 7am ET from missophs/daily-briefing (branch webhooks).", ""]))
state["seen"] = sorted(seen)[-300:]
state["trashjudged"] = sorted(judged)[-300:]
state["ourtrash"] = sorted(ourtrash)[-300:]


def replace_doc(name: str, content: str, text_mime: str, parents: list[str] | None = None) -> None:
    scope = f" and '{parents[0]}' in parents" if parents else ""
    old = drive.files().list(q=f"name='{name}' and trashed=false{scope}", fields="files(id,parents)").execute().get("files", [])
    par = parents or (old[0].get("parents") if old else None) or ["18kMOjJuNFY_7u6rEVxsanFRUlX_GXJkh"]  # keep files where Melissa put them; new ones go in Ellie Files, never loose in Drive
    meta = {"name": name, **({"parents": par} if par else {})}
    if text_mime == "text/html":
        meta["mimeType"] = "application/vnd.google-apps.document"
    media = MediaIoBaseUpload(io.BytesIO(content.encode()), mimetype=text_mime)
    if old:  # rewrite in place: same file, Drive keeps every earlier version (File > Version history), nothing is trashed
        drive.files().update(fileId=old[0]["id"], media_body=media, fields="id").execute()
        print(f"updated {name} in place: {old[0]['id']}")
    else:
        new = drive.files().create(body=meta, media_body=media, fields="id").execute()
        print(f"created {name}: {new['id']}")


replace_doc("Ellie", doc, "text/html")
# Setup guide: Git is the source, the Drive copy is refreshed only when it changes
if os.path.exists("Docs/Setting Up Ellie.md"):
    import markdown
    guide = "<html><body>" + markdown.markdown(read("Docs/Setting Up Ellie.md"), extensions=["tables"]) + "</body></html>"
    gdigest = hashlib.md5(guide.encode()).hexdigest()
    if state.get("setup") != gdigest:
        fname = "Setting Up Ellie - Every Piece"
        found = drive.files().list(q=f"name='{fname}' and mimeType='application/vnd.google-apps.folder' and '18kMOjJuNFY_7u6rEVxsanFRUlX_GXJkh' in parents and trashed=false",
                                   fields="files(id)").execute().get("files", [])
        folder = found[0]["id"] if found else drive.files().create(body={"name": fname, "mimeType": "application/vnd.google-apps.folder",
                                   "parents": ["18kMOjJuNFY_7u6rEVxsanFRUlX_GXJkh"]}, fields="id").execute()["id"]
        replace_doc("Setting Up Ellie", guide, "text/html", [folder])
        state["setup"] = gdigest
for t, d in topic_docs.items():
    digest = hashlib.md5(d.replace(now.strftime("%Y-%m-%d"), "").encode()).hexdigest()
    if state.get("topics", {}).get(t) != digest:
        replace_doc(f"Where we left off - {t}", d, "text/html", [FOLDERS[t]])
        state.setdefault("topics", {})[t] = digest
if tell:
    replace_doc("Tell Ellie", f"<p>{PLACEHOLDER} Ellie files it at 6:30am and 4:30pm ET.</p>", "text/html", tell[0].get("parents"))

# --- midday email: 1pm only, and only if something actually happened (routines/email-template.md section 4)
if os.environ.get("LIGHT") == "1":
    built = build_midday(now, filed_notes, done_list, needs_call)
    if built:
        subject, email_body = built
        dup = gmail.users().messages().list(userId="me", q=f'in:sent newer_than:1d subject:"{subject}"').execute().get("messages")
        if dup:
            print("Midday email already sent today, not sending again.")
        else:
            msg = MIMEText(email_body, "html", "utf-8")
            msg["To"], msg["From"], msg["Subject"] = ME, ME, subject
            gmail.users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}).execute()
            print(f"Midday email sent: {subject}")

json.dump(state, open(STATE, "w"))
print(f"ai tokens: {usage}")
print(f"done: captures={len(captures)} trashed={len(trashed)} events={len(cal_lines)}")
