"""Builds the single combined morning email (HTML) in the layout of routines/email-template.md.

Pure function: morning_briefing.py passes in what it read from Gmail, Calendar and the vault.
No gradients (Gmail strips them); every background carries bgcolor + inline style. Replaces the
separate "Melissa Daily Briefing" (missophs/daily-briefing) and the old paused "Ellie — Morning
Standup" cloud routine with one email: subject "Ellie - EA - <date>".
"""
import html
import re
from datetime import datetime

from ellie_ui import box as _box, header
from briefing_cards import calendar_rows, draft_rows, mail_action_cards, summary_cards, triage_rows

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
    """Blue card like the old briefing's Prepare: date label + event, then a check-marked list."""
    items = "".join(f'<div style="padding:3px 0 3px 8px;">&#9989;&nbsp;{_e(c)}</div>' for c in checklist) if checklist else _e("not in vault")
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:10px 12px;{B}">'
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
            '<td width="4" bgcolor="#2F6BFF" style="background-color:#2F6BFF;font-size:0;line-height:0;">&nbsp;</td>'
            f'<td bgcolor="#EAF2FB" style="background-color:#EAF2FB;padding:12px 14px;">'
            f'<div style="{F}font-size:14px;font-weight:bold;color:#12233C;">{_e(date_label)} &mdash; {_e(what)}</div>'
            f'<div style="{F}font-size:13px;line-height:19px;color:#33404F;padding-top:6px;">{items}</div></td></tr></table></td></tr>')


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


def _stale(who: str, what: str, days: int) -> str:
    bg, ink = ("#F2D6D7", "#8A2B30") if days >= 10 else ("#F5E9CB", "#7A5A18") if days >= 5 else ("#DCE6F5", "#24456F")
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 10px 12px 16px;{B}">'
            f'<div style="{F}font-size:13px;font-weight:bold;color:#12233C;">{_e(who)}</div>'
            f'<div style="{F}font-size:12px;color:#8994A3;padding-top:2px;">{_e(what)}</div></td>'
            f'<td align="right" width="60" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 16px 12px 0;{B}">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="right"><tr>'
            f'<td bgcolor="{bg}" style="background-color:{bg};border-radius:3px;padding:4px 9px;{F}font-size:11px;font-weight:bold;color:{ink};">{days}d</td>'
            "</tr></table></td></tr>")


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




CATS = ["Security / Risk", "Phishing / Scam", "Job Search", "Recruiters / Networking", "Calendar / Events", "Medical / Health", "Financial / Billing",
        "Professional Development", "Personal", "Newsletters / Subscriptions", "Promotional / Retail", "Other"]
CAT_ACTION = {"Security / Risk": "Confirm it was you; call the company if not.", "Phishing / Scam": "Delete. Do not click anything.", "Job Search": "Review alerts, apply to strong fits.",
              "Recruiters / Networking": "Reply if a person is waiting on you.", "Calendar / Events": "Check the date, RSVP if needed.", "Medical / Health": "Check for appointments or bills.",
              "Financial / Billing": "Confirm amounts and deadlines.", "Professional Development": "Read if useful.", "Personal": "Read when free.",
              "Newsletters / Subscriptions": "Keep or unsubscribe.", "Promotional / Retail": "Ignore or delete.", "Other": "Skim, then delete."}
KEEP_CATS = {"Security / Risk", "Job Search", "Recruiters / Networking", "Calendar / Events", "Medical / Health", "Financial / Billing", "Professional Development", "Personal"}
LOC_LABEL = {"inbox": "📥 Inbox", "rescued": "✅ Rescued", "trash": "🗑 Trash", "spam": "🚫 Spam", "other": "🗂 Archived"}
CELL = f"background-color:#FFFFFF;padding:10px 12px;{F}font-size:12px;color:#33404F;vertical-align:top;{B}"


def _grid(headers: list[str], rows: list[list[str]]) -> list[str]:
    """Table rows for a box: header row then data rows; cells are already-escaped HTML."""
    hc = f"background-color:#F5F7FA;padding:8px 12px;{F}font-size:10px;font-weight:bold;letter-spacing:0.6px;text-transform:uppercase;color:#8994A3;{B}"
    out = ["<tr>" + "".join(f'<td bgcolor="#F5F7FA" style="{hc}">{h}</td>' for h in headers) + "</tr>"]
    out += ["<tr>" + "".join(f'<td bgcolor="#FFFFFF" style="{CELL}">{c}</td>' for c in r) + "</tr>" for r in rows]
    return out


def _wide(text: str, cols: int, bg: str = "#F3F1FB") -> str:
    return f'<tr><td colspan="{cols}" bgcolor="{bg}" style="background-color:{bg};padding:10px 12px;{F}font-size:12px;color:#44546B;{B}">{text}</td></tr>'


def _senders(items: list[dict], n: int = 4) -> str:
    names = list(dict.fromkeys(_e(m["frm"]) for m in items))
    return ", ".join(names[:n]) + (f" +{len(names) - n} more" if len(names) > n else "")


def build_morning(now: datetime, calendar_days: list[dict], rescued: list[tuple[str, str]], inbox_trashed: list[tuple[str, str]],
                  inbox_rows: list[tuple[bool, str, str, str]], prepare_items: list[tuple[str, str, list[str]]],
                  draft_candidates: list[tuple[str, str, str]], top3: list[str], waiting: list[tuple[str, str, int]],
                  role_count: int, awaiting_count: int, open_count: int,
                  action_items: list[str] | None = None, rsvp_needed: list[tuple[str, str]] | None = None,
                  mail: list[dict] | None = None, pipeline: list[tuple[str, str, str]] | None = None,
                  cal_cards: list[str] | None = None, cal_rich: list[tuple[str, bool, list[dict]]] | None = None) -> tuple[str, str]:
    """calendar_days = [{"label": "Sat 9/27", "events": [("9:00am", "Mahjong", conflict, rsvp), ...]}, ...] for 7 days,
    today first, every day included even with an empty events list. inbox_rows = (needs_her, from, subject, one-line
    summary), needs-first. prepare_items = (date label, what, checklist lines — vault-only, "not in vault" if
    missing). draft_candidates = (who, subject, why a reply is owed), highest value first, max 5. top3 = board lines,
    Today then This Week, board order. waiting = (who, what she's waiting on, days since). action_items = board
    lines with an explicit due date, any section, due-date order (not capped at 3 like top3). rsvp_needed =
    (day label, what) for events where she hasn't responded. mail = every email from the last day, each
    {"frm","subj","line","cat","loc","needs"} with cat one of CATS and loc inbox|rescued|trash|spam|other.
    pipeline = (company - role, detail, High|Medium|Low fit)."""
    action_items = action_items or []
    rsvp_needed = rsvp_needed or []
    mail = [m for m in (mail or []) if m["loc"] != "spam"]  # Melissa 2026-10-01: nothing in Spam is reported
    pipeline = pipeline or []
    subject = f"Ellie - EA - {now.strftime('%A, %B')} {now.day}"
    boxes: list[str] = []

    def add(title: str, accent: str, rows: list[str], colspan: bool | int = False) -> None:
        boxes.append(_box(title, accent, rows, first=not boxes, colspan=colspan))

    by_cat = {c: [m for m in mail if m["cat"] == c] for c in CATS}
    n_mail, phishing, sec = len(mail), len(by_cat["Phishing / Scam"]), len(by_cat["Security / Risk"])
    n_events = sum(len(d["events"]) for d in calendar_days)
    conflict_count = sum(1 for day in calendar_days for e in day["events"] if e[2])
    needs_you = [r for r in inbox_rows if r[0]]
    in_trash = [m for m in mail if m["loc"] in ("trash", "spam")]
    review = [m for m in in_trash if m["cat"] in KEEP_CATS]

    def days_left(due: str) -> int:
        try:
            return (datetime.strptime(due, "%Y-%m-%d").date() - now.date()).days
        except ValueError:
            return 99

    # 1. triage quick list
    tri = rescued or inbox_rows
    auto_phish = [m for m in in_trash if m["cat"] == "Phishing / Scam"]
    auto_bulk = [m for m in in_trash if m["cat"] in ("Newsletters / Subscriptions", "Promotional / Retail")]
    rows_tri = triage_rows(rescued, inbox_rows, [(len(auto_phish), "phishing/scams"), (len(auto_bulk), "newsletters/promotions")],
                           len(in_trash) - len(auto_phish) - len(auto_bulk))
    add("Inbox Triage — Quick List", "#2F6BFF", rows_tri if (tri or in_trash) else [_empty("Nothing new in the inbox.")], colspan=4)

    # 2. executive summary: three cards, then the email-by-category list
    today_ev = calendar_days[0]["events"] if calendar_days else []
    job_alerts = [m for m in by_cat["Job Search"] if m["loc"] in ("inbox", "rescued")]
    recruiters = [m for m in by_cat["Recruiters / Networking"] if m["loc"] in ("inbox", "rescued")]
    risk = (f"{phishing} phishing/scam email{'s' if phishing != 1 else ''} caught; {sec} security/account alert{'s' if sec != 1 else ''} to confirm were you."
            if (phishing or sec) else "No security issues in the last 24 hours.")
    if needs_you:
        risk += f" {len(needs_you)} inbox item{'s' if len(needs_you) != 1 else ''} need your call today."
    iv_today = [e for e in today_ev if re.search(r"interview|screen", e[1], re.I)]
    job = (f"{iv_today[0][1]} TODAY at {iv_today[0][0]}. " if iv_today else (f"{pipeline[0][0]} — {pipeline[0][1]}. " if pipeline else "")) + \
        f"{len(job_alerts)} job alert{'s' if len(job_alerts) != 1 else ''}, {len(recruiters)} recruiter/networking message{'s' if len(recruiters) != 1 else ''} today."
    cal = (f"Today: " + " → ".join(f"{t} {w}" for t, w, *_ in today_ev[:6]) + ". ") if today_ev else "Nothing on the calendar today. "
    if conflict_count:
        cal += f"{conflict_count} calendar conflict{'s' if conflict_count != 1 else ''} this week. "
    if rsvp_needed:
        cal += f"{len(rsvp_needed)} RSVP{'s' if len(rsvp_needed) != 1 else ''} pending. "
    if action_items:
        cal += f"Next deadline: {_parse(action_items[0])[0]} ({_parse(action_items[0])[2]})."
    cal = cal.strip()
    # by category under the three cards (every non-spam email in exactly one category)
    cat_rows: list[str] = []
    for c in CATS:
        items = by_cat[c]
        if not items:
            continue
        cat_rows.append(_wide(f"<b>{_e(c)}</b> — {len(items)} email{'s' if len(items) != 1 else ''} · {_e(CAT_ACTION[c])}", 3))
        for m in items[:8]:
            cells = (_e(m["frm"]), _e(m["subj"][:90]), f'{LOC_LABEL.get(m["loc"], "")} — {_e(m["line"] or CAT_ACTION[c])}')
            cat_rows.append("<tr>" + "".join(f'<td bgcolor="#FFFFFF" style="{CELL}">{x}</td>' for x in cells) + "</tr>")
        if len(items) > 8:
            cat_rows.append(_wide(f"+{len(items) - 8} more in this category", 3, "#FFFFFF"))
    cards = [c.replace("<tr><td ", '<tr><td colspan="3" ', 1) for c in summary_cards(risk, job, cal)]
    add("Executive Summary", "#6D21C9", cards + ([_wide("<b>EMAIL BY CATEGORY</b>", 3, "#EDE7F8")] + cat_rows if cat_rows else [_empty("No mail in the last 24 hours.")]), colspan=3)

    # 3. action required
    def bar_for(due: str) -> str:
        d = days_left(due)
        return "#FF3B3B" if d <= 0 else "#FFAA00" if d <= 3 else "#2F6BFF"
    act_rows = (cal_cards or []) + mail_action_cards(mail, CAT_ACTION) + [_priority(*_parse(t)[:3], bar_for(_parse(t)[2])) for t in action_items[:12]]
    if act_rows:
        add("Action Required", "#FF3B3B", act_rows)

    # 3A. drafts (Daily Briefing look)
    add("Draft Replies — Awaiting Your OK", "#12A06B", draft_rows(
        [(who, subj, why) for who, subj, why in draft_candidates[:5]],
        'Tell Ellie the numbers you want drafted, e.g. "Tell Ellie: draft 1 and 3." Nothing is sent. Drafts run through a humanize pass and land only in your Gmail Drafts folder, only once you say which numbers. Doing nothing drafts nothing.'))

    # 4. calendar, 4A prepare
    cal_rows: list[str] = []
    for day in calendar_days:
        events = day["events"]
        cal_rows.append(_title(day["label"], "Nothing scheduled." if not events else ""))
        cal_rows.extend(_time(t, w, c, r) for t, w, c, r in events)
    add("Full 7-Day Calendar", "#2F6BFF", calendar_rows(cal_rich) if cal_rich else cal_rows, colspan=True)
    add("Prepare — Next 7 Days", "#2F6BFF", [_prep(d, w, c) for d, w, c in prepare_items] if prepare_items else [_empty("Nothing to prepare this week.")])

    # 5. job search pipeline
    job_rows = [_title(t, f"{fit} fit · {d}"[:240]) for t, d, fit in pipeline[:10]]
    job_rows += [_title(m["subj"][:100], f"Job alert · {m['line'] or m['frm']}"[:200]) for m in job_alerts[:5]]
    job_rows += [_title(m["subj"][:100], f"{m['frm']} · {m['line']}"[:200]) for m in recruiters[:5]]
    add("Job Search &amp; Interview Pipeline", "#00D68F", job_rows or [_empty("No open roles or new alerts.")])

    # 7. trash review
    restore = [f"{w} — {s}" for w, s in rescued]
    safe = [m for m in in_trash if m not in review]
    add("Trash Review", "#8994A3", [
        _title("Restore", "; ".join(restore)[:300] if restore else "Nothing to restore."),
        _title("Review", (f"{len(review)}: " + _senders(review) + " — look before they are gone.").replace("&amp;", "&") if review else "Nothing in Trash needs a second look."),
        _title("Safe to Delete", (f"{len(safe)}: " + _senders(safe) + ". Ellie never deletes permanently.").replace("&amp;", "&") if safe else "Nothing.")])

    # 8/9. promotional + newsletters, grouped by sender
    def group_rows(cat: str, keep_label: str) -> list[list[str]]:
        out = []
        for name in dict.fromkeys(m["frm"] for m in by_cat[cat]):
            g = [m for m in by_cat[cat] if m["frm"] == name]
            out.append([_e(name), str(len(g)), _e(g[0]["subj"][:80]), "Delete" if all(m["loc"] in ("trash", "spam") for m in g) else keep_label])
        return out
    promo = group_rows("Promotional / Retail", "Ignore")
    add("Promotional / Retail Summary", "#E0860B", _grid(["Sender", "Count", "Subject / theme", "Recommendation"], promo) if promo else [_empty("No promotional mail.")], colspan=4)
    news = group_rows("Newsletters / Subscriptions", "Keep or unsubscribe")
    add("Newsletters &amp; Subscriptions", "#A239FF", _grid(["Sender", "Count", "Subject / topic", "Recommendation"], news) if news else [_empty("No newsletters.")], colspan=4)

    # 10. accounting: counts add up to the total
    acct = [[_e(c), str(len(by_cat[c])), _e(CAT_ACTION[c])] for c in CATS if by_cat[c]] + [["<b>Total Emails Reviewed</b>", f"<b>{n_mail}</b>", ""]]
    add("Email Accounting", "#44546B", _grid(["Category", "Count", "Recommendation"], acct) if n_mail else [_empty("No mail in the last 24 hours.")], colspan=3)

    # 11. dashboard
    interviews = sum(1 for d in calendar_days for e in d["events"] if re.search(r"interview|screen", e[1], re.I))
    due_week = sum(1 for t in action_items if days_left(_parse(t)[2]) <= 7) + len(by_cat["Financial / Billing"])
    dash = [["Important unread (need your call)", str(len(needs_you))], ["Security alerts", str(sec)], ["Action items", str(len(action_items))],
            ["Upcoming meetings (7 days)", str(n_events)], ["Open job leads", str(role_count)], ["Interviews scheduled", str(interviews)],
            ["Bills / deadlines this week", str(due_week)], ["Trash items to review", str(len(review))], ["Awaiting reply", str(awaiting_count)], ["Open tasks", str(open_count)]]
    add("Dashboard", "#2F6BFF", _grid(["Item", "Now"], dash), colspan=2)

    # 12. action items table
    ai_rows = []
    for t in action_items[:15]:
        a, _w, due, _c = _parse(t)
        d = days_left(due)
        ai_rows.append(["HIGH" if d <= 0 else "MEDIUM" if d <= 3 else "LOW", _e(a), "Task Board", _e(due)])
    ai_rows += [["HIGH", _e(f"Reply / decide: {r[2]}"[:120]), _e(r[1]), "Today"] for r in needs_you[:5]]
    ai_rows.sort(key=lambda r: ["HIGH", "MEDIUM", "LOW"].index(r[0]))
    add("Action Items", "#00D68F", _grid(["Priority", "Action", "Source", "Due"], ai_rows) if ai_rows else [_empty("Nothing due.")], colspan=4)

    # 13. top 3 & follow up, then commands
    t3_rows: list[str] = []
    if top3:
        bars = ["#FF3B3B", "#FFAA00", "#2F6BFF"]
        t3_rows.extend(_priority(*_parse(t)[:3], bars[i]) for i, t in enumerate(top3[:3]))
    if waiting:
        t3_rows.extend(_stale(w, d, n) for w, d, n in waiting[:10])
    add("Top 3 &amp; Follow Up", "#FFAA00", t3_rows if t3_rows else [_empty("Nothing today, nothing waiting.")])
    add("Ellie Commands", "#44546B", [_title(c, d) for c, d in EA_COMMANDS])

    mast = "#6D21C9"
    interviews_today = sum(1 for e in (calendar_days[0]["events"] if calendar_days else []) if re.search(r"interview|screen", e[1], re.I))
    tiles = [("", str(n_mail), "Emails Reviewed"), ("", str(n_events), "Calendar Events (7-day window)"), ("", str(phishing), "Auto-Trashed (Phishing)"),
             ("", str(len(rescued)), "Rescued from Trash"), ("", str(interviews_today), "Interview Today"), ("⚠️", str(len(rsvp_needed)), "RSVPs Pending")]
    body = (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F3F1FB" style="background-color:#F3F1FB;"><tr><td align="center" style="padding:26px 10px;">'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="width:100%;max-width:600px;background-color:#FFFFFF;border:1px solid #E5E0F5;border-radius:8px;">'
        + header("Ellie &nbsp;&middot;&nbsp; Morning", now, 'Good morning, <b style="color:#E0C97F;font-weight:bold;">Melissa</b> ☀️', "Executive Daily Briefing", tiles, mast) +
        f'<tr><td style="padding:22px;">{"".join(boxes)}</td></tr>'
        '<tr><td bgcolor="#F5F7FA" style="background-color:#F5F7FA;border-top:1px solid #D7DEE7;padding:14px;text-align:center;font-family:Georgia,\'Times New Roman\',serif;font-size:13px;font-style:italic;color:#8994A3;border-radius:0 0 7px 7px;">Ellie</td></tr>'
        "</table></td></tr></table>")
    return subject, body


if __name__ == "__main__":  # runnable check: python scripts/morning_briefing_email.py (synthetic data only)
    n = datetime(2026, 9, 27, 7, 30)
    days = [{"label": "Sun 9/27", "events": [("9:00am", "Mahjong", False, False), ("9:30am", "Overlap test", True, False)]},
            {"label": "Mon 9/28", "events": [("1:00pm", "Doctor's appointment", False, True)]},
            {"label": "Tue 9/29", "events": [("all day", "Call about documents", False, False)]},
            {"label": "Wed 9/30", "events": []}, {"label": "Thu 10/1", "events": []}, {"label": "Fri 10/2", "events": []}, {"label": "Sat 10/3", "events": []}]
    mail = [{"frm": "Ashley F", "subj": "Re: screen", "line": "Awaiting her decision", "cat": "Recruiters / Networking", "loc": "inbox", "needs": True},
            {"frm": "LinkedIn", "subj": "New jobs", "line": "Weekly digest", "cat": "Job Search", "loc": "inbox", "needs": False},
            {"frm": "Cash App", "subj": "Payment declined", "line": "Fake", "cat": "Phishing / Scam", "loc": "trash", "needs": False},
            {"frm": "Bank", "subj": "Withdrawal", "line": "Confirm", "cat": "Financial / Billing", "loc": "trash", "needs": False},
            {"frm": "Retailer", "subj": "50% off", "line": "", "cat": "Promotional / Retail", "loc": "trash", "needs": False},
            {"frm": "SpamCo", "subj": "Casino bonus", "line": "", "cat": "Promotional / Retail", "loc": "spam", "needs": False},
            {"frm": "Daily Skimm", "subj": "News", "line": "", "cat": "Newsletters / Subscriptions", "loc": "inbox", "needs": False}]
    s, h = build_morning(
        n, days, rescued=[("Nasreen B", "Re: Acme")], inbox_trashed=[],
        inbox_rows=[(True, "Ashley F", "Re: screen", "Awaiting her decision"), (False, "LinkedIn", "New jobs", "Weekly digest")],
        prepare_items=[("Mon 9/28", "Acme prep", ["Stage: Screen"])],
        draft_candidates=[("Ashley F", "Re: screen", "She may reply")],
        top3=["Call about documents — due 2026-09-29 — captured 2026-09-26 · #task"],
        waiting=[("Ashley F (Acme)", "Awaiting decision", 2), ("Patsy D", "No reply yet", 11)],
        role_count=14, awaiting_count=7, open_count=41,
        action_items=["Call about documents — due 2026-09-29 — captured 2026-09-26 · #task", "Renew bond — due 2026-09-26 — captured 2026-09-20 · #task"],
        rsvp_needed=[("Mon 9/28", "Doctor's appointment")], mail=mail,
        pipeline=[("Acme - HR Director", "Screen · last contact 2026-09-25", "Medium")])
    assert s == "Ellie - EA - Sunday, September 27" and h.startswith("<table") and "$(" not in h and "/tmp/" not in h
    for needle in ("Good morning,", "Emails Reviewed", "Executive Summary", "1 phishing/scam email caught", "RSVP pending", "calendar conflict",
                   "Inbox Triage — Quick List", "NEEDS YOU", "RESCUED", "in Trash —", "AUTO-TRASHED", "BIGGEST RISK / URGENT", "BIGGEST JOB SEARCH / OPPORTUNITY", "BIGGEST CALENDAR / DEADLINE", "Why it matters:", "Review Withdrawal", "Action Required", "Renew bond", "Full 7-Day Calendar", "CONFLICT",
                   "RSVP NEEDED", "Prepare", "Draft Replies", "Tell Ellie: draft 1 and 3", "Job Search &amp; Interview Pipeline", "Medium fit",
                   "EMAIL BY CATEGORY", "Trash Review", "Restore", "Safe to Delete", "Promotional / Retail Summary", "Retailer",
                   "Newsletters &amp; Subscriptions", "Email Accounting", "Total Emails Reviewed", "Dashboard", "Action Items", "HIGH",
                   "Top 3 &amp; Follow Up", "Patsy D", "11d", "Ellie Commands", "/ea:setup"):
        assert needle in h, needle
    assert "<b>6</b>" in h and "SpamCo" not in h and "Full Email Review by Category" not in h  # spam excluded; accounting total equals mail count
    s2, h2 = build_morning(n, [{"label": "Sun 9/27", "events": []}] * 7, [], [], [], [], [], [], [], 0, 0, 0)
    for needle in ("Nothing new in the inbox.", "No replies owed today.", "Nothing today, nothing waiting.", "Nothing to prepare this week.",
                   "No security issues in the last 24 hours.", "No mail in the last 24 hours.", "Nothing due.", "No open roles or new alerts."):
        assert needle in h2, needle
    print("ok")
