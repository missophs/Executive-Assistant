"""Builds the end-of-day wrap-up email (HTML) in the layout of routines/email-template.md.

Pure function: wrap_up.py passes in what it read from the vault and calendar. No gradients (Gmail strips them);
every background carries bgcolor + inline style. Colour key: red urgent, amber follow-up, blue calendar, green job search/done, purple other, gray low.
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


def _title(title: str, detail: str) -> str:
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;{B}">'
            f'<div style="{F}font-size:14px;font-weight:bold;color:#12233C;">{_e(title)}</div>'
            f'<div style="{F}font-size:13px;line-height:19px;color:#5C6B7F;padding-top:4px;">{_e(detail)}</div></td></tr>')


def _priority(action: str, why: str, due: str, bar: str) -> str:
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;{B}">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr>'
            f'<td width="4" bgcolor="{bar}" style="background-color:{bar};font-size:0;line-height:0;">&nbsp;</td><td style="padding-left:12px;">'
            f'<div style="{F}font-size:15px;font-weight:bold;color:#12233C;">{_e(action)}</div>'
            + (f'<div style="{F}font-size:13px;line-height:19px;color:#5C6B7F;padding-top:4px;">{_e(why)}</div>' if why else "")
            + (f'<div style="{F}font-size:11px;letter-spacing:0.4px;color:#93A0AF;padding-top:8px;">Due {_e(due)}</div>' if due else "")
            + "</td></tr></table></td></tr>")


def _time(when: str, what: str, color: str = "#2F6BFF") -> str:
    return (f'<tr><td width="150" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 0 12px 16px;{F}font-size:12px;font-weight:bold;color:{color};white-space:nowrap;{B}">{_e(when)}</td>'
            f'<td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:12px 16px 12px 10px;{F}font-size:13px;color:#33404F;{B}">{_e(what)}</td></tr>')


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
    cap = next((m.group(1) for p in parts for m in [re.match(r"captured (\d{4}-\d{2}-\d{2})", p)] if m), "")
    rest = [p for p in parts[1:] if not re.match(r"(due|captured) \d{4}-", p)]
    return parts[0].replace("**", "")[:160] if parts else task[:160], " — ".join(rest).replace("**", "")[:200], due, cap


def build_wrapup(now: datetime, done_today: list[str], filed: list[str], cal_added: list[str], focus: list[str], n_open: int,
                 waiting: list[tuple[str, str]], reminders: list[tuple[str, str]], pipeline: list[tuple[str, str]],
                 week: list[tuple[str, str]] | None) -> tuple[str, str]:
    """focus = open tasks from Today then This Week, board order. filed = everything captured into Ellie today.
    waiting = (who, detail). reminders = (YYYY-MM-DD, text) for the next 7 days. pipeline = (company - role, detail).
    week = (when, title) for the days ahead; None means the calendar could not be checked."""
    today = now.strftime("%Y-%m-%d")
    subject = f"Ellie - EA Wrap-Up - {now.strftime('%A, %B')} {now.day}"
    boxes: list[str] = []

    def add(title: str, accent: str, rows: list[str], colspan: bool = False) -> None:
        boxes.append(_box(title, accent, rows, first=not boxes, colspan=colspan))

    add("Closed Out Today", "#00D68F", [_plain([f"&#10003;&nbsp;{_e(d[:200])}" for d in done_today])] if done_today else [_empty("Nothing closed today.")])
    if filed:
        add("Filed Into Ellie Today", "#A239FF", [_plain([f"&#8226;&nbsp;{_e(f[:200])}" for f in filed])])
    if cal_added:
        add("Added To Your Calendar", "#2F6BFF", [_plain([_e(c.removeprefix("Calendar: ")) for c in cal_added])])
    if focus:
        bars = ["#FF3B3B", "#FFAA00", "#2F6BFF"]
        add("Carrying Into Tomorrow", "#FFAA00", [_priority(*_parse(t)[:1], _parse(t)[1], _parse(t)[2], bars[i]) for i, t in enumerate(focus[:3])])
    if focus[3:]:
        add("Also Open This Week", "#FFAA00", [_plain([f"&#8226;&nbsp;{_e(_parse(t)[0])}" + (f" (due {_parse(t)[2]})" if _parse(t)[2] else "") for t in focus[3:12]])])
    slipping = []
    for t in focus:
        a, _, due, cap = _parse(t)
        age = (now.date() - datetime.strptime(cap, "%Y-%m-%d").date()).days if cap else 0
        if due and due < today:
            slipping.append(_title(a, f"Overdue since {due}"))
        elif age >= 3:
            slipping.append(_title(a, f"Captured {cap}, no movement in {age} days"))
    if slipping:
        add("Slipping", "#FF3B3B", slipping[:5])
    if week is None:
        rows = [_empty("Calendar could not be checked.")]
    elif week:
        rows = [_time(w, s) for w, s in week]
    else:
        rows = [_empty("Calendar is clear.")]
    add("Calendar - Week Ahead", "#2F6BFF", rows, colspan=bool(week))
    if reminders:
        add("Reminders - Next 7 Days", "#FFAA00", [_time(datetime.strptime(d, "%Y-%m-%d").strftime("%a %-m/%-d"), t[:160], "#B26A00") for d, t in reminders])
    if waiting:
        add("Waiting On", "#FFAA00", [_title(w, d[:200]) for w, d in waiting[:10]])
    if pipeline:
        add("Job Pipeline", "#00D68F", [_title(t, d[:220]) for t, d in pipeline[:8]])
    add("Where To Look", "#8994A3", [_plain([
        "Phone board: Google Drive &rarr; Ellie Files &rarr; <b>Ellie</b> (rebuilt 6:30am and 4:30pm ET).",
        "Topic files, one per folder: <b>Where we left off</b> - Job Search, Meetings &amp; Prep, Reminders &amp; Tasks, Saved Links, Ellie Setup, Calendar.",
        "To capture something: write it in the Drive file <b>Tell Ellie</b> or email yourself."])])

    mast = "#3B1B8F"
    body = (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F3F1FB" style="background-color:#F3F1FB;"><tr><td align="center" style="padding:26px 10px;">'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="width:100%;max-width:600px;background-color:#FFFFFF;border:1px solid #E5E0F5;border-radius:8px;">'
        f'<tr><td bgcolor="{mast}" style="background-color:{mast};padding:28px 26px 24px 26px;border-radius:7px 7px 0 0;">'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
        f'<tr><td style="{F}font-size:10px;font-weight:bold;letter-spacing:2.4px;text-transform:uppercase;color:#FFAA00;padding-bottom:9px;">Ellie &nbsp;&middot;&nbsp; End of Day</td></tr>'
        f'<tr><td style="font-family:Georgia,\'Times New Roman\',serif;font-size:28px;line-height:33px;color:#FFFFFF;">{now.strftime("%A, %B")} {now.day}</td></tr>'
        f'<tr><td style="{F}font-size:12px;line-height:18px;color:#F5E9FF;padding-top:10px;">{len(done_today)} done today &nbsp;&middot;&nbsp; {n_open} still open &nbsp;&middot;&nbsp; {len(waiting)} awaiting reply</td></tr>'
        '</table></td></tr>'
        f'<tr><td style="padding:22px;">{"".join(boxes)}</td></tr>'
        '<tr><td bgcolor="#F5F7FA" style="background-color:#F5F7FA;border-top:1px solid #D7DEE7;padding:14px;text-align:center;font-family:Georgia,\'Times New Roman\',serif;font-size:13px;font-style:italic;color:#8994A3;border-radius:0 0 7px 7px;">Ellie</td></tr>'
        "</table></td></tr></table>")
    return subject, body


if __name__ == "__main__":  # runnable check: python scripts/wrapup_email.py
    n = datetime(2026, 9, 26, 16, 30)
    s, h = build_wrapup(n, ["Call Anthem — done 2026-09-26"], ["Saved link: Marsh CPO role"], ["Vet — Wed 9/30 · all day"],
                        ["Call NYC about documents — due 2026-09-29 — captured 2026-09-26 · #task · #priority", "Old thing — due 2026-09-20 — captured 2026-09-10 · #task",
                         "Third", "Fourth thing — due 2026-10-01"],
                        7, [("Ashley Fredericks (LRN)", "since 2026-09-25 — awaiting decision")], [("2026-09-29", "Call NYC")],
                        [("LRN - VP of People", "Screen · last contact 2026-09-25: awaiting decision")],
                        [("Sun 9/27 · 9:00am", "Standup"), ("Mon 9/28 · all day", "Doctor")])
    assert s == "Ellie - EA Wrap-Up - Saturday, September 26" and h.startswith("<table") and "$(" not in h and "/tmp/" not in h and "gradient" not in h
    for needle in ("Overdue since 2026-09-20", "Standup", "Call NYC about documents", "Marsh CPO", "Calendar - Week Ahead", "Also Open This Week",
                   "Fourth thing", "Waiting On", "Ashley Fredericks", "Reminders - Next 7 Days", "Job Pipeline", "Where To Look", "1 awaiting reply"):
        assert needle in h, needle
    s2, h2 = build_wrapup(n, [], [], [], [], 0, [], [], [], None)
    assert "Nothing closed today." in h2 and "Calendar could not be checked." in h2 and "Carrying Into Tomorrow" not in h2 and "Waiting On" not in h2
    print("ok")
