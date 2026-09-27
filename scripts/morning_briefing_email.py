"""Builds the single combined morning email (HTML) in the layout of routines/email-template.md.

Pure function: morning_briefing.py passes in what it read from Gmail, Calendar and the vault.
No gradients (Gmail strips them); every background carries bgcolor + inline style. Replaces the
separate "Melissa Daily Briefing" (missophs/daily-briefing) and the old paused "Ellie — Morning
Standup" cloud routine with one email: subject "Ellie - EA - <date>".
"""
import html
import re
from datetime import datetime

F = "font-family:Helvetica,Arial,sans-serif;"
B = "@B@"  # row border placeholder: filled for every row except the last of a box


def _e(t: str) -> str:
    return html.escape(t, quote=False)


def _plain(lines: list[str]) -> str:
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;{F}font-size:13px;line-height:21px;color:#5C6B7F;{B}">'
            + "<br>".join(lines) + "</td></tr>")


def _empty(msg: str) -> str:
    return f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;{F}font-size:13px;color:#93A0AF;">{_e(msg)}</td></tr>'


def _title(title: str, detail: str = "") -> str:
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;{B}">'
            f'<div style="{F}font-size:14px;font-weight:bold;color:#12233C;">{_e(title)}</div>'
            + (f'<div style="{F}font-size:13px;line-height:19px;color:#5C6B7F;padding-top:4px;">{_e(detail)}</div>' if detail else "")
            + "</td></tr>")


def _prep(date_label: str, what: str, checklist: list[str]) -> str:
    """Like a TITLE row, but the detail is a bulleted checklist instead of one line."""
    items = "<br>".join(f"&#8226;&nbsp;{_e(c)}" for c in checklist) if checklist else _e("not in vault")
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;{B}">'
            f'<div style="{F}font-size:14px;font-weight:bold;color:#12233C;">{_e(date_label)} &mdash; {_e(what)}</div>'
            f'<div style="{F}font-size:13px;line-height:19px;color:#5C6B7F;padding-top:4px;">{items}</div></td></tr>')


def _priority(action: str, why: str, due: str, bar: str) -> str:
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;{B}">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr>'
            f'<td width="4" bgcolor="{bar}" style="background-color:{bar};font-size:0;line-height:0;">&nbsp;</td><td style="padding-left:12px;">'
            f'<div style="{F}font-size:15px;font-weight:bold;color:#12233C;">{_e(action)}</div>'
            + (f'<div style="{F}font-size:13px;line-height:19px;color:#5C6B7F;padding-top:4px;">{_e(why)}</div>' if why else "")
            + (f'<div style="{F}font-size:11px;letter-spacing:0.4px;color:#93A0AF;padding-top:8px;">Due {_e(due)}</div>' if due else "")
            + "</td></tr></table></td></tr>")


def _time(when: str, what: str, conflict: bool = False, rsvp: bool = False) -> str:
    color = "#FF3B3B" if conflict else "#2F6BFF"
    tag = ""
    if conflict:
        tag += ' <span style="color:#FF3B3B;font-weight:bold;">&#9888;&nbsp;CONFLICT</span>'
    if rsvp:
        tag += ' <span style="color:#FFAA00;font-weight:bold;">RSVP NEEDED</span>'
    return (f'<tr><td width="150" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 0 12px 16px;{F}font-size:12px;font-weight:bold;color:{color};white-space:nowrap;{B}">{_e(when)}</td>'
            f'<td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 16px 12px 10px;{F}font-size:13px;color:#33404F;{B}">{_e(what)}{tag}</td></tr>')


def _triage_rows(inbox_rows: list[tuple[bool, str, str, str]]) -> list[str]:
    """Email Triage Quick List as an actual table (ported from missophs/daily-briefing, was a plain
    list here before 2026-09-27)."""
    hcell = f'style="{F}font-size:10px;font-weight:bold;letter-spacing:0.6px;text-transform:uppercase;color:#8994A3;padding:8px 12px;background-color:#F5F7FA;"'
    rows = [f'<tr><td bgcolor="#F5F7FA" {hcell}>From</td><td bgcolor="#F5F7FA" {hcell}>Subject</td><td bgcolor="#F5F7FA" {hcell}>Note</td></tr>']
    for needs, frm, subj, line in inbox_rows[:15]:
        bg = "#FDEDED" if needs else "#FFFFFF"
        badge = '<span style="color:#FF3B3B;font-weight:bold;">NEEDS YOU</span>&nbsp;' if needs else ""
        cell = f'bgcolor="{bg}" style="background-color:{bg};padding:10px 12px;{F}font-size:12px;border-bottom:1px solid #E9EDF2;"'
        rows.append(f'<tr><td {cell}font-weight:bold;color:#12233C;">{badge}{_e(frm)}</td>'
                    f'<td {cell}color:#33404F;">{_e(subj)}</td>'
                    f'<td {cell}color:#5C6B7F;">{_e(line)}</td></tr>')
    if len(rows) > 1:
        rows[-1] = rows[-1].replace("border-bottom:1px solid #E9EDF2;", "")
    return rows


def _stale(who: str, what: str, days: int) -> str:
    bg, ink = ("#F2D6D7", "#8A2B30") if days >= 10 else ("#F5E9CB", "#7A5A18") if days >= 5 else ("#DCE6F5", "#24456F")
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 10px 12px 16px;{B}">'
            f'<div style="{F}font-size:13px;font-weight:bold;color:#12233C;">{_e(who)}</div>'
            f'<div style="{F}font-size:12px;color:#8994A3;padding-top:2px;">{_e(what)}</div></td>'
            f'<td align="right" width="60" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 16px 12px 0;{B}">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="right"><tr>'
            f'<td bgcolor="{bg}" style="background-color:{bg};border-radius:3px;padding:4px 9px;{F}font-size:11px;font-weight:bold;color:{ink};">{days}d</td>'
            "</tr></table></td></tr>")


def _box(title: str, accent: str, rows: list[str], first: bool, colspan: bool = False) -> str:
    border = "border-bottom:1px solid #E9EDF2;"
    rows = [r.replace(B, border) for r in rows[:-1]] + [rows[-1].replace(B, "")]
    span = ' colspan="2"' if colspan else ""
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid #D7DEE7;border-radius:6px;{"" if first else "margin-top:16px;"}">'
            f'<tr><td{span} bgcolor="#F5F7FA" style="background-color:#F5F7FA;padding:10px 16px;border-bottom:1px solid #D7DEE7;border-radius:5px 5px 0 0;">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td bgcolor="{accent}" width="9" height="9" style="background-color:{accent};font-size:0;line-height:0;">&nbsp;</td>'
            f'<td style="padding-left:9px;{F}font-size:10px;font-weight:bold;letter-spacing:1.8px;text-transform:uppercase;color:#44546B;">{title}</td>'
            "</tr></table></td></tr>" + "".join(rows) + "</table>")


def _parse(task: str) -> tuple[str, str, str, str]:
    """(action, why, due, captured) from a board line like 'Do X — due 2026-09-29 — captured 2026-09-26 · #task'."""
    parts = [p.strip() for p in re.sub(r"\s*·\s*#\w+", "", task).split(" — ") if p.strip()]
    due = next((m.group(1) for p in parts for m in [re.match(r"due (\d{4}-\d{2}-\d{2})", p)] if m), "")
    rest = [p for p in parts[1:] if not re.match(r"(due|captured) \d{4}-", p)]
    return parts[0].replace("**", "")[:160] if parts else task[:160], " — ".join(rest).replace("**", "")[:200], due, ""


EA_COMMANDS = [
    ("/ea:setup", "Initialize memory, configure connectors"),
    ("/ea:sync", "Pull updates from Notion, Slack, GitHub into memory"),
    ("/ea:done", "Process completed items — archive, promote wins, update people files"),
    ("/ea:meeting-prep", "Generate prep docs with full context for any meeting"),
    ("/ea:assess", "Compare self-assessments against your manager notes"),
    ("/ea:draft-reply", "Draft a reply in your voice with full memory context"),
    ("/ea:review-doc", "Review a document, present feedback plan, post approved comments"),
    ("/ea:improve", "Audit and optimize the entire memory system"),
]  # ported from missophs/daily-briefing generate_briefing.py; /ea:inbox dropped per Standing Instructions ("skip /ea:inbox as a command — the briefing triages")


def build_morning(now: datetime, calendar_days: list[dict], rescued: list[tuple[str, str]], inbox_trashed: list[tuple[str, str]],
                  inbox_rows: list[tuple[bool, str, str, str]], prepare_items: list[tuple[str, str, list[str]]],
                  draft_candidates: list[tuple[str, str, str]], top3: list[str], waiting: list[tuple[str, str, int]],
                  role_count: int, awaiting_count: int, open_count: int,
                  action_items: list[str] | None = None, rsvp_needed: list[tuple[str, str]] | None = None) -> tuple[str, str]:
    """calendar_days = [{"label": "Sat 9/27", "events": [("9:00am", "Mahjong", conflict, rsvp), ...]}, ...] for 7 days,
    today first, every day included even with an empty events list. inbox_rows = (needs_her, from, subject, one-line
    summary), needs-first. prepare_items = (date label, what, checklist lines — vault-only, "not in vault" if
    missing). draft_candidates = (who, subject, why a reply is owed), highest value first, max 5. top3 = board lines,
    Today then This Week, board order. waiting = (who, what she's waiting on, days since). action_items = board
    lines with an explicit due date, any section, due-date order (not capped at 3 like top3). rsvp_needed =
    (day label, what) for events where she hasn't responded."""
    action_items = action_items or []
    rsvp_needed = rsvp_needed or []
    subject = f"Ellie - EA - {now.strftime('%A, %B')} {now.day}"
    boxes: list[str] = []

    def add(title: str, accent: str, rows: list[str], colspan: bool = False) -> None:
        boxes.append(_box(title, accent, rows, first=not boxes, colspan=colspan))

    conflict_count = sum(1 for day in calendar_days for e in day["events"] if e[2])
    needs_you_count = sum(1 for r in inbox_rows if r[0])
    summary_lines = []
    if top3:
        summary_lines.append(f"Top priority: {_parse(top3[0])[0]}")
    if needs_you_count:
        summary_lines.append(f"{needs_you_count} inbox item{'s' if needs_you_count != 1 else ''} need your call today")
    if waiting:
        summary_lines.append(f"Longest open wait: {waiting[0][0]} ({waiting[0][2]}d)")
    if rsvp_needed:
        summary_lines.append(f"{len(rsvp_needed)} event{'s' if len(rsvp_needed) != 1 else ''} awaiting your RSVP")
    if conflict_count:
        summary_lines.append(f"{conflict_count} calendar conflict{'s' if conflict_count != 1 else ''} this week — see Calendar")
    if not summary_lines:
        summary_lines.append("Nothing urgent. Light day.")
    add("Executive Summary", "#6D21C9", [_plain([f"&#8226;&nbsp;{_e(l)}" for l in summary_lines])])

    if rescued:
        add("Rescued From Trash", "#FF3B3B", [_title(f, s) for f, s in rescued[:10]])

    add("Inbox Triage — Quick List", "#2F6BFF", _triage_rows(inbox_rows) if inbox_rows else [_empty("Nothing new in the inbox.")], colspan=True)

    if inbox_trashed:
        add("Inbox Trash (undo from Gmail Trash if wrong)", "#8994A3", [_plain([f"&#8226;&nbsp;{_e(f)} &mdash; {_e(s)}" for f, s in inbox_trashed[:15]])])

    if action_items:
        def bar_for(due: str) -> str:
            try:
                days = (datetime.strptime(due, "%Y-%m-%d").date() - now.date()).days
            except ValueError:
                days = 99
            return "#FF3B3B" if days <= 0 else "#FFAA00" if days <= 3 else "#2F6BFF"
        add("Action Required", "#FF3B3B", [_priority(*_parse(t)[:3], bar_for(_parse(t)[2])) for t in action_items[:12]])

    cal_rows: list[str] = []
    for day in calendar_days:
        events = day["events"]
        cal_rows.append(_title(day["label"], "Nothing scheduled." if not events else ""))
        cal_rows.extend(_time(t, w, c, r) for t, w, c, r in events)
    add("Calendar — Next 7 Days", "#2F6BFF", cal_rows, colspan=True)

    if prepare_items:
        add("Prepare", "#2F6BFF", [_prep(d, w, c) for d, w, c in prepare_items])
    else:
        add("Prepare", "#2F6BFF", [_empty("Nothing to prepare this week.")])

    if draft_candidates:
        add("Draft Replies — Awaiting Your OK", "#A239FF",
            [_title(f"{i}. {who} — {subj}"[:140], why) for i, (who, subj, why) in enumerate(draft_candidates[:5], 1)])
        boxes.append('<div style="font-family:Helvetica,Arial,sans-serif;font-size:11px;color:#93A0AF;padding:7px 2px 0 2px;">'
                     'Tell Ellie the numbers you want drafted, e.g. &quot;Tell Ellie: draft 1 and 3.&quot; Nothing is sent — '
                     'drafts run through a humanize pass and land only in Gmail Drafts, only once you say which numbers. '
                     'Doing nothing drafts nothing.</div>')
    else:
        add("Draft Replies — Awaiting Your OK", "#A239FF", [_empty("No replies owed today.")])

    t3_rows: list[str] = []
    if top3:
        bars = ["#FF3B3B", "#FFAA00", "#2F6BFF"]
        t3_rows.extend(_priority(*_parse(t)[:3], bars[i]) for i, t in enumerate(top3[:3]))
    if waiting:
        t3_rows.extend(_stale(w, d, n) for w, d, n in waiting[:10])
    add("Top 3 &amp; Follow Up", "#FFAA00", t3_rows if t3_rows else [_empty("Nothing today, nothing waiting.")])

    add("Ellie Commands", "#44546B", [_title(c, d) for c, d in EA_COMMANDS])

    mast = "#6D21C9"
    body = (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F3F1FB" style="background-color:#F3F1FB;"><tr><td align="center" style="padding:26px 10px;">'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="width:100%;max-width:600px;background-color:#FFFFFF;border:1px solid #E5E0F5;border-radius:8px;">'
        f'<tr><td bgcolor="{mast}" style="background-color:{mast};padding:28px 26px 24px 26px;border-radius:7px 7px 0 0;">'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
        f'<tr><td style="{F}font-size:10px;font-weight:bold;letter-spacing:2.4px;text-transform:uppercase;color:#FFAA00;padding-bottom:9px;">Ellie &nbsp;&middot;&nbsp; Morning</td></tr>'
        f'<tr><td style="font-family:Georgia,\'Times New Roman\',serif;font-size:28px;line-height:33px;color:#FFFFFF;">{now.strftime("%A, %B")} {now.day}</td></tr>'
        f'<tr><td style="{F}font-size:12px;line-height:18px;color:#F5E9FF;padding-top:10px;">{role_count} active roles &nbsp;&middot;&nbsp; {awaiting_count} awaiting reply &nbsp;&middot;&nbsp; {open_count} open tasks</td></tr>'
        '</table></td></tr>'
        f'<tr><td style="padding:22px;">{"".join(boxes)}</td></tr>'
        '<tr><td bgcolor="#F5F7FA" style="background-color:#F5F7FA;border-top:1px solid #D7DEE7;padding:14px;text-align:center;font-family:Georgia,\'Times New Roman\',serif;font-size:13px;font-style:italic;color:#8994A3;border-radius:0 0 7px 7px;">Ellie</td></tr>'
        "</table></td></tr></table>")
    return subject, body


if __name__ == "__main__":  # runnable check: python scripts/morning_briefing_email.py
    n = datetime(2026, 9, 27, 7, 30)
    days = [{"label": "Sun 9/27", "events": [("9:00am", "Mahjong", False, False), ("9:30am", "Overlap test", True, False)]},
            {"label": "Mon 9/28", "events": [("1:00pm", "Doctor's appointment", False, True)]},
            {"label": "Tue 9/29", "events": [("all day", "Call New York City about documents", False, False)]},
            {"label": "Wed 9/30", "events": []},
            {"label": "Thu 10/1", "events": []},
            {"label": "Fri 10/2", "events": []},
            {"label": "Sat 10/3", "events": []}]
    s, h = build_morning(
        n, days,
        rescued=[("Nasreen Bharoocha", "Re: Conduit Health")],
        inbox_trashed=[("email.openai.com", "Look what you can do now")],
        inbox_rows=[(True, "Ashley Fredericks", "Re: LRN screen", "Awaiting her decision after the video screen"),
                    (False, "LinkedIn", "New jobs for you", "Weekly digest, no action needed")],
        prepare_items=[],
        draft_candidates=[("Ashley Fredericks", "Re: LRN screen", "Screen held 9/25, thank-you sent — she may reply, watch for it")],
        top3=["Call New York City about documents — due 2026-09-29 — captured 2026-09-26 · #task · #priority"],
        waiting=[("Ashley Fredericks (LRN)", "Awaiting her decision after the video screen", 2),
                 ("Patsy Doerr (LRN)", "No reply to your outreach yet", 11)],
        role_count=14, awaiting_count=7, open_count=41,
        action_items=["Call New York City about documents — due 2026-09-29 — captured 2026-09-26 · #task",
                     "Renew notary bond — due 2026-09-26 — captured 2026-09-20 · #task"],
        rsvp_needed=[("Mon 9/28", "Doctor's appointment")],
    )
    assert s == "Ellie - EA - Sunday, September 27" and h.startswith("<table") and "$(" not in h and "/tmp/" not in h and "gradient" not in h.replace("background-image:linear-gradient", "")
    for needle in ("Executive Summary", "Top priority: Call New York City", "awaiting your RSVP", "calendar conflict", "Rescued From Trash",
                   "Nasreen Bharoocha", "Inbox Triage — Quick List", "NEEDS YOU", "Inbox Trash", "Action Required", "Renew notary bond",
                   "Calendar — Next 7 Days", "Mahjong", "CONFLICT", "RSVP NEEDED", "Nothing scheduled.", "Prepare",
                   "Nothing to prepare this week.", "Draft Replies", "Tell Ellie: draft 1 and 3",
                   "Top 3 &amp; Follow Up", "Call New York City", "Patsy Doerr", "11d", "Ellie Commands", "/ea:setup"):
        assert needle in h, needle
    s2, h2 = build_morning(n, [{"label": "Sun 9/27", "events": []}] * 7, [], [], [], [], [], [], [], 0, 0, 0)
    assert "Nothing new in the inbox." in h2 and "No replies owed today." in h2 and "Nothing today, nothing waiting." in h2 and "Nothing to prepare this week." in h2 and "Nothing urgent. Light day." in h2
    print("ok")
