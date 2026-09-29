"""Builds the 1pm midday email (HTML) in the layout of routines/email-template.md, section 4 "Midday".

Pure function, no I/O. Sections: Filed Your Notes, Marked Done, Needs Your Call. Omit any section
with nothing in it; if all are empty, the caller must send nothing (see build_midday's None return).
"""
import html
from datetime import datetime

from ellie_ui import box as _box, header

F = "font-family:Helvetica,Arial,sans-serif;"
B = "@B@"


def _e(t: str) -> str:
    return html.escape(t, quote=False)


def _plain(lines: list[str]) -> str:
    return (f'<tr><td bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:14px 16px;{F}font-size:13px;line-height:21px;color:#5C6B7F;{B}">'
            + "<br>".join(lines) + "</td></tr>")


def build_midday(now: datetime, filed: list[str], done: list[str], needs_call: list[str]) -> tuple[str, str] | None:
    """filed = notes/tasks/links filed this run. done = tasks closed out by a capture. needs_call = ambiguous
    captures she needs to resolve herself. Returns None if all three are empty: send nothing."""
    if not (filed or done or needs_call):
        return None
    subject = f"Ellie - EA Midday - {now.strftime('%A, %B')} {now.day}"
    boxes: list[str] = []

    def add(title: str, accent: str, rows: list[str]) -> None:
        boxes.append(_box(title, accent, rows, first=not boxes))

    if filed:
        add("Filed Your Notes", "#00D68F", [_plain([f"&#8226;&nbsp;{_e(f[:200])}" for f in filed])])
    if done:
        add("Marked Done", "#00D68F", [_plain([f"&#10003;&nbsp;{_e(d[:200])}" for d in done])])
    if needs_call:
        add("Needs Your Call", "#FFAA00", [_plain([f"&#8226;&nbsp;{_e(n[:200])}" for n in needs_call])])

    mast = "#D6249E"
    tiles = [("📥", str(len(filed)), "Filed"), ("✅", str(len(done)), "Marked done"), ("❓", str(len(needs_call)), "Needs your call")]
    body = (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F3F1FB" style="background-color:#F3F1FB;"><tr><td align="center" style="padding:26px 10px;">'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="width:100%;max-width:600px;background-color:#FFFFFF;border:1px solid #E5E0F5;border-radius:8px;">'
        + header("Ellie &nbsp;&middot;&nbsp; Midday", now, "Good afternoon, Melissa 👋", "Here is what came in from your phone since the morning.", tiles, mast) +
        f'<tr><td style="padding:22px;">{"".join(boxes)}</td></tr>'
        '<tr><td bgcolor="#F5F7FA" style="background-color:#F5F7FA;border-top:1px solid #D7DEE7;padding:14px;text-align:center;font-family:Georgia,\'Times New Roman\',serif;font-size:13px;font-style:italic;color:#8994A3;border-radius:0 0 7px 7px;">Ellie</td></tr>'
        "</table></td></tr></table>")
    return subject, body


if __name__ == "__main__":  # runnable check: python scripts/midday_email.py
    n = datetime(2026, 9, 27, 13, 0)
    assert build_midday(n, [], [], []) is None
    s, h = build_midday(n, ["Call New York City about documents — due 2026-09-29"], ["Call the dentist"], ["\"It's a recording\" — unclear what this refers to"])
    assert s == "Ellie - EA Midday - Sunday, September 27" and h.startswith("<table") and "$(" not in h and "/tmp/" not in h and "gradient" not in h
    for needle in ("Filed Your Notes", "Marked Done", "Needs Your Call", "Call New York City", "Call the dentist", "recording", "Good afternoon, Melissa"):
        assert needle in h, needle
    print("ok")
