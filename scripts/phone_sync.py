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

# --- file captures into the vault
board = read("Task Board.md")
rules = read("routines/trash-rules.md")
memory = read("Memory.md")
apps = read("Applications.md")
added: list[str] = []
always: list[str] = []
plan_log: list[str] = []
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
              '{"i":<note number>,"kind":"task|application|memory|link|done|calendar|prep|trash|unclear","text":"short clean version",'
              '"match":<open task number or null, for done>,"date":"YYYY-MM-DD or null","time":"HH:MM or null","sender":"for trash"}.\n'
              "kind meanings: task=something to do or a reminder; application=company/role/recruiter/stage news; memory=person, preference or decision; "
              "link=bare link with no action; done=says something is finished or cancelled (set match to the open task number); "
              "calendar=explicit request to put something on the calendar (needs date); prep=starts with Prep:; trash=always trash a sender; unclear=cannot tell. "
              "Never invent facts. Output only the JSON array.\n\nOPEN TASKS:\n" +
              "\n".join(f"{n}. {t[:110]}" for n, t in enumerate(open_tasks, 1)) + "\n\nNOTES:\n" +
              "\n".join(f"{n}. {t[:600]}" for n, (_, t) in enumerate(items, 1)))
    txt = ask_haiku(prompt, 1500)
    return json.loads(txt[txt.index("["):txt.rindex("]") + 1])


open_tasks = [l for l in board.splitlines() if l.startswith("- [ ]")]
plan: list[dict] = []
if captures and os.environ.get("ANTHROPIC_API_KEY"):
    try:
        plan = classify(captures, open_tasks)
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
    elif kind == "memory":
        memory = add_after(memory, "Decisions & Context", f"- {today}: {text}")
        added.append(text)
    elif kind == "link":
        memory = add_after(memory, "Saved Links", f"- {today}: {text}")
        added.append(text)
    elif kind == "done":
        n = item.get("match")
        if isinstance(n, int) and 1 <= n <= len(open_tasks) and open_tasks[n - 1] in board:
            board = board.replace(open_tasks[n - 1] + "\n", "", 1)
            text = re.sub(r"^- \[ \] ", "", open_tasks[n - 1])[:150]
        board = add_after(board, "✅ Done", f"- [x] {text} — done {today}")
    elif kind == "trash":
        always.append((item.get("sender") or text).lower())
    elif kind == "calendar" and item.get("date"):
        day = item["date"]
        t0 = item.get("time")
        existing = cal.events().list(calendarId="primary", timeMin=f"{day}T00:00:00-04:00", timeMax=f"{day}T23:59:59-04:00",
                                     singleEvents=True, timeZone="America/New_York").execute().get("items", [])
        if not any(e.get("summary", "").lower() == text.lower() for e in existing) and not DRY:
            if t0:
                end = (datetime.fromisoformat(f"{day}T{t0}") + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:00")
                when = {"start": {"dateTime": f"{day}T{t0}:00", "timeZone": "America/New_York"},
                        "end": {"dateTime": end, "timeZone": "America/New_York"}}
            else:
                when = {"start": {"date": day}, "end": {"date": (datetime.fromisoformat(day) + timedelta(days=1)).strftime("%Y-%m-%d")}}
            cal.events().insert(calendarId="primary", body={"summary": text, **when}).execute()
        added.append(f"Calendar: {text} {day}")
        if item.get("priority"):  # a calendar block she also called a priority is a task too
            board = add_after(board, "🔥 Today" if day == today else "⏭ This Week", f"- [ ] {text} — due {day} — captured {today} · #task · #priority")
    elif kind == "prep":
        board = add_after(board, "Needs Melissa", f"- [ ] Prep requested: {text} (Ellie prep docs not automated yet) — {today}")
    else:  # unclear or unsorted
        board = add_after(board, "📥 Captured (unsorted)", f"- [ ] {src[:400]} — captured {today} · #unsorted")
        added.append(src[:80])
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
for t in gmail.users().threads().list(userId="me", q="in:inbox newer_than:1d").execute().get("threads", []):
    th = gmail.users().threads().get(userId="me", id=t["id"], format="metadata", metadataHeaders=["From", "Subject"]).execute()
    hd = {h["name"]: h["value"] for h in th["messages"][0]["payload"]["headers"]}
    frm, subj = hd.get("From", "").lower(), hd.get("Subject", "")
    hay = f"{subj} {th['messages'][0].get('snippet', '')}".lower()
    if any(p in frm for p in protected) or any(n in hay for n in never_subj):
        if not subj.lower().startswith(OWN_MAIL):
            kept.append((t["id"], hd.get("From", ""), subj, th["messages"][0].get("snippet", "")))
        continue
    if any(a in frm for a in always_l):
        trashed.append((hd.get("From", ""), subj))
        if not DRY:
            gmail.users().threads().trash(userId="me", id=t["id"]).execute()
        continue
    if not subj.lower().startswith(OWN_MAIL):
        kept.append((t["id"], hd.get("From", ""), subj, th["messages"][0].get("snippet", "")))

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


# --- inbox triage: one Haiku line per NEW thread, cached by thread id
mail_cache = state.setdefault("mail", {})
fresh = [k for k in kept if k[0] not in mail_cache]
if fresh and os.environ.get("ANTHROPIC_API_KEY"):
    try:
        out = ask_haiku(f"Today is {today}. Melissa is a senior HR executive job searching. For each inbox email return a JSON array, same order: "
                        '{"i":<n>,"needs":true|false,"line":"one plain line, max 14 words, what it is and any amount or deadline"}. '
                        "needs=true only for replies awaited, recruiter or interview mail, deadlines, security or money alerts. Never invent facts. JSON only.\n\n" +
                        "\n".join(f"{n}. From: {f[:60]} | Subject: {sb[:90]} | {sn[:160]}" for n, (_, f, sb, sn) in enumerate(fresh, 1)), 1200)
        for r in json.loads(out[out.index("["):out.rindex("]") + 1]):
            if 1 <= r.get("i", 0) <= len(fresh):
                mail_cache[fresh[r["i"] - 1][0]] = [bool(r.get("needs")), str(r.get("line", ""))[:140]]
    except Exception as exc:
        print("AI mail triage failed:", exc)
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
page = [f"<h1>ELLIE - LIVE BOARD</h1><p>Melissa Weiss, Senior HR executive, New York (US Eastern). Last updated: {now.strftime('%Y-%m-%d %-I:%M%p')} ET</p>",
        h("What happened today", "green"),
        ul([f"Filed {len(added)} new capture(s)"] + [f"Closed: {d}" for d in done_today] + ([f"Always-trash added: {', '.join(always)}"] if always else [])),
        h("On your calendar, rest of the week", "blue"), ul(cal_lines),
        h("Reminders, next 7 days", "amber"), ul([f"{d}: {t}" for d, t in reminders]),
        h("Inbox: what needs you and what else is there", "blue"),
        ("<table border='1' cellpadding='4'><tr><th>Status</th><th>From</th><th>Subject</th><th>Summary</th></tr>" +
         "".join(f"<tr><td style='color:{COLORS['red' if n else 'gray']}'>{'NEEDS YOU' if n else 'INBOX'}</td><td>{html.escape(f)}</td><td>{html.escape(sb)}</td><td>{html.escape(ln)}</td></tr>"
                 for n, f, sb, ln in mail_rows) + "</table>") if mail_rows else "<p>Nothing new in the inbox.</p>",
        h("Inbox trash (undo from Gmail Trash if wrong)", "red"), ul([f"{f} | {s}" for f, s in trashed]),
        h("Current priorities", "green"), ul([trunc(x, 420) for x in section(memory, "Current Priorities")[:3]]),
        h("Today", "red"), ul(section(board, "🔥 Today")),
        h("This week", "amber"), ul(section(board, "⏭ This Week")),
        h("Captured, not yet sorted", "purple"), ul(section(board, "📥 Captured")),
        h("Application pipeline (open roles)", "green"), ul(pipeline(apps)),
        h("Waiting on", "amber"), ul(section(board, "⏳ Waiting On")),
        h("People", "blue"), ul([trunc(x, 200) for x in section(memory, "People")[:30]]),
        h("Decisions & context", "purple"), ul([trunc(x, 260) for x in section(memory, "Decisions & Context")[:15]]),
        h("Backlog", "gray"), ul(section(board, "📋 Backlog")),
        "<p>To close a task, tell Ellie: mark it done. To capture, write in the Tell Ellie file.</p>"]
doc = "<html><body>" + "".join(page) + "</body></html>"

# --- "Where we left off" topic files (rebuilt only when their content changed)
FOLDERS = {"Job Search": "1EJE9YAHK2pnaLZ8o-VkXF6g1bpq4ydtu", "Meetings & Prep": "1Y1DKfI-w471txK-t4Zlp6EhXYHW3J5Bm",
           "Reminders & Tasks": "1K8Aleb9OqEDmroWDQtuF2kbRZdEuXzI9", "Saved Links": "14nnStHuMg8uPtxvq53GY1UvxqSaMD7td",
           "Ellie Setup": "1hNbRyq0LmeudaDbPmqlqpSrNHluKfN9F", "Calendar": "1-9RxuHy0MaUD5rpb4I2-CjMixPt_Ghiv"}
COLOR_OF = {"Job Search": "green", "Meetings & Prep": "blue", "Reminders & Tasks": "amber", "Saved Links": "purple", "Ellie Setup": "gray", "Calendar": "blue"}
meet_files = sorted(f for f in os.listdir("Meetings") if f.endswith(".md")) if os.path.isdir("Meetings") else []
app_rows = [l for l in apps.splitlines() if l.startswith("|") and not l.startswith("|---")][:40]
links = section(memory, "Saved Links")[:15]
topics = {
    "Job Search": (app_rows or ["No applications listed."]) + ["Waiting on:"] + section(board, "⏳ Waiting On"),
    "Meetings & Prep": [f"Prep doc: {f}" for f in meet_files[-10:]] or ["No prep docs yet."],
    "Reminders & Tasks": ["Today:"] + section(board, "🔥 Today") + ["This week:"] + section(board, "⏭ This Week") + ["Not yet sorted:"] + section(board, "📥 Captured"),
    "Saved Links": links or ["No saved links."],
    "Ellie Setup": [l for l in read("Standing Instructions.md").splitlines() if l.startswith("- ")][-25:],
    "Calendar": cal_lines or ["Nothing left on the calendar this week."],
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
state["seen"] = sorted(seen)[-300:]


def replace_doc(name: str, content: str, text_mime: str, parents: list[str] | None = None) -> None:
    scope = f" and '{parents[0]}' in parents" if parents else ""
    old = drive.files().list(q=f"name='{name}' and trashed=false{scope}", fields="files(id,parents)").execute().get("files", [])
    par = parents or (old[0].get("parents") if old else None) or ["18kMOjJuNFY_7u6rEVxsanFRUlX_GXJkh"]  # keep files where Melissa put them; new ones go in Ellie Files, never loose in Drive
    meta = {"name": name, **({"parents": par} if par else {})}
    if text_mime == "text/html":
        meta["mimeType"] = "application/vnd.google-apps.document"
    media = MediaIoBaseUpload(io.BytesIO(content.encode()), mimetype=text_mime)
    new = drive.files().create(body=meta, media_body=media, fields="id").execute()
    for o in old:
        drive.files().update(fileId=o["id"], body={"trashed": True}).execute()
    print(f"replaced {name}: new {new['id']}, trashed {len(old)}")


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
json.dump(state, open(STATE, "w"))
print(f"ai tokens: {usage}")
print(f"done: captures={len(captures)} trashed={len(trashed)} events={len(cal_lines)}")
